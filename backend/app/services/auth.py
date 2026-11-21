from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    generate_session_token,
    hash_password,
    hash_token,
    needs_rehash,
    verify_password,
)
from app.models import Session as SessionRecord
from app.models import User


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email.lower().strip()))
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)
        db.add(user)
    return user


def create_session(
    db: Session, user: User, ip_address: str | None = None, user_agent: str | None = None
) -> tuple[SessionRecord, str]:
    settings = get_settings()
    token = generate_session_token()
    now = datetime.now(UTC)
    record = SessionRecord(
        token_hash=hash_token(token),
        user_id=user.id,
        expires_at=now + timedelta(seconds=settings.session_max_age_seconds),
        ip_address=ip_address,
        user_agent=(user_agent or "")[:255] or None,
    )
    db.add(record)
    user.last_login_at = now
    db.add(user)
    db.commit()
    db.refresh(record)
    return record, token


def revoke_session(db: Session, token: str) -> None:
    record = db.scalar(select(SessionRecord).where(SessionRecord.token_hash == hash_token(token)))
    if record is not None and record.revoked_at is None:
        record.revoked_at = datetime.now(UTC)
        db.add(record)
        db.commit()


def get_session_user(db: Session, token: str) -> User | None:
    record = db.scalar(select(SessionRecord).where(SessionRecord.token_hash == hash_token(token)))
    if record is None or record.revoked_at is not None:
        return None
    now = datetime.now(UTC)
    expires = record.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)
    if expires < now:
        return None
    user = db.get(User, record.user_id)
    if user is None or not user.is_active:
        return None
    return user
