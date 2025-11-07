from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.intake import BriefCreateRequest
from apps.intake.models import Brief
from domain.models.user import User


class IntakeServiceDB:
    """Сервис брифов на PostgreSQL (async SQLAlchemy)."""

    async def create_brief(self, session: AsyncSession, payload: BriefCreateRequest, user: User) -> Brief:
        brief = Brief(
            campaign_name=payload.campaign_name,
            objective=payload.objective,
            target_audience=payload.target_audience,
            launch_date=payload.launch_date,
            budget=payload.budget,
            created_by=user.email,
        )
        session.add(brief)
        await session.commit()
        await session.refresh(brief)
        return brief

    async def list_briefs(self, session: AsyncSession) -> list[Brief]:
        result = await session.execute(select(Brief).order_by(Brief.created_at.desc()))
        return list(result.scalars().all())

    async def get_brief(self, session: AsyncSession, brief_id: str) -> Brief | None:
        return await session.get(Brief, brief_id)

    async def update_brief(self, session: AsyncSession, brief: Brief, **fields) -> Brief:
        for k, v in fields.items():
            if v is not None:
                setattr(brief, k, v)
        await session.commit()
        await session.refresh(brief)
        return brief

    async def delete_brief(self, session: AsyncSession, brief: Brief) -> None:
        await session.delete(brief)
        await session.commit()


intake_service = IntakeServiceDB()
