from fastapi import FastAPI

from api.routers.v1 import auth, intake, script, assets
from config.logging import setup_logging
from config.settings import settings
from infrastructure.db.base import Base
from infrastructure.db.session import get_engine
from infrastructure.storage.minio_client import ensure_bucket_exists

app = FastAPI(title="Auto Video Platform API", version="0.1.0")

setup_logging(settings.log_level)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(intake.router, prefix="/api/v1/intake", tags=["intake"])
app.include_router(script.router, prefix="/api/v1/script", tags=["script"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["assets"])


@app.on_event("startup")
async def on_startup() -> None:
    """Создать таблицы при старте (временное решение вместо Alembic)."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Обеспечить наличие бакета для ассетов
    from config.settings import settings as _settings
    ensure_bucket_exists(_settings.storage.bucket_assets)


@app.get("/healthz", tags=["meta"])
async def healthcheck() -> dict[str, str]:
    """Проверка состояния сервиса."""
    return {"status": "ok"}
