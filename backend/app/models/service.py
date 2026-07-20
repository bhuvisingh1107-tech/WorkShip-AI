from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.incident import Incident
    from app.models.team import Team


class Service(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "services"
    __table_args__ = (
        UniqueConstraint("workspace_id", "name", name="uq_service_workspace_name"),
    )

    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
    criticality: Mapped[str | None] = mapped_column(String(100), nullable=True)

    owner_team: Mapped[Team] = relationship(back_populates="owned_services")
    incidents: Mapped[list[Incident]] = relationship(back_populates="service")