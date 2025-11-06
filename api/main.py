from fastapi import FastAPI

from api.routers.v1 import auth, intake

app = FastAPI(title="Auto Video Platform API", version="0.1.0")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(intake.router, prefix="/api/v1/intake", tags=["intake"])


@app.get("/healthz", tags=["meta"])
async def healthcheck() -> dict[str, str]:
    """Проверка состояния сервиса."""
    return {"status": "ok"}
