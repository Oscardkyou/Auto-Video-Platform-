from __future__ import annotations

from datetime import timedelta

from temporalio import activity, workflow


@activity.defn
async def intake_activity(brief_id: str) -> str:
    """Заглушка приема брифа."""
    return f"processed:{brief_id}"


@workflow.defn
class CampaignWorkflow:
    """Базовый каркас workflow кампании."""

    @workflow.run
    async def run(self, brief_id: str) -> str:  # noqa: D401
        """Основной сценарий работы skeleton."""
        result = await workflow.execute_activity(
            intake_activity,
            brief_id,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=workflow.RetryPolicy(maximum_attempts=3),
        )
        return result
