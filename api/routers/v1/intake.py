from fastapi import APIRouter, Depends, status

from api.deps import require_roles
from api.schemas.intake import BriefCreateRequest, BriefListResponse, BriefResponse
from apps.intake.service import intake_service
from domain.models.user import User

AUTHORIZED_ROLES_CREATE = ("marketing", "producer", "admin")
AUTHORIZED_ROLES_READ = ("marketing", "producer", "legal", "brand", "admin")

router = APIRouter()


@router.post("/briefs", response_model=BriefResponse, status_code=status.HTTP_201_CREATED)
async def create_brief(
    payload: BriefCreateRequest,
    current_user: User = Depends(require_roles(*AUTHORIZED_ROLES_CREATE)),
) -> BriefResponse:
    """Создание нового брифа."""
    brief = intake_service.create_brief(payload, current_user)
    return BriefResponse.model_validate(brief.model_dump())


@router.get("/briefs", response_model=BriefListResponse)
async def list_briefs(
    _: User = Depends(require_roles(*AUTHORIZED_ROLES_READ)),
) -> BriefListResponse:
    """Получить список брифов."""
    briefs = intake_service.list_briefs()
    return BriefListResponse(items=[BriefResponse.model_validate(b.model_dump()) for b in briefs])
