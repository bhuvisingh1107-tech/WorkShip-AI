from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LogEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "log_entries"

    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id"), nullable=False, index=True)
    service: Mapped[str] = mapped_column(String(255), index=True)
    level: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    message: Mapped[str] = mapped_column(Text)