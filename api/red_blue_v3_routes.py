"""V3 Microfinance Development pilot: authenticated, seat-filtered match API.

All writes lock the match row. Beta is forbidden even when a caller knows the
endpoint. Match truth and seed never enter public responses or logs.
"""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import os
import time
from secrets import token_urlsafe, token_hex
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db_dependencies import get_db
from learning_routes import student_only
from models import User, RedBlueV3Match, RedBlueV3Seat
from cyber_warfare import v3_clock, v3_pilot as pilot
from red_blue_routes import BoundedRoute, private_response

router = APIRouter(prefix="/api/v1/red-blue-v3", tags=["red-blue-v3"], route_class=BoundedRoute, dependencies=[Depends(private_response)])


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Start(Strict):
    side: Literal["red", "blue"] = "blue"
    mode: Literal["human", "computer"] = "computer"
    match_minutes: Literal[15, 30, 60, 120] = 30
    turn_seconds: Literal[30, 60, 90, 180, 300] = 90


class Preparation(Strict):
    policy: Literal["patch_management", "network_segmentation", "security_monitoring", "access_governance"] | None = None
    control: Literal["monitoring", "patched", "segmented", "hardened"] | None = None
    target: str | None = Field(None, max_length=48, pattern=r"^[a-z][a-z0-9_-]*$")
    strategy: Literal["surface_mapping", "quiet_investigation"] | None = None


class Join(Strict):
    token: str = Field(min_length=43, max_length=43, pattern=r"^[A-Za-z0-9_-]+$")


class Move(Strict):
    command_id: UUID
    expected_sequence: StrictInt = Field(ge=1, le=1000000)
    action: str = Field(min_length=1, max_length=30, pattern=r"^[a-z_]+$")
    target: str | None = Field(None, max_length=48, pattern=r"^[a-z][a-z0-9_-]*$")
    source: str | None = Field(None, max_length=48, pattern=r"^[a-z][a-z0-9_-]*$")


def enabled():
    if os.getenv("EDUCYBER_ENV") != "development":
        raise HTTPException(404, "V3 pilot is not available in Beta")


def identity(user):
    return f"user:{user.id}"


def save(db):
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503, "V3 match storage unavailable") from None


def owned(db, match_id, user, *, lock=False):
    member = select(RedBlueV3Seat.match_id).where(RedBlueV3Seat.user_id == user.id)
    stmt = select(RedBlueV3Match).where(
        RedBlueV3Match.id == match_id, RedBlueV3Match.id.in_(member))
    if lock:
        stmt = stmt.with_for_update()
    row = db.scalar(stmt)
    if row is None:
        raise HTTPException(404, "V3 match not found")
    if row.transcript.get("edition") != pilot.EDITION:
        raise HTTPException(409, "Unsupported saved pilot edition")
    return row


def public(row, user):
    observation = pilot.project(row.transcript, identity(user), int(time.time())
                                if row.transcript["phase"] == "engage" else None)
    return {"id": row.id, "mode": row.mode, "status": row.status, **observation}


@router.get("/catalog")
def catalog(user=Depends(student_only)):
    enabled()
    return {"edition": pilot.EDITION, "scenario": "microfinance",
            "match_minutes": [15, 30, 60, 120],
            "turn_seconds": [30, 60, 90, 180, 300],
            "development_only": True}


@router.post("/matches", status_code=201)
def start(body: Start, user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    db.scalar(select(User.id).where(User.id == user.id).with_for_update())
    since = datetime.now(timezone.utc) - timedelta(days=1)
    count = db.scalar(select(func.count()).select_from(RedBlueV3Match).where(
        RedBlueV3Match.creator_id == user.id, RedBlueV3Match.created_at >= since))
    if count >= 20:
        raise HTTPException(429, "Daily V3 pilot creation limit reached")
    opponent = "computer" if body.mode == "computer" else "open"
    blue = identity(user) if body.side == "blue" else opponent
    red = identity(user) if body.side == "red" else opponent
    config = v3_clock.Config(body.match_minutes, body.turn_seconds)
    state = pilot.new(token_hex(20), blue, red, config)
    if body.mode == "computer":
        state = pilot.ready(state, "computer", int(time.time()))
    row = RedBlueV3Match(creator_id=user.id, transcript=state,
                         status="prepare", mode=body.mode)
    db.add(row)
    db.flush()
    db.add_all([
        RedBlueV3Seat(match_id=row.id, side=side,
                      user_id=user.id if side == body.side else None)
        for side in ("red", "blue")
    ])
    save(db)
    return public(row, user)


@router.get("/matches")
def history(user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    entries = db.execute(
        select(RedBlueV3Match, RedBlueV3Seat.side)
        .join(RedBlueV3Seat, RedBlueV3Seat.match_id == RedBlueV3Match.id)
        .where(RedBlueV3Seat.user_id == user.id)
        .order_by(RedBlueV3Match.id.desc()).limit(20)
    ).all()
    return {"matches": [
        {"id": row.id, "status": row.status, "side": side,
         "mode": row.mode, "created_at": row.created_at.isoformat()}
        for row, side in entries
    ]}


@router.get("/matches/{match_id}")
def resume(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    return public(owned(db, match_id, user), user)


@router.post("/matches/{match_id}/invite")
def invite(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    row = owned(db, match_id, user, lock=True)
    if row.creator_id != user.id or row.mode != "human" or row.status != "prepare":
        raise HTTPException(409, "Only a waiting match creator can invite")
    token = token_urlsafe(32)
    row.invite_hash = sha256(token.encode()).hexdigest()
    row.invite_expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    save(db)
    return {"token": token, "expires_at": row.invite_expires_at.isoformat()}


@router.post("/join")
def join(body: Join, user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    row = db.scalar(select(RedBlueV3Match).where(
        RedBlueV3Match.invite_hash == sha256(body.token.encode()).hexdigest()).with_for_update())
    if (row is None or row.mode != "human" or row.status != "prepare"
            or not row.invite_expires_at or
            row.invite_expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc)):
        raise HTTPException(404, "V3 invitation expired or unavailable")
    if row.creator_id == user.id:
        raise HTTPException(409, "Use a second account")
    seat = db.scalar(select(RedBlueV3Seat).where(
        RedBlueV3Seat.match_id == row.id, RedBlueV3Seat.user_id.is_(None)).with_for_update())
    if seat is None:
        raise HTTPException(409, "Both seats already assigned")
    state = dict(row.transcript)
    state = __import__("copy").deepcopy(state)
    state["players"][seat.side] = identity(user)
    row.transcript = state
    seat.user_id = user.id
    row.invite_hash = None
    row.invite_expires_at = None
    save(db)
    return public(row, user)


@router.post("/matches/{match_id}/prepare")
def prepare(match_id: int, body: Preparation, user=Depends(student_only),
            db: Session = Depends(get_db)):
    enabled()
    row = owned(db, match_id, user, lock=True)
    try:
        state = pilot.prepare(row.transcript, identity(user), **body.model_dump())
    except (ValueError, PermissionError):
        raise HTTPException(409, "Preparation not available for this seat") from None
    row.transcript = state
    save(db)
    return public(row, user)


@router.post("/matches/{match_id}/ready")
def ready(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    enabled()
    row = owned(db, match_id, user, lock=True)
    try:
        state = pilot.ready(row.transcript, identity(user), int(time.time()))
    except (ValueError, PermissionError):
        raise HTTPException(409, "Seat already ready or pending another player") from None
    row.transcript = state
    row.status = state["phase"]
    save(db)
    return public(row, user)


@router.post("/matches/{match_id}/commands")
def command(match_id: int, body: Move, user=Depends(student_only),
            db: Session = Depends(get_db)):
    enabled()
    row = owned(db, match_id, user, lock=True)
    order = {key: getattr(body, key) for key in ("action", "target", "source")}
    try:
        state = pilot.act(row.transcript, identity(user), order,
                          int(time.time()), str(body.command_id), body.expected_sequence)
    except (ValueError, PermissionError):
        raise HTTPException(409, "Action unavailable or turn expired") from None
    row.transcript = state
    row.status = state["phase"]
    save(db)
    return public(row, user)
