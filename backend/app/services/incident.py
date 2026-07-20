from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.services.document import DocumentService


class IncidentService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = IncidentRepository(db)
        self.workspace_id = workspace_id

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        service_id: UUID | None = None,
        owner_team_id: UUID | None = None,
        severity: str | None = None,
        status: str | None = None,
    ):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if service_id:
            filters.append(self.repository.model.service_id == service_id)
        if owner_team_id:
            filters.append(self.repository.model.owner_team_id == owner_team_id)
        if severity:
            filters.append(self.repository.model.severity == severity)
        if status:
            filters.append(self.repository.model.status == status)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, incident_id: UUID) -> Incident:
        incident = self.repository.get(incident_id)
        if incident is None or incident.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Incident not found")
        return incident

    def create(self, payload: IncidentCreate) -> Incident:
        data = payload.model_dump()
        data["workspace_id"] = self.workspace_id
        return self.repository.create(data)

    def update(self, incident_id: UUID, payload: IncidentUpdate) -> Incident:
        incident = self.get(incident_id)
        return self.repository.update(incident, payload.model_dump(exclude_unset=True))

    def delete(self, incident_id: UUID) -> None:
        incident = self.get(incident_id)
        self.repository.delete(incident)

    def simulate(self, *, title: str, description: str, severity: str):
        from app.models.service import Service

        service_name = next(
            (
                name
                for keyword, name in {
                    "payment": "Payroll Processing",
                    "database": "Data Warehouse",
                    "auth": "Identity Gateway",
                }.items()
                if keyword in f"{title} {description}".lower()
            ),
            "Incident Command Center",
        )
        service = self.repository.db.query(Service).filter(
            Service.workspace_id == self.workspace_id,
            Service.name == service_name
        ).one()
        incident = self.create(
            IncidentCreate(
                title=title,
                severity=severity,
                status="investigating",
                service_id=service.id,
                owner_team_id=service.owner_team_id,
                summary=description,
            )
        )
        similar_incidents, _ = self.list(
            skip=0,
            limit=3,
            sort_by="created_at",
            sort_order="desc",
            service_id=service.id,
            owner_team_id=None,
            severity=None,
            status=None,
        )
        documents = DocumentService(self.repository.db, self.workspace_id).semantic_search(
            query=f"{title} {description}", limit=3
        )
        return incident, similar_incidents[1:], documents