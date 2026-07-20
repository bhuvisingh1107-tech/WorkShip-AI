import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.api.router import api_router
from app.core.exceptions import DatabaseIntegrityError, ResourceNotFoundError
from app.db.session import initialize_database


def _get_rate_limit_key(request: Request):
    return get_remote_address(request)


limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])


def get_cors_origins() -> List[str]:
    """Parse CORS origins from environment variable."""
    cors_env = os.getenv("BACKEND_CORS_ORIGINS", "")
    if not cors_env:   # was: if not cors_embedding
        return []
    return [origin.strip() for origin in cors_env.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="WorkShip AI API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
cors_origins = get_cors_origins()
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


# Apply rate limit to auth endpoints via middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/auth/"):
        return await limiter.http_middleware("default")(request, call_next)
    return await call_next(request)


@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(_, error: ResourceNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(error), "code": "resource_not_found"},
    )


@app.exception_handler(DatabaseIntegrityError)
async def database_integrity_handler(_, error: DatabaseIntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(error), "code": "database_constraint_violation"},
    )


app.include_router(api_router)