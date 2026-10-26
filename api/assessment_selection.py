"""Deterministic, bounded practice selection and server-side grading.

Practice tests are not timed or proctored exams. Sampling spreads questions
across the ordered bank; formal topic balancing needs future objective tags.
"""
MAX_QUESTIONS = 100


def unique_questions(rows):
    """Avoid repeated prompts while preserving the bank's author-defined order."""
    seen = set()
    unique = []
    for row in rows:
        key = ' '.join(row.prompt.casefold().split())
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique


def select_questions(rows, count=None):
    """Recompute the same selection on submit; never trust client-selected IDs.

    Omitting count preserves the legacy full-bank contract. Explicit counts
    select unique prompts and are limited by both bank size and server policy.
    """
    if count is None:
        return rows
    bank = unique_questions(rows)
    if type(count) is not int or not 1 <= count <= min(len(bank), MAX_QUESTIONS):
        raise ValueError('Choose a question count within the available range')
    if count == 1:
        return bank[:1]
    return [bank[index * (len(bank) - 1) // (count - 1)] for index in range(count)]


def grade_questions(rows, answers):
    """Require the entire server-selected set and validate options before grading."""
    if not rows or set(answers) != {row.id for row in rows}:
        raise ValueError('Answer every selected question exactly once')
    if any(type(answers[row.id]) is not int or
           not 0 <= answers[row.id] < len(row.options) for row in rows):
        raise ValueError('Invalid answer option')
    score = sum(answers[row.id] == row.correct_index for row in rows)
    return {
        'score': score, 'total': len(rows),
        'percentage': round(100 * score / len(rows)),
        'feedback': [{
            'question_id': row.id, 'correct_index': row.correct_index,
            'selected_index': answers[row.id],
            'correct': answers[row.id] == row.correct_index,
            'explanation': row.explanation,
        } for row in rows],
    }
