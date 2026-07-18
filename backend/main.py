from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.exceptions import DatabaseIntegrityError, ResourceNotFoundError
from app.db.session import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="WorkShip AI API",
    version="0.1.0",
    lifespan=lifespan,
)


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
