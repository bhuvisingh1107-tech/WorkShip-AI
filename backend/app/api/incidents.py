from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.incident import (
    IncidentCreate,
    IncidentRead,
    IncidentSimulationRequest,
    IncidentSimulationResponse,
    IncidentUpdate,
    RelatedDocument,
    RelatedIncident,
)
from app.services.incident import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


def get_incident_service(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
) -> IncidentService:
    return IncidentService(db, current_user.workspace_id)


@router.get("", response_model=PaginatedResponse[IncidentRead])
def list_incidents(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Literal["title", "severity", "status", "created_at"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    service_id: UUID | None = None,
    owner_team_id: UUID | None = None,
    severity: str | None = None,
    incident_status: str | None = Query(None, alias="status"),
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> PaginatedResponse[IncidentRead]:
    items, total = service.list(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        service_id=service_id,
        owner_team_id=owner_team_id,
        severity=severity,
        status=incident_status,
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentRead:
    return service.get(incident_id)


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(
    *,
    db: Session = Depends(get_db),
    payload: IncidentCreate,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentRead:
    return service.create(payload)


@router.post("/simulate", response_model=IncidentSimulationResponse, status_code=status.HTTP_201_CREATED)
def simulate_incident(
    *,
    db: Session = Depends(get_db),
    payload: IncidentSimulationRequest,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentSimulationResponse:
    incident, similar_incidents, documents, analysis = service.simulate(
        title=payload.title, description=payload.description, severity=payload.severity
    )
    return IncidentSimulationResponse(
        incident=incident,
        similarIncidents=[
            RelatedIncident(
                title=item.title,
                relationship="Recent incident on the same service; not a semantic similarity score",
            )
            for item in similar_incidents
        ],
        relatedDocuments=[
            RelatedDocument(title=document.title, similarity=round(similarity, 4))
            for document, similarity in documents
        ],
        recommendedActions=analysis.recommendedActions,
        timeline=analysis.timeline,
        rootCauseHypothesis=analysis.rootCauseHypothesis,
    )


@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident(
    *,
    db: Session = Depends(get_db),
    incident_id: UUID,
    payload: IncidentUpdate,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentRead:
    return service.update(incident_id, payload)


@router.delete("/{incident_id}", response_model=MessageResponse)
def delete_incident(
    *,
    db: Session = Depends(get_db),
    incident_id: UUID,
    current_user: Employee = Depends(deps.get_current_active_user),
    service: IncidentService = Depends(get_incident_service),
) -> MessageResponse:
    service.delete(incident_id)
    return MessageResponse(detail="Incident deleted")
