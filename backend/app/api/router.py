from fastapi import APIRouter

from app.api.copilot import router as copilot_router
from app.api.dashboard import router as dashboard_router
from app.api.documents import router as documents_router
from app.api.employees import router as employees_router
from app.api.health import router as health_router
from app.api.incidents import router as incidents_router
from app.api.meetings import router as meetings_router
from app.api.search import router as search_router
from app.api.services import router as services_router
from app.api.teams import router as teams_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(copilot_router)
api_router.include_router(dashboard_router)
api_router.include_router(teams_router)
api_router.include_router(employees_router)
api_router.include_router(services_router)
api_router.include_router(documents_router)
api_router.include_router(search_router)
api_router.include_router(incidents_router)
api_router.include_router(meetings_router)
