from fastapi import APIRouter, HTTPException, Request, Response, status

from app.api.deps import CurrentUser, DbSession
from app.core.config import get_settings
from app.schemas.auth import LoginRequest, Message, UserOut
from app.services import auth as auth_service
from app.services.audit import record_event
from app.services.serialize import user_out

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_max_age_seconds,
        httponly=True,
        samesite="lax",
        secure=settings.app_env == "production",
        path="/",
    )


@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest, request: Request, response: Response, db: DbSession) -> UserOut:
    user = auth_service.authenticate(db, payload.email, payload.password)
    if user is None:
        record_event(
            db,
            action="auth.login_failed",
            entity_type="user",
            entity_id=payload.email,
            new_state={"ip": request.client.host if request.client else None},
            commit=True,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    _, token = auth_service.create_session(
        db,
        user,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    _set_session_cookie(response, token)
    record_event(
        db,
        action="auth.login",
        entity_type="user",
        entity_id=user.id,
        user_id=user.id,
        commit=True,
    )
    db.refresh(user)
    return user_out(user)


@router.post("/logout", response_model=Message)
def logout(request: Request, response: Response, db: DbSession) -> Message:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        auth_service.revoke_session(db, token)
    response.delete_cookie(settings.session_cookie_name, path="/")
    return Message(detail="Logged out")


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> UserOut:
    return user_out(user)
