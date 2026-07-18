from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)

    def list(self, *, skip: int, limit: int, sort_by: str, sort_order: str, category: str | None, source: str | None):
        filters = []
        if category:
            filters.append(Document.category == category)
        if source:
            filters.append(Document.source == source)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Document:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Document not found")
        return resource

    def create(self, payload: DocumentCreate) -> Document:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: DocumentUpdate) -> Document:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
