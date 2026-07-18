from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MeetingBase(BaseModel):
    title: str
    date: date
    participants: list[str]
    transcript: str | None = None


class MeetingCreate(MeetingBase):
    pass


class MeetingRead(MeetingBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
