from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from api.schemas.intake import BriefCreateRequest
from domain.models.user import User
from pydantic import BaseModel


class Brief(BaseModel):
    id: str
    campaign_name: str
    objective: str
    target_audience: str
    launch_date: datetime
    budget: float
    status: str = "received"
    created_by: str
    created_at: datetime


class IntakeService:
    """Простейший in-memory сервис брифов."""

    def __init__(self) -> None:
        self._briefs: Dict[str, Brief] = {}

    def create_brief(self, payload: BriefCreateRequest, user: User) -> Brief:
        brief = Brief(
            id=str(uuid4()),
            campaign_name=payload.campaign_name,
            objective=payload.objective,
            target_audience=payload.target_audience,
            launch_date=payload.launch_date,
            budget=payload.budget,
            created_by=user.email,
            created_at=datetime.utcnow(),
        )
        self._briefs[brief.id] = brief
        return brief

    def list_briefs(self) -> List[Brief]:
        return list(self._briefs.values())


intake_service = IntakeService()
