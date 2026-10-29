"""Authenticated two-seat adapter. Secrets are stored privately, never sent as state.

PostgreSQL READ COMMITTED + a match row lock serializes joins and commands across
workers. A round precondition permits both independent same-round submissions.
The pinned replay is bounded to 30 rounds/60 orders and recomputed on restore.
"""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_hex, token_urlsafe
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db_dependencies import get_db
from learning_routes import student_only
from models import User, RedBlueMatch, RedBlueSeat, RedBlueReceipt
from cyber_warfare import engine
from cyber_warfare.catalog import ACTIONS
from cyber_warfare.opponent import choose_order
from cyber_warfare.scenario import load_scenario, list_scenarios


def private_response(response: Response):
    response.headers['Cache-Control'] = 'no-store'


router = APIRouter(prefix='/api/v1/red-blue', tags=['red-blue'], dependencies=[Depends(private_response)])


class StrictBody(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Start(StrictBody):
    scenario: str = Field(min_length=1, max_length=40, pattern=r'^[a-z_]+$')
    side: Literal['red', 'blue']
    mode: Literal['computer', 'human'] = 'computer'
    difficulty: Literal['easy', 'standard', 'hard'] = 'standard'


class Join(StrictBody):
    token: str = Field(min_length=43, max_length=43, pattern=r'^[A-Za-z0-9_-]+$')


class Command(StrictBody):
    command_id: UUID
    expected_turn: StrictInt = Field(ge=1, le=30)
    action: str = Field(min_length=1, max_length=30, pattern=r'^[a-z_]+$')
    target: str | None = Field(default=None, max_length=40, pattern=r'^[a-z0-9_]+$')
    source: str | None = Field(default=None, max_length=40, pattern=r'^[a-z0-9_]+$')


def identity(user_id):
    return f'user:{user_id}'


def owned(db, match_id, user_id, lock=False):
    membership = select(RedBlueSeat.match_id).where(RedBlueSeat.user_id == user_id)
    stmt = select(RedBlueMatch).where(RedBlueMatch.id == match_id, RedBlueMatch.id.in_(membership))
    if lock:
        stmt = stmt.with_for_update()
    row = db.scalar(stmt)
    if row is None:
        raise HTTPException(404, 'Match not found')
    return row


def restore(row):
    # Internal integrity failures fail closed without including private diagnostics.
    try:
        return engine.replay(row.transcript)
    except (ValueError, KeyError, TypeError, PermissionError):
        raise HTTPException(409, 'Saved rules unavailable; this match requires maintainer review') from None


def public(row, user_id):
    match = restore(row)
    observation = engine.view(match, identity(user_id))
    return {'id': row.id, 'status': row.status, 'difficulty': row.difficulty,
            **observation, 'orders': [o.dump() for o in engine.available_orders(observation)] if row.status == 'active' else []}


@router.get('/catalog')
def catalog(user=Depends(student_only)):
    # Never return configurations: those contain initial hidden access/weaknesses.
    scenarios = list_scenarios()
    return {'scenarios': [{'id': s.id, 'title': s.title, 'industry': s.industry,
                          'difficulty': s.difficulty, 'turn_limit': s.turn_limit} for s in scenarios],
            'actions': [a.public() for a in ACTIONS.values()]}


@router.post('/matches', status_code=201)
def start(body: Start, user=Depends(student_only), db: Session = Depends(get_db)):
    try:
        scenario = load_scenario(body.scenario)
    except ValueError:
        raise HTTPException(422, 'Unknown scenario') from None
    # Same database-backed per-user cap as existing activities, separate counts.
    db.scalar(select(User).where(User.id == user.id).with_for_update())
    since = datetime.now(timezone.utc) - timedelta(days=1)
    count = db.scalar(select(func.count()).select_from(RedBlueMatch).where(
        RedBlueMatch.creator_id == user.id, RedBlueMatch.created_at >= since))
    if count >= 100:
        raise HTTPException(429, 'Daily match creation limit reached; resume a saved match')
    other = 'blue' if body.side == 'red' else 'red'
    seats = {body.side: identity(user.id), other: 'computer' if body.mode == 'computer' else 'open'}
    match = engine.new_match(scenario, token_hex(32), seats['red'], seats['blue'])
    row = RedBlueMatch(creator_id=user.id, transcript=engine.export_replay(match),
                       difficulty=body.difficulty, status='active' if body.mode == 'computer' else 'waiting')
    db.add(row); db.flush()
    db.add_all([RedBlueSeat(match_id=row.id, side=side, user_id=user.id if side == body.side else None)
                for side in engine.SIDES])
    db.commit()
    return public(row, user.id)


@router.get('/matches')
def history(before_id: int | None = Query(None, ge=1), user=Depends(student_only), db: Session = Depends(get_db)):
    stmt = select(RedBlueMatch, RedBlueSeat.side).join(RedBlueSeat).where(RedBlueSeat.user_id == user.id)
    if before_id:
        stmt = stmt.where(RedBlueMatch.id < before_id)
    rows = db.execute(stmt.order_by(RedBlueMatch.id.desc()).limit(21)).all()
    return {'matches': [{'id': row.id, 'side': side, 'status': row.status,
                        'title': row.transcript['scenario']['title'], 'created_at': row.created_at.isoformat()}
                       for row, side in rows[:20]],
            'next_before_id': rows[19][0].id if len(rows) > 20 else None}


@router.get('/matches/{match_id}')
def resume(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    return public(owned(db, match_id, user.id), user.id)


@router.post('/matches/{match_id}/invite')
def invite(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    row = owned(db, match_id, user.id, lock=True)
    if row.creator_id != user.id or row.status != 'waiting':
        raise HTTPException(409, 'Only the creator of a waiting match can issue an invitation')
    token = token_urlsafe(32)
    row.invite_hash = sha256(token.encode()).hexdigest()
    row.invite_expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    db.commit()
    return {'token': token, 'expires_at': row.invite_expires_at.isoformat()}


@router.post('/join')
def join(body: Join, user=Depends(student_only), db: Session = Depends(get_db)):
    row = db.scalar(select(RedBlueMatch).where(RedBlueMatch.invite_hash == sha256(body.token.encode()).hexdigest()).with_for_update())
    if row is None or row.status != 'waiting' or row.invite_expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(404, 'Invitation unavailable or expired')
    if row.creator_id == user.id:
        raise HTTPException(409, 'Two different learners are required')
    seat = db.scalar(select(RedBlueSeat).where(RedBlueSeat.match_id == row.id, RedBlueSeat.user_id.is_(None)))
    match = restore(row)
    match.seats[seat.side] = identity(user.id)
    seat.user_id = user.id
    row.transcript = engine.export_replay(match)
    row.status, row.invite_hash, row.invite_expires_at = 'active', None, None
    db.commit()
    return public(row, user.id)


@router.post('/matches/{match_id}/commands')
def command(match_id: int, body: Command, user=Depends(student_only), db: Session = Depends(get_db)):
    row = owned(db, match_id, user.id, lock=True)
    payload = body.model_dump(mode='json')
    prior = db.scalar(select(RedBlueReceipt).where(RedBlueReceipt.match_id == row.id,
        RedBlueReceipt.user_id == user.id, RedBlueReceipt.command_id == str(body.command_id)))
    if prior:
        if prior.request != payload:
            raise HTTPException(409, 'Command ID already used for different input')
        return public(row, user.id)  # Latest authorized projection, never a private receipt.
    if row.status != 'active':
        raise HTTPException(409, 'Match is waiting or finished')
    match = restore(row)
    observation = engine.view(match, identity(user.id))
    if body.expected_turn != match.turn or observation['committed']:
        raise HTTPException(409, 'Round changed or choice already sealed; reload the match')
    order = engine.Order(body.action, body.target, body.source)
    if order not in engine.available_orders(observation):
        raise HTTPException(422, 'Order unavailable in your current information')
    # Decide the computer's order from its pre-commit projection. It cannot inspect
    # the human commitment, even in memory. Persist both in this one transaction.
    computer_side = next((s for s, actor in match.seats.items() if actor == 'computer'), None)
    computer_order = choose_order(engine.view(match, 'computer'), row.difficulty) if computer_side else None
    match = engine.commit(match, identity(user.id), order, body.expected_turn, str(body.command_id))
    if computer_order:
        match = engine.commit(match, 'computer', computer_order, body.expected_turn, f'computer-{body.expected_turn}')
    row.transcript = engine.export_replay(match)
    row.status = 'finished' if match.winner else 'active'
    db.add(RedBlueReceipt(match_id=row.id, user_id=user.id, command_id=str(body.command_id), request=payload))
    db.commit()
    return public(row, user.id)


@router.get('/matches/{match_id}/debrief')
def debrief(match_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    row = owned(db, match_id, user.id)
    if row.status != 'finished':
        raise HTTPException(409, 'Debrief is available only after the match')
    return engine.debrief(restore(row), identity(user.id))
