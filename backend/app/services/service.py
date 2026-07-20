from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.service import Service
from app.repositories.service import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = ServiceRepository(db)
        self.workspace_id = workspace_id

    def list(self, *, skip: int = 0, limit: int = 100, sort_by: str = "created_at", sort_order: str = "asc", owner_team_id: UUID | None = None, criticality: str | None = None):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if owner_team_id:
            filters.append(self.repository.model.owner_team_id == owner_team_id)
        if criticality:
            filters.append(self.repository.model.criticality == criticality)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, service_id: UUID) -> Service:
        service = self.repository.get(service_id)
        if service is None or service.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Service not found")
        return service

    def create(self, payload: ServiceCreate) -> Service:
        data = payload.model_dump()
        data["workspace_id"] = self.workspace_id
        return self.repository.create(data)

    def update(self, service_id: UUID, payload: ServiceUpdate) -> Service:
        service = self.get(service_id)
        return self.repository.update(service, payload.model_dump(exclude_unset=True))

    def delete(self, service_id: UUID) -> None:
        service = self.get(service_id)
        self.repository.delete(service)