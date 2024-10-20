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
                "match_phrase_prefix": {
                    "laureates.firstname": query
                }
            }
        }
    )
    return response['hits']['hits']