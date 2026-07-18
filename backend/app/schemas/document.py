from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    category: str | None = None
    source: str | None = None
    content: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    source: str | None = None
    content: str | None = None


class DocumentRead(DocumentBase):
    id: UUID
    summary: str | None = None
    tags: list[str] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
