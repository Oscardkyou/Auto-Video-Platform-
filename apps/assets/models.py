from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class Asset(Base):
    """Digital asset stored in S3-compatible storage and referenced in DB."""

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    brief_id: Mapped[str] = mapped_column(String, nullable=False)

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=True)

    # s3 object key and public URL (if any)
    object_key: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # image/audio/video/doc
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="uploaded")

    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_by: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
