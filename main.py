from contextlib import asynccontextmanager
from typing import Annotated
import uuid
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import text, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import engine
from schemas import DocumentCreate, DocumentResponse
from models import Document
from dependencies import get_db_session, get_elasticsearch_client
from service import create_doc, delete_doc
from search.client import create_elasticsearch_client
from search.index import (
    ensure_index,
    index_document,
    remove_document,
    search_documents,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start...")
    client = create_elasticsearch_client()
    try:
        if not await client.ping():
            raise RuntimeError("Elasticsearch недоступен")

        await ensure_index(client)
        app.state.elasticsearch = client
        yield
    finally:
        print("Finish...")
        await client.close()
        await engine.dispose()


app = FastAPI(
    title="Test",
    lifespan=lifespan)


@app.post("/documents", response_model=DocumentResponse)
async def doc_create_url(document: DocumentCreate,
                         session: AsyncSession = Depends(get_db_session), 
                         elastic: AsyncElasticsearch = Depends(get_elasticsearch_client)):

    try:
        doc = await create_doc(session, document)
        await index_document(elastic, doc)
        return doc
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"{e}")


@app.get("/documents", response_model=list[DocumentResponse])
async def list_docs(session: AsyncSession = Depends(get_db_session),
                    limit: Annotated[int, Query(ge=1, le=100)] = 20):
    q = select(Document).order_by(Document.created_date.desc()).limit(limit)

    res = await session.execute(q)

    return [DocumentResponse(id=str(doc.id),
                             created_date=doc.created_date,
                             text=doc.text, rubrics=doc.rubrics) for doc in res.scalars().all()]


@app.delete("/documents/{doc_id}", status_code=204)
async def delete_document(doc_id: uuid.UUID,
                          session: AsyncSession = Depends(get_db_session),
                          elastic: AsyncElasticsearch = Depends(get_elasticsearch_client)):
    if not await delete_doc(session, doc_id):
        raise HTTPException(status_code=404, detail="Document not found")
    
    await remove_document(elastic, str(doc_id))


@app.get("/documents/search", response_model=list[DocumentResponse])
async def search_document_text(q: Annotated[str, Query(min_length=1, 
                                                       description="Текст для поиска")],
                                                       elastic: AsyncElasticsearch = Depends(get_elasticsearch_client)):
    if not q.strip():
        raise HTTPException(
            status_code=422,
            detail="Текст для поиска пустой",
        )

    return await search_documents(elastic, q.strip())