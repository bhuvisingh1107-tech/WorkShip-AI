from sqlalchemy import func, select
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.document import Document
from app.models.employee import Employee
from app.models.incident import Incident
from app.models.meeting import Meeting
from app.models.service import Service
from app.models.team import Team


class DashboardRepository:
    """Read-optimized aggregation queries for dashboard data."""

    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.db = db
        self.workspace_id = workspace_id

    def get_overview_and_incident_counts(self) -> dict[str, int]:
        def count(model):
            return select(func.count()).select_from(model).where(model.workspace_id == self.workspace_id).scalar_subquery()

        def severity_count(severity: str):
            return (
                select(func.count())
                .select_from(Incident)
                .where(Incident.workspace_id == self.workspace_id)
                .where(func.lower(Incident.severity) == severity)
                .scalar_subquery()
            )

        statement = select(
            count(Employee).label("total_employees"),
            count(Team).label("total_teams"),
            count(Service).label("total_services"),
            count(Document).label("total_documents"),
            count(Incident).label("total_incidents"),
            count(Meeting).label("total_meetings"),
            severity_count("critical").label("critical"),
            severity_count("high").label("high"),
            severity_count("medium").label("medium"),
            severity_count("low").label("low"),
        )
        return dict(self.db.execute(statement).mappings().one())

    def get_service_status_counts(self) -> dict[str, int]:
        """Return the available service classification aggregation.

        The current Service model has no status column, so all persisted services
        are represented by an explicit unclassified bucket.
        """

        total = self.db.scalar(select(func.count()).select_from(Service).where(Service.workspace_id == self.workspace_id)) or 0
        return {"unclassified": total}

    def get_recent_activity(self) -> tuple[list[Incident], list[Meeting], list[Document]]:
        incidents = list(
            self.db.scalars(
                select(Incident)
                .where(Incident.workspace_id == self.workspace_id)
                .order_by(Incident.created_at.desc())
                .limit(5)
            ).all()
        )
        meetings = list(
            self.db.scalars(
                select(Meeting)
                .where(Meeting.workspace_id == self.workspace_id)
                .order_by(Meeting.created_at.desc())
                .limit(5)
            ).all()
        )
        documents = list(
            self.db.scalars(
                select(Document)
                .where(Document.workspace_id == self.workspace_id)
                .order_by(Document.created_at.desc())
                .limit(5)
            ).all()
        )
        return incidents, meetings, documents