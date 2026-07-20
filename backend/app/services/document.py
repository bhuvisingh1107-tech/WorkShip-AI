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
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = DocumentRepository(db)
        self.processing_service = DocumentProcessingService()
        self.embedding_service = EmbeddingService(db)
        self.workspace_id = workspace_id

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        category: str | None = None,
        source: str | None = None,
        query: str | None = None,
    ):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if category:
            filters.append(self.repository.model.category == category)
        if source:
            filters.append(self.repository.model.source == source)
        if query:
            pattern = f"%{query.strip()}%"
            filters.append(
                or_(
                    self.repository.model.title.ilike(pattern),
                    self.repository.model.content.ilike(pattern),
                    self.repository.model.summary.ilike(pattern),
                    cast(self.repository.model.tags, String).ilike(pattern),
                )
            )
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, document_id: UUID) -> Document:
        document = self.repository.get(document_id)
        if document is None or document.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Document not found")
        return document

    def semantic_search(self, *, query: str, limit: int):
        query_embedding = self.embedding_service.generate_embedding(query)
        return self.repository.semantic_search(query_embedding, limit, self.workspace_id)

    def create(self, payload: DocumentCreate) -> Document:
        processing = self.processing_service.process(
            title=payload.title,
            content=payload.content,
            category=payload.category,
            source=payload.source,
        )
        data = payload.model_dump()
        data.update(
            workspace_id=self.workspace_id,
            content=processing.content,
            summary=processing.summary,
            tags=processing.tags,
            embedding=self.embedding_service.generate_embedding(processing.content),
        )
        return self.repository.create(data)

    def update(self, document_id: UUID, payload: DocumentUpdate) -> Document:
        document = self.get(document_id)
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

    def delete(self, document_id: UUID) -> None:
        document = self.get(document_id)
        self.repository.delete(document)