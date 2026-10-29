"""Add independent saved workshops without rewriting any previous activity."""
from alembic import op
import sqlalchemy as sa
revision='0013_journey_workshops'
down_revision='0012_red_blue_matches'
branch_labels=None
depends_on=None


def upgrade():
    op.create_table('journey_workshop_runs',sa.Column('id',sa.Integer(),primary_key=True),
        sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),
        sa.Column('state',sa.JSON(),nullable=False),
        sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    op.create_index('ix_journey_workshop_runs_user_id','journey_workshop_runs',['user_id'])


def downgrade():
    op.drop_table('journey_workshop_runs')
