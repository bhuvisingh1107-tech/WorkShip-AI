from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.db.session import get_db
from app.schemas.copilot import CopilotQueryRequest, CopilotQueryResponse
from app.services.copilot import CopilotService
from app.models.employee import Employee


def get_copilot_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> CopilotService:
    return CopilotService(db, current_user.workspace_id)


router = APIRouter(prefix="/copilot", tags=["Copilot"])


@router.post("/query", response_model=CopilotQueryResponse)
def query_copilot(
    payload: CopilotQueryRequest,
    service: CopilotService = Depends(get_copilot_service),
) -> CopilotQueryResponse:
    answer, sources, context = service.query(payload.question)
    return CopilotQueryResponse(answer=answer, sources=sources, context=context)