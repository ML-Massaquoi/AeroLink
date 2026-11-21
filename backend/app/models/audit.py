from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.models.base import Base

# JSONB on PostgreSQL, generic JSON elsewhere (e.g. SQLite tests)
JSONType = JSON().with_variant(JSONB(), "postgresql")


class AuditEvent(Base):
    """Append-only history of infrastructure and security-relevant changes."""

    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(64))
    previous_state: Mapped[dict[str, Any] | None] = mapped_column(JSONType)
    new_state: Mapped[dict[str, Any] | None] = mapped_column(JSONType)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    user = relationship("User")

    __table_args__ = ({"sqlite_autoincrement": True},)
