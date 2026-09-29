from elasticsearch import AsyncElasticsearch
from fastapi import Request

from db import session_factory


def get_elasticsearch_client(request: Request) -> AsyncElasticsearch:
    return request.app.state.elasticsearch


async def get_db_session():
    async with session_factory() as session:
        yield session
