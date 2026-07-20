import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MeetingBase(BaseModel):
    title: str
    date: datetime.date
    participants: list[str]
    transcript: str | None = None


class MeetingCreate(MeetingBase):
    pass


class MeetingUpdate(BaseModel):
    title: str | None = None
    date: datetime.date | None = None
    participants: list[str] | None = None
    transcript: str | None = None


class MeetingRead(MeetingBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)