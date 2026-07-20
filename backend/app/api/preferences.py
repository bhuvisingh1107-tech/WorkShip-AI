from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.employee import Employee
from app.services.employee import EmployeeService

router = APIRouter(prefix="/users/me/preferences", tags=["Preferences"])


def get_employee_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> EmployeeService:
    return EmployeeService(db, current_user.workspace_id)


@router.get("", response_model=dict)
def get_preferences(
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    """
    Get the preferences of the current user.
    """
    return service.get_preferences(service.repository.model.id)


@router.put("", response_model=dict)
def update_preferences(
    preferences: dict,
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    """
    Update the preferences of the current user.
    """
    return service.update_preferences(service.repository.model.id, preferences)