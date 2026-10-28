"""Read-only student dashboard projections from owned, published learning data."""
from sqlalchemy import case, func, select
from models import Course, Enrollment, LearnerProgress, Lesson, QuizAttempt


def overview(db, user_id):
    # Aggregate lesson completion without loading answers, snapshots or other learners.
    totals = select(Lesson.course_id, func.count(Lesson.id).label('total')).group_by(Lesson.course_id).subquery()
    done = select(Lesson.course_id, func.count(LearnerProgress.id).label('completed')).join(
        LearnerProgress, LearnerProgress.lesson_id == Lesson.id).where(
        LearnerProgress.learner_id == str(user_id)).group_by(Lesson.course_id).subquery()
    total = func.coalesce(totals.c.total, 0)
    completed = func.coalesce(done.c.completed, 0)
    finished = (total > 0) & (completed == total)
    rows = db.execute(select(Course.id, Course.title, total.label('total'), completed.label('completed'),
                             finished.label('finished')).join(Enrollment, Enrollment.course_id == Course.id)
                      .outerjoin(totals, totals.c.course_id == Course.id)
                      .outerjoin(done, done.c.course_id == Course.id)
                      .where(Enrollment.user_id == user_id, Course.status == 'published')
                      .order_by(case((finished, 1), else_=0), Enrollment.enrolled_at.desc(), Course.id)).all()
    previews = []
    for row in rows[:3]:
        completed_ids = select(LearnerProgress.lesson_id).where(LearnerProgress.learner_id == str(user_id))
        next_lesson = db.execute(select(Lesson.id, Lesson.title).where(
            Lesson.course_id == row.id, Lesson.id.not_in(completed_ids))
            .order_by(Lesson.position, Lesson.id).limit(1)).first()
        previews.append({'id': row.id, 'title': row.title, 'total_lessons': row.total,
                         'completed_lessons': row.completed,
                         'progress_percent': round(100 * row.completed / row.total) if row.total else 0,
                         'completed': bool(row.finished),
                         'next_lesson': {'id': next_lesson.id, 'title': next_lesson.title} if next_lesson else None})
    attempts = db.execute(select(QuizAttempt.id, QuizAttempt.course_id, Course.title,
                                 QuizAttempt.score, QuizAttempt.total, QuizAttempt.submitted_at)
                          .join(Course, Course.id == QuizAttempt.course_id)
                          .join(Enrollment, (Enrollment.course_id == Course.id) & (Enrollment.user_id == user_id))
                          .where(QuizAttempt.user_id == user_id, Course.status == 'published')
                          .order_by(QuizAttempt.submitted_at.desc(), QuizAttempt.id.desc()).limit(3)).all()
    return {'enrolled_count': len(rows), 'completed_courses': sum(bool(row.finished) for row in rows),
            'courses': previews, 'recent_attempts': [
                {'id': row.id, 'course_id': row.course_id, 'course_title': row.title, 'score': row.score,
                 'total': row.total, 'percentage': round(100 * row.score / row.total) if row.total else 0,
                 'submitted_at': row.submitted_at.isoformat()} for row in attempts]}
