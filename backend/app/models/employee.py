from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid, JSON, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.workspace import Workspace


class Employee(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "employees"
    __table_args__ = (
        UniqueConstraint("workspace_id", "email", name="uq_employee_workspace_email"),
        UniqueConstraint("supabase_user_id", name="uq_employee_supabase_user_id"),
    )

    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id"), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    supabase_user_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), unique=True, nullable=True)
    preferences: Mapped[Dict[str, Any]] = mapped_column(
        JSON, nullable=False, server_default=text("'{}'")
    )
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    avatar: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    manager_id: Mapped[UUID | None] = mapped_column(ForeignKey("employees.id"), nullable=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    manager: Mapped[Employee | None] = relationship(
        back_populates="direct_reports", remote_side="Employee.id"
    )
    direct_reports: Mapped[list[Employee]] = relationship(back_populates="manager")
    team: Mapped[Team] = relationship(back_populates="employees")
    workspace: Mapped[Workspace] = relationship()