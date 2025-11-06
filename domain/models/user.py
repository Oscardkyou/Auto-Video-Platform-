from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["marketing", "producer", "legal", "brand", "admin"]


class User(BaseModel):
    """Пользователь платформы."""

    id: str
    email: str
    full_name: str
    hashed_password: str
    role: Role
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
