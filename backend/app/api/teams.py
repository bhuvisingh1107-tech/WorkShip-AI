from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


def get_team_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> TeamService:
    return TeamService(db, current_user.workspace_id)


@router.get("", response_model=PaginatedResponse[TeamRead])
def list_teams(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["name", "created_at"] = "name",
    sort_order: Literal["asc", "desc"] = "asc",
    name: str | None = None,
    current_user: Employee = Depends(deps.get_current_active_user),
) -> PaginatedResponse[TeamRead]:
    service = TeamService(db, current_user.workspace_id)
    items, total = service.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, name=name)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamRead)
def get_team(
    team_id: UUID,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
):
    service = TeamService(db, current_user.workspace_id)
    team = service.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    *,
    db: Session = Depends(get_db),
    payload: TeamCreate,
    current_user: Employee = Depends(deps.get_current_active_user),
):
    service = TeamService(db, current_user.workspace_id)
    team = service.create(payload)
    return team


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    *,
    db: Session = Depends(get_db),
    team_id: UUID,
    payload: TeamUpdate,
    current_user: Employee = Depends(deps.get_current_active_user),
):
    service = TeamService(db, current_user.workspace_id)
    team = service.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team = service.update(team_id, payload)
    return team


@router.delete("/{team_id}", response_model=MessageResponse)
def delete_team(
    *,
    db: Session = Depends(get_db),
    team_id: UUID,
    current_user: Employee = Depends(deps.get_current_active_user),
):
    service = TeamService(db, current_user.workspace_id)
    team = service.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    service.delete(team_id)
    return MessageResponse(detail="Team deleted")