"""Preview/apply Cyber Safety and Digital Citizenship through the dev launcher.

All selected courses are preflighted before any row is changed. The caller owns
one commit/rollback transaction. No startup writes, schema migration or deletion
of historic questions, attempts or learner completion is performed.
"""
import argparse
import os
import sys
from sqlalchemy import select, text
from curriculum_registry import RELEASES
from development_runtime import validate_development_database
from models import Course, Lesson, QuizQuestion


class PublicationError(ValueError):
    """Fixed non-secret error suitable for an operator-facing message."""


def _prepare(db, release):
    courses = db.scalars(select(Course).where(
        Course.academy_id == release.ACADEMY_ID,
        Course.title == release.COURSE_TITLE).with_for_update()).all()
    if len(courses) != 1:
        raise PublicationError('Expected one seeded course per release; check the development seeds')
    course = courses[0]
    if course.status != 'published':
        raise PublicationError('Expected the published demonstration course')
    rows = db.scalars(select(Lesson).where(Lesson.course_id == course.id).with_for_update()).all()
    matched = []
    for item in release.LESSONS:
        existing = [row for row in rows if row.title == item['title']]
        if len(existing) != 1 or existing[0].content not in (
                item['legacy_content'], release.MARKER + item['key']):
            raise PublicationError('Lesson missing, duplicated or customized; refusing to overwrite it')
        matched.append((existing[0], release.MARKER + item['key']))
    bank = db.scalars(select(QuizQuestion).where(QuizQuestion.course_id == course.id)).all()
    planned = []
    for position, (_, prompt, options, answer, explanation) in enumerate(release.QUESTIONS, 1):
        existing = [row for row in bank if row.prompt == prompt]
        if len(existing) > 1 or (existing and (
                existing[0].options != options or existing[0].correct_index != answer or
                existing[0].explanation != explanation)):
            raise PublicationError('Conflicting question content; refusing to rewrite historical answer keys')
        if not existing:
            planned.append(QuizQuestion(course_id=course.id, prompt=prompt, options=options,
                                       correct_index=answer, explanation=explanation, position=position))
    return matched, planned


def publish_releases(db, keys=('cyber', 'citizenship'), *, apply=False):
    """Preflight the complete selection, then apply it atomically on caller commit."""
    keys = tuple(keys)
    if not keys or len(set(keys)) != len(keys) or any(key not in RELEASES for key in keys):
        raise PublicationError('Choose distinct known curriculum releases')
    # Fixed lock order prevents two multi-course publishers taking opposite locks.
    selected = [(key, RELEASES[key]) for key in RELEASES if key in keys]
    plans = [(key, release, *_prepare(db, release)) for key, release in selected]
    results = []
    for key, release, matched, planned in plans:
        if apply:
            for lesson, marker in matched:
                lesson.content = marker
            db.add_all(planned)
        results.append({'course': key, 'lessons': len(matched),
                        'guided_checks': sum(len(item['exercises']) for item in release.LESSONS),
                        'new_questions': len(planned), 'active_questions': len(release.QUESTIONS),
                        'applied': apply})
    return {'courses': len(results), 'results': results,
            **{field: sum(result[field] for result in results)
               for field in ('lessons', 'guided_checks', 'new_questions', 'active_questions')},
            'applied': apply}


def run_cli(keys=('cyber', 'citizenship'), description=__doc__):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    validate_development_database(os.getenv('DATABASE_URL', ''))
    if os.getenv('EDUCYBER_LOCAL_DEVELOPMENT') != 'enabled':
        raise PublicationError('Use the isolated development launcher')
    from database import SessionLocal
    with SessionLocal() as db:
        if db.scalar(text('SELECT current_database()')) != 'educyber_dev':
            raise PublicationError('Unexpected database identity')
        result = publish_releases(db, keys, apply=args.apply)
        if args.apply:
            db.commit()
        else:
            db.rollback()
    print(('APPLIED' if args.apply else 'PREVIEW ONLY') + ': ' +
          str(result['courses']) + ' course(s), ' + str(result['lessons']) + ' lessons, ' +
          str(result['guided_checks']) + ' guided checks, ' + str(result['active_questions']) +
          ' aligned questions; ' + str(result['new_questions']) +
          ' new question rows. Existing learner records retained.')


def safe_cli(keys=('cyber', 'citizenship'), description=__doc__):
    try:
        run_cli(keys, description)
        return 0
    except PublicationError as error:
        print(str(error), file=sys.stderr)
    except Exception as error:
        # Do not print driver exceptions, input values or connection strings.
        print('Content publication stopped (' + type(error).__name__ +
              '). Verify development configuration and schema readiness.', file=sys.stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(safe_cli())
