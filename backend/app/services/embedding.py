from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document

EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class EmbeddingBackfillResult:
    embedded: int = 0
    skipped: int = 0


class EmbeddingService:
    """OpenAI embedding boundary for document storage and retrieval."""

    def __init__(self, db: Session, client: OpenAI | None = None) -> None:
        self.db = db
        self.client = client or OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_embedding(self, content: str) -> list[float]:
        return self.generate_embeddings([content])[0]

    def generate_embeddings(self, contents: list[str]) -> list[list[float]]:
        if not contents:
            return []
        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=contents,
            encoding_format="float",
        )
        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]

    def update_document_embedding(self, document: Document) -> Document:
        document.embedding = self.generate_embedding(document.content)
        self.db.commit()
        self.db.refresh(document)
        return document

    def backfill_missing_embeddings(self, batch_size: int = 100) -> EmbeddingBackfillResult:
        result = EmbeddingBackfillResult()
        while True:
            documents = list(
                self.db.scalars(
                    select(Document)
                    .where(Document.embedding.is_(None))
                    .order_by(Document.created_at)
                    .limit(batch_size)
                ).all()
            )
            if not documents:
                return result

            embeddings = self.generate_embeddings(
                [document.content for document in documents]
            )
            for document, embedding in zip(documents, embeddings, strict=True):
                document.embedding = embedding
                result.embedded += 1
            self.db.commit()
