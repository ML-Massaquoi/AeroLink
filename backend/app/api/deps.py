from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models import User
from app.services.auth import get_session_user

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(request: Request, db: DbSession) -> User:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = get_session_user(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_permission(codename: str) -> Callable[[User], User]:
    def checker(user: CurrentUser) -> User:
        if codename not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {codename}",
            )
        return user

    return checker


def get_optional_user(request: Request, db: DbSession) -> User | None:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        return None
    try:
        return get_session_user(db, token)
    except Exception:
        return None
