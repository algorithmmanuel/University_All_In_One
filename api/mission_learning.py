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
import mfa_mission_learning
import backup_mission_learning
import firewall_mission_learning
import network_mission_learning
import web_mission_learning
import cloud_mission_learning
import forensics_mission_learning
import malware_mission_learning
import identity_mission_learning
import delivery_mission_learning
import hunt_mission_learning
import response_mission_learning
import risk_mission_learning
import zerotrust_mission_learning
import cloud_command_mission_learning
import supplier_mission_learning
import recovery_command_mission_learning
import privileged_mission_learning
import board_mission_learning
import ai_mission_learning
import audit_mission_learning

GUIDES = {
    guide.MISSION_ID: guide for guide in (
        scholarship_mission_learning, account_mission_learning, soc_mission_learning,
        privacy_mission_learning, scam_mission_learning, social_mission_learning,
        device_mission_learning, wifi_mission_learning, footprint_mission_learning,
        mfa_mission_learning, backup_mission_learning, firewall_mission_learning,
        network_mission_learning, web_mission_learning, cloud_mission_learning,
        forensics_mission_learning, malware_mission_learning, identity_mission_learning,
        delivery_mission_learning, hunt_mission_learning, response_mission_learning,
        risk_mission_learning, zerotrust_mission_learning, cloud_command_mission_learning,
        supplier_mission_learning, recovery_command_mission_learning, privileged_mission_learning,
        board_mission_learning, ai_mission_learning, audit_mission_learning
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
