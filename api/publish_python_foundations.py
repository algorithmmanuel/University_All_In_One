"""Preview/apply Python foundations only through the guarded development launcher.

The transaction preserves course/lesson IDs, learner completion and old quiz rows.
No automatic startup migration or destructive replacement of assessment history.
"""
import argparse
import os
import sys
from sqlalchemy import select, text
from development_runtime import validate_development_database
from models import Course, Lesson, QuizQuestion
from python_foundations import ACADEMY_ID, COURSE_TITLE, LESSONS, MARKER, QUESTIONS


def publish(db, *, apply=False):
    """Validate the complete release before changing any content; caller owns commit."""
    courses = db.scalars(select(Course).where(
        Course.academy_id == ACADEMY_ID, Course.title == COURSE_TITLE).with_for_update()).all()
    if len(courses) != 1:
        raise ValueError('Expected one seeded Python course; run the development seeds first')
    course = courses[0]
    if course.status != 'published':
        raise ValueError('Expected the published demonstration course')
    rows = db.scalars(select(Lesson).where(Lesson.course_id == course.id).with_for_update()).all()
    matched = []
    for item in LESSONS:
        existing = [row for row in rows if row.title == item['title']]
        if len(existing) != 1 or existing[0].content not in (item['legacy_content'], MARKER + item['key']):
            raise ValueError('Lesson missing, duplicated or customized; refusing to overwrite it')
        matched.append((existing[0], item))
    bank = db.scalars(select(QuizQuestion).where(QuizQuestion.course_id == course.id)).all()
    planned = []
    for position, (_, prompt, options, answer, explanation) in enumerate(QUESTIONS, 1):
        existing = [row for row in bank if row.prompt == prompt]
        if len(existing) > 1 or (existing and (existing[0].options != options or
                existing[0].correct_index != answer or existing[0].explanation != explanation)):
            raise ValueError('Conflicting question content; refusing to rewrite historical answer keys')
        if not existing:
            planned.append(QuizQuestion(course_id=course.id, prompt=prompt, options=options,
                                       correct_index=answer, explanation=explanation, position=position))
    if apply:
        for row, item in matched:
            row.content = MARKER + item['key']
        db.add_all(planned)
    return {'lessons': len(matched), 'new_questions': len(planned), 'active_questions': len(QUESTIONS),
            'applied': apply}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    validate_development_database(os.getenv('DATABASE_URL', ''))
    if os.getenv('EDUCYBER_LOCAL_DEVELOPMENT') != 'enabled':
        raise ValueError('Use the isolated development launcher')
    from database import SessionLocal
    with SessionLocal() as db:
        if db.scalar(text('SELECT current_database()')) != 'educyber_dev':
            raise ValueError('Unexpected database identity')
        result = publish(db, apply=args.apply)
        if args.apply:
            db.commit()
        else:
            db.rollback()
    print(('APPLIED' if args.apply else 'PREVIEW ONLY') +
          ': 3 Python lessons, 6 guided checks, 20 aligned questions; ' +
          str(result['new_questions']) + ' new question rows. Existing learner records retained.')


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        # Only our fixed validation messages are displayed; no input/URL values.
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from None
    except Exception as error:
        print('Content publication stopped (' + type(error).__name__ +
              '). Verify development configuration and schema readiness.', file=sys.stderr)
        raise SystemExit(1) from None
