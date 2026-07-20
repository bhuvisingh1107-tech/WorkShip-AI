from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = EmployeeRepository(db)
        self.workspace_id = workspace_id

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "full_name",
        sort_order: str = "asc",
        team_id: UUID | None = None,
        role: str | None = None,
    ):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if team_id:
            filters.append(self.repository.model.team_id == team_id)
        if role:
            filters.append(self.repository.model.role == role)
        return self.repository.list(
            skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters
        )

    def get(self, employee_id: UUID) -> Employee:
        employee = self.repository.get(employee_id)
        if employee is None or employee.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Employee not found")
        return employee

    def create(self, payload: EmployeeCreate) -> Employee:
        data = payload.model_dump()
        # No password hashing; auth handled by Supabase
        data["workspace_id"] = self.workspace_id
        # Ensure full_name is set from first_name and last_name if not provided
        if not data.get("full_name"):
            first = data.get("first_name")
            last = data.get("last_name")
            if first or last:
                data["full_name"] = f"{first or ''} {last or ''}".strip()
            else:
                # fallback to email prefix
                data["full_name"] = data["email"].split("@")[0]
        # Ensure first_name and last_name from full_name if not provided
        if not data.get("first_name") and not data.get("last_name") and data.get("full_name"):
            parts = data["full_name"].split()
            data["first_name"] = parts[0] if len(parts) > 0 else None
            data["last_name"] = " ".join(parts[1:]) if len(parts) > 1 else None
        # If first_name or last_name provided but full_name missing, sync
        if ("first_name" in data or "last_name" in data) and not data.get("full_name"):
            first = data.get("first_name")
            last = data.get("last_name")
            data["full_name"] = f"{first or ''} {last or ''}".strip()
        employee = self.repository.create(data)
        return employee

    def update(self, employee_id: UUID, payload: EmployeeUpdate) -> Employee:
        employee = self.get(employee_id)
        update_data = payload.model_dump(exclude_unset=True)
        # If full_name is updated, try to keep first_name and last_name in sync
        if "full_name" in update_data:
            full_name = update_data["full_name"]
            if full_name:
                parts = full_name.split()
                update_data["first_name"] = (
                    parts[0] if len(parts) > 0 else None
                )
                update_data["last_name"] = (
                    " ".join(parts[1:]) if len(parts) > 1 else None
                )
            else:
                update_data["first_name"] = None
                update_data["last_name"] = None
        # If first_name or last_name updated, update full_name
        if "first_name" in update_data or "last_name" in update_data:
            first = update_data.get("first_name", employee.first_name)
            last = update_data.get("last_name", employee.last_name)
            if first or last:
                update_data["full_name"] = f"{first or ''} {last or ''}".strip()
            else:
                update_data["full_name"] = ""
        updated_employee = self.repository.update(employee, update_data)
        return updated_employee

    def delete(self, employee_id: UUID) -> None:
        employee = self.get(employee_id)
        self.repository.delete(employee)

    def get_preferences(self, employee_id: UUID) -> dict:
        employee = self.get(employee_id)
        return employee.preferences or {}

    def update_preferences(self, employee_id: UUID, preferences: dict) -> dict:
        employee = self.get(employee_id)
        employee.preferences = preferences
        self.repository.db.add(employee)
        self.repository.db.commit()
        self.repository.db.refresh(employee)
        return employee.preferences