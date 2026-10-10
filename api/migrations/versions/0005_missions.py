"""Mission progress storage."""
from alembic import op
import sqlalchemy as sa
revision = "0005_missions"
down_revision = "0004_assessments"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("mission_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mission_id", sa.String(60), nullable=False),
        sa.Column("step_index", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("choices", sa.JSON(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_mission_runs_user_id", "mission_runs", ["user_id"])
    op.create_index("ix_mission_runs_mission_id", "mission_runs", ["mission_id"])

def downgrade():
    op.drop_index("ix_mission_runs_mission_id", table_name="mission_runs")
    op.drop_index("ix_mission_runs_user_id", table_name="mission_runs")
    op.drop_table("mission_runs")
