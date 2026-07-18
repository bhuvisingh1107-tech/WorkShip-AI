from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


def get_team_service(db: Session = Depends(get_db)) -> TeamService:
    return TeamService(db)


@router.get("", response_model=PaginatedResponse[TeamRead])
def list_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["name", "created_at"] = "name",
    sort_order: Literal["asc", "desc"] = "asc",
    name: str | None = None,
    service: TeamService = Depends(get_team_service),
) -> PaginatedResponse[TeamRead]:
    items, total = service.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, name=name)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: UUID, service: TeamService = Depends(get_team_service)) -> TeamRead:
    return service.get(team_id)


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, service: TeamService = Depends(get_team_service)) -> TeamRead:
    return service.create(payload)


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(team_id: UUID, payload: TeamUpdate, service: TeamService = Depends(get_team_service)) -> TeamRead:
    return service.update(team_id, payload)


@router.delete("/{team_id}", response_model=MessageResponse)
def delete_team(team_id: UUID, service: TeamService = Depends(get_team_service)) -> MessageResponse:
    service.delete(team_id)
    return MessageResponse(detail="Team deleted")
