from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.service import Service
    from app.models.team import Team


class Incident(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incidents"

    title: Mapped[str] = mapped_column(String(500))
    severity: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100))
    service_id: Mapped[UUID] = mapped_column(ForeignKey("services.id"), nullable=False)
    owner_team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    root_cause: Mapped[str | None] = mapped_column(Text, nullable=True)

    service: Mapped[Service] = relationship(back_populates="incidents")
    owner_team: Mapped[Team] = relationship(back_populates="owned_incidents")
