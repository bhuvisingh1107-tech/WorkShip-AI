from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DashboardOverview(BaseModel):
    total_employees: int = Field(serialization_alias="totalEmployees")
    total_teams: int = Field(serialization_alias="totalTeams")
    total_services: int = Field(serialization_alias="totalServices")
    total_documents: int = Field(serialization_alias="totalDocuments")
    total_incidents: int = Field(serialization_alias="totalIncidents")
    total_meetings: int = Field(serialization_alias="totalMeetings")


class IncidentAnalytics(BaseModel):
    critical: int
    high: int
    medium: int
    low: int


class ServiceAnalytics(BaseModel):
    by_status: dict[str, int] = Field(serialization_alias="byStatus")


class RecentIncident(BaseModel):
    id: UUID
    title: str
    severity: str
    status: str
    created_at: datetime = Field(serialization_alias="createdAt")

    model_config = ConfigDict(from_attributes=True)


class RecentMeeting(BaseModel):
    id: UUID
    title: str
    date: date
    created_at: datetime = Field(serialization_alias="createdAt")

    model_config = ConfigDict(from_attributes=True)


class RecentDocument(BaseModel):
    id: UUID
    title: str
    category: str | None
    created_at: datetime = Field(serialization_alias="createdAt")

    model_config = ConfigDict(from_attributes=True)


class RecentActivity(BaseModel):
    incidents: list[RecentIncident]
    meetings: list[RecentMeeting]
    documents: list[RecentDocument]


class DashboardResponse(BaseModel):
    overview: DashboardOverview
    incident_analytics: IncidentAnalytics = Field(serialization_alias="incidentAnalytics")
    service_analytics: ServiceAnalytics = Field(serialization_alias="serviceAnalytics")
    recent_activity: RecentActivity = Field(serialization_alias="recentActivity")
