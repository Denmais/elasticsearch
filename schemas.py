from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):

    rubrics: List[str]

    text: str

    created_date: datetime


class DocumentResponse(BaseModel):
    id: str
    text: str
    rubrics: list[str]
    created_date: datetime
