"""Real content/assessment HTTP handlers, synthetic SQLite and overridden identity.

No PostgreSQL locking, complete login or deployed browser claim is made here.
"""
import os
from types import SimpleNamespace
from unittest.mock import patch
import pytest


@pytest.fixture
def content_state():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite+pysqlite:///:memory:'}):
        import learning_routes, quiz_routes
        from database import Base
        from models import Academy, BetaFeedback, Course, Enrollment, LearnerProgress, Lesson, QuizAttempt, QuizQuestion, User
        from curriculum_registry import RELEASES
    engine = create_engine('sqlite+pysqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with Session.begin() as db:
        for key in ('cyber','secondary','university'):
            db.add(Academy(id=key, name='Synthetic '+key))
        for user_id in (1,2):
            db.add(User(id=user_id, full_name='Synthetic learner', email=f'learner{user_id}@example.com',
                        password_hash='disabled', role='student', age_band='adult'))
        db.flush()
        for course_id,key in enumerate(('cyber','citizenship','python'),1):
            release = RELEASES[key]
            db.add(Course(id=course_id, academy_id=release.ACADEMY_ID, title=release.COURSE_TITLE, status='published'))
            db.flush()
            for position,item in enumerate(release.LESSONS,1):
                db.add(Lesson(id=(course_id-1)*3+position, course_id=course_id,
                              title=item['title'], content=item['legacy_content'], position=position))
            db.add(Enrollment(user_id=1, course_id=course_id))
            db.add(QuizQuestion(id=course_id, course_id=course_id, prompt=f'Legacy question {course_id}',
                                options=['Old A','Old B'], correct_index=0, explanation='Legacy explanation', position=1))
            db.flush()
            db.add(QuizAttempt(id=course_id, user_id=1, course_id=course_id,
                               answers={str(course_id):0}, score=1, total=1))
            db.add(LearnerProgress(id=course_id, learner_id='1', lesson_id=(course_id-1)*3+1))
        db.add(Course(id=4, academy_id='university', title=RELEASES['cyber'].COURSE_TITLE, status='published'))
        db.flush()
        item=RELEASES['cyber'].LESSONS[0]
        db.add(Lesson(id=10, course_id=4, title=item['title'], content=item['legacy_content'], position=1))
        db.add(Enrollment(user_id=1, course_id=4))
        db.add(BetaFeedback(id=1, user_id=1, category='content', message='Synthetic retained feedback', page='/learn'))
    # Simulate the accepted Python pilot before publishing either new course.
    from publish_python_foundations import publish
    with Session.begin() as db:
        publish(db, apply=True)
    def get_db():
        with Session() as db:
            yield db
    learner=SimpleNamespace(id=1, role='student')
    app=FastAPI()
    app.include_router(learning_routes.router)
    app.include_router(quiz_routes.router)
    app.dependency_overrides[learning_routes.get_db]=get_db
    app.dependency_overrides[learning_routes.current_user]=lambda:learner
    try:
        with TestClient(app) as client:
            yield client,Session,learner
    finally:
        engine.dispose()


def apply_content(Session):
    from publish_foundations import publish_releases
    with Session.begin() as db:
        return publish_releases(db, apply=True)


def test_explicit_atomic_idempotent_publication_retains_history_and_python(content_state):
    from sqlalchemy import func,select
    from models import BetaFeedback,LearnerProgress,Lesson,QuizAttempt,QuizQuestion,User
    from publish_foundations import publish_releases
    from learning_content import active_question_prompts
    client,Session,_=content_state
    with Session() as db:
        python_before=[(db.get(Lesson,i).id,db.get(Lesson,i).content) for i in (7,8,9)]
        count=db.scalar(select(func.count(QuizQuestion.id)))
        preview=publish_releases(db)
        assert (preview['courses'],preview['lessons'],preview['guided_checks'],preview['new_questions'])==(2,6,12,40)
        assert not preview['applied'] and not db.dirty and not db.new
        assert active_question_prompts(db,1) is None and active_question_prompts(db,2) is None
        assert db.scalar(select(func.count(QuizQuestion.id)))==count
    assert apply_content(Session)['new_questions']==40
    assert apply_content(Session)['new_questions']==0
    with Session() as db:
        assert [(db.get(Lesson,i).id,db.get(Lesson,i).content) for i in (7,8,9)]==python_before
        assert db.scalar(select(func.count(QuizQuestion.id)))==count+40
        assert db.scalar(select(func.count(User.id)))==2
        assert db.scalar(select(func.count(LearnerProgress.id)))==3
        assert db.get(BetaFeedback,1).message=='Synthetic retained feedback'
        for i in (1,2,3):
            assert db.get(QuizQuestion,i).prompt==f'Legacy question {i}'
            attempt=db.get(QuizAttempt,i)
            assert (attempt.answers,attempt.score,attempt.total)==({str(i):0},1,1)
    for course,revision in [(1,'cyber-foundations-v1'),(2,'digital-citizenship-v1'),(3,'python-foundations-v1')]:
        rows=client.get(f'/api/v1/learning/courses/{course}/lessons').json()['lessons']
        assert len(rows)==3 and rows[0]['completed']
        for row in rows:
            assert row['content'] and 'educyber.lesson:' not in row['content']
            guide=row['learning_guide']
            assert guide['revision']==revision and len(guide['exercises'])==2
            assert all('answer' not in e and 'feedback' not in e for e in guide['exercises'])
        assert client.get(f'/api/v1/quizzes/courses/{course}/options').json()['available_count']==20
    foreign=client.get('/api/v1/learning/courses/4/lessons').json()['lessons'][0]
    assert foreign['learning_guide'] is None and foreign['content'].startswith('Phishing messages')


@pytest.mark.parametrize('defect',['customized','missing','duplicate_lesson','draft','duplicate_course','conflicting_key','duplicate_prompt'])
def test_second_course_preflight_failure_does_not_change_first(content_state,defect):
    from sqlalchemy import func,select
    from models import Course,Lesson,QuizQuestion
    from curriculum_registry import RELEASES
    from publish_foundations import PublicationError,publish_releases
    _,Session,_=content_state
    with Session.begin() as db:
        if defect=='customized':
            db.get(Lesson,5).content='Teacher-authored material'
        elif defect=='missing':
            db.delete(db.get(Lesson,5))
        elif defect=='duplicate_lesson':
            item=RELEASES['citizenship'].LESSONS[1]
            db.add(Lesson(course_id=2,title=item['title'],content=item['legacy_content'],position=2))
        elif defect=='draft':
            db.get(Course,2).status='draft'
        elif defect=='duplicate_course':
            db.add(Course(academy_id='secondary',title=RELEASES['citizenship'].COURSE_TITLE,status='published'))
        else:
            q=RELEASES['citizenship'].QUESTIONS[0]
            for _ in range(2 if defect=='duplicate_prompt' else 1):
                db.add(QuizQuestion(course_id=2,prompt=q[1],options=q[2] if defect=='duplicate_prompt' else ['Custom','Other'],
                                    correct_index=q[3] if defect=='duplicate_prompt' else 0,explanation=q[4],position=1))
    with Session() as db:
        count=db.scalar(select(func.count(QuizQuestion.id)))
        with pytest.raises(PublicationError):publish_releases(db,apply=True)
        assert not db.dirty and not db.new
        assert db.get(Lesson,1).content.startswith('Phishing messages')
        assert db.scalar(select(func.count(QuizQuestion.id)))==count


@pytest.mark.parametrize('course,key',[(1,'cyber'),(2,'citizenship')])
@pytest.mark.parametrize('count',[5,10,20])
def test_real_assessment_selection_grading_and_history(content_state,course,key,count):
    from curriculum_registry import RELEASES
    client,Session,_=content_state;apply_content(Session)
    options=client.get(f'/api/v1/quizzes/courses/{course}/options').json()
    assert options['available_count']==20 and options['presets']==[5,10,20]
    questions=client.get(f'/api/v1/quizzes/courses/{course}?question_count={count}').json()['questions']
    assert len(questions)==count and len({q['prompt'] for q in questions})==count
    assert all(q['id']!=course and 'correct_index' not in q and 'explanation' not in q for q in questions)
    keys={q[1]:q[3] for q in RELEASES[key].QUESTIONS}
    answers={str(q['id']):keys[q['prompt']] for q in questions}
    first=questions[0];answers[str(first['id'])]=(keys[first['prompt']]+1)%len(first['options'])
    response=client.post(f'/api/v1/quizzes/courses/{course}/submit',json={'question_count':count,'answers':answers})
    assert response.status_code==201
    assert (response.json()['score'],response.json()['total'])==(count-1,count)
    assert all(item['explanation'] for item in response.json()['feedback'])
    history=client.get(f'/api/v1/quizzes/courses/{course}/attempts').json()['attempts']
    assert (history[0]['score'],history[0]['total'])==(count-1,count)
    assert (history[1]['score'],history[1]['total'])==(1,1)
    assert len(client.get(f'/api/v1/quizzes/courses/{course}').json()['questions'])==20


def practice_cases():
    from curriculum_registry import RELEASES
    return [(key,course,index,e['id']) for key,course in [('cyber',1),('citizenship',2)]
            for index,lesson in enumerate(RELEASES[key].LESSONS) for e in lesson['exercises']]


@pytest.mark.parametrize('key,course,index,exercise_id',practice_cases())
def test_all_practice_choices_explain_without_saving_grade_or_completion(content_state,key,course,index,exercise_id):
    from sqlalchemy import func,select
    from models import LearnerProgress,QuizAttempt
    from curriculum_registry import RELEASES
    client,Session,_=content_state;apply_content(Session)
    exercise=next(e for e in RELEASES[key].LESSONS[index]['exercises'] if e['id']==exercise_id)
    lesson=(course-1)*3+index+1
    for option in ((exercise['answer']+1)%len(exercise['options']),exercise['answer']):
        response=client.post(f'/api/v1/learning/lessons/{lesson}/practice',json={'exercise_id':exercise_id,'option_index':option})
        assert response.status_code==200
        assert response.json()['correct'] is (option==exercise['answer'])
        assert response.json()['explanation']==exercise['feedback'][option] and 'score' not in response.json()
    with Session() as db:
        assert db.scalar(select(func.count(QuizAttempt.id)))==3
        assert db.scalar(select(func.count(LearnerProgress.id)))==3


@pytest.mark.parametrize('option',[True,'1',1.5,-1,3])
def test_invalid_practice_options(content_state,option):
    client,Session,_=content_state;apply_content(Session)
    assert client.post('/api/v1/learning/lessons/1/practice',json={'exercise_id':'scholarship-route','option_index':option}).status_code==422


def test_enrollment_role_publication_and_cross_course_boundaries(content_state):
    from models import Course
    client,Session,learner=content_state;apply_content(Session)
    body={'exercise_id':'scholarship-route','option_index':1}
    assert client.post('/api/v1/learning/lessons/1/practice',json={**body,'correct':True}).status_code==422
    for lesson in [4,10]:assert client.post(f'/api/v1/learning/lessons/{lesson}/practice',json=body).status_code==404
    learner.id=2
    assert client.get('/api/v1/learning/courses/1/lessons').status_code==403
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==403
    assert client.get('/api/v1/quizzes/courses/1/options').status_code==403
    learner.id=1;learner.role='teacher'
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==403
    learner.role='student'
    with Session.begin() as db:db.get(Course,1).status='draft'
    assert client.get('/api/v1/learning/courses/1/lessons').status_code==404
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==404


def test_partial_or_foreign_markers_do_not_activate_bank(content_state):
    from models import Course,Lesson
    from learning_content import active_question_prompts,guide_for
    from curriculum_registry import RELEASES
    _,Session,_=content_state
    with Session.begin() as db:db.get(Lesson,1).content=RELEASES['cyber'].MARKER+'phishing'
    with Session() as db:
        assert active_question_prompts(db,1) is None
        lesson=db.get(Lesson,1)
        assert guide_for(db.get(Course,4),lesson) is None
        lesson.content=RELEASES['citizenship'].MARKER+'footprint'
        assert guide_for(db.get(Course,1),lesson) is None


def test_all_banks_are_distinct_and_every_objective_is_taught():
    from curriculum_registry import RELEASES
    prompts=[]
    for release in RELEASES.values():
        assert len(release.LESSONS)==3 and len(release.QUESTIONS)==20
        objectives={o['id'] for item in release.LESSONS for o in item['objectives']}
        assert len(objectives)==9 and {q[0] for q in release.QUESTIONS}==objectives
        prompts.extend(q[1].strip().casefold() for q in release.QUESTIONS)
        ids=set()
        for item in release.LESSONS:
            assert len(item['sections'])>=4 and len(item['exercises'])==2
            for e in item['exercises']:
                assert e['id'] not in ids;ids.add(e['id'])
                assert e['objective'] in {o['id'] for o in item['objectives']}
                assert len(e['feedback'])==len(e['options']) and all(e['feedback'])
                assert len(set(e['options']))==len(e['options']) and 0<=e['answer']<len(e['options'])
        for _,_,options,answer,explanation in release.QUESTIONS:
            assert len(set(options))==len(options) and 0<=answer<len(options) and explanation
    assert len(set(prompts))==60


def test_cli_rejects_beta_target_without_echoing_values(monkeypatch,capsys):
    import publish_foundations
    monkeypatch.setattr('sys.argv',['publish_foundations'])
    monkeypatch.setenv('DATABASE_URL','postgresql+psycopg://user:never-display-this@127.0.0.1:5433/beta')
    monkeypatch.setenv('EDUCYBER_LOCAL_DEVELOPMENT','enabled')
    assert publish_foundations.safe_cli()==1
    captured=capsys.readouterr()
    assert captured.out=='' and 'never-display-this' not in captured.err and 'Content publication stopped' in captured.err


@pytest.mark.parametrize('action,module,apply', [
    ('content-preview','publish_python_foundations',False),
    ('content-apply','publish_python_foundations',True),
    ('foundations-preview','publish_foundations',False),
    ('foundations-apply','publish_foundations',True),
])
def test_content_launcher_dispatch_preserves_configuration_guard(monkeypatch,action,module,apply):
    import importlib.util
    from pathlib import Path
    path=Path(__file__).resolve().parents[1]/'scripts'/'development.py'
    spec=importlib.util.spec_from_file_location('foundations_dev_launcher',path)
    launcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(launcher)
    settings={'DATABASE_URL':'synthetic-guarded-environment'}
    called=[]
    monkeypatch.setattr('sys.argv',['development.py',action])
    monkeypatch.setattr(launcher,'configuration',lambda:settings)
    monkeypatch.setattr(launcher.subprocess,'call',lambda command,**kwargs:called.append((command,kwargs)) or 0)
    monkeypatch.setattr(launcher,'require_free_port',lambda port:pytest.fail('Content publication must not start services'))
    assert launcher.main()==0
    command,kwargs=called[0]
    assert command[1:]==['-m',module]+(['--apply'] if apply else [])
    assert kwargs['env'] is settings and kwargs['cwd']==path.parents[1]/'api'
    def refuse():raise ValueError('Refused synthetic configuration')
    monkeypatch.setattr(launcher,'configuration',refuse)
    assert launcher.main()==1 and len(called)==1
