from __future__ import annotations

from dataclasses import dataclass

from sentence_transformers import SentenceTransformer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL_EMBEDDING_DIMENSIONS = 384
STORED_EMBEDDING_DIMENSIONS = 1536


@dataclass
class EmbeddingBackfillResult:
    embedded: int = 0
    skipped: int = 0


class EmbeddingService:
    """Local embedding boundary for document storage and retrieval."""

    _model: SentenceTransformer | None = None

    def __init__(self, db: Session) -> None:
        self.db = db

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL)
        return cls._model

    def generate_embedding(self, content: str) -> list[float]:
        return self.generate_embeddings([content])[0]

    def generate_embeddings(self, contents: list[str]) -> list[list[float]]:
        if not contents:
            return []
        embeddings = self._get_model().encode(
            contents,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return [
            self._pad_for_pgvector(embedding.tolist())
            for embedding in embeddings
        ]

    @staticmethod
    def _pad_for_pgvector(embedding: list[float]) -> list[float]:
        if len(embedding) != MODEL_EMBEDDING_DIMENSIONS:
            raise ValueError(
                f"Expected {MODEL_EMBEDDING_DIMENSIONS} dimensions from {EMBEDDING_MODEL}, "
                f"received {len(embedding)}"
            )
        return embedding + [0.0] * (
            STORED_EMBEDDING_DIMENSIONS - MODEL_EMBEDDING_DIMENSIONS
        )

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
