"""Owned strategy/practice HTTP operations; all state and answer keys stay server-owned."""
from datetime import datetime, timedelta, timezone
from copy import deepcopy
from secrets import SystemRandom, token_hex
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy import select, func, cast, Text
from sqlalchemy.orm import Session
from auth import current_user
from db_dependencies import get_db
from models import User, StrategyRun, StrategyCommand, CyberPracticeSession, CyberStudyProgress
from learning_routes import student_only
import strategy_engine as engine
from cyber_content import BANK, MODULES, TOPICS, REVISION, lessons
from strategy_catalog import SCENARIOS
import strategy_siege as siege
from cyber_campaign import campaign_progress

router = APIRouter(prefix='/api/v1/cyber-lab', tags=['cyber-lab'])


def owned(db, model, user_id, row_id, lock=False):
    stmt = select(model).where(model.id == row_id, model.user_id == user_id)
    if lock: stmt = stmt.with_for_update()
    row = db.scalar(stmt)
    if row is None: raise HTTPException(404, 'Saved activity not found')
    return row


def creation_limit(db, model, user_id):
    # Serialise per-user creation limits across workers, not an in-memory counter.
    db.scalar(select(User).where(User.id == user_id).with_for_update())
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    count = db.scalar(select(func.count()).select_from(model).where(model.user_id == user_id, model.created_at >= since))
    if count >= 100: raise HTTPException(429, 'Daily activity creation limit reached; resume a saved activity')


@router.get('/catalog')
def catalog(user=Depends(student_only), db: Session = Depends(get_db)):
    completed = set(db.scalars(select(CyberStudyProgress.module_id).where(
        CyberStudyProgress.user_id == user.id, CyberStudyProgress.revision == REVISION)))
    previous = set(db.scalars(select(CyberStudyProgress.module_id).where(
        CyberStudyProgress.user_id == user.id, CyberStudyProgress.revision != REVISION)))
    graded_rows = recent_graded_sessions(db, user.id)
    mistakes = recent_mistakes(db, user.id, graded_rows)
    return {'revision': REVISION, 'question_count': len(BANK),
        'campaign': campaign_progress(db, user.id, completed, graded_rows), 'scenarios': list(SCENARIOS.values()),
        'modules': [{**item, 'completed': item['id'] in completed,
                     'previously_completed': item['id'] in previous} for item in lessons()],
        'topics': [{'id': key, 'title': value[0], 'count': sum(q['topic'] == key for q in BANK),
            'counts': {level: sum(q['topic'] == key and q['difficulty'] == level for q in BANK)
                       for level in ('foundational', 'applied', 'challenging')},
            'mistakes': {level: sum(q['topic'] == key and q['id'] in mistakes and
                              (level == 'all' or q['difficulty'] == level) for q in BANK)
                         for level in ('all', 'foundational', 'applied', 'challenging')}}
                   for key, value in TOPICS.items()]}



@router.post('/study/{module_id}/complete')
def study_complete(module_id: str, user=Depends(student_only), db: Session = Depends(get_db)):
    if module_id not in {m['id'] for m in MODULES}: raise HTTPException(404, 'Module not found')
    db.scalar(select(User).where(User.id == user.id).with_for_update())
    row = db.scalar(select(CyberStudyProgress).where(CyberStudyProgress.user_id == user.id,
        CyberStudyProgress.module_id == module_id, CyberStudyProgress.revision == REVISION))
    if row is None: db.add(CyberStudyProgress(user_id=user.id, module_id=module_id, revision=REVISION))
    db.commit()
    return {'module_id': module_id, 'completed': True, 'revision': REVISION}


class StrategyStart(BaseModel):
    model_config = ConfigDict(extra='forbid')
    scenario: str = Field(default='branch', max_length=30)
    replay_run_id: StrictInt | None = Field(default=None, ge=1, le=2_147_483_647)


@router.post('/runs', status_code=201)
def start(body: StrategyStart = StrategyStart(), user=Depends(student_only), db: Session = Depends(get_db)):
    if body.scenario not in SCENARIOS: raise HTTPException(422, 'Unknown scenario')
    creation_limit(db, StrategyRun, user.id)
    seed = token_hex(16)
    parent = None
    if body.replay_run_id is not None:
        parent = owned(db, StrategyRun, user.id, body.replay_run_id)
        if (body.scenario != 'siege' or parent.state.get('revision') != siege.REVISION
                or parent.state['status'] == 'active'):
            raise HTTPException(422, 'Replay requires a completed Branch Siege run of the same edition')
        seed = parent.state['seed']
    state = engine.new_state(seed, body.scenario)
    if parent is not None:
        state['replay_of'] = parent.id
        state['comparison_baseline'] = siege.summary(parent.state)
    run = StrategyRun(user_id=user.id, state=state)
    db.add(run); db.commit(); db.refresh(run)
    return {'id': run.id, **engine.public(run.state)}


@router.get('/runs')
def runs(before_id: int | None = Query(None, ge=1), user=Depends(student_only), db: Session = Depends(get_db)):
    stmt = select(StrategyRun).where(StrategyRun.user_id == user.id)
    if before_id: stmt = stmt.where(StrategyRun.id < before_id)
    page = db.scalars(stmt.order_by(StrategyRun.id.desc()).limit(21)).all()
    return {'runs': [{'id': row.id, 'turn': row.state['turn'], 'status': row.state['status'],
        'scenario': row.state.get('scenario', 'branch'),
        'title': SCENARIOS[row.state.get('scenario', 'branch')]['title'],
        'created_at': row.created_at.isoformat()} for row in page[:20]],
        'next_before_id': page[19].id if len(page) > 20 else None}


@router.get('/runs/{run_id}')
def resume(run_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    run = owned(db, StrategyRun, user.id, run_id)
    return {'id': run.id, **engine.public(run.state)}


class Command(BaseModel):
    model_config = ConfigDict(extra='forbid')
    command_id: UUID
    expected_version: StrictInt = Field(ge=0)
    action: str = Field(min_length=1, max_length=20)
    target: str | None = Field(default=None, max_length=20)


@router.post('/runs/{run_id}/commands')
def command(run_id: int, body: Command, user=Depends(student_only), db: Session = Depends(get_db)):
    run = owned(db, StrategyRun, user.id, run_id, lock=True)
    payload = body.model_dump(mode='json')
    prior = db.scalar(select(StrategyCommand).where(StrategyCommand.run_id == run_id,
        StrategyCommand.command_id == str(body.command_id)))
    if prior:
        if prior.request != payload: raise HTTPException(409, 'Command ID already used for different input')
        return {'id': run.id, **engine.public(run.state)}
    if body.expected_version != run.state['version']:
        raise HTTPException(409, 'Activity changed; reload the saved run before acting')
    if body.action == 'end_turn' and body.target is not None:
        raise HTTPException(422, 'End turn does not take an asset')
    try: next_state = engine.advance(run.state, body.action, body.target)
    except ValueError as error: raise HTTPException(422, str(error)) from None
    run.state = next_state
    db.add(StrategyCommand(run_id=run.id, command_id=str(body.command_id), request=payload))
    db.commit()
    return {'id': run.id, **engine.public(run.state)}


class PracticeStart(BaseModel):
    model_config = ConfigDict(extra='forbid')
    mode: str = Field(default='fresh', max_length=20)
    topic: str = Field(default='all', max_length=30)
    difficulty: str = Field(default='all', max_length=20)
    count: StrictInt = Field(default=10, ge=1, le=20)


def practice_public(row):
    return {'id': row.id, 'revision': row.snapshot[0]['revision'] if len({q['revision'] for q in row.snapshot}) == 1 else 'mixed', 'questions': [
        {key: q[key] for key in ('id', 'revision', 'topic', 'objective', 'difficulty', 'prompt', 'options', 'module')}
        for q in row.snapshot], 'result': row.result}


def recent_graded_sessions(db, user_id):
    """Bounded graded window; unfinished sessions must not displace real results."""
    return db.scalars(select(CyberPracticeSession).where(CyberPracticeSession.user_id == user_id,
        CyberPracticeSession.result.is_not(None), cast(CyberPracticeSession.result, Text) != 'null')
        .order_by(CyberPracticeSession.id.desc()).limit(50)).all()


def recent_mistakes(db, user_id, rows=None):
    """Latest graded verdict per ID within a bounded 50-session review window."""
    if rows is None: rows = recent_graded_sessions(db, user_id)
    # New submissions carry server time. Older results keep their existing data
    # and use creation order only as an explicit legacy fallback.
    rows = sorted(rows, key=lambda row: (row.result or {}).get('submitted_at') or (row.created_at.astimezone(timezone.utc) if row.created_at.tzinfo else row.created_at.replace(tzinfo=timezone.utc)).isoformat(), reverse=True)
    verdicts = {}
    for row in rows:
        if not row.result: continue
        for item in row.result.get('feedback', []): verdicts.setdefault(item['id'], item['correct'])
    return {key for key, correct in verdicts.items() if not correct}


@router.post('/practice', status_code=201)
def start_practice(body: PracticeStart, user=Depends(student_only), db: Session = Depends(get_db)):
    if body.topic != 'all' and body.topic not in TOPICS: raise HTTPException(422, 'Unknown topic')
    if body.mode not in ('fresh', 'mistakes'): raise HTTPException(422, 'Unknown practice mode')
    if body.difficulty not in ('all', 'foundational', 'applied', 'challenging'): raise HTTPException(422, 'Unknown difficulty')
    eligible = [q for q in BANK if (body.topic == 'all' or q['topic'] == body.topic)
                and (body.difficulty == 'all' or q['difficulty'] == body.difficulty)]
    if body.mode == 'mistakes':
        mistakes = recent_mistakes(db, user.id)
        eligible = [q for q in eligible if q['id'] in mistakes]
    if body.count > len(eligible): raise HTTPException(422, f'Only {len(eligible)} questions match these choices; choose a smaller session or another mode')
    creation_limit(db, CyberPracticeSession, user.id)
    recent = db.scalars(select(CyberPracticeSession).where(CyberPracticeSession.user_id == user.id)
        .order_by(CyberPracticeSession.id.desc()).limit(50)).all()
    # Most recent occurrence determines freshness. Previously unseen questions rank first.
    recency = {}
    for order, session in enumerate(recent):
        for q in session.snapshot: recency.setdefault(q['id'], order)
    random = SystemRandom()
    pool = list(eligible); random.shuffle(pool)
    selected = []; topic_count = {}
    while len(selected) < body.count:
        # Prioritise freshness, then balance topics at the same freshness level.
        pool.sort(key=lambda q: (q['id'] in recency, -recency.get(q['id'], 0), topic_count.get(q['topic'], 0)))
        q = deepcopy(pool.pop(0))
        order = list(range(len(q['options']))); random.shuffle(order)
        q['options'] = [q['options'][index] for index in order]
        q['answer'] = order.index(q['answer'])
        selected.append(q); topic_count[q['topic']] = topic_count.get(q['topic'], 0) + 1
    row = CyberPracticeSession(user_id=user.id, snapshot=selected)
    db.add(row); db.commit(); db.refresh(row)
    return practice_public(row)


@router.get('/practice')
def practice_history(before_id: int | None = Query(None, ge=1), user=Depends(student_only), db: Session = Depends(get_db)):
    stmt = select(CyberPracticeSession).where(CyberPracticeSession.user_id == user.id)
    if before_id: stmt = stmt.where(CyberPracticeSession.id < before_id)
    page = db.scalars(stmt.order_by(CyberPracticeSession.id.desc()).limit(21)).all()
    return {'sessions': [{'id': row.id, 'count': len(row.snapshot), 'completed': row.result is not None,
        'score': row.result['score'] if row.result else None} for row in page[:20]],
        'next_before_id': page[19].id if len(page) > 20 else None}


@router.get('/practice/{session_id}')
def resume_practice(session_id: int, user=Depends(student_only), db: Session = Depends(get_db)):
    return practice_public(owned(db, CyberPracticeSession, user.id, session_id))


class Answers(BaseModel):
    model_config = ConfigDict(extra='forbid')
    answers: dict[Annotated[str, Field(max_length=64)], StrictInt] = Field(max_length=20)


@router.post('/practice/{session_id}/submit')
def submit_practice(session_id: int, body: Answers, user=Depends(student_only), db: Session = Depends(get_db)):
    row = owned(db, CyberPracticeSession, user.id, session_id, lock=True)
    if set(body.answers) != {q['id'] for q in row.snapshot} or any(
            not 0 <= body.answers[q['id']] < len(q['options']) for q in row.snapshot):
        raise HTTPException(422, 'Answer each selected question with an available option')
    if row.result is not None:
        if row.result['answers'] != body.answers: raise HTTPException(409, 'This saved practice has already been submitted')
        return practice_public(row)
    feedback = [{'id': q['id'], 'prompt': q['prompt'], 'topic': q['topic'], 'module': q['module'],
        'correct': body.answers[q['id']] == q['answer'], 'selected': q['options'][body.answers[q['id']]],
        'expected': q['options'][q['answer']], 'explanation': q['explanation'], 'source': q['source']} for q in row.snapshot]
    row.result = {'submitted_at': datetime.now(timezone.utc).isoformat(), 'answers': body.answers, 'score': sum(q['correct'] for q in feedback),
        'total': len(feedback), 'feedback': feedback,
        'notice': 'This practice sample is not a certification or a complete measure of topic mastery.'}
    db.commit()
    return practice_public(row)
