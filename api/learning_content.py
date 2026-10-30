"""Resolve explicitly published curriculum markers; unknown content stays plain text.

No HTML, interpreter or user-selected module loading is involved. All expected
lesson markers must match before the course switches to a curated assessment bank.
"""
from sqlalchemy import select
from models import Course, Lesson
from curriculum_registry import release_for


def guide_for(course, lesson):
    release = release_for(course)
    if release is None:
        return None
    item = next((item for item in release.LESSONS if lesson.title == item['title']
                 and lesson.content == release.MARKER + item['key']), None)
    return {**item, 'revision': release.REVISION} if item else None


def public_guide(guide):
    """Keep practice answer keys and assessment answers out of lesson responses."""
    return {'revision': guide['revision'], 'objectives': guide['objectives'],
            'sections': guide['sections'], 'exercises': [
                {key: exercise[key] for key in ('id', 'objective', 'prompt', 'options', 'code') if key in exercise}
                for exercise in guide['exercises']]}


def active_question_prompts(db, course_id):
    course = db.get(Course, course_id)
    release = release_for(course) if course else None
    if release is None:
        return None
    rows = db.scalars(select(Lesson).where(Lesson.course_id == course_id)).all()
    # Retain historic questions, but activate only the bank whose teaching release
    # was published in full. Partial/foreign markers never activate another bank.
    if not all(sum(row.title == item['title'] and row.content == release.MARKER + item['key']
                   for row in rows) == 1 for item in release.LESSONS):
        return None
    return [item[1] for item in release.QUESTIONS]
