from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LogEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "log_entries"

    service: Mapped[str] = mapped_column(String(255), index=True)
    level: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    message: Mapped[str] = mapped_column(Text)
