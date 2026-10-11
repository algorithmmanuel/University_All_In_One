"""Course quizzes: server-side grading and persisted attempts."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import current_user
from db_dependencies import get_db
from models import Course, Enrollment, QuizAttempt, QuizQuestion, User

router = APIRouter(prefix="/api/v1/quizzes", tags=["quizzes"])

def eligible(db: Session, user: User, course_id: int):
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Student account required")
    course = db.get(Course, course_id)
    if course is None or course.status != "published":
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled = db.scalar(select(Enrollment.id).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if enrolled is None:
        raise HTTPException(status_code=403, detail="Enroll in this course first")

class Submission(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: dict[int, int] = Field(max_length=100)

@router.get("/courses/{course_id}")
def questions(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    rows = db.scalars(select(QuizQuestion).where(QuizQuestion.course_id == course_id)
                      .order_by(QuizQuestion.position, QuizQuestion.id)).all()
    return {"course_id": course_id, "questions": [
        {"id": q.id, "prompt": q.prompt, "options": q.options} for q in rows]}

@router.post("/courses/{course_id}/submit", status_code=201)
def submit(course_id: int, body: Submission, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    rows = db.scalars(select(QuizQuestion).where(QuizQuestion.course_id == course_id)
                      .order_by(QuizQuestion.position, QuizQuestion.id)).all()
    if not rows:
        raise HTTPException(status_code=404, detail="No quiz available")
    expected = {q.id for q in rows}
    if set(body.answers) != expected:
        raise HTTPException(status_code=422, detail="Answer every question exactly once")
    if any(type(body.answers[q.id]) is not int or not 0 <= body.answers[q.id] < len(q.options) for q in rows):
        raise HTTPException(status_code=422, detail="Invalid answer option")
    score = sum(body.answers[q.id] == q.correct_index for q in rows)
    attempt = QuizAttempt(user_id=user.id, course_id=course_id,
                          answers={str(k): v for k,v in body.answers.items()},
                          score=score, total=len(rows))
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, "score": score, "total": len(rows),
            "percentage": round(100 * score / len(rows)),
            "feedback": [{"question_id": q.id, "correct_index": q.correct_index,
                          "selected_index": body.answers[q.id],
                          "correct": body.answers[q.id] == q.correct_index,
                          "explanation": q.explanation} for q in rows]}

@router.get("/courses/{course_id}/attempts")
def attempts(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    rows = db.scalars(select(QuizAttempt).where(
        QuizAttempt.user_id == user.id, QuizAttempt.course_id == course_id)
        .order_by(QuizAttempt.submitted_at.desc(), QuizAttempt.id.desc()).limit(20)).all()
    return {"attempts": [{"id": a.id, "score": a.score, "total": a.total,
                           "percentage": round(100 * a.score / a.total) if a.total else 0,
                           "submitted_at": a.submitted_at.isoformat()} for a in rows]}
