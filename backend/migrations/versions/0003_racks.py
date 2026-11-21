"""racks table

Revision ID: 0003_racks
Revises: 0002_locations
Create Date: 2026-11-21

"""

import sqlalchemy as sa
from alembic import op

revision = "0003_racks"
down_revision = "0002_locations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "racks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("locations.id"), nullable=False),
        sa.Column("height_u", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_racks_code", "racks", ["code"], unique=True)
    op.create_index("ix_racks_location_id", "racks", ["location_id"])


def downgrade() -> None:
    op.drop_table("racks")
