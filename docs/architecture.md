# Архитектура Skeleton-проекта

## Сервисы и директории

- `api/` — FastAPI приложение, роутеры и схемы.
- `apps/` — доменные сервисы по этапам pipeline (intake, planning, production и т.д.).
- `workflows/` — Temporal workflows и activities.
- `domain/` — бизнес-модели и доменные сервисы.
- `infrastructure/` — адаптеры к БД, хранилищу, внешним API, кешу.
- `config/` — настройки, логирование, переменные окружения.
- `scripts/` — служебные скрипты (worker и пр.).
- `docker/` — Dockerfile'ы и docker-compose для локального окружения.
- `tests/` — модульные и интеграционные тесты.

## Запуск окружения

1. Поднять инфраструктуру:
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```
2. Запустить API:
   ```bash
   poetry run uvicorn api.main:app --reload
   ```
3. Запустить Temporal worker:
   ```bash
   poetry run python scripts/worker.py
   ```
4. Temporal UI доступен на `http://localhost:8080`.

## Настройки

- Все переменные в `.env` (см. `config/env/.env.example`).
- Настройки БД и Temporal инициализируются через `config/settings.py`.

## Дальнейшие шаги

- Реализовать доменные модели и репозитории.
- Добавить миграции Alembic в `infrastructure/db/migrations`.
- Расширить workflows, добавить approvals и ветвления.
- Настроить интеграцию с внешними API через клиенты в `infrastructure/external_clients/`.
