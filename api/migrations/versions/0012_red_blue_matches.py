"""Independent Red/Blue match, seat and sealed receipt storage; legacy tables untouched."""
from alembic import op
import sqlalchemy as sa
revision = '0012_red_blue_matches'
down_revision = '0011_strategy_learning'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('red_blue_matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('transcript', sa.JSON(), nullable=False),
        sa.Column('difficulty', sa.String(12), nullable=False),
        sa.Column('status', sa.String(12), nullable=False),
        sa.Column('invite_hash', sa.String(64), unique=True),
        sa.Column('invite_expires_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index('ix_red_blue_matches_creator_id', 'red_blue_matches', ['creator_id'])
    op.create_table('red_blue_seats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_id', sa.Integer(), sa.ForeignKey('red_blue_matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('side', sa.String(4), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.UniqueConstraint('match_id', 'side', name='uq_red_blue_side'),
        sa.UniqueConstraint('match_id', 'user_id', name='uq_red_blue_participant'),
        sa.CheckConstraint("side IN ('red', 'blue')", name='ck_red_blue_side'))
    op.create_table('red_blue_receipts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_id', sa.Integer(), sa.ForeignKey('red_blue_matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('command_id', sa.String(36), nullable=False),
        sa.Column('request', sa.JSON(), nullable=False),
        sa.UniqueConstraint('match_id', 'user_id', 'command_id', name='uq_red_blue_receipt'))
    for table in ('red_blue_seats', 'red_blue_receipts'):
        for column in ('match_id', 'user_id'):
            op.create_index(f'ix_{table}_{column}', table, [column])


def downgrade():
    for table in ('red_blue_receipts', 'red_blue_seats', 'red_blue_matches'):
        op.drop_table(table)
