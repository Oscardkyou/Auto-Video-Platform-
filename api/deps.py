from __future__ import annotations

from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from domain.models.user import Role, User
from infrastructure.auth.security import verify_password
from apps.core.user_service import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.security.secret_key,
            algorithms=[settings.security.algorithm],
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as exc:  # pragma: no cover - внешняя библиотека
        raise credentials_exception from exc

    user = user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def require_roles(*roles: Role):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if roles and current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return role_checker


async def authenticate_user(email: str, password: str) -> User | None:
    user = user_service.get_user_by_email(email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def create_token_for_user(user: User) -> str:
    expires = timedelta(minutes=settings.security.access_token_expire_minutes)
    payload = {"sub": user.email}
    from infrastructure.auth.security import create_access_token  # локальный импорт чтобы избежать циклов

    return create_access_token(payload, expires_delta=expires)
