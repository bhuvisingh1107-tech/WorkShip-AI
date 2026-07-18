from typing import Any

from pydantic import BaseModel


class DocumentSection(BaseModel):
    heading: str
    content: str
    word_count: int


class DocumentProcessingResult(BaseModel):
    content: str
    summary: str
    tags: list[str]
    reading_time_minutes: int
    sections: list[DocumentSection]
    metadata: dict[str, Any]
