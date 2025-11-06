from __future__ import annotations

import logging
from typing import Any

import structlog


def setup_logging(level: str = "INFO") -> None:
    """Конфигурация структурированного логирования."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str, **context: Any) -> structlog.stdlib.BoundLogger:
    """Возвращает структурированный логгер с привязанным контекстом."""
    logger = structlog.get_logger(name)
    if context:
        logger = logger.bind(**context)
    return logger  # type: ignore[return-value]
