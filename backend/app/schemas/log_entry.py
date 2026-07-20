from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LogEntryBase(BaseModel):
    service: str
    level: str
    timestamp: datetime
    message: str


class LogEntryCreate(LogEntryBase):
    pass


class LogEntryRead(LogEntryBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)