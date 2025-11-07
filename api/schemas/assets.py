from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class AssetUploadURLRequest(BaseModel):
    brief_id: str
    filename: str = Field(..., max_length=255)
    content_type: str = Field(..., max_length=128)
    type: Literal["image", "audio", "video", "doc"]
    size: int | None = Field(default=None, ge=0)


class AssetUploadURLResponse(BaseModel):
    object_key: str
    upload_url: str


class AssetAttachRequest(BaseModel):
    brief_id: str
    object_key: str
    filename: str
    content_type: str
    type: Literal["image", "audio", "video", "doc"]
    size: int | None = Field(default=None, ge=0)
    meta: dict | None = None


class AssetResponse(BaseModel):
    id: str
    brief_id: str
    filename: str
    content_type: str
    size: int | None
    object_key: str
    url: str | None
    type: str
    status: str
    meta: dict | None
    created_by: str
    created_at: datetime
    updated_at: datetime


class AssetListResponse(BaseModel):
    items: list[AssetResponse]
