from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config.settings import settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Ленивое создание движка."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(str(settings.database.url), echo=False)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Возвращает фабрику сессий."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _session_factory


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Зависимость FastAPI: асинхронная сессия БД."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session
