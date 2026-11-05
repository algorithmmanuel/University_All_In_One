"""Preserve topic evidence and explanations for future attempts; no backfill."""
from alembic import op
import sqlalchemy as sa

revision = '0010_attempt_results'
down_revision = '0009_password_reset'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('quiz_attempts', sa.Column('result_snapshot', sa.JSON(), nullable=True))


def downgrade():
    op.drop_column('quiz_attempts', 'result_snapshot')
