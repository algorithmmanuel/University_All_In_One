"""Authenticated course enrollment and persistent lesson completion."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from learning_content import guide_for, public_guide
from learning_overview import overview
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from auth import current_user
from db_dependencies import get_db
from models import Academy, Course, Enrollment, LearnerProgress, Lesson, User

router = APIRouter(prefix="/api/v1", tags=["learning"])

def student_only(user: User = Depends(current_user)) -> User:
    if user.role != "student":
        raise HTTPException(status_code=403, detail="Student account required")
    return user

def course_payload(course: Course):
    return {"id": course.id, "academy_id": course.academy_id,
            "title": course.title, "description": course.description}

def course_access(db: Session, user: User, course_id: int) -> Course:
    course = db.get(Course, course_id)
    if course is None or course.status != "published":
        raise HTTPException(status_code=404, detail="Course not found")
    if db.scalar(select(Enrollment.id).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id)) is None:
        raise HTTPException(status_code=403, detail="Enroll in this course first")
    return course

@router.get("/learning/catalog")
def catalog(academy_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Course).where(Course.status == "published")
    if academy_id:
        stmt = stmt.where(Course.academy_id == academy_id)
    courses = db.scalars(stmt.order_by(Course.id)).all()
    return {"courses": [dict(course_payload(c), lesson_count=db.scalar(
        select(func.count(Lesson.id)).where(Lesson.course_id == c.id))) for c in courses]}

@router.post("/learning/enrollments/{course_id}", status_code=201)
def enroll(course_id: int, user: User = Depends(student_only), db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None or course.status != "published":
        raise HTTPException(status_code=404, detail="Course not found")
    existing = db.scalar(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course_id))
    if existing:
        return {"message": "Already enrolled", "course_id": course_id}
    db.add(Enrollment(user_id=user.id, course_id=course_id))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"message": "Already enrolled", "course_id": course_id}
    return {"message": "Enrolled", "course_id": course_id}

@router.get('/learning/overview')
def learning_overview(user: User = Depends(student_only), db: Session = Depends(get_db)):
    return overview(db, user.id)


@router.get("/learning/enrollments")
def my_enrollments(user: User = Depends(student_only), db: Session = Depends(get_db)):
    rows = db.execute(select(Enrollment, Course).join(Course, Enrollment.course_id == Course.id)
                      .where(Enrollment.user_id == user.id).order_by(Enrollment.enrolled_at.desc())).all()
    output = []
    for enrollment, course in rows:
        total = db.scalar(select(func.count(Lesson.id)).where(Lesson.course_id == course.id))
        completed = db.scalar(select(func.count(LearnerProgress.id)).join(
            Lesson, LearnerProgress.lesson_id == Lesson.id).where(
            Lesson.course_id == course.id, LearnerProgress.learner_id == str(user.id)))
        output.append(dict(course_payload(course), enrolled_at=enrollment.enrolled_at.isoformat(),
                           total_lessons=total, completed_lessons=completed,
                           progress_percent=round(100 * completed / total) if total else 0))
    return {"enrollments": output}

@router.get("/learning/courses/{course_id}/lessons")
def lessons(course_id: int, user: User = Depends(student_only), db: Session = Depends(get_db)):
    course = course_access(db, user, course_id)
    rows = db.scalars(select(Lesson).where(Lesson.course_id == course.id).order_by(Lesson.position, Lesson.id)).all()
    completed = set(db.scalars(select(LearnerProgress.lesson_id).where(
        LearnerProgress.learner_id == str(user.id), LearnerProgress.lesson_id.in_([l.id for l in rows]))).all()) if rows else set()
    return {"course": course_payload(course), "lessons": [
        lesson_payload(course, lesson, lesson.id in completed) for lesson in rows]}


def lesson_payload(course, lesson, completed):
    """Keep a plain text fallback for API consumers that do not render guides."""
    guide = guide_for(course, lesson)
    content = "\n\n".join(section["body"] for section in guide["sections"]) if guide else lesson.content
    return {"id": lesson.id, "title": lesson.title, "content": content,
            "learning_guide": public_guide(guide) if guide else None,
            "position": lesson.position, "completed": completed}

@router.post("/learning/lessons/{lesson_id}/complete")
def complete(lesson_id: int, user: User = Depends(student_only), db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    course_access(db, user, lesson.course_id)
    existing = db.scalar(select(LearnerProgress.id).where(
        LearnerProgress.learner_id == str(user.id), LearnerProgress.lesson_id == lesson_id))
    if existing is None:
        db.add(LearnerProgress(learner_id=str(user.id), lesson_id=lesson_id))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    return {"lesson_id": lesson_id, "completed": True}


class PracticeAnswer(BaseModel):
    model_config = ConfigDict(extra='forbid')
    exercise_id: str = Field(min_length=1, max_length=60)
    option_index: StrictInt = Field(ge=0, le=9)


@router.post('/learning/lessons/{lesson_id}/practice')
def practice(lesson_id: int, body: PracticeAnswer, user: User = Depends(student_only),
             db: Session = Depends(get_db)):
    """Low-stakes feedback only: no saved grade or automatic lesson completion."""
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail='Lesson not found')
    course = course_access(db, user, lesson.course_id)
    guide = guide_for(course, lesson)
    exercise = next((item for item in guide['exercises'] if item['id'] == body.exercise_id), None) if guide else None
    if exercise is None:
        raise HTTPException(status_code=404, detail='Practice check not found')
    if body.option_index >= len(exercise['options']):
        raise HTTPException(status_code=422, detail='Choose one of the available answers')
    return {'exercise_id': exercise['id'], 'correct': body.option_index == exercise['answer'],
            'explanation': exercise['feedback'][body.option_index]}
