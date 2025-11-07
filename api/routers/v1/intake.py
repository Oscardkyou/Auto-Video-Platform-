from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import require_roles
from api.schemas.intake import (
    BriefCreateRequest,
    BriefListResponse,
    BriefResponse,
    BriefStatusUpdateRequest,
    BriefUpdateRequest,
)
from apps.intake.models import Brief
from apps.intake.service import intake_service
from domain.models.user import User
from infrastructure.db.session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

AUTHORIZED_ROLES_CREATE = ("marketing", "producer", "admin")
AUTHORIZED_ROLES_READ = ("marketing", "producer", "legal", "brand", "admin")
AUTHORIZED_ROLES_WRITE = ("marketing", "producer", "admin")

router = APIRouter()


@router.post("/briefs", response_model=BriefResponse, status_code=status.HTTP_201_CREATED)
async def create_brief(
    payload: BriefCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_roles(*AUTHORIZED_ROLES_CREATE)),
) -> BriefResponse:
    """Создание нового брифа."""
    brief = await intake_service.create_brief(session, payload, current_user)
    return BriefResponse.model_validate({
        "id": brief.id,
        "campaign_name": brief.campaign_name,
        "objective": brief.objective,
        "target_audience": brief.target_audience,
        "launch_date": brief.launch_date,
        "budget": brief.budget,
        "status": brief.status,
        "created_by": brief.created_by,
        "created_at": brief.created_at,
    })


@router.get("/briefs", response_model=BriefListResponse)
async def list_briefs(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> BriefListResponse:
    """Получить список брифов."""
    briefs = await intake_service.list_briefs(session)
    items = [
        BriefResponse.model_validate({
            "id": b.id,
            "campaign_name": b.campaign_name,
            "objective": b.objective,
            "target_audience": b.target_audience,
            "launch_date": b.launch_date,
            "budget": b.budget,
            "status": b.status,
            "created_by": b.created_by,
            "created_at": b.created_at,
        })
        for b in briefs
    ]
    return BriefListResponse(items=items)


@router.get("/briefs/{brief_id}", response_model=BriefResponse)
async def get_brief(
    brief_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> BriefResponse:
    brief = await intake_service.get_brief(session, brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return BriefResponse.model_validate({
        "id": brief.id,
        "campaign_name": brief.campaign_name,
        "objective": brief.objective,
        "target_audience": brief.target_audience,
        "launch_date": brief.launch_date,
        "budget": brief.budget,
        "status": brief.status,
        "created_by": brief.created_by,
        "created_at": brief.created_at,
    })


@router.patch("/briefs/{brief_id}", response_model=BriefResponse)
async def update_brief(
    brief_id: str,
    payload: BriefUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> BriefResponse:
    brief = await intake_service.get_brief(session, brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    brief = await intake_service.update_brief(
        session,
        brief,
        campaign_name=payload.campaign_name,
        objective=payload.objective,
        target_audience=payload.target_audience,
        launch_date=payload.launch_date,
        budget=payload.budget,
    )
    return BriefResponse.model_validate({
        "id": brief.id,
        "campaign_name": brief.campaign_name,
        "objective": brief.objective,
        "target_audience": brief.target_audience,
        "launch_date": brief.launch_date,
        "budget": brief.budget,
        "status": brief.status,
        "created_by": brief.created_by,
        "created_at": brief.created_at,
    })


@router.patch("/briefs/{brief_id}/status", response_model=BriefResponse)
async def update_brief_status(
    brief_id: str,
    payload: BriefStatusUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> BriefResponse:
    brief = await intake_service.get_brief(session, brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    brief = await intake_service.update_brief(session, brief, status=payload.status)
    return BriefResponse.model_validate({
        "id": brief.id,
        "campaign_name": brief.campaign_name,
        "objective": brief.objective,
        "target_audience": brief.target_audience,
        "launch_date": brief.launch_date,
        "budget": brief.budget,
        "status": brief.status,
        "created_by": brief.created_by,
        "created_at": brief.created_at,
    })


@router.delete("/briefs/{brief_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brief(
    brief_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_WRITE)),
) -> None:
    brief = await intake_service.get_brief(session, brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    await intake_service.delete_brief(session, brief)
    return None
