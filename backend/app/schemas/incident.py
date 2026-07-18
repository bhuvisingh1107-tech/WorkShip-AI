from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):
    title: str
    severity: str
    status: str
    service_id: UUID
    owner_team_id: UUID
    summary: str | None = None
    root_cause: str | None = None


class IncidentCreate(IncidentBase):
    pass


class IncidentRead(IncidentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
