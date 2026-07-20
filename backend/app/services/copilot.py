from sqlalchemy.orm import Session
from uuid import UUID

from openai import OpenAI

from app.core.config import settings
from app.services.document import DocumentService

CHAT_MODEL = "gpt-4.1"


class CopilotService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.document_service = DocumentService(db, workspace_id)
        self.client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required to use the AI Copilot")
        if self.client is None:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self.client

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
        prompt_context = "\n\n".join(
            f"Source: {source['title']}\nExcerpt: {excerpt}"
            for source, excerpt in zip(sources, context, strict=True)
        )
        completion = self._get_client().chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer only from the supplied enterprise knowledge. "
                        "If the context is insufficient, say so. Cite the source titles used."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nKnowledge:\n{prompt_context}",
                },
            ],
        )
        answer = completion.choices[0].message.content
        if not answer:
            raise RuntimeError("OpenAI returned an empty Copilot response")
        return answer, sources, context
