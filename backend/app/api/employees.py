from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.get("", response_model=PaginatedResponse[EmployeeRead])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["full_name", "email", "role", "created_at"] = "full_name",
    sort_order: Literal["asc", "desc"] = "asc",
    team_id: UUID | None = None,
    role: str | None = None,
    service: EmployeeService = Depends(get_employee_service),
) -> PaginatedResponse[EmployeeRead]:
    items, total = service.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, team_id=team_id, role=role)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: UUID, service: EmployeeService = Depends(get_employee_service)) -> EmployeeRead:
    return service.get(employee_id)


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)) -> EmployeeRead:
    return service.create(payload)


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(employee_id: UUID, payload: EmployeeUpdate, service: EmployeeService = Depends(get_employee_service)) -> EmployeeRead:
    return service.update(employee_id, payload)


@router.delete("/{employee_id}", response_model=MessageResponse)
def delete_employee(employee_id: UUID, service: EmployeeService = Depends(get_employee_service)) -> MessageResponse:
    service.delete(employee_id)
    return MessageResponse(detail="Employee deleted")
