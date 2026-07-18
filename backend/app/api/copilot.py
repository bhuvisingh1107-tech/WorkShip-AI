from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.copilot import CopilotQueryRequest, CopilotQueryResponse
from app.services.copilot import CopilotService

router = APIRouter(prefix="/copilot", tags=["Copilot"])


def get_copilot_service(db: Session = Depends(get_db)) -> CopilotService:
    return CopilotService(db)


@router.post("/query", response_model=CopilotQueryResponse)
def query_copilot(
    payload: CopilotQueryRequest,
    service: CopilotService = Depends(get_copilot_service),
) -> CopilotQueryResponse:
    answer, sources, context = service.query(payload.question)
    return CopilotQueryResponse(answer=answer, sources=sources, context=context)
