from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Базовая модель SQLAlchemy."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: D401
        """Автоматически генерирует имя таблицы из имени класса."""
        return cls.__name__.lower()

    id: Any
