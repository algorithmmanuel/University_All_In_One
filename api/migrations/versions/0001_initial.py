"""Initial academies, courses, lessons, and progress tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("academies", sa.Column("id", sa.String(30), primary_key=True), sa.Column("name", sa.String(100), nullable=False), sa.Column("status", sa.String(30), nullable=False))
    op.create_table("courses", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("academy_id", sa.String(30), sa.ForeignKey("academies.id"), nullable=False), sa.Column("title", sa.String(180), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("status", sa.String(30), nullable=False))
    op.create_index("ix_courses_academy_id", "courses", ["academy_id"])
    op.create_table("lessons", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False), sa.Column("title", sa.String(180), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("position", sa.Integer(), nullable=False))
    op.create_index("ix_lessons_course_id", "lessons", ["course_id"])
    op.create_table("learner_progress", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("learner_id", sa.String(100), nullable=False), sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id"), nullable=False), sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("learner_id", "lesson_id", name="uq_learner_lesson"))
    op.create_index("ix_learner_progress_learner_id", "learner_progress", ["learner_id"])
    op.bulk_insert(sa.table("academies", sa.column("id", sa.String), sa.column("name", sa.String), sa.column("status", sa.String)), [{"id":"secondary","name":"Secondary School","status":"preview"},{"id":"university","name":"University","status":"preview"},{"id":"cyber","name":"Cybersecurity Academy","status":"preview"}])

def downgrade():
    op.drop_index("ix_learner_progress_learner_id", table_name="learner_progress")
    op.drop_table("learner_progress")
    op.drop_index("ix_lessons_course_id", table_name="lessons")
    op.drop_table("lessons")
    op.drop_index("ix_courses_academy_id", table_name="courses")
    op.drop_table("courses")
    op.drop_table("academies")
