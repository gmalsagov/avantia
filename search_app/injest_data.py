import json
from elasticsearch import Elasticsearch, helpers

INDEX_NAME = 'nobel_prizes'

def create_index():
    mapping = {
        "mappings": {
            "properties": {
                "year": {"type": "integer"},
                "category": {"type": "text"},
                "laureates": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "text"},
                        "firstname": {"type": "text"},
                        "surname": {"type": "text"},
                        "motivation": {"type": "text"}
                    }
                }
            }
        }
    }

    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def ingest_data():
    with open('data/prize.json', 'r') as f:
        data = json.load(f)

    actions = []
    for prize in data['prizes']:
        action = {
            "_index": INDEX_NAME,
            "_source": prize
        }
        actions.append(action)

    helpers.bulk(es, actions)
    print(f"Ingested {len(actions)} documents into '{INDEX_NAME}' index.")

if __name__ == "__main__":

    try:
        es = Elasticsearch("http://localhost:9200")
        print("Connection to ES Server successful")
    except:
        print("Unable to connect to server")
        exit(1)


    create_index()
    ingest_data()
