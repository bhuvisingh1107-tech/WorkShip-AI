from typing import Generic, TypeVar

from pydantic import BaseModel, Field

SchemaType = TypeVar("SchemaType")


class PaginatedResponse(BaseModel, Generic[SchemaType]):
    items: list[SchemaType]
    total: int
    skip: int = Field(ge=0)
    limit: int = Field(ge=1)


class MessageResponse(BaseModel):
    detail: str
