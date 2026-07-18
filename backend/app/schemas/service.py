from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    description: str | None = None
    owner_team_id: UUID
    criticality: str | None = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_team_id: UUID | None = None
    criticality: str | None = None


class ServiceRead(ServiceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
