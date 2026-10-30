"""Feature regressions using synthetic in-memory state; auth is overridden."""
import io
import os
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch
import pytest


@pytest.fixture
def client_state():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    with patch.dict(os.environ, {'DATABASE_URL':'sqlite+pysqlite:///:memory:'}):
        import learning_routes,quiz_routes
        from database import Base
        from models import Academy,Course,Enrollment,LearnerProgress,Lesson,QuizAttempt,QuizQuestion,User
        from python_foundations import COURSE_TITLE,LESSONS
    engine=create_engine('sqlite+pysqlite:///:memory:',connect_args={'check_same_thread':False},poolclass=StaticPool)
    Session=sessionmaker(bind=engine,expire_on_commit=False);Base.metadata.create_all(engine)
    with Session.begin() as db:
        db.add(Academy(id='university',name='Synthetic university'))
        db.add(User(id=1,full_name='Synthetic learner',email='learner@example.com',password_hash='disabled',role='student'))
        db.flush()
        db.add(Course(id=1,academy_id='university',title=COURSE_TITLE,status='published'))
        db.add(Course(id=2,academy_id='university',title='Other',status='published'));db.flush()
        db.add(Enrollment(user_id=1,course_id=1))
        for i,item in enumerate(LESSONS,1):db.add(Lesson(id=i,course_id=1,title=item['title'],content=item['legacy_content'],position=i))
        db.add(Lesson(id=4,course_id=2,title='Other',content='Plain text',position=1))
        db.add(QuizQuestion(id=1,course_id=1,prompt='Old unaligned question',options=['A','B'],correct_index=0,explanation='Legacy',position=1));db.flush()
        db.add(LearnerProgress(id=1,learner_id='1',lesson_id=1))
        db.add(QuizAttempt(id=1,user_id=1,course_id=1,answers={'1':0},score=1,total=1))
    def get_db():
        with Session() as db:yield db
    learner=SimpleNamespace(id=1,role='student')
    app=FastAPI();app.include_router(learning_routes.router);app.include_router(quiz_routes.router)
    app.dependency_overrides[learning_routes.get_db]=get_db
    app.dependency_overrides[learning_routes.current_user]=lambda:learner
    try:
        with TestClient(app) as client:yield client,Session,learner
    finally:engine.dispose()


def activate(Session):
    from publish_python_foundations import publish
    with Session.begin() as db:return publish(db,apply=True)


def test_publish_is_explicit_idempotent_and_preserves_history(client_state):
    from sqlalchemy import func,select
    from models import LearnerProgress,Lesson,QuizAttempt,QuizQuestion
    from publish_python_foundations import publish
    client,Session,_=client_state
    with Session() as db:
        assert publish(db)['new_questions']==20
        assert db.get(Lesson,1).content.startswith('Python variables')
    assert client.get('/api/v1/quizzes/courses/1/options').json()['available_count']==1
    assert activate(Session)['new_questions']==20
    assert activate(Session)['new_questions']==0
    with Session() as db:
        assert db.scalar(select(func.count(QuizQuestion.id)))==21
        assert db.get(QuizQuestion,1).prompt=='Old unaligned question'
        assert (db.get(QuizAttempt,1).answers,db.get(QuizAttempt,1).score,db.get(QuizAttempt,1).total)==({'1':0},1,1)
        assert db.get(LearnerProgress,1).lesson_id==1
    lessons=client.get('/api/v1/learning/courses/1/lessons').json()['lessons']
    assert lessons[0]['completed'] is True
    assert all(row['content'] and 'educyber.lesson:' not in row['content'] for row in lessons)
    for row in lessons:
        assert len(row['learning_guide']['exercises'])==2
        assert all('answer' not in e and 'feedback' not in e for e in row['learning_guide']['exercises'])
    assert client.get('/api/v1/quizzes/courses/1/options').json()['presets']==[5,10,20]
    for count in [5,10,20]:
        questions=client.get(f'/api/v1/quizzes/courses/1?question_count={count}').json()['questions']
        assert len(questions)==count and all(q['id']!=1 for q in questions)
        assert all('correct_index' not in q and 'explanation' not in q for q in questions)
    assert len(client.get('/api/v1/quizzes/courses/1').json()['questions'])==20


def test_customized_lessons_cannot_be_overwritten_or_partially_published(client_state):
    from models import Lesson
    from publish_python_foundations import publish
    from learning_content import active_question_prompts
    _,Session,_=client_state
    with Session.begin() as db:db.get(Lesson,2).content='Teacher customized material'
    with Session() as db:
        with pytest.raises(ValueError,match='customized'):publish(db,apply=True)
        assert db.get(Lesson,1).content.startswith('Python variables')
        assert active_question_prompts(db,1) is None


@pytest.mark.parametrize('lesson_id,exercise,option,correct',[(1,'trace-balance',0,False),(1,'trace-balance',1,True),(1,'text-number',1,True),(2,'boundary',0,True),(2,'two-rules',1,True),(3,'range-total',1,True),(3,'while-stop',0,True)])
def test_practice_feedback_never_saves_a_grade_or_completion(client_state,lesson_id,exercise,option,correct):
    from sqlalchemy import func,select
    from models import LearnerProgress,QuizAttempt
    client,Session,_=client_state;activate(Session)
    response=client.post(f'/api/v1/learning/lessons/{lesson_id}/practice',json={'exercise_id':exercise,'option_index':option})
    assert response.status_code==200
    assert response.json()['correct'] is correct and response.json()['explanation']
    assert 'score' not in response.json()
    with Session() as db:
        assert db.scalar(select(func.count(QuizAttempt.id)))==1
        assert db.scalar(select(func.count(LearnerProgress.id)))==1


@pytest.mark.parametrize('body',[{'exercise_id':'trace-balance','option_index':True},{'exercise_id':'trace-balance','option_index':'1'},{'exercise_id':'trace-balance','option_index':-1},{'exercise_id':'trace-balance','option_index':3},{'exercise_id':'trace-balance','option_index':1,'correct':True}])
def test_invalid_or_forged_practice_answers_are_rejected(client_state,body):
    client,Session,_=client_state;activate(Session)
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==422


def test_practice_retains_enrollment_role_publication_boundaries(client_state):
    from models import Course
    client,Session,learner=client_state;activate(Session);body={'exercise_id':'trace-balance','option_index':1}
    for lesson,status in [(4,403),(999,404),(2,404)]:
        assert client.post(f'/api/v1/learning/lessons/{lesson}/practice',json=body).status_code==status
    learner.role='teacher'
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==403
    learner.role='student'
    with Session.begin() as db:db.get(Course,1).status='draft'
    assert client.post('/api/v1/learning/lessons/1/practice',json=body).status_code==404


def test_assessments_are_aligned_and_author_examples_produce_documented_output():
    from python_foundations import LESSONS,QUESTIONS
    assert {q[0] for q in QUESTIONS}=={o['id'] for lesson in LESSONS for o in lesson['objectives']}
    assert len({q[1].strip().casefold() for q in QUESTIONS})==20
    for lesson in LESSONS:
        for exercise in lesson['exercises']:assert exercise['objective'] in {o['id'] for o in lesson['objectives']}
        for section in lesson['sections']:
            if 'code' not in section:continue
            output=io.StringIO()
            # Fixed author examples only; learner input is never executed by the app.
            with redirect_stdout(output):exec(section['code'],{'__builtins__':{'print':print,'range':range,'len':len}})
            assert output.getvalue().rstrip('\n')==section['output']


def test_aligned_bank_is_recomputed_and_historical_attempt_is_not_rewritten(client_state):
    from python_foundations import QUESTIONS
    client,Session,_=client_state;activate(Session)
    selected=client.get('/api/v1/quizzes/courses/1?question_count=20').json()['questions']
    keys={q[1]:q[3] for q in QUESTIONS}
    answers={str(q['id']):keys[q['prompt']] for q in selected}
    first=selected[0];answers[str(first['id'])]=(keys[first['prompt']]+1)%len(first['options'])
    response=client.post('/api/v1/quizzes/courses/1/submit',json={'question_count':20,'answers':answers})
    assert response.status_code==201
    assert (response.json()['score'],response.json()['total'])==(19,20)
    assert all(item['explanation'] for item in response.json()['feedback'])
    history=client.get('/api/v1/quizzes/courses/1/attempts').json()['attempts']
    assert (history[0]['score'],history[0]['total'])==(19,20)
    assert (history[1]['score'],history[1]['total'])==(1,1)


def test_conflicting_question_keys_abort_without_overwriting(client_state):
    from models import Lesson,QuizQuestion
    from python_foundations import QUESTIONS
    from publish_python_foundations import publish
    _,Session,_=client_state
    with Session.begin() as db:
        db.add(QuizQuestion(course_id=1,prompt=QUESTIONS[0][1],options=['Custom','Other'],correct_index=0,explanation='Custom',position=2))
    with Session() as db:
        with pytest.raises(ValueError,match='Conflicting'):publish(db,apply=True)
        assert db.get(Lesson,1).content.startswith('Python variables')
