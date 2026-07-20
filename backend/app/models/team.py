from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.incident import Incident
    from app.models.service import Service


class Team(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("workspace_id", "name", name="uq_team_workspace_name"),
    )

    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    employees: Mapped[list[Employee]] = relationship(back_populates="team")
    owned_services: Mapped[list[Service]] = relationship(back_populates="owner_team")
    owned_incidents: Mapped[list[Incident]] = relationship(back_populates="owner_team")