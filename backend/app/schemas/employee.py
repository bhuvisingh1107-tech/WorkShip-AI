from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    full_name: str
    email: str
    role: str | None = None
    is_active: bool = True
    avatar: str | None = None
    phone: str | None = None
    department: str | None = None
    job_title: str | None = None
    manager_id: UUID | None = None
    team_id: UUID


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    email: str | None = None
    role: str | None = None
    is_active: bool | None = None
    avatar: str | None = None
    phone: str | None = None
    department: str | None = None
    job_title: str | None = None
    manager_id: UUID | None = None
    team_id: UUID | None = None


class EmployeeRead(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None

    model_config = ConfigDict(from_attributes=True)