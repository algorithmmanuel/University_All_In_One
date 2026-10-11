"""Persistent authentication attempt counters."""
from alembic import op
import sqlalchemy as sa

revision = "0006_login_limits"
down_revision = "0005_missions"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "login_attempt_buckets",
        sa.Column("key_hash", sa.String(64), primary_key=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_login_attempt_buckets_window_start",
                    "login_attempt_buckets", ["window_start"])

def downgrade():
    op.drop_index("ix_login_attempt_buckets_window_start", table_name="login_attempt_buckets")
    op.drop_table("login_attempt_buckets")
