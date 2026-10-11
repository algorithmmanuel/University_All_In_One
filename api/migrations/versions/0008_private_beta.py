"""Private beta invitations and feedback storage."""
from alembic import op
import sqlalchemy as sa

revision = "0008_private_beta"
down_revision = "0007_age_safeguards"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("beta_invites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("redeemed_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_table("beta_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("page", sa.String(160), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_beta_feedback_user_id", "beta_feedback", ["user_id"])

def downgrade():
    op.drop_index("ix_beta_feedback_user_id", table_name="beta_feedback")
    op.drop_table("beta_feedback")
    op.drop_table("beta_invites")
