from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.services.service import ServiceService

router = APIRouter(prefix="/services", tags=["Services"])


def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    return ServiceService(db)


@router.get("", response_model=PaginatedResponse[ServiceRead])
def list_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["name", "criticality", "created_at"] = "name",
    sort_order: Literal["asc", "desc"] = "asc",
    owner_team_id: UUID | None = None,
    criticality: str | None = None,
    service: ServiceService = Depends(get_service_service),
) -> PaginatedResponse[ServiceRead]:
    items, total = service.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, owner_team_id=owner_team_id, criticality=criticality)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{service_id}", response_model=ServiceRead)
def get_service(service_id: UUID, service: ServiceService = Depends(get_service_service)) -> ServiceRead:
    return service.get(service_id)


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, service: ServiceService = Depends(get_service_service)) -> ServiceRead:
    return service.create(payload)


@router.patch("/{service_id}", response_model=ServiceRead)
def update_service(service_id: UUID, payload: ServiceUpdate, service: ServiceService = Depends(get_service_service)) -> ServiceRead:
    return service.update(service_id, payload)


@router.delete("/{service_id}", response_model=MessageResponse)
def delete_service(service_id: UUID, service: ServiceService = Depends(get_service_service)) -> MessageResponse:
    service.delete(service_id)
    return MessageResponse(detail="Service deleted")
