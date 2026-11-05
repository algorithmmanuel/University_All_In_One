"""Actual HTTP snapshot/authorization checks with synthetic state and overridden auth."""
import pytest
from test_foundations_courses import content_state, apply_content


def submit(client, Session, course=1, count=20, wrong=False):
    from models import QuizQuestion
    questions = client.get(f'/api/v1/quizzes/courses/{course}?question_count={count}').json()['questions']
    with Session() as db:
        answers = {str(q['id']): (db.get(QuizQuestion, q['id']).correct_index + int(wrong)) % len(q['options'])
                   for q in questions}
    response = client.post(f'/api/v1/quizzes/courses/{course}/submit',
                           json={'question_count': count, 'answers': answers})
    assert response.status_code == 201, response.text
    return response.json()


@pytest.mark.parametrize('course', [1, 2, 3])
@pytest.mark.parametrize('wrong', [False, True])
def test_topic_counts_and_recommendations_match_actual_attempt(content_state, course, wrong):
    from curriculum_registry import RELEASES
    client, Session, _ = content_state
    apply_content(Session)
    result = submit(client, Session, course, wrong=wrong)
    analysis = result['analysis']
    assert len(analysis['topics']) == 9 and analysis['unmapped_count'] == 0
    assert sum(t['total'] for t in analysis['topics']) == result['total'] == 20
    assert sum(t['correct'] for t in analysis['topics']) == result['score'] == (0 if wrong else 20)
    assert all(t['total'] >= 2 for t in analysis['topics'])
    assert {t['status'] for t in analysis['topics']} == ({'revisit'} if wrong else {'strength_in_this_attempt'})
    release = RELEASES[('cyber','citizenship','python')[course-1]]
    assert analysis['curriculum_revision'] == release.REVISION
    mapping = {q[1]: q[0] for q in release.QUESTIONS}
    assert all(item['objective_id'] == mapping[item['prompt']] for item in analysis['feedback'])
    assert all(t['lesson_id'] and t['lesson_title'] and t['recommendation'] for t in analysis['topics'])
    detail = client.get(f'/api/v1/quizzes/courses/{course}/attempts/{result["attempt_id"]}').json()
    assert detail['analysis'] == analysis and detail['score'] == result['score']


def test_small_sample_and_repeated_attempts_never_imply_mastery(content_state):
    client, Session, _ = content_state
    apply_content(Session)
    for _ in range(3):
        analysis = submit(client, Session, count=1)['analysis']
        assert [t['status'] for t in analysis['topics']].count('limited_evidence') == 1
        assert [t['status'] for t in analysis['topics']].count('not_assessed') == 8
        assert sum(t['total'] for t in analysis['topics']) == 1
    analysis = submit(client, Session, count=1, wrong=True)['analysis']
    topic = next(t for t in analysis['topics'] if t['total'])
    assert topic['status'] == 'limited_evidence' and topic['correct'] == 0
    assert 'Review' in topic['recommendation']


def test_legacy_scores_preserved_without_inventing_topic_history(content_state):
    from models import QuizAttempt
    client, Session, _ = content_state
    apply_content(Session)
    with Session() as db:
        old = db.get(QuizAttempt, 1)
        before = (old.answers, old.score, old.total, old.submitted_at)
    assert client.get('/api/v1/quizzes/courses/1/attempts/1').json()['analysis'] is None
    submit(client, Session)
    with Session() as db:
        old = db.get(QuizAttempt, 1)
        assert (old.answers, old.score, old.total, old.submitted_at) == before
        assert old.result_snapshot is None


@pytest.mark.parametrize('change', ['question', 'lesson', 'course'])
def test_snapshot_is_stable_after_catalogue_edits(content_state, change):
    from models import Course, Lesson, QuizQuestion
    client, Session, _ = content_state
    apply_content(Session)
    result = submit(client, Session)
    with Session.begin() as db:
        if change == 'question':
            row = db.get(QuizQuestion, result['analysis']['feedback'][0]['question_id'])
            row.prompt = 'Changed'; row.options = ['Changed']; row.correct_index = 0; row.explanation = 'Changed'
        elif change == 'lesson':
            db.get(Lesson, 1).content = 'Changed teaching'
        else:
            db.get(Course, 1).title = 'Changed course'
    assert client.get(f'/api/v1/quizzes/courses/1/attempts/{result["attempt_id"]}').json()['analysis'] == result['analysis']


def test_foreign_owner_course_missing_and_nonstudent_rejected(content_state):
    from models import Enrollment
    client, Session, learner = content_state
    apply_content(Session)
    result = submit(client, Session)
    path = f'/api/v1/quizzes/courses/1/attempts/{result["attempt_id"]}'
    assert client.get(path.replace('/courses/1/', '/courses/2/')).status_code == 404
    assert client.get('/api/v1/quizzes/courses/1/attempts/999999').status_code == 404
    with Session.begin() as db:
        db.add(Enrollment(user_id=2, course_id=1))
    learner.id = 2
    assert client.get(path).status_code == 404
    learner.role = 'teacher'
    assert client.get(path).status_code == 403
    learner.id = 1; learner.role = 'student'
    with Session.begin() as db:
        db.delete(db.query(Enrollment).filter_by(user_id=1, course_id=1).one())
    assert client.get(path).status_code == 403


@pytest.mark.parametrize('defect', ['options', 'key', 'explanation', 'partial_publication'])
def test_customized_content_gets_no_guessed_objective_credit(content_state, defect):
    from models import Lesson, QuizQuestion
    from sqlalchemy import select
    client, Session, _ = content_state
    apply_content(Session)
    with Session.begin() as db:
        # Identify an active (not retained legacy) item by its reviewed prompt.
        from cyber_foundations import QUESTIONS
        row = db.scalar(select(QuizQuestion).where(QuizQuestion.course_id == 1, QuizQuestion.prompt == QUESTIONS[0][1]))
        if defect == 'options': row.options = list(reversed(row.options))
        elif defect == 'key': row.correct_index = (row.correct_index + 1) % len(row.options)
        elif defect == 'explanation': row.explanation = 'Customized'
        else: db.get(Lesson, 1).content = 'Partial teaching release'
    result = submit(client, Session, count=20)
    assert result['analysis']['unmapped_count'] >= 1
    if defect == 'partial_publication': assert result['analysis']['topics'] == []


def test_forged_analysis_rejected(content_state):
    client, Session, _ = content_state
    assert client.post('/api/v1/quizzes/courses/1/submit', json={
        'answers': {'1': 0}, 'analysis': {'topics': []}}).status_code == 422


def test_duplicate_reviewed_rows_do_not_inflate_topic_evidence(content_state):
    from models import QuizQuestion
    from cyber_foundations import QUESTIONS
    client, Session, _ = content_state
    apply_content(Session)
    q = QUESTIONS[0]
    with Session.begin() as db:
        db.add(QuizQuestion(course_id=1, position=99, prompt=q[1], options=q[2], correct_index=q[3], explanation=q[4]))
    from sqlalchemy import select
    with Session() as db:
        rows = db.scalars(select(QuizQuestion).where(QuizQuestion.course_id == 1, QuizQuestion.prompt.in_([q[1] for q in QUESTIONS]))).all()
        answers = {str(row.id): row.correct_index for row in rows}
    result = client.post('/api/v1/quizzes/courses/1/submit', json={'answers': answers}).json()
    assert result['score'] == result['total'] == 21
    assert sum(t['total'] for t in result['analysis']['topics']) == 20
    assert result['analysis']['unmapped_count'] == 1
