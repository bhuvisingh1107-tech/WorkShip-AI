from uuid import UUID

from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services.embedding import EmbeddingService
from app.services.document_processing import DocumentProcessingService


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)
        self.processing_service = DocumentProcessingService()
        self.embedding_service = EmbeddingService(db)

    def list(
        self,
        *,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
        category: str | None,
        source: str | None,
        query: str | None,
    ):
        filters = []
        if category:
            filters.append(Document.category == category)
        if source:
            filters.append(Document.source == source)
        if query:
            pattern = f"%{query.strip()}%"
            filters.append(
                or_(
                    Document.title.ilike(pattern),
                    Document.content.ilike(pattern),
                    Document.summary.ilike(pattern),
                    cast(Document.tags, String).ilike(pattern),
                )
            )
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Document:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Document not found")
        return resource

    def create(self, payload: DocumentCreate) -> Document:
        processing = self.processing_service.process(
            title=payload.title,
            content=payload.content,
            category=payload.category,
            source=payload.source,
        )
        data = payload.model_dump()
        data.update(
            content=processing.content,
            summary=processing.summary,
            tags=processing.tags,
            embedding=self.embedding_service.generate_embedding(processing.content),
        )
        return self.repository.create(data)

    def update(self, resource_id: UUID, payload: DocumentUpdate) -> Document:
        document = self.get(resource_id)
        data = payload.model_dump(exclude_unset=True)
        if {"title", "category", "source", "content"}.intersection(data):
            processing = self.processing_service.process(
                title=data.get("title", document.title),
                content=data.get("content", document.content),
                category=data.get("category", document.category),
                source=data.get("source", document.source),
            )
            data.update(
                content=processing.content,
                summary=processing.summary,
                tags=processing.tags,
            )
            if "content" in data:
                data["embedding"] = self.embedding_service.generate_embedding(
                    processing.content
                )
        return self.repository.update(document, data)

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
