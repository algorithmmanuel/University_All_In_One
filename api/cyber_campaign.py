"""Derived campaign guidance; no mutable achievements or client-awarded credit.

Strategies remain freely playable. Read markers are not comprehension checks,
practice coverage is a bounded activity sample, and simulation wins are not mastery.
"""
from sqlalchemy import select, func
from models import StrategyRun
from cyber_content import BANK
from strategy_scenarios import SCENARIOS

CHAPTERS = (
    ('branch', 'protect', 'Establish the defences'),
    ('supplier', 'defend', 'Control connected access'),
    ('ransomware', 'recover', 'Restore a trusted service'),
)


def campaign_progress(db, user_id, completed, graded_rows):
    """Aggregate all saved strategy outcomes; use at most 50 graded practice rows."""
    scenario = func.coalesce(StrategyRun.state['scenario'].as_string(), 'branch')
    status = StrategyRun.state['status'].as_string()
    groups = db.execute(select(scenario, status, func.count(), func.max(StrategyRun.id))
        .where(StrategyRun.user_id == user_id).group_by(scenario, status)).all()
    outcomes = {(s, state): (count, last_id) for s, state, count, last_id in groups}
    # A distinct question only counts once even when it was submitted repeatedly.
    question_modules = {q['id']: q['module'] for q in BANK}
    attempted = {item['id'] for row in graded_rows for item in (row.result or {}).get('feedback', [])
                 if item['id'] in question_modules}
    chapters = []
    for scenario_id, module_id, title in CHAPTERS:
        wins = outcomes.get((scenario_id, 'won'), (0, None))[0]
        active = outcomes.get((scenario_id, 'active'), (0, None))
        count = sum(question_modules[qid] == module_id for qid in attempted)
        read = module_id in completed
        if not read:
            next_step = {'kind': 'learn', 'module': module_id, 'label': 'Read the supporting module'}
        elif count < 5:
            next_step = {'kind': 'practice', 'module': module_id, 'label': 'Practise a supporting topic'}
        elif not wins:
            next_step = {'kind': 'play', 'scenario': scenario_id, 'run_id': active[1],
                         'label': 'Resume this scenario' if active[1] else 'Try this scenario'}
        else:
            next_step = {'kind': 'play', 'scenario': scenario_id, 'run_id': active[1],
                         'label': 'Compare another strategy'}
        chapters.append({'scenario': scenario_id, 'module': module_id, 'title': title,
            'scenario_title': SCENARIOS[scenario_id]['title'], 'module_read': read,
            'practice_distinct': count, 'practice_target': 5, 'wins': wins,
            'active_runs': active[0], 'resume_id': active[1],
            'milestones_met': read and count >= 5 and wins > 0, 'next': next_step})
    return {'chapters': chapters, 'completed': sum(c['milestones_met'] for c in chapters),
            'total': len(chapters), 'practice_window': 50,
            'notice': 'Activity milestones: current-edition modules marked read, distinct questions in up to 50 recent submitted practice sessions, and saved scenario wins. These are not proof of mastery. All scenarios remain available.'}
