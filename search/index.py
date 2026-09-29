from elasticsearch import AsyncElasticsearch, BadRequestError, NotFoundError

from config import ELASTICSEARCH_INDEX
from schemas import DocumentResponse


INDEX_MAPPING = {
    "properties": {
        "id": {"type": "keyword"},
        "rubrics": {"type": "keyword"},
        "text": {"type": "text", "analyzer": "russian"},
        "created_date": {"type": "date"},
    }
}


async def ensure_index(client: AsyncElasticsearch) -> bool:
    if await client.indices.exists(index=ELASTICSEARCH_INDEX):
        return False

    try:
        await client.indices.create(
            index=ELASTICSEARCH_INDEX,
            mappings=INDEX_MAPPING,
        )
    except BadRequestError as error:
        if error.error != "resource_already_exists_exception":
            raise
        return False

    return True


async def index_document(client: AsyncElasticsearch, doc: DocumentResponse):
    await client.index(
        index=ELASTICSEARCH_INDEX,
        id=doc.id,
        document=doc.model_dump(mode="json"),
        refresh="wait_for",
    )


async def remove_document(client: AsyncElasticsearch, doc_id: str):
    try:
        await client.delete(
            index=ELASTICSEARCH_INDEX,
            id=doc_id,
            refresh="wait_for",
        )
    except NotFoundError:
        pass


async def search_documents(client: AsyncElasticsearch, query: str):
    result = await client.search(
        index=ELASTICSEARCH_INDEX,
        query={"match": {"text": query}},
        sort=[
            {"created_date": {"order": "desc"}}
        ],
        size=20,
    )

    return [DocumentResponse.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]