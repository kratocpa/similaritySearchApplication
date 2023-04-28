from elasticsearch import Elasticsearch
from app.config.elasticsearch import ES_URL, ES_INDEX_NAME, ES_VERIFY_CERTS


class ElasticsearchGateway:
    def __init__(self):
        self.es = Elasticsearch(ES_URL, verify_certs=ES_VERIFY_CERTS)
        self.index = ES_INDEX_NAME

        self.es.indices.create(
            index=self.index,
            body={
                "settings": {
                    "index": {
                        "number_of_shards": "1",
                        "number_of_replicas": "0",
                        "analysis": {
                            "analyzer": {
                                "czech": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": [
                                        "czech_stemmer",
                                        "asciifolding",
                                        "czech_stop",
                                        "lowercase",
                                        "unique_on_same_position"
                                    ]
                                }
                            },
                            "filter": {
                                "czech_stop": {
                                    "type": "stop",
                                    "stopwords": ["že", "_czech_"]
                                },
                                "unique_on_same_position": {
                                    "type": "unique",
                                    "only_on_same_position": True
                                },
                                "czech_stemmer": {
                                    "type": "stemmer",
                                    "name": "czech"
                                }
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "description": {
                            "type": "text",
                            "analyzer": "czech"
                        },
                        "company_id": {
                            "type": "integer"
                        }
                    }
                }
            },
            ignore=400
        )

    def upload_item(self, company_id, description):
        item = {
            'description': description,
            'company_id': company_id
        }
        self.es.index(index=self.index, document=item)

    def search_item(self, search_term, size):
        query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": search_term,
                            "operator": "or",
                            "fields": [
                                "description"
                            ]
                        }
                    }
                ]
            }
        }
        resp = self.es.search(index=self.index, query=query, size=size)
        return [hit['_source'] for hit in resp['hits']['hits']]
