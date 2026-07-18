from sqlalchemy import select

from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    model = Document

    def semantic_search(
        self, query_embedding: list[float], limit: int
    ) -> list[tuple[Document, float]]:
        distance = Document.embedding.cosine_distance(query_embedding)
        statement = (
            select(Document, (1 - distance).label("similarity"))
            .where(Document.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
        )
        return [
            (document, float(similarity))
            for document, similarity in self.db.execute(statement).all()
        ]
