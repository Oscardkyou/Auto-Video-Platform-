from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.script.models import Script


class ScriptServiceDB:
    async def create(self, session: AsyncSession, *, brief_id: str, title: str, outline: str | None, draft_text: str | None, created_by: str) -> Script:
        obj = Script(
            brief_id=brief_id,
            title=title,
            outline=outline,
            draft_text=draft_text,
            created_by=created_by,
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def list(self, session: AsyncSession, *, brief_id: str | None = None) -> list[Script]:
        stmt = select(Script).order_by(Script.created_at.desc())
        if brief_id:
            stmt = stmt.where(Script.brief_id == brief_id)
        res = await session.execute(stmt)
        return list(res.scalars().all())

    async def get(self, session: AsyncSession, script_id: str) -> Script | None:
        return await session.get(Script, script_id)

    async def update(self, session: AsyncSession, obj: Script, *, title: str | None = None, outline: str | None = None, draft_text: str | None = None) -> Script:
        if title is not None:
            obj.title = title
        if outline is not None:
            obj.outline = outline
        if draft_text is not None:
            obj.draft_text = draft_text
        await session.commit()
        await session.refresh(obj)
        return obj

    async def set_status(self, session: AsyncSession, obj: Script, *, status: str) -> Script:
        obj.status = status
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: Script) -> None:
        await session.delete(obj)
        await session.commit()


script_service = ScriptServiceDB()
