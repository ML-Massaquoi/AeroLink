from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

RACK_STATUSES: tuple[str, ...] = ("planned", "active", "inactive")

# Location types allowed to hold racks (README Module C: technical rooms).
RACK_LOCATION_TYPES: tuple[str, ...] = ("room", "technical_room")

MIN_RACK_U = 1
MAX_RACK_U = 60


class Rack(Base, TimestampMixin):
    __tablename__ = "racks"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )
    height_u: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    description: Mapped[str | None] = mapped_column(Text)
    is_archived: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    location = relationship("Location", back_populates="racks")
