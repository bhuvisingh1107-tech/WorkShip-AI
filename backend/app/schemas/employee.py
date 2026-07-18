from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    full_name: str
    email: str
    role: str | None = None
    manager_id: UUID | None = None
    team_id: UUID


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
