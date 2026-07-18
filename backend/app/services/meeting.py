from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.meeting import Meeting
from app.repositories.meeting import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate


class MeetingService:
    def __init__(self, db: Session) -> None:
        self.repository = MeetingRepository(db)

    def list(
        self,
        *,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
        date_from: date | None,
        date_to: date | None,
    ):
        filters = []
        if date_from:
            filters.append(Meeting.date >= date_from)
        if date_to:
            filters.append(Meeting.date <= date_to)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Meeting:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Meeting not found")
        return resource

    def create(self, payload: MeetingCreate) -> Meeting:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: MeetingUpdate) -> Meeting:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
