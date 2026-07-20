from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentSimulationRequest(BaseModel):
    title: str
    description: str
    severity: str


class RelatedIncident(BaseModel):
    title: str
    # Incident lookup is currently ordered by recency, rather than by semantic score.
    relationship: str


class RelatedDocument(BaseModel):
    title: str
    similarity: float


class IncidentSimulationResponse(BaseModel):
    incident: IncidentRead
    similarIncidents: list[RelatedIncident]
    relatedDocuments: list[RelatedDocument]
    recommendedActions: list[str]
    timeline: list[str]
    rootCauseHypothesis: str


class IncidentAIAnalysis(BaseModel):
    recommendedActions: list[str] = Field(
        min_length=3,
        max_length=5,
        description="Specific actions grounded in the incident and retrieved knowledge.",
    )
    timeline: list[str] = Field(
        min_length=3,
        max_length=6,
        description="Ordered investigation and mitigation steps for this incident.",
    )
    rootCauseHypothesis: str = Field(
        min_length=1,
        description="A short, evidence-based root-cause hypothesis.",
    )

    model_config = ConfigDict(extra="forbid")
