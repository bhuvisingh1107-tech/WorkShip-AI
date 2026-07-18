from datetime import date

from sqlalchemy import JSON, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Meeting(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "meetings"

    title: Mapped[str] = mapped_column(String(500))
    date: Mapped[date] = mapped_column(Date)
    participants: Mapped[list[str]] = mapped_column(JSON)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
