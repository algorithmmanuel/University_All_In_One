"""Add age declarations without guessing ages for existing learners."""
from alembic import op
import sqlalchemy as sa

revision = "0007_age_safeguards"
down_revision = "0006_login_limits"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("date_of_birth", sa.Date(), nullable=True))
    op.add_column("users", sa.Column("age_band", sa.String(20), nullable=False,
                                     server_default="unverified"))
    op.add_column("users", sa.Column("guardian_consent_verified", sa.Boolean(),
                                     nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column("users", "guardian_consent_verified")
    op.drop_column("users", "age_band")
    op.drop_column("users", "date_of_birth")
