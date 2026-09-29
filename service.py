import uuid
from schemas import DocumentCreate, DocumentResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from models import Document


async def create_doc(session: AsyncSession, 
                     document: DocumentCreate):
    async with session.begin():
        doc = Document(id=uuid.uuid4(), rubrics=document.rubrics,
                       text=document.text, created_date=document.created_date)
        session.add(doc)
        await session.flush()

    return DocumentResponse(id=str(doc.id),
                            created_date=doc.created_date, text=doc.text,
                            rubrics=doc.rubrics)


async def delete_doc(session: AsyncSession, id: uuid.UUID) -> bool:
    async with session.begin():
        doc = await session.get(Document, id)
        if doc is None:
            return False
        await session.delete(doc)
    return True
