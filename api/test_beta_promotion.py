"""Beta environment boundaries and non-destructive multi-course publication."""
from copy import deepcopy
from urllib.parse import urlsplit, unquote
import pytest
from beta_runtime import application_environment, validate_beta_database, validate_mail
from beta_promotion import capture, assert_preserved, publish_verified
from test_foundations_courses import content_state


def test_beta_environment_cannot_inherit_development_targets_or_disable_invites():
    inherited = {'PATH': '/system', 'DATABASE_URL': 'development-secret', 'TEST_DATABASE_URL': 'bad',
        'EDUCYBER_LOCAL_DEVELOPMENT': 'enabled', 'EDUCYBER_PRIVATE_BETA': 'disabled',
        'EDUCYBER_API_ORIGIN': 'http://127.0.0.1:8010', 'NEXT_PUBLIC_API_BASE_URL': 'bad',
        'PGHOST': 'elsewhere', 'NODE_OPTIONS': 'unsafe', 'BREVO_API_KEY': 'synthetic-provider-key'}
    before = deepcopy(inherited)
    env = application_environment(inherited, 'synthetic $:/# password')
    assert inherited == before and env['PATH'] == '/system'
    target = urlsplit(env['DATABASE_URL'])
    assert target.hostname == '127.0.0.1' and target.port == 5433 and target.path == '/educyber'
    assert unquote(target.password) == 'synthetic $:/# password'
    assert env['EDUCYBER_PRIVATE_BETA'] == 'enabled'
    assert env['EDUCYBER_LOCAL_DEVELOPMENT'] == 'disabled'
    assert env['EDUCYBER_API_ORIGIN'] == 'http://127.0.0.1:8000'
    assert env['NEXT_PUBLIC_API_BASE_URL'] == ''
    assert not any(key in env for key in ('TEST_DATABASE_URL','PGHOST','NODE_OPTIONS'))
    assert env['BREVO_API_KEY'] == inherited['BREVO_API_KEY']


@pytest.mark.parametrize('target', [
 'postgresql+psycopg://educyber_dev:x@127.0.0.1:5435/educyber_dev?connect_timeout=5',
 'postgresql+psycopg://educyber:x@external.invalid:5433/educyber?connect_timeout=5',
 'postgresql+psycopg://educyber:x@127.0.0.1:5433/educyber?host=external.invalid',
 'sqlite:///beta.db', '',
])
def test_beta_database_guard_rejects_other_targets(target):
    with pytest.raises(ValueError): validate_beta_database(target)


def test_private_mail_file_cannot_override_application_or_database_settings():
    env = application_environment({}, 'password', {'DATABASE_URL': 'bad', 'EDUCYBER_PRIVATE_BETA': 'disabled',
        'BREVO_API_KEY': 'synthetic', 'EDUCYBER_EMAIL_SENDER': 'sender@example.invalid',
        'EDUCYBER_PUBLIC_WEB_URL': 'https://beta.example.invalid'})
    validate_mail(env)
    assert env['EDUCYBER_PRIVATE_BETA'] == 'enabled' and 'bad' not in env['DATABASE_URL']
    for url in ('http://external.invalid', 'https://user:secret@host.invalid', 'https://host.invalid/path', 'https://host.invalid?token=secret'):
        with pytest.raises(ValueError): validate_mail({**env, 'EDUCYBER_PUBLIC_WEB_URL': url})


def test_publication_preserves_existing_records_and_is_idempotent(content_state):
    from sqlalchemy import select, func
    from models import QuizQuestion, Lesson
    _, Session, _ = content_state
    with Session.begin() as db:
        baseline = capture(db.connection())
        before_questions = db.scalar(select(func.count()).select_from(QuizQuestion))
        first = publish_verified(db, baseline)
        assert first['courses'] == 3 and first['active_questions'] == 60
        assert first['new_questions'] == 40  # Fixture already published Python.
        assert db.scalar(select(func.count()).select_from(QuizQuestion)) == before_questions + 40
    with Session.begin() as db:
        assert_preserved(db.connection(), baseline)
        assert publish_verified(db, capture(db.connection()))['new_questions'] == 0
        from curriculum_registry import RELEASES
        assert all(any(row.content.startswith(r.MARKER) for r in RELEASES.values()) for row in db.scalars(select(Lesson).where(Lesson.id <= 9)))


def test_changed_historical_answer_is_detected_and_transaction_rolls_back(content_state):
    from models import QuizQuestion, BetaFeedback
    _, Session, _ = content_state
    with Session() as db: baseline = capture(db.connection())
    with pytest.raises(ValueError):
        with Session.begin() as db:
            db.get(QuizQuestion, 1).correct_index = 1
            db.flush()
            assert_preserved(db.connection(), baseline)
    with Session() as db:
        assert db.get(QuizQuestion, 1).correct_index == 0
        assert db.get(BetaFeedback, 1).message == 'Synthetic retained feedback'


def test_custom_content_preflight_is_atomic(content_state):
    from models import Lesson
    _, Session, _ = content_state
    with Session.begin() as db: db.get(Lesson, 5).content = 'Custom retained teaching'
    with pytest.raises(ValueError):
        with Session.begin() as db: publish_verified(db, capture(db.connection()))
    with Session() as db:
        assert db.get(Lesson, 5).content == 'Custom retained teaching'
        assert not db.get(Lesson, 1).content.startswith('educyber:')


def beta_script():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location('beta_launcher_test', Path(__file__).parents[1] / 'scripts' / 'beta.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('action', ['api', 'web', 'build'])
def test_startup_is_explicit_beta_and_never_migrates_or_publishes(monkeypatch, action):
    module = beta_script()
    env = application_environment({}, 'password', {'BREVO_API_KEY': 'synthetic',
        'EDUCYBER_EMAIL_SENDER': 'sender@example.invalid', 'EDUCYBER_PUBLIC_WEB_URL': 'https://beta.example.invalid'})
    monkeypatch.setattr(module, 'require_context', lambda: None)
    monkeypatch.setattr(module, 'configuration', lambda: dict(env))
    monkeypatch.setattr(module, 'require_free_port', lambda port: None)
    monkeypatch.setattr(module.shutil, 'which', lambda _: '/synthetic/npm')
    monkeypatch.setattr(module.sys, 'argv', ['beta.py', action])
    calls = []
    def call(command, **kwargs): calls.append((command, kwargs)); return 0
    monkeypatch.setattr(module.subprocess, 'call', call)
    assert module.main() == 0 and len(calls) == 1
    command, settings = calls[0]
    assert not any('alembic' in item or 'promotion' in item for item in command)
    assert settings['env']['EDUCYBER_PRIVATE_BETA'] == 'enabled'
    if action in ('web', 'build'):
        assert 'DATABASE_URL' not in settings['env'] and 'BREVO_API_KEY' not in settings['env']
        assert command[-1] == ('build' if action == 'build' else '3000')
    else: assert '8000' in command and settings['env']['BREVO_API_KEY'] == 'synthetic'


def test_preparation_refuses_running_services_before_subprocess(monkeypatch):
    module = beta_script()
    monkeypatch.setattr(module, 'require_context', lambda: None)
    monkeypatch.setattr(module, 'configuration', lambda: {})
    monkeypatch.setattr(module.sys, 'argv', ['beta.py', 'prepare'])
    def occupied(_): raise OSError('synthetic occupied port')
    monkeypatch.setattr(module, 'require_free_port', occupied)
    monkeypatch.setattr(module.subprocess, 'call', lambda *a, **k: pytest.fail('Must not migrate while beta runs'))
    assert module.main() == 1


def test_launcher_rejects_a_development_branch(monkeypatch):
    module = beta_script()
    monkeypatch.setattr(module.subprocess, 'check_output', lambda *a, **k: 'feature/beta-continuous-improvement\n')
    with pytest.raises(ValueError): module.require_context()


def test_backup_copy_is_binary_verified_and_hash_manifest_retained(monkeypatch, tmp_path):
    import hashlib
    import beta_promotion as promotion
    monkeypatch.setattr(promotion, 'ROOT', tmp_path)
    payload = bytes(range(256)) * 16
    digest = hashlib.sha256(payload).hexdigest()
    calls = []
    def command(args, **kwargs):
        calls.append(args)
        if args[1] == 'cp':
            from pathlib import Path
            Path(args[-1]).write_bytes(payload)
        if 'sha256sum' in args: return digest + '  archive'
        return ''
    monkeypatch.setattr(promotion, 'run', command)
    target = promotion.backup('synthetic-container')
    assert target.read_bytes() == payload
    assert target.with_suffix('.dump.sha256').read_text().strip() == digest
    assert any('pg_restore' in call and '--list' in call for call in calls)
    assert not any('pg_restore' in call and '--dbname' in call for call in calls)


@pytest.mark.integration
def test_postgres_publication_preserves_populated_learner_history():
    import os
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import make_url
    from sqlalchemy.orm import Session
    url = os.getenv('TEST_DATABASE_URL')
    if not url: pytest.skip('Isolated PostgreSQL required')
    target = make_url(url)
    if (not target.drivername.startswith('postgresql') or target.database != 'educyber_test'
        or target.host not in ('127.0.0.1','localhost') or os.getenv('DATABASE_URL') != url):
        pytest.fail('Refusing non-local or non-test database')
    from database import Base
    from models import Academy, User, AuthSession, Course, Lesson, QuizQuestion, QuizAttempt, Enrollment, LearnerProgress, MissionRun, BetaFeedback, BetaInvite
    from curriculum_registry import RELEASES
    schema = 'promotion_' + uuid4().hex
    administrative = create_engine(url)
    with administrative.begin() as conn: conn.execute(text('CREATE SCHEMA ' + schema))
    engine = create_engine(url, connect_args={'options': '-csearch_path=' + schema})
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as db:
            for key in ('cyber','secondary','university'): db.add(Academy(id=key, name='Synthetic'))
            user = User(full_name='Synthetic preserved learner',email='promotion@example.invalid',password_hash='disabled',role='student',age_band='adult')
            db.add(user); db.flush()
            expiry = datetime.now(timezone.utc)+timedelta(days=1)
            db.add(AuthSession(user_id=user.id,token_hash='a'*64,expires_at=expiry))
            db.add(BetaInvite(code_hash='b'*64,expires_at=expiry,redeemed_by=user.id))
            db.add(BetaFeedback(user_id=user.id,category='content',message='Synthetic retained feedback'))
            db.add(MissionRun(user_id=user.id,mission_id='risk-command',step_index=1,score=5,choices=[]))
            from models import RedBlueMatch, RedBlueSeat, RedBlueReceipt, JourneyWorkshopRun
            from cyber_warfare import engine as warfare
            from cyber_warfare.scenario import load_scenario
            from journey_workshops import engine as workshops
            actor=f'user:{user.id}'
            match=warfare.new_match(load_scenario('microfinance'),'synthetic-private-seed',actor,'computer')
            command_id=str(uuid4())
            match=warfare.commit(match,actor,warfare.Order('wait_red'),1,command_id)
            saved=RedBlueMatch(creator_id=user.id,transcript=warfare.export_replay(match),difficulty='easy',status='active')
            db.add(saved);db.flush()
            db.add(RedBlueSeat(match_id=saved.id,side='red',user_id=user.id))
            db.add(RedBlueSeat(match_id=saved.id,side='blue',user_id=None))
            db.add(RedBlueReceipt(match_id=saved.id,user_id=user.id,command_id=command_id,request={'action':'wait_red'}))
            state=workshops.advance(workshops.new_state(workshops.CASES['scholarship-pressure']),'a',0,str(uuid4()))
            db.add(JourneyWorkshopRun(user_id=user.id,state=state))
            for release in RELEASES.values():
                course = Course(academy_id=release.ACADEMY_ID,title=release.COURSE_TITLE,status='published')
                db.add(course); db.flush()
                lesson_id = None
                for position,item in enumerate(release.LESSONS,1):
                    lesson = Lesson(course_id=course.id,title=item['title'],content=item['legacy_content'],position=position)
                    db.add(lesson); db.flush(); lesson_id=lesson.id
                q = QuizQuestion(course_id=course.id,prompt='Legacy '+release.COURSE_TITLE,options=['A','B'],correct_index=0,explanation='Original',position=1)
                db.add(q); db.flush()
                db.add(Enrollment(user_id=user.id,course_id=course.id))
                db.add(LearnerProgress(learner_id=str(user.id),lesson_id=lesson_id))
                db.add(QuizAttempt(user_id=user.id,course_id=course.id,answers={str(q.id):0},score=1,total=1))
            db.commit()
        with Session(engine) as db:
            baseline=capture(db.connection())
            assert publish_verified(db,baseline)['new_questions'] == 60
            db.commit()
        with Session(engine) as db:
            assert_preserved(db.connection(),baseline)
            assert publish_verified(db,capture(db.connection()))['new_questions'] == 0
            db.commit()
    finally:
        engine.dispose()
        with administrative.begin() as conn: conn.execute(text('DROP SCHEMA '+schema+' CASCADE'))
        administrative.dispose()


def test_beta_preservation_includes_private_matches_and_workshops(content_state):
    from models import RedBlueMatch, RedBlueSeat, RedBlueReceipt, JourneyWorkshopRun
    _, Session, _ = content_state
    with Session.begin() as db:
        row=RedBlueMatch(creator_id=1,transcript={'seed':'synthetic-private','commands':{'red:x':{'action':'wait_red'}}},difficulty='easy',status='active')
        db.add(row);db.flush()
        db.add(RedBlueSeat(match_id=row.id,side='red',user_id=1))
        db.add(RedBlueReceipt(match_id=row.id,user_id=1,command_id='synthetic',request={'action':'wait_red'}))
        db.add(JourneyWorkshopRun(user_id=1,state={'decisions':['a'],'snapshot':{'id':'synthetic'}}))
    with Session() as db:
        baseline=capture(db.connection())
        assert all(name in baseline for name in ('red_blue_matches','red_blue_seats','red_blue_receipts','journey_workshop_runs'))
        assert 'synthetic-private' not in repr(baseline)
    with Session.begin() as db:
        assert_preserved(db.connection(),baseline)
        assert publish_verified(db,baseline)['courses']==3


def test_beta_check_uses_current_schema_head(monkeypatch):
    module=beta_script()
    from schema_readiness import expected_revision
    from urllib.error import HTTPError
    import io,json
    class Reply(io.BytesIO):
        def __enter__(self):return self
        def __exit__(self,*args):self.close()
    class Opener:
        def open(self,url,**kwargs):
            if url.endswith('/health/development'):raise HTTPError(url,404,'not found',{},None)
            body={'schema':'ready','revision':expected_revision()} if url.endswith('/health/schema') else {'database':'connected'} if url.endswith('/health/db') else {'status':'ok'}
            return Reply(json.dumps(body).encode())
    monkeypatch.setattr(module,'build_opener',lambda *args:Opener())
    module.check()
