# Auto Video Platform Skeleton

Каркас проекта для системы автоматизации медиаконтента.

## Быстрый старт

1. Установите Poetry `curl -sSL https://install.python-poetry.org | python3 -`.
2. Установите зависимости:
   ```bash
   poetry install
   ```
3. Скопируйте файл `.env.example`:
   ```bash
   cp config/env/.env.example .env
   ```
4. Запустите docker-compose (PostgreSQL, MinIO, Temporal, Web UI):
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```
5. Запустите локально API:
   ```bash
   poetry run uvicorn api.main:app --reload
   ```
6. Запустите Temporal worker:
   ```bash
   poetry run python scripts/worker.py
   ```

## Структура каталога

См. раздел "Project layout" в `docs/architecture.md`.

## Код-стайл и тесты

- Форматирование: `poetry run black .`
- Линтинг: `poetry run ruff check .`
- Статический анализ: `poetry run mypy .`
- Тесты: `poetry run pytest`
