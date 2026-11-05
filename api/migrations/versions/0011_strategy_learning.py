"""Add independent strategy, practice and study state; retain all legacy data."""
from alembic import op
import sqlalchemy as sa
revision = '0011_strategy_learning'
down_revision = '0010_attempt_results'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('strategy_runs', sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('state', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index('ix_strategy_runs_user_id', 'strategy_runs', ['user_id'])
    op.create_table('strategy_commands', sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('run_id', sa.Integer(), sa.ForeignKey('strategy_runs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('command_id', sa.String(36), nullable=False), sa.Column('request', sa.JSON(), nullable=False),
        sa.UniqueConstraint('run_id', 'command_id', name='uq_strategy_command'))
    op.create_index('ix_strategy_commands_run_id', 'strategy_commands', ['run_id'])
    op.create_table('cyber_practice_sessions', sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('snapshot', sa.JSON(), nullable=False), sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index('ix_cyber_practice_sessions_user_id', 'cyber_practice_sessions', ['user_id'])
    op.create_table('cyber_study_progress', sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('module_id', sa.String(40), nullable=False), sa.Column('revision', sa.String(40), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('user_id', 'module_id', 'revision', name='uq_cyber_study'))
    op.create_index('ix_cyber_study_progress_user_id', 'cyber_study_progress', ['user_id'])


def downgrade():
    for table in ('cyber_study_progress', 'cyber_practice_sessions', 'strategy_commands', 'strategy_runs'):
        op.drop_table(table)
