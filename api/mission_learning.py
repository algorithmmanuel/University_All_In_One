"""Static mission guidance registry and server-owned, ungraded review checks.

Only reviewed source modules can register guides. Requests select the guide from
an owned run's mission ID, never a client-supplied module or answer key. Guidance
is additive: it does not change the mission engine's steps, scoring or history.
"""
import account_mission_learning
import scholarship_mission_learning
import soc_mission_learning
import privacy_mission_learning
import scam_mission_learning
import social_mission_learning
import device_mission_learning
import wifi_mission_learning
import footprint_mission_learning

GUIDES = {
    guide.MISSION_ID: guide for guide in (
        scholarship_mission_learning, account_mission_learning, soc_mission_learning,
        privacy_mission_learning, scam_mission_learning, social_mission_learning,
        device_mission_learning, wifi_mission_learning, footprint_mission_learning
    )
}


def has_learning(mission_id):
    return mission_id in GUIDES


def finding_explanation(mission_id, step_index):
    """Reveal finding reasoning only after the stage decision is committed."""
    guide = GUIDES.get(mission_id)
    return ' '+guide.FINDING_EXPLANATIONS[step_index] if guide else ''


def public_learning(mission_id, step_index, completed):
    guide = GUIDES.get(mission_id)
    if guide is None:
        return None
    return {**guide.BRIEFING, 'stage': None if completed else guide.STAGES[step_index],
            'review': [{key: item[key] for key in ('id', 'prompt', 'options')}
                       for item in guide.REVIEW] if completed else []}


def review_answer(mission_id, question_id, option_index):
    guide = GUIDES.get(mission_id)
    question = next((item for item in guide.REVIEW if item['id'] == question_id), None) if guide else None
    if question is None or not 0 <= option_index < len(question['options']):
        raise ValueError('Unknown review question or option')
    return {'question_id': question_id, 'correct': option_index == question['answer'],
            'explanation': question['feedback'][option_index]}
