"""Additive two-seat storage; never reuse single-owner StrategyRun records."""
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class RedBlueMatch(Base):
    __tablename__ = 'red_blue_matches'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    transcript: Mapped[dict] = mapped_column(JSON, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(12), nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False)
    invite_hash: Mapped[str | None] = mapped_column(String(64), unique=True)
    invite_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RedBlueSeat(Base):
    __tablename__ = 'red_blue_seats'
    __table_args__ = (UniqueConstraint('match_id', 'side', name='uq_red_blue_side'),
                     UniqueConstraint('match_id', 'user_id', name='uq_red_blue_participant'),
                     CheckConstraint("side IN ('red', 'blue')", name='ck_red_blue_side'))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey('red_blue_matches.id', ondelete='CASCADE'), index=True)
    side: Mapped[str] = mapped_column(String(4), nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)


class RedBlueReceipt(Base):
    """Actor-scoped UUID plus sealed order; transactionally stored with resolution."""
    __tablename__ = 'red_blue_receipts'
    __table_args__ = (UniqueConstraint('match_id', 'user_id', 'command_id', name='uq_red_blue_receipt'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey('red_blue_matches.id', ondelete='CASCADE'), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    command_id: Mapped[str] = mapped_column(String(36), nullable=False)
    request: Mapped[dict] = mapped_column(JSON, nullable=False)
