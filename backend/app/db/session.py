from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.database import Base

engine_options: dict[str, Any] = {"pool_pre_ping": True}
if settings.DATABASE_URL == "sqlite://":
    engine_options.update(
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

engine = create_engine(settings.DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for request-scoped dependencies."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database() -> None:
    """Register declarative models and initialize the configured database schema."""

    import app.models  # noqa: F401

    ensure_pgvector_extension()
    Base.metadata.create_all(bind=engine)
    ensure_document_rag_columns()
    ensure_document_embedding_column()


def ensure_pgvector_extension() -> None:
    """Enable pgvector when running against PostgreSQL; safe on repeated startup."""

    if engine.dialect.name != "postgresql":
        return
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


def ensure_document_rag_columns() -> None:
    """Safely add the small persisted document fields required for RAG preparation."""

    existing_columns = {
        column["name"] for column in inspect(engine).get_columns("documents")
    }
    additions = {
        "summary": "TEXT",
        "tags": "JSONB" if engine.dialect.name == "postgresql" else "JSON",
    }
    missing_columns = [
        (name, column_type)
        for name, column_type in additions.items()
        if name not in existing_columns
    ]
    if not missing_columns:
        return

    with engine.begin() as connection:
        for name, column_type in missing_columns:
            if engine.dialect.name == "postgresql":
                connection.execute(
                    text(
                        f"ALTER TABLE documents ADD COLUMN IF NOT EXISTS {name} {column_type}"
                    )
                )
            else:
                connection.execute(text(f"ALTER TABLE documents ADD COLUMN {name} {column_type}"))


def ensure_document_embedding_column() -> None:
    """Safely add the fixed-size embedding column used by semantic retrieval."""

    existing_columns = {
        column["name"] for column in inspect(engine).get_columns("documents")
    }
    if "embedding" in existing_columns:
        return

    column_type = "vector(1536)" if engine.dialect.name == "postgresql" else "JSON"
    with engine.begin() as connection:
        if engine.dialect.name == "postgresql":
            connection.execute(
                text(
                    "ALTER TABLE documents "
                    "ADD COLUMN IF NOT EXISTS embedding vector(1536)"
                )
            )
        else:
            connection.execute(text(f"ALTER TABLE documents ADD COLUMN embedding {column_type}"))
