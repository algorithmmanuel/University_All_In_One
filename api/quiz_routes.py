"""Course quizzes: server-side grading and persisted attempts."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict, StrictInt
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import current_user
from db_dependencies import get_db
from models import Course, Enrollment, QuizAttempt, QuizQuestion, User
from learning_content import active_question_prompts
from assessment_selection import MAX_QUESTIONS, grade_questions, select_questions, unique_questions

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
    answers: dict[int, StrictInt] = Field(max_length=MAX_QUESTIONS)
    question_count: StrictInt | None = Field(default=None, ge=1, le=MAX_QUESTIONS)


def question_bank(db: Session, course_id: int):
    stmt = select(QuizQuestion).where(QuizQuestion.course_id == course_id)
    prompts = active_question_prompts(db, course_id)
    if prompts is not None:
        stmt = stmt.where(QuizQuestion.prompt.in_(prompts))
    return db.scalars(stmt.order_by(QuizQuestion.position, QuizQuestion.id)).all()


@router.get("/courses/{course_id}/options")
def assessment_options(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    available = min(MAX_QUESTIONS, len(unique_questions(question_bank(db, course_id))))
    return {"course_id": course_id, "available_count": available,
            "presets": [count for count in (5, 10, 20) if count <= available]}

@router.get("/courses/{course_id}")
def questions(course_id: int, question_count: int | None = Query(default=None, ge=1, le=MAX_QUESTIONS),
              user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    try:
        rows = select_questions(question_bank(db, course_id), question_count)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from None
    return {"course_id": course_id, "question_count": len(rows), "questions": [
        {"id": q.id, "prompt": q.prompt, "options": q.options} for q in rows]}

@router.post("/courses/{course_id}/submit", status_code=201)
def submit(course_id: int, body: Submission, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    bank = question_bank(db, course_id)
    if not bank:
        raise HTTPException(status_code=404, detail="No quiz available")
    try:
        rows = select_questions(bank, body.question_count)
        result = grade_questions(rows, body.answers)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from None
    attempt = QuizAttempt(user_id=user.id, course_id=course_id,
                          answers={str(k): v for k,v in body.answers.items()},
                          score=result["score"], total=result["total"])
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, **result}

@router.get("/courses/{course_id}/attempts")
def attempts(course_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    eligible(db, user, course_id)
    rows = db.scalars(select(QuizAttempt).where(
        QuizAttempt.user_id == user.id, QuizAttempt.course_id == course_id)
        .order_by(QuizAttempt.submitted_at.desc(), QuizAttempt.id.desc()).limit(20)).all()
    return {"attempts": [{"id": a.id, "score": a.score, "total": a.total,
                           "percentage": round(100 * a.score / a.total) if a.total else 0,
                           "submitted_at": a.submitted_at.isoformat()} for a in rows]}

