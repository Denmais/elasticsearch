from elasticsearch import AsyncElasticsearch

from config import ELASTICSEARCH_URL


def create_elasticsearch_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(ELASTICSEARCH_URL)