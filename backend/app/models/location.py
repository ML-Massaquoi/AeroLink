from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.rack import Rack

# Allowed parent types per location type (empty = root level).
LOCATION_TYPES: tuple[str, ...] = (
    "building",
    "floor",
    "area",
    "room",
    "technical_room",
)

ALLOWED_PARENTS: dict[str, tuple[str, ...]] = {
    "building": (),
    "floor": ("building",),
    "area": ("building", "floor"),
    "room": ("floor", "area"),
    "technical_room": ("floor", "area"),
}


class Location(Base, TimestampMixin):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"), nullable=True, index=True
    )
    description: Mapped[str | None] = mapped_column(Text)
    is_archived: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    parent: Mapped[Location | None] = relationship(
        "Location", remote_side=[id], back_populates="children"
    )
    children: Mapped[list[Location]] = relationship(
        "Location", back_populates="parent", order_by="Location.name"
    )
    racks: Mapped[list[Rack]] = relationship(
        "Rack", back_populates="location", order_by="Rack.name"
    )
