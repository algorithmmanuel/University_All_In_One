"""Resolve explicitly published curriculum markers; unknown content stays plain text.

No HTML, Python interpreter or user-controlled module loading is involved. Marker
activation requires the maintained course identity and all expected lessons, so a
partial publish cannot switch the assessment bank to a different curriculum.
"""
from sqlalchemy import select
from models import Course, Lesson
from python_foundations import ACADEMY_ID, COURSE_TITLE, LESSONS, MARKER, QUESTIONS, REVISION


def guide_for(course, lesson):
    if course.academy_id != ACADEMY_ID or course.title != COURSE_TITLE:
        return None
    return next((item for item in LESSONS
                 if lesson.title == item['title'] and lesson.content == MARKER + item['key']), None)


def public_guide(guide):
    """Assessment answers and practice answer keys are never in lesson responses."""
    return {'revision': REVISION, 'objectives': guide['objectives'],
            'sections': guide['sections'], 'exercises': [
                {key: exercise[key] for key in ('id', 'objective', 'prompt', 'options', 'code') if key in exercise}
                for exercise in guide['exercises']]}


def active_question_prompts(db, course_id):
    course = db.get(Course, course_id)
    if course is None or course.academy_id != ACADEMY_ID or course.title != COURSE_TITLE:
        return None
    rows = db.scalars(select(Lesson).where(Lesson.course_id == course_id)).all()
    # Require exactly one current marker for every taught lesson. Preserve old
    # question rows for historical attempts; only the active bank is selected.
    if not all(sum(row.title == item['title'] and row.content == MARKER + item['key']
                   for row in rows) == 1 for item in LESSONS):
        return None
    return [item[1] for item in QUESTIONS]
