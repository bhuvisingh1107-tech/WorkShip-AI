from sqlalchemy.orm import Session
from uuid import UUID

from app.services.document import DocumentService


class CopilotService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.document_service = DocumentService(db, workspace_id)

    def query(self, question: str):
        results = self.document_service.semantic_search(query=question, limit=3)
        sources = [
            {
                "title": document.title,
                "category": document.category,
                "similarity": similarity,
            }
            for document, similarity in results
        ]
        context = [document.summary or document.content[:500] for document, _ in results]
        return "Relevant enterprise knowledge found from retrieved documents.", sources, context