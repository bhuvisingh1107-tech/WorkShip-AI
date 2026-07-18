from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.service import Service
from app.repositories.service import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, db: Session) -> None:
        self.repository = ServiceRepository(db)

    def list(self, *, skip: int, limit: int, sort_by: str, sort_order: str, owner_team_id: UUID | None, criticality: str | None):
        filters = []
        if owner_team_id:
            filters.append(Service.owner_team_id == owner_team_id)
        if criticality:
            filters.append(Service.criticality == criticality)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Service:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Service not found")
        return resource

    def create(self, payload: ServiceCreate) -> Service:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: ServiceUpdate) -> Service:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
