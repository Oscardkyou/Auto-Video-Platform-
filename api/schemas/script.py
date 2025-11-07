from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ScriptCreateRequest(BaseModel):
    brief_id: str = Field(...)
    title: str = Field(..., max_length=255)
    outline: str | None = None
    draft_text: str | None = None


class ScriptUpdateRequest(BaseModel):
    title: str | None = Field(None, max_length=255)
    outline: str | None = None
    draft_text: str | None = None


class ScriptStatusUpdateRequest(BaseModel):
    status: Literal["pending", "drafted", "approved", "rejected"]


class ScriptResponse(BaseModel):
    id: str
    brief_id: str
    title: str
    outline: str | None
    draft_text: str | None
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class ScriptListResponse(BaseModel):
    items: list[ScriptResponse]
