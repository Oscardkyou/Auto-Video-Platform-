from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.assets.models import Asset


class AssetServiceDB:
    async def attach(
        self,
        session: AsyncSession,
        *,
        brief_id: str,
        object_key: str,
        filename: str,
        content_type: str,
        size: int | None,
        type: str,
        created_by: str,
        meta: dict | None = None,
    ) -> Asset:
        obj = Asset(
            brief_id=brief_id,
            object_key=object_key,
            filename=filename,
            content_type=content_type,
            size=size,
            type=type,
            created_by=created_by,
            meta=meta,
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def list(self, session: AsyncSession, *, brief_id: str | None = None) -> list[Asset]:
        stmt = select(Asset).order_by(Asset.created_at.desc())
        if brief_id:
            stmt = stmt.where(Asset.brief_id == brief_id)
        res = await session.execute(stmt)
        return list(res.scalars().all())

    async def get(self, session: AsyncSession, asset_id: str) -> Asset | None:
        return await session.get(Asset, asset_id)

    async def delete(self, session: AsyncSession, obj: Asset) -> None:
        await session.delete(obj)
        await session.commit()


asset_service = AssetServiceDB()
