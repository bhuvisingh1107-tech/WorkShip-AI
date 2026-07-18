from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.services.document import DocumentService


class IncidentService:
    def __init__(self, db: Session) -> None:
        self.repository = IncidentRepository(db)

    def list(
        self,
        *,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
        service_id: UUID | None,
        owner_team_id: UUID | None,
        severity: str | None,
        status: str | None,
    ):
        filters = []
        if service_id:
            filters.append(Incident.service_id == service_id)
        if owner_team_id:
            filters.append(Incident.owner_team_id == owner_team_id)
        if severity:
            filters.append(Incident.severity == severity)
        if status:
            filters.append(Incident.status == status)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Incident:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Incident not found")
        return resource

    def create(self, payload: IncidentCreate) -> Incident:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: IncidentUpdate) -> Incident:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))

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
        service = self.repository.db.query(Service).filter(Service.name == service_name).one()
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
        documents = DocumentService(self.repository.db).semantic_search(
            query=f"{title} {description}", limit=3
        )
        return incident, similar_incidents[1:], documents
