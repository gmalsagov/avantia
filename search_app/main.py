from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch(hosts=["http://elasticsearch:9200"])


@app.get("/search/name")
def search_name(query: str):
    response = es.search(
        index="nobel_prizes",
        body={
            "query": {
                "nested": {
                    "path": "laureates",
                    "query": {
                        "match": {
                            "laureates.firstname": query
                        }
                    }
                }
            }
        }
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