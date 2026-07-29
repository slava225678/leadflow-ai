from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, DateTime, Integer, String, Text, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LeadStatus(StrEnum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str] = mapped_column(Text)

    summary = mapped_column(Text, nullable=True)
    priority = mapped_column(
        String(20),
        nullable=True,
    )
    budget = mapped_column(
        Integer,
        nullable=True,
    )
    analysis_json = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[LeadStatus] = mapped_column(
        SqlEnum(LeadStatus),
        default=LeadStatus.NEW,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
