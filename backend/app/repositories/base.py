from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseIntegrityError
from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, resource_id: UUID) -> ModelType | None:
        return self.db.get(self.model, resource_id)

    def list(
        self,
        *,
        skip: int,
        limit: int,
        sort_by: str,
        sort_order: str,
        filters: list[Any] | None = None,
    ) -> tuple[list[ModelType], int]:
        filters = filters or []
        sort_column = getattr(self.model, sort_by)
        order_by = sort_column.desc() if sort_order == "desc" else sort_column.asc()
        statement = (
            select(self.model)
            .where(*filters)
            .order_by(order_by)
            .offset(skip)
            .limit(limit)
        )
        count_statement = select(func.count()).select_from(self.model).where(*filters)
        return list(self.db.scalars(statement).all()), self.db.scalar(count_statement) or 0

    def create(self, data: dict[str, Any]) -> ModelType:
        resource = self.model(**data)
        self.db.add(resource)
        self._commit()
        self.db.refresh(resource)
        return resource

    def update(self, resource: ModelType, data: dict[str, Any]) -> ModelType:
        for field, value in data.items():
            setattr(resource, field, value)
        self._commit()
        self.db.refresh(resource)
        return resource

    def delete(self, resource: ModelType) -> None:
        self.db.delete(resource)
        self._commit()

    def _commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as error:
            self.db.rollback()
            raise DatabaseIntegrityError("Database constraint violation") from error
