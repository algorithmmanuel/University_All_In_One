from datetime import datetime, date
from sqlalchemy import Boolean, JSON, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Academy(Base):
    __tablename__ = "academies"
    id: Mapped[str] = mapped_column(String(30), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="preview")
    courses: Mapped[list["Course"]] = relationship(back_populates="academy")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    academy_id: Mapped[str] = mapped_column(ForeignKey("academies.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    academy: Mapped[Academy] = relationship(back_populates="courses")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="course")

class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    course: Mapped[Course] = relationship(back_populates="lessons")

class LearnerProgress(Base):
    __tablename__ = "learner_progress"
    __table_args__ = (UniqueConstraint("learner_id", "lesson_id", name="uq_learner_lesson"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date(), nullable=True)
    age_band: Mapped[str] = mapped_column(String(20), nullable=False, default="unverified")
    guardian_consent_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="student")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_enrollment_user_course"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSON, nullable=False)
    correct_index: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)

class MissionRun(Base):
    __tablename__ = "mission_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    mission_id: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    choices: Mapped[list] = mapped_column(JSON, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class LoginAttemptBucket(Base):
    """Shared, bounded-window counter for authentication abuse protection."""
    __tablename__ = "login_attempt_buckets"
    key_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

class BetaInvite(Base):
    """Hashed, reusable invite for one registered adult learner."""
    __tablename__ = "beta_invites"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    redeemed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BetaFeedback(Base):
    """Private feedback linked to a learner; never returned to other learners."""
    __tablename__ = "beta_feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class PasswordResetToken(Base):
    """Recovery token digest only; never persist plaintext bearer links."""
    __tablename__ = "password_reset_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StrategyRun(Base):
    """Version-pinned independent strategy mode; legacy MissionRun is untouched."""
    __tablename__ = 'strategy_runs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    state: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class StrategyCommand(Base):
    __tablename__ = 'strategy_commands'
    __table_args__ = (UniqueConstraint('run_id', 'command_id', name='uq_strategy_command'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey('strategy_runs.id', ondelete='CASCADE'), index=True)
    command_id: Mapped[str] = mapped_column(String(36), nullable=False)
    request: Mapped[dict] = mapped_column(JSON, nullable=False)


class CyberPracticeSession(Base):
    """Immutable private question snapshot; no recomputed sample on grading."""
    __tablename__ = 'cyber_practice_sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    snapshot: Mapped[list] = mapped_column(JSON, nullable=False)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CyberStudyProgress(Base):
    __tablename__ = 'cyber_study_progress'
    __table_args__ = (UniqueConstraint('user_id', 'module_id', 'revision', name='uq_cyber_study'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    module_id: Mapped[str] = mapped_column(String(40), nullable=False)
    revision: Mapped[str] = mapped_column(String(40), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

# Register the independent simulator metadata for migrations/readiness and tests.
from red_blue_models import RedBlueMatch, RedBlueSeat, RedBlueReceipt  # noqa: F401,E402
