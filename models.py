import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, Text, func, CheckConstraint, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Document(Base):
    __tablename__ = "Documents"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    rubrics: Mapped[List[str]] = mapped_column(JSON, default=list)

    text: Mapped[str] = mapped_column(Text, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())