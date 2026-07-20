from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.db.session import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import DashboardService
from app.models.employee import Employee


def get_dashboard_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> DashboardService:
    return DashboardService(db, current_user.workspace_id)


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardResponse:
    return service.get_dashboard()