from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.document import SemanticSearchResponse, SemanticSearchResult
from app.services.document import DocumentService

router = APIRouter(prefix="/search", tags=["Search"])


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)


@router.get("", response_model=SemanticSearchResponse)
def semantic_search(
    q: str = Query(..., min_length=1, description="Semantic search query"),
    limit: int = Query(10, ge=1, le=50),
    service: DocumentService = Depends(get_document_service),
) -> SemanticSearchResponse:
    results = service.semantic_search(query=q, limit=limit)
    return SemanticSearchResponse(
        query=q,
        results=[
            SemanticSearchResult(document=document, similarity=similarity)
            for document, similarity in results
        ],
    )
