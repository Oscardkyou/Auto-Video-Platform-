from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class Brief(Base):
    """Brief entity stored in PostgreSQL."""

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    campaign_name: Mapped[str] = mapped_column(String, nullable=False)
    objective: Mapped[str] = mapped_column(String, nullable=False)
    target_audience: Mapped[str] = mapped_column(String, nullable=False)
    launch_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="received")
    created_by: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
