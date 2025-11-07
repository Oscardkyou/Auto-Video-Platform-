from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class BriefCreateRequest(BaseModel):
    campaign_name: str = Field(..., max_length=255)
    objective: Literal["awareness", "consideration", "conversion"]
    target_audience: str
    launch_date: datetime
    budget: float = Field(ge=0)


class BriefResponse(BaseModel):
    id: str
    campaign_name: str
    objective: str
    target_audience: str
    launch_date: datetime
    budget: float
    status: str
    created_by: str
    created_at: datetime


class BriefListResponse(BaseModel):
    items: list[BriefResponse]


class BriefUpdateRequest(BaseModel):
    campaign_name: str | None = Field(None, max_length=255)
    objective: Literal["awareness", "consideration", "conversion"] | None = None
    target_audience: str | None = None
    launch_date: datetime | None = None
    budget: float | None = Field(default=None, ge=0)


class BriefStatusUpdateRequest(BaseModel):
    status: Literal["received", "in_progress", "approved", "rejected", "scheduled", "published"]
