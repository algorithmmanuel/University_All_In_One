"""End-to-end object authorization and quiz integrity checks.

Uses an isolated PostgreSQL database, real bearer sessions, and actual HTTP
endpoints. Temporary records are removed even when assertions fail.
"""
import os
import uuid

import pytest


@pytest.mark.integration
def test_learning_quiz_and_mission_access_boundaries():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is required")
    from sqlalchemy.engine import make_url
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql")
            or parsed.database != "educyber_test"
            or parsed.host not in ("127.0.0.1", "localhost")
            or os.getenv("DATABASE_URL") not in (None, url)):
        pytest.fail("Refusing non-isolated database")
    os.environ["DATABASE_URL"] = url

    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, delete
    from sqlalchemy.orm import sessionmaker
    from auth import issue_session
    from database import Base
    from main import app
    from mission_data import MISSIONS
    from models import (Academy, AuthSession, Course, Enrollment, Lesson,
                        LearnerProgress, MissionRun, QuizAttempt, QuizQuestion, User)

    engine = create_engine(url)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    unique = uuid.uuid4().hex
    academy_id = ("s" + unique)[:30]
    user_ids = []
    course_ids = []
    lesson_ids = []
    quiz_ids = []
    mission_run_ids = []
    try:
        with Session.begin() as db:
            db.add(Academy(id=academy_id, name="Authorization Fixture", status="active"))
            db.flush()
            published = Course(academy_id=academy_id, title="Published Test",
                               description="Test", status="published")
            draft = Course(academy_id=academy_id, title="Draft Test",
                           description="Test", status="draft")
            db.add_all([published, draft])
            db.flush()
            course_ids.extend([published.id, draft.id])
            lesson = Lesson(course_id=published.id, title="Private Lesson",
                            content="Test content", position=0)
            quiz = QuizQuestion(course_id=published.id, prompt="Safe question?",
                                options=["yes", "no"], correct_index=0,
                                explanation="Correct", position=0)
            db.add_all([lesson, quiz])
            db.flush()
            lesson_ids.append(lesson.id)
            quiz_ids.append(quiz.id)
            users = []
            for role in ("student", "student", "teacher"):
                user = User(full_name="Access Test", email=f"{uuid.uuid4().hex}@example.com",
                            password_hash="test-only", role=role, is_active=True,
                            is_approved=True)
                db.add(user)
                users.append(user)
            db.flush()
            user_ids.extend(user.id for user in users)
            db.add(Enrollment(user_id=users[0].id, course_id=published.id))
            run = MissionRun(user_id=users[0].id, mission_id=next(iter(MISSIONS)),
                             step_index=0, score=0, choices=[])
            db.add(run)
            db.flush()
            mission_run_ids.append(run.id)
            owner_id, other_id, teacher_id = user_ids
            course_id, draft_id = course_ids
            lesson_id = lesson.id
            run_id = run.id

        with Session() as db:
            tokens = {}
            for name, uid in (("owner", owner_id), ("other", other_id),
                              ("teacher", teacher_id)):
                tokens[name] = issue_session(db, db.get(User, uid))
        headers = {name: {"Authorization": f"Bearer {token}"}
                   for name, token in tokens.items()}

        with TestClient(app) as client:
            # Private progress cannot be accessed with a different learner's token.
            assert client.get(f"/api/v1/missions/runs/{run_id}",
                              headers=headers["other"]).status_code == 404
            assert client.post(f"/api/v1/missions/runs/{run_id}/decide",
                               headers=headers["other"],
                               json={"option_index": 0, "expected_step": 0}).status_code == 404
            assert client.get(f"/api/v1/missions/runs/{run_id}",
                              headers=headers["owner"]).status_code == 200
            assert client.get("/api/v1/learning/enrollments",
                              headers=headers["other"]).json()["enrollments"] == []
            assert client.get(f"/api/v1/learning/courses/{course_id}/lessons",
                              headers=headers["other"]).status_code == 403
            assert client.post(f"/api/v1/learning/lessons/{lesson_id}/complete",
                               headers=headers["other"]).status_code == 403
            assert client.get(f"/api/v1/quizzes/courses/{course_id}",
                              headers=headers["other"]).status_code == 403
            assert client.get(f"/api/v1/quizzes/courses/{course_id}/attempts",
                              headers=headers["other"]).status_code == 403
            assert client.post(f"/api/v1/quizzes/courses/{course_id}/submit",
                               headers=headers["other"],
                               json={"answers": {str(quiz_ids[0]): 0}}).status_code == 403

            # Teacher accounts cannot impersonate a student or earn mission scores.
            assert client.get("/api/v1/missions", headers=headers["teacher"]).status_code == 403
            assert client.post(f"/api/v1/learning/enrollments/{course_id}",
                               headers=headers["teacher"]).status_code == 403
            assert client.get(f"/api/v1/quizzes/courses/{course_id}",
                              headers=headers["teacher"]).status_code == 403

            # Draft content is not accessible, even to an enrolled learner.
            assert client.post(f"/api/v1/learning/enrollments/{draft_id}",
                               headers=headers["owner"]).status_code == 404
            assert client.get(f"/api/v1/quizzes/courses/{draft_id}",
                              headers=headers["owner"]).status_code == 404

            # Server grading rejects injected scores, missing answers and invalid choices.
            endpoint = f"/api/v1/quizzes/courses/{course_id}/submit"
            assert client.post(endpoint, headers=headers["owner"],
                               json={"answers": {str(quiz_ids[0]): 1}, "score": 100}).status_code == 422
            assert client.post(endpoint, headers=headers["owner"],
                               json={"answers": {}}).status_code == 422
            assert client.post(endpoint, headers=headers["owner"],
                               json={"answers": {str(quiz_ids[0]): 99}}).status_code == 422
            graded = client.post(endpoint, headers=headers["owner"],
                                 json={"answers": {str(quiz_ids[0]): 1}})
            assert graded.status_code == 201
            assert graded.json()["score"] == 0
            assert graded.json()["total"] == 1
            assert client.get(f"/api/v1/quizzes/courses/{course_id}/attempts",
                              headers=headers["other"]).status_code == 403
            assert len(client.get(f"/api/v1/quizzes/courses/{course_id}/attempts",
                                  headers=headers["owner"]).json()["attempts"]) == 1

            # Missing IDs are handled as controlled 404s, not internal errors.
            assert client.get("/api/v1/missions/runs/2147483647",
                              headers=headers["owner"]).status_code == 404
            assert client.get("/api/v1/learning/courses/2147483647/lessons",
                              headers=headers["owner"]).status_code == 404
            assert client.get("/api/v1/quizzes/courses/2147483647",
                              headers=headers["owner"]).status_code == 404
    finally:
        with Session.begin() as db:
            db.execute(delete(QuizAttempt).where(QuizAttempt.user_id.in_(user_ids)))
            db.execute(delete(LearnerProgress).where(LearnerProgress.learner_id.in_(
                [str(uid) for uid in user_ids])))
            db.execute(delete(MissionRun).where(MissionRun.id.in_(mission_run_ids)))
            db.execute(delete(Enrollment).where(Enrollment.user_id.in_(user_ids)))
            db.execute(delete(AuthSession).where(AuthSession.user_id.in_(user_ids)))
            db.execute(delete(QuizQuestion).where(QuizQuestion.id.in_(quiz_ids)))
            db.execute(delete(Lesson).where(Lesson.id.in_(lesson_ids)))
            db.execute(delete(Course).where(Course.id.in_(course_ids)))
            db.execute(delete(User).where(User.id.in_(user_ids)))
            db.execute(delete(Academy).where(Academy.id == academy_id))
        engine.dispose()
