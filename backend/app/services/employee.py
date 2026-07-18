from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repository = EmployeeRepository(db)

    def list(self, *, skip: int, limit: int, sort_by: str, sort_order: str, team_id: UUID | None, role: str | None):
        filters = []
        if team_id:
            filters.append(Employee.team_id == team_id)
        if role:
            filters.append(Employee.role == role)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, resource_id: UUID) -> Employee:
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError("Employee not found")
        return resource

    def create(self, payload: EmployeeCreate) -> Employee:
        return self.repository.create(payload.model_dump())

    def update(self, resource_id: UUID, payload: EmployeeUpdate) -> Employee:
        return self.repository.update(self.get(resource_id), payload.model_dump(exclude_unset=True))

    def delete(self, resource_id: UUID) -> None:
        self.repository.delete(self.get(resource_id))
