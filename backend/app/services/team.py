from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.team import Team
from app.repositories.team import TeamRepository
from app.schemas.team import TeamCreate, TeamUpdate


class TeamService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = TeamRepository(db)
        self.workspace_id = workspace_id

    def list(self, *, skip: int = 0, limit: int = 100, sort_by: str = "name", sort_order: str = "asc", name: str | None = None):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if name:
            filters.append(self.repository.model.name.ilike(f"%{name}%"))
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, team_id: UUID) -> Team:
        team = self.repository.get(team_id)
        if team is None or team.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Team not found")
        return team

    def create(self, payload: TeamCreate) -> Team:
        data = payload.model_dump()
        data["workspace_id"] = self.workspace_id
        return self.repository.create(data)

    def update(self, team_id: UUID, payload: TeamUpdate) -> Team:
        team = self.get(team_id)
        return self.repository.update(team, payload.model_dump(exclude_unset=True))

    def delete(self, team_id: UUID) -> None:
        team = self.get(team_id)
        self.repository.delete(team)