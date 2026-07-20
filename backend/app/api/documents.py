from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.services.document import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


def get_document_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> DocumentService:
    return DocumentService(db, current_user.workspace_id)


@router.get("", response_model=PaginatedResponse[DocumentRead])
def list_documents(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["title", "category", "source", "created_at"] = "title",
    sort_order: Literal["asc", "desc"] = "asc",
    category: str | None = None,
    source: str | None = None,
    query: str | None = Query(None, min_length=1, description="Search title, content, summary, or tags"),
    current_user: Employee = Depends(deps.get_current_active_user),
    service: DocumentService = Depends(get_document_service),
) -> PaginatedResponse[DocumentRead]:
    items, total = service.list(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        category=category,
        source=source,
        query=query,
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentRead:
    return service.get(document_id)


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    *,
    db: Session = Depends(get_db),
    payload: DocumentCreate,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentRead:
    return service.create(payload)


@router.patch("/{document_id}", response_model=DocumentRead)
def update_document(
    *,
    db: Session = Depends(get_db),
    document_id: UUID,
    payload: DocumentUpdate,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: DocumentService = Depends(get_document_service),
) -> DocumentRead:
    return service.update(document_id, payload)


@router.delete("/{document_id}", response_model=MessageResponse)
def delete_document(
    *,
    db: Session = Depends(get_db),
    document_id: UUID,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: DocumentService = Depends(get_document_service),
) -> MessageResponse:
    service.delete(document_id)
    return MessageResponse(detail="Document deleted")
