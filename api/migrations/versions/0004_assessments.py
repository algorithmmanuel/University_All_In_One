"""Quiz questions and attempts.

Revision ID: 0004_assessments
Revises: 0003_enrollments
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_assessments"
down_revision = "0003_enrollments"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("quiz_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_index", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.CheckConstraint("correct_index >= 0", name="ck_quiz_correct_index"))
    op.create_index("ix_quiz_questions_course_id", "quiz_questions", ["course_id"])
    op.create_table("quiz_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_quiz_attempts_user_id", "quiz_attempts", ["user_id"])
    op.create_index("ix_quiz_attempts_course_id", "quiz_attempts", ["course_id"])

def downgrade():
    op.drop_index("ix_quiz_attempts_course_id", table_name="quiz_attempts")
    op.drop_index("ix_quiz_attempts_user_id", table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
    op.drop_index("ix_quiz_questions_course_id", table_name="quiz_questions")
    op.drop_table("quiz_questions")
