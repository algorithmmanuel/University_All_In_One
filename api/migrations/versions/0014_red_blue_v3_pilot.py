"""Isolated authenticated V3 Microfinance pilot match and participant tables."""
from alembic import op
import sqlalchemy as sa

revision = "0014_red_blue_v3_pilot"
down_revision = "0013_journey_workshops"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "red_blue_v3_matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("creator_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("transcript", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("mode", sa.String(12), nullable=False),
        sa.Column("invite_hash", sa.String(64), unique=True),
        sa.Column("invite_expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_red_blue_v3_matches_creator_id", "red_blue_v3_matches", ["creator_id"])
    op.create_table(
        "red_blue_v3_seats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("red_blue_v3_matches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("side", sa.String(4), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.UniqueConstraint("match_id", "side", name="uq_rb_v3_side"),
        sa.UniqueConstraint("match_id", "user_id", name="uq_rb_v3_participant"),
        sa.CheckConstraint("side IN ('red','blue')", name="ck_rb_v3_side"),
    )
    op.create_index("ix_red_blue_v3_seats_match_id", "red_blue_v3_seats", ["match_id"])
    op.create_index("ix_red_blue_v3_seats_user_id", "red_blue_v3_seats", ["user_id"])


def downgrade():
    op.drop_table("red_blue_v3_seats")
    op.drop_table("red_blue_v3_matches")
