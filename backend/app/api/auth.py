from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Placeholder endpoint for health check
@router.get("/health")
def auth_health():
    return {"status": "auth service ok"}