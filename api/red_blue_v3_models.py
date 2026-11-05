"""Independent V3 pilot storage; no V1/V2 gameplay rows are modified."""
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class RedBlueV3Match(Base):
    __tablename__ = "red_blue_v3_matches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transcript: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    mode: Mapped[str] = mapped_column(String(12), nullable=False)
    invite_hash: Mapped[str | None] = mapped_column(String(64), unique=True)
    invite_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RedBlueV3Seat(Base):
    __tablename__ = "red_blue_v3_seats"
    __table_args__ = (
        UniqueConstraint("match_id", "side", name="uq_rb_v3_side"),
        UniqueConstraint("match_id", "user_id", name="uq_rb_v3_participant"),
        CheckConstraint("side IN ('red','blue')", name="ck_rb_v3_side"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("red_blue_v3_matches.id", ondelete="CASCADE"), nullable=False, index=True)
    side: Mapped[str] = mapped_column(String(4), nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
