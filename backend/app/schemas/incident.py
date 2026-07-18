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


class IncidentUpdate(BaseModel):
    title: str | None = None
    severity: str | None = None
    status: str | None = None
    service_id: UUID | None = None
    owner_team_id: UUID | None = None
    summary: str | None = None
    root_cause: str | None = None


class IncidentRead(IncidentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentSimulationRequest(BaseModel):
    title: str
    description: str
    severity: str


class RelatedIncident(BaseModel):
    title: str
    similarity: float


class RelatedDocument(BaseModel):
    title: str
    similarity: float


class IncidentSimulationResponse(BaseModel):
    incident: IncidentRead
    similarIncidents: list[RelatedIncident]
    relatedDocuments: list[RelatedDocument]
    recommendedActions: list[str]
    timeline: list[str]
