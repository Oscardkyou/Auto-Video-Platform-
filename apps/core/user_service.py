from __future__ import annotations

from typing import Dict

from domain.models.user import Role, User
from infrastructure.auth.security import get_password_hash
from config.settings import settings


class InMemoryUserService:
    """Простейший сервис пользователей для skeleton."""

    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._bootstrap()

    def _bootstrap(self) -> None:
        admin = User(
            id="admin",
            email=settings.demo_user.admin_email,
            full_name="Default Admin",
            hashed_password=get_password_hash(settings.demo_user.admin_password),
            role="admin",
        )
        self._users[admin.email] = admin
        # Псевдоним для упрощенного логина без домена
        self._users.setdefault("admin", admin)

    def get_user_by_email(self, email: str) -> User | None:
        return self._users.get(email)

    def create_user(self, email: str, full_name: str, password: str, role: Role) -> User:
        if email in self._users:
            raise ValueError("User already exists")
        user = User(
            id=email,
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=role,
        )
        self._users[email] = user
        return user


user_service = InMemoryUserService()
