from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.meeting import Meeting
from app.repositories.meeting import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate


class MeetingService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = MeetingRepository(db)
        self.workspace_id = workspace_id

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "date",
        sort_order: str = "desc",
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if date_from:
            filters.append(self.repository.model.date >= date_from)
        if date_to:
            filters.append(self.repository.model.date <= date_to)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, meeting_id: UUID) -> Meeting:
        meeting = self.repository.get(meeting_id)
        if meeting is None or meeting.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Meeting not found")
        return meeting

    def create(self, payload: MeetingCreate) -> Meeting:
        data = payload.model_dump()
        data["workspace_id"] = self.workspace_id
        return self.repository.create(data)

    def update(self, meeting_id: UUID, payload: MeetingUpdate) -> Meeting:
        meeting = self.get(meeting_id)
        return self.repository.update(meeting, payload.model_dump(exclude_unset=True))

    def delete(self, meeting_id: UUID) -> None:
        meeting = self.get(meeting_id)
        self.repository.delete(meeting)