import json
from typing import Sequence
from uuid import UUID

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundError
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.schemas.incident import IncidentAIAnalysis, IncidentCreate, IncidentUpdate
from app.services.document import DocumentService


class IncidentService:
    def __init__(self, db: Session, workspace_id: UUID) -> None:
        self.repository = IncidentRepository(db)
        self.workspace_id = workspace_id
        self.client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required to simulate an incident")
        if self.client is None:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self.client

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        service_id: UUID | None = None,
        owner_team_id: UUID | None = None,
        severity: str | None = None,
        status: str | None = None,
    ):
        filters = [self.repository.model.workspace_id == self.workspace_id]
        if service_id:
            filters.append(self.repository.model.service_id == service_id)
        if owner_team_id:
            filters.append(self.repository.model.owner_team_id == owner_team_id)
        if severity:
            filters.append(self.repository.model.severity == severity)
        if status:
            filters.append(self.repository.model.status == status)
        return self.repository.list(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, filters=filters)

    def get(self, incident_id: UUID) -> Incident:
        incident = self.repository.get(incident_id)
        if incident is None or incident.workspace_id != self.workspace_id:
            raise ResourceNotFoundError("Incident not found")
        return incident

    def create(self, payload: IncidentCreate) -> Incident:
        data = payload.model_dump()
        data["workspace_id"] = self.workspace_id
        return self.repository.create(data)

    def update(self, incident_id: UUID, payload: IncidentUpdate) -> Incident:
        incident = self.get(incident_id)
        return self.repository.update(incident, payload.model_dump(exclude_unset=True))

    def delete(self, incident_id: UUID) -> None:
        incident = self.get(incident_id)
        self.repository.delete(incident)

    def simulate(self, *, title: str, description: str, severity: str):
        from app.models.service import Service

        service_name = next(
            (
                name
                for keyword, name in {
                    "payment": "Payroll Processing",
                    "database": "Data Warehouse",
                    "auth": "Identity Gateway",
                }.items()
                if keyword in f"{title} {description}".lower()
            ),
            "Incident Command Center",
        )
        service = self.repository.db.query(Service).filter(
            Service.workspace_id == self.workspace_id,
            Service.name == service_name
        ).one()
        incident = self.create(
            IncidentCreate(
                title=title,
                severity=severity,
                status="investigating",
                service_id=service.id,
                owner_team_id=service.owner_team_id,
                summary=description,
            )
        )
        similar_incidents, _ = self.list(
            skip=0,
            limit=3,
            sort_by="created_at",
            sort_order="desc",
            service_id=service.id,
            owner_team_id=None,
            severity=None,
            status=None,
        )
        documents = DocumentService(self.repository.db, self.workspace_id).semantic_search(
            query=f"{title} {description}", limit=3
        )
        historical_incidents = [item for item in similar_incidents if item.id != incident.id]
        analysis = self._analyze_incident(
            title=title,
            description=description,
            severity=severity,
            similar_incidents=historical_incidents,
            documents=documents,
        )
        incident.root_cause = analysis.rootCauseHypothesis
        self.repository.db.commit()
        self.repository.db.refresh(incident)
        return incident, historical_incidents, documents, analysis

    def _analyze_incident(
        self,
        *,
        title: str,
        description: str,
        severity: str,
        similar_incidents: Sequence[Incident],
        documents: Sequence[tuple],
    ) -> IncidentAIAnalysis:
        incident_context = "\n".join(
            (
                f"- Title: {item.title}\n"
                f"  Severity: {item.severity}; Status: {item.status}\n"
                f"  Summary: {item.summary or 'No summary available'}\n"
                f"  Root cause: {item.root_cause or 'Not recorded'}"
            )
            for item in similar_incidents
        ) or "No similar historical incidents found."
        document_context = "\n".join(
            (
                f"- Title: {document.title} (retrieval similarity: {similarity:.4f})\n"
                f"  Excerpt: {document.summary or document.content[:800]}"
            )
            for document, similarity in documents
        ) or "No related knowledge documents found."
        completion = self._get_client().chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an incident commander. Generate a response only from the "
                        "reported incident and supplied enterprise knowledge. Produce 3 to 5 "
                        "specific, ordered recommended actions and 3 to 6 ordered timeline steps. "
                        "Do not invent systems, deployment events, owners, or evidence. If the "
                        "context is insufficient, state that limitation in the root-cause hypothesis."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Incident title: {title}\nDescription: {description}\nSeverity: {severity}\n\n"
                        f"Similar incidents:\n{incident_context}\n\nRelated documents:\n{document_context}"
                    ),
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "incident_analysis",
                    "strict": True,
                    "schema": IncidentAIAnalysis.model_json_schema(),
                },
            },
        )
        content = completion.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty incident analysis")
        return IncidentAIAnalysis.model_validate(json.loads(content))
