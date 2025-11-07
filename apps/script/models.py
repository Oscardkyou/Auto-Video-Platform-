from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class Script(Base):
    """Script/Storyboard entity linked to a brief."""

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    brief_id: Mapped[str] = mapped_column(String, nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    outline: Mapped[str] = mapped_column(Text, nullable=True)
    draft_text: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")

    created_by: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
