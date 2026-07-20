from sqlalchemy.orm import Session
from uuid import UUID

from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardResponse,
    IncidentAnalytics,
    RecentActivity,
    ServiceAnalytics,
)


class DashboardService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = DashboardRepository(db, workspace_id)

    def get_dashboard(self) -> DashboardResponse:
        counts = self.repository.get_overview_and_incident_counts()
        incidents, meetings, documents = self.repository.get_recent_activity()

        return DashboardResponse(
            overview=DashboardOverview(
                total_employees=counts["total_employees"],
                total_teams=counts["total_teams"],
                total_services=counts["total_services"],
                total_documents=counts["total_documents"],
                total_incidents=counts["total_incidents"],
                total_meetings=counts["total_meetings"],
            ),
            incident_analytics=IncidentAnalytics(
                critical=counts["critical"],
                high=counts["high"],
                medium=counts["medium"],
                low=counts["low"],
            ),
            service_analytics=ServiceAnalytics(
                by_status=self.repository.get_service_status_counts()
            ),
            recent_activity=RecentActivity(
                incidents=incidents,
                meetings=meetings,
                documents=documents,
            ),
        )