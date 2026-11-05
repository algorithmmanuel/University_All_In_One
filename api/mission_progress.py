"""Owned activity projections, not an assessment of mastery or future readiness."""
from sqlalchemy import func, select
from models import MissionRun
from mission_data import MISSIONS


def decision_recap(run):
    """Use original saved feedback/points; never regrade historical choices."""
    output = []
    for item in run.choices:
        stage = item.get('step')
        if type(stage) is not int or not 0 <= stage < run.step_index:
            continue
        points = item.get('points')
        known = type(points) is int and 0 <= points <= 15
        output.append({'stage': stage + 1, 'points': points if known else None,
                       'feedback': str(item.get('feedback', 'Explanation unavailable for this historical decision.'))[:4000],
                       'next_step': ('Review this saved explanation and the mission briefing before replaying.'
                                     if known and points < 15 else
                                     'Try applying this reasoning to another fictional scenario.' if known else
                                     'Detailed scoring evidence is unavailable; revisit the briefing and optional review.')})
    return output


def progress(db, user_id):
    known_ids = list(MISSIONS)
    latest = select(MissionRun.mission_id, func.max(MissionRun.id).label('id')).where(
        MissionRun.user_id == user_id, MissionRun.mission_id.in_(known_ids)).group_by(MissionRun.mission_id).subquery()
    active_count = db.scalar(select(func.count()).select_from(MissionRun).join(latest, latest.c.id == MissionRun.id)
                             .where(MissionRun.completed_at.is_(None)))
    completed = db.scalar(select(func.count(func.distinct(MissionRun.mission_id))).where(
        MissionRun.user_id == user_id, MissionRun.mission_id.in_(known_ids), MissionRun.completed_at.is_not(None)))
    rows = db.execute(select(MissionRun.id, MissionRun.mission_id, MissionRun.score, MissionRun.step_index,
                             MissionRun.completed_at).join(latest, latest.c.id == MissionRun.id)
                      .order_by(MissionRun.id.desc()).limit(3)).all()
    return {'completed_missions': completed, 'active_missions': active_count, 'available_missions': len(known_ids),
            'recent_missions': [{'run_id': row.id, 'title': MISSIONS[row.mission_id]['title'],
                                 'score': row.score, 'max_score': len(MISSIONS[row.mission_id]['steps']) * 15,
                                 'completed_stages': row.step_index, 'total_stages': len(MISSIONS[row.mission_id]['steps']),
                                 'completed': row.completed_at is not None} for row in rows]}
