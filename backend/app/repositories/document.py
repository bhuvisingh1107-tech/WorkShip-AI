from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    model = Document

    def semantic_search(
        self, query_embedding: list[float], limit: int, workspace_id: UUID | None = None
    ) -> list[tuple[Document, float]]:
        distance = Document.embedding.cosine_distance(query_embedding)
        statement = (
            select(Document, (1 - distance).label("similarity"))
            .where(Document.embedding.is_not(None))
        )
        if workspace_id is not None:
            statement = statement.where(Document.workspace_id == workspace_id)
        statement = statement.order_by(distance).limit(limit)
        return [
            (document, float(similarity))
            for document, similarity in self.db.execute(statement).all()
        ]