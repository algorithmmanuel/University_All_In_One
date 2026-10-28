"""Versioned, server-authored evidence for one practice attempt, never a diagnosis.

Only fully published, exactly matching reviewed items receive objective credit.
Snapshots keep their original wording and grading when the catalogue changes.
Repeated attempts are deliberately not combined into independent evidence.
"""
from curriculum_registry import release_for
from learning_content import active_question_prompts
from models import Course, Lesson
from sqlalchemy import select

VERSION = 1


def snapshot(db, course_id, rows, result):
    course = db.get(Course, course_id)
    release = release_for(course)
    topics = []
    mapping = {}
    if release and active_question_prompts(db, course_id) is not None:
        lessons = db.scalars(select(Lesson).where(Lesson.course_id == course_id)).all()
        for lesson in release.LESSONS:
            saved = next(row for row in lessons if row.title == lesson['title']
                         and row.content == release.MARKER + lesson['key'])
            for objective in lesson['objectives']:
                topics.append({'objective_id': objective['id'], 'objective': objective['text'],
                               'lesson_id': saved.id, 'lesson_title': saved.title,
                               'correct': 0, 'total': 0})
        for objective, prompt, options, answer, explanation in release.QUESTIONS:
            mapping[prompt] = (objective, options, answer, explanation)
    by_objective = {topic['objective_id']: topic for topic in topics}
    feedback = []
    unmapped = 0
    credited_prompts = set()
    for row, item in zip(rows, result['feedback']):
        match = mapping.get(row.prompt)
        objective = None
        if match and row.prompt not in credited_prompts and (row.options, row.correct_index, row.explanation) == match[1:]:
            credited_prompts.add(row.prompt)
            objective = match[0]
            topic = by_objective[objective]
            topic['total'] += 1
            topic['correct'] += int(item['correct'])
        else:
            unmapped += 1
        feedback.append({**item, 'prompt': row.prompt, 'options': list(row.options),
                         'objective_id': objective})
    for topic in topics:
        total, correct = topic['total'], topic['correct']
        topic['percentage'] = round(100 * correct / total) if total else None
        # One item cannot establish a strength or weakness. Thresholds are
        # transparent practice heuristics, not validated mastery standards.
        topic['status'] = ('not_assessed' if not total else 'limited_evidence' if total < 2
                           else 'strength_in_this_attempt' if correct / total >= .8 else 'revisit')
        topic['recommendation'] = (
            'Study this lesson, then try a longer assessment to sample this objective.' if not total else
            'Review the explanation and lesson, then practise again.' if correct < total else
            'Try a longer assessment or apply this idea in a new example.')
    return {'version': VERSION, 'curriculum_revision': release.REVISION if topics else None,
            'topics': topics, 'unmapped_count': unmapped, 'feedback': feedback,
            'evidence_note': 'One practice attempt, not proof of mastery. Fewer than two questions is limited evidence; '
                             'repeated questions and optional practice are not independent evidence.'}
