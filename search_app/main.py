from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch(hosts=["http://elasticsearch:9200"])


@app.get("/search/name")
def search_name(query: str):
    firstname = query
    surname = ""
    if len(query.split(" ")) > 1:
        firstname = query.split(" ")[0],
        surname = query.split(" ")[1]

    body={
        "query": {
            "nested": {
                "path": "laureates",
                "query": {
                    "match": {
                        "laureates.firstname": firstname
                    }
                }
            }
        }
    }
    if surname:
        body = {
            "query": {
                "query_string": {
                    "query": f"(laureates.firstname:{firstname}) AND (laureates.surname:{surname})"
                }
            }
        }
    print(body)
    response = es.search(
        index="nobel_prizes",
        body=body
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]


@app.get("/search/category")
def search_category(query: str):
    response = es.search(
        index="nobel_prizes",
        body={
            "query": {
                "match": {
                    "category": query
                }
            }
        }
    )
    return response['hits']['hits']