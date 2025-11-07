from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import require_roles
from api.schemas.script import (
    ScriptCreateRequest,
    ScriptListResponse,
    ScriptResponse,
    ScriptStatusUpdateRequest,
    ScriptUpdateRequest,
)
from apps.script.service import script_service
from domain.models.user import User
from infrastructure.db.session import get_db_session

AUTHORIZED_ROLES_CREATE = ("marketing", "producer", "admin")
AUTHORIZED_ROLES_READ = ("marketing", "producer", "legal", "brand", "admin")
AUTHORIZED_ROLES_WRITE = ("marketing", "producer", "admin")

router = APIRouter()


@router.post("/scripts", response_model=ScriptResponse, status_code=status.HTTP_201_CREATED)
async def create_script(
    payload: ScriptCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_roles(*AUTHORIZED_ROLES_CREATE)),
) -> ScriptResponse:
    obj = await script_service.create(
        session,
        brief_id=payload.brief_id,
        title=payload.title,
        outline=payload.outline,
        draft_text=payload.draft_text,
        created_by=current_user.email,
    )
    return ScriptResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "title": obj.title,
            "outline": obj.outline,
            "draft_text": obj.draft_text,
            "status": obj.status,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.get("/scripts", response_model=ScriptListResponse)
async def list_scripts(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
    brief_id: str | None = None,
) -> ScriptListResponse:
    objs = await script_service.list(session, brief_id=brief_id)
    items = [
        ScriptResponse.model_validate(
            {
                "id": o.id,
                "brief_id": o.brief_id,
                "title": o.title,
                "outline": o.outline,
                "draft_text": o.draft_text,
                "status": o.status,
                "created_by": o.created_by,
                "created_at": o.created_at,
                "updated_at": o.updated_at,
            }
        )
        for o in objs
    ]
    return ScriptListResponse(items=items)


@router.get("/scripts/{script_id}", response_model=ScriptResponse)
async def get_script(
    script_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> ScriptResponse:
    obj = await script_service.get(session, script_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Script not found")
    return ScriptResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "title": obj.title,
            "outline": obj.outline,
            "draft_text": obj.draft_text,
            "status": obj.status,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.patch("/scripts/{script_id}", response_model=ScriptResponse)
async def update_script(
    script_id: str,
    payload: ScriptUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> ScriptResponse:
    obj = await script_service.get(session, script_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Script not found")
    obj = await script_service.update(
        session, obj, title=payload.title, outline=payload.outline, draft_text=payload.draft_text
    )
    return ScriptResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "title": obj.title,
            "outline": obj.outline,
            "draft_text": obj.draft_text,
            "status": obj.status,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.patch("/scripts/{script_id}/status", response_model=ScriptResponse)
async def update_script_status(
    script_id: str,
    payload: ScriptStatusUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> ScriptResponse:
    obj = await script_service.get(session, script_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Script not found")
    obj = await script_service.set_status(session, obj, status=payload.status)
    return ScriptResponse.model_validate(
        {
            "id": obj.id,
            "brief_id": obj.brief_id,
            "title": obj.title,
            "outline": obj.outline,
            "draft_text": obj.draft_text,
            "status": obj.status,
            "created_by": obj.created_by,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
    )


@router.delete("/scripts/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_script(
    script_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> Response:
    obj = await script_service.get(session, script_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Script not found")
    await script_service.delete(session, obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
