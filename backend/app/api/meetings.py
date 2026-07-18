from datetime import date
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.meeting import MeetingCreate, MeetingRead, MeetingUpdate
from app.services.meeting import MeetingService

router = APIRouter(prefix="/meetings", tags=["Meetings"])


def get_meeting_service(db: Session = Depends(get_db)) -> MeetingService:
    return MeetingService(db)


@router.get("", response_model=PaginatedResponse[MeetingRead])
def list_meetings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["title", "date", "created_at"] = "date",
    sort_order: Literal["asc", "desc"] = "desc",
    date_from: date | None = None,
    date_to: date | None = None,
    service: MeetingService = Depends(get_meeting_service),
) -> PaginatedResponse[MeetingRead]:
    items, total = service.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, date_from=date_from, date_to=date_to)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: UUID, service: MeetingService = Depends(get_meeting_service)) -> MeetingRead:
    return service.get(meeting_id)


@router.post("", response_model=MeetingRead, status_code=status.HTTP_201_CREATED)
def create_meeting(payload: MeetingCreate, service: MeetingService = Depends(get_meeting_service)) -> MeetingRead:
    return service.create(payload)


@router.patch("/{meeting_id}", response_model=MeetingRead)
def update_meeting(meeting_id: UUID, payload: MeetingUpdate, service: MeetingService = Depends(get_meeting_service)) -> MeetingRead:
    return service.update(meeting_id, payload)


@router.delete("/{meeting_id}", response_model=MessageResponse)
def delete_meeting(meeting_id: UUID, service: MeetingService = Depends(get_meeting_service)) -> MessageResponse:
    service.delete(meeting_id)
    return MessageResponse(detail="Meeting deleted")
