from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import require_roles
from api.schemas.assets import (
    AssetAttachRequest,
    AssetListResponse,
    AssetResponse,
    AssetUploadURLRequest,
    AssetUploadURLResponse,
)
from apps.assets.service import asset_service
from config.settings import settings
from domain.models.user import User
from infrastructure.db.session import get_db_session
from infrastructure.storage.minio_client import create_presigned_get, create_presigned_put

AUTHORIZED_ROLES_CREATE = ("marketing", "producer", "admin")
AUTHORIZED_ROLES_READ = ("marketing", "producer", "legal", "brand", "admin")
AUTHORIZED_ROLES_WRITE = ("marketing", "producer", "admin")

router = APIRouter()


@router.post("/upload-url", response_model=AssetUploadURLResponse)
async def create_upload_url(
    payload: AssetUploadURLRequest,
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> AssetUploadURLResponse:
    object_key = f"briefs/{payload.brief_id}/{uuid4()}_{payload.filename}"
    url = create_presigned_put(
        bucket=settings.storage.bucket_assets,
        object_key=object_key,
        expires=timedelta(minutes=15),
        content_type=payload.content_type,
    )
    return AssetUploadURLResponse(object_key=object_key, upload_url=url)


@router.post("/attach", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def attach_uploaded_asset(
    payload: AssetAttachRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> AssetResponse:
    obj = await asset_service.attach(
        session,
        brief_id=payload.brief_id,
        object_key=payload.object_key,
        filename=payload.filename,
        content_type=payload.content_type,
        size=payload.size,
        type=payload.type,
        created_by=current_user.email,
        meta=payload.meta,
    )
    return AssetResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "filename": obj.filename,
            "content_type": obj.content_type,
            "size": obj.size,
            "object_key": obj.object_key,
            "url": obj.url,
            "type": obj.type,
            "status": obj.status,
            "meta": obj.meta,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.get("/assets", response_model=AssetListResponse)
async def list_assets(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
    brief_id: str | None = None,
) -> AssetListResponse:
    objs = await asset_service.list(session, brief_id=brief_id)
    items = [
        AssetResponse.model_validate(
            {
                "id": o.id,
                "brief_id": o.brief_id,
                "filename": o.filename,
                "content_type": o.content_type,
                "size": o.size,
                "object_key": o.object_key,
                "url": o.url,
                "type": o.type,
                "status": o.status,
                "meta": o.meta,
                "created_by": o.created_by,
                "created_at": o.created_at,
                "updated_at": o.updated_at,
            }
        )
        for o in objs
    ]
    return AssetListResponse(items=items)


@router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> AssetResponse:
    obj = await asset_service.get(session, asset_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    return AssetResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "filename": obj.filename,
            "content_type": obj.content_type,
            "size": obj.size,
            "object_key": obj.object_key,
            "url": obj.url,
            "type": obj.type,
            "status": obj.status,
            "meta": obj.meta,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.get("/assets/{asset_id}/download-url")
async def get_download_url(
    asset_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> dict[str, str]:
    obj = await asset_service.get(session, asset_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    url = create_presigned_get(
        bucket=settings.storage.bucket_assets,
        object_key=obj.object_key,
    )
    return {"download_url": url}


@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> Response:
    obj = await asset_service.get(session, asset_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    await asset_service.delete(session, obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
