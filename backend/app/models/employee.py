from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.team import Team


class Employee(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "employees"

    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    manager_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("employees.id"), nullable=True
    )
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)

    manager: Mapped[Employee | None] = relationship(
        back_populates="direct_reports", remote_side="Employee.id"
    )
    direct_reports: Mapped[list[Employee]] = relationship(back_populates="manager")
    team: Mapped[Team] = relationship(back_populates="employees")
