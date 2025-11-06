from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from temporalio import worker
from temporalio.client import Client

from config.settings import settings
from config.logging import get_logger, setup_logging
from workflows.campaign import CampaignWorkflow, intake_activity


setup_logging(settings.log_level)
logger = get_logger(__name__)


async def _connect_with_retry(
    factory: Callable[[], Any], *, retries: int | None = None
) -> Any:
    """Пытается подключиться к Temporal с экспоненциальной задержкой."""

    attempt = 0
    last_error: Exception | None = None
    while retries is None or attempt < retries:
        attempt += 1
        try:
            return await factory()
        except Exception as exc:  # pragma: no cover - инфраструктурный код
            last_error = exc
            wait_seconds = min(5 * attempt, 30)
            logger.warning(
                "Temporal connection failed, retrying",
                attempt=attempt,
                wait_seconds=wait_seconds,
                error=str(exc),
            )
            await asyncio.sleep(wait_seconds)
    raise RuntimeError("Unable to connect to Temporal") from last_error


async def main() -> None:
    temporal_address = f"{settings.temporal.hostname}:{settings.temporal.port}"
    logger.info("Connecting to Temporal", address=temporal_address)

    async def _factory() -> Client:
        return await Client.connect(
            temporal_address,
            namespace=settings.temporal.namespace,
        )

    client = await _connect_with_retry(_factory)
    logger.info("Temporal connection established")

    await worker.Worker(
        client,
        task_queue="campaign-production",
        workflows=[CampaignWorkflow],
        activities=[intake_activity],
    ).run()


if __name__ == "__main__":
    asyncio.run(main())
