"""locations table

Revision ID: 0002_locations
Revises: 0001_initial
Create Date: 2026-11-21

"""

import sqlalchemy as sa
from alembic import op

revision = "0002_locations"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("locations.id"), nullable=True),
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
    op.create_index("ix_locations_code", "locations", ["code"], unique=True)
    op.create_index("ix_locations_type", "locations", ["type"])
    op.create_index("ix_locations_parent_id", "locations", ["parent_id"])


def downgrade() -> None:
    op.drop_table("locations")
