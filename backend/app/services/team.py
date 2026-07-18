from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.team import Team
from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreate, TeamUpdate


class TeamService:
    def __init__(self, db: Session) -> None:
        self.repository = TeamRepository(db)

    def list(self, *, skip: int, limit: int, sort_by: str, sort_order: str, name: str | None):
        filters = [Team.name.ilike(f"%{name}%")] if name else []
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Team:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Team not found")
        return resource

    def create(self, payload: TeamCreate) -> Team:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: TeamUpdate) -> Team:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
