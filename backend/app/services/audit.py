from typing import Any

from sqlalchemy.orm import Session

from app.models import AuditEvent


def record_event(
    db: Session,
    *,
    action: str,
    entity_type: str,
    entity_id: str | int | None = None,
    user_id: int | None = None,
    previous_state: dict[str, Any] | None = None,
    new_state: dict[str, Any] | None = None,
    reason: str | None = None,
    commit: bool = False,
) -> AuditEvent:
    event = AuditEvent(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id is not None else None,
        previous_state=previous_state,
        new_state=new_state,
        reason=reason,
    )
    db.add(event)
    if commit:
        db.commit()
        db.refresh(event)
    return event
