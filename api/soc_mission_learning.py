"""Midnight Login Alerts guidance v1; all logs and accounts are fictional.

Teach triage and proportionality without executing containment, contacting an
account owner, deleting logs or querying a live network.
"""
MISSION_ID = 'soc-alert-triage'
REVISION = 'midnight-login-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'You are a trainee security analyst reviewing a fictional privileged-account alert.',
    'objectives': [
        'Prioritise a suspicious sign-in pattern without calling an unverified alert a confirmed breach.',
        'Correlate sign-in, device and later activity evidence before deciding what happened.',
        'Escalate confirmed suspicious activity under the incident plan while preserving evidence.',
    ],
    'workflow': [
        'Read the stage task and inspect each fictional alert or activity record.',
        'Choose the finding that matters most to the stage’s investigation question.',
        'Choose a defensive response and commit the decision to see the reasoning.',
        'Complete all three stages to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed stage decisions save the mission result. Review is separate, repeatable practice that does not change that score.',
}
STAGES = [
    {
        'task': 'Set the priority for failed sign-ins followed by a privileged success, while separating suspicion from confirmation.',
        'hints': [
            'Look at the sequence rather than dismissing failures in isolation.',
            'A successful sign-in after many failures deserves prompt validation. Legitimate mistakes can also generate alerts.',
        ],
        'artifacts': [
            {'title': 'Failure summary', 'body': '00:36–00:42: the fictional admin.ops account has 37 unsuccessful sign-ins. Repeated failures can reflect attempted guessing or a legitimate problem. The count alone does not establish who attempted access.'},
            {'title': 'Successful sign-in', 'body': '00:42: a successful privileged sign-in follows the failures. Correlate account, time, source, device and later activity, then verify through a trusted owner/support channel. The sequence makes this a prompt investigation, not automatic proof of a breach.'},
        ],
    },
    {
        'task': 'Choose evidence that can validate the sign-in and explain what the account did afterward.',
        'hints': [
            'Correlate records that describe the same account and time window.',
            'An unfamiliar device or unusual location needs context. Compare logs and follow-on actions, not just the user’s job title.',
        ],
        'artifacts': [
            {'title': 'Unrecognised device', 'body': 'The sign-in’s device is not recognised in the available approved-device records. Compare the event with inventory, the account owner’s expected access and actions after sign-in. An unknown device is an important validation lead, not by itself conclusive attribution.'},
            {'title': 'Location context', 'body': 'The event shows an unexpected location. Travel, network routing or a VPN may affect location signals, so location alone does not prove compromise. Review it with sign-in logs, device information and subsequent privileged actions. Preserve the source records.'},
        ],
    },
    {
        'task': 'Respond to confirmed unusual administrative activity using the incident plan and preserve the investigation record.',
        'hints': [
            'The scenario now confirms suspicious activity; earlier uncertainty does not justify ignoring this new evidence.',
            'Escalation and authorised, proportionate containment should retain logs rather than disable monitoring.',
        ],
        'artifacts': [
            {'title': 'Validated activity report', 'body': 'The response team confirms unusual administrative activity associated with the suspect session. Escalate using the incident procedure, preserve sign-in and action logs, and coordinate authorised containment such as session revocation where appropriate. Keep monitoring active. Record what is known and unknown; do not declare zero impact merely because available logs show no extraction.'},
        ],
    },
]
FINDING_EXPLANATIONS = [
    'The successful privileged sign-in after the failures changes the priority: possible access now needs prompt validation. Failed attempts alone do not establish a successful compromise.',
    'The unrecognised device is a direct lead to correlate with account, sign-in and subsequent activity records. Unexpected location adds context, but neither location nor a job title settles legitimacy.',
    'Confirmed unusual privileged activity warrants incident escalation and proportionate authorised containment. Preserve evidence and monitoring so the team can assess scope and recovery.',
]
REVIEW = [
    {'id': 'alert-priority', 'prompt': 'Why investigate a privileged success following 37 failures promptly?',
     'options': ['The failure count proves data theft', 'The success may indicate access and needs validation alongside the failures', 'Every login alert can be dismissed'], 'answer': 1,
     'feedback': ['Failures do not prove theft. Check whether access occurred and what followed.', 'Correct. The sequence raises concern about access; validate it without claiming a confirmed breach from the alert alone.', 'Dismissing the sequence skips a potentially important access event.']},
    {'id': 'correlation-scope', 'prompt': 'Which evidence set best helps validate the suspicious sign-in?',
     'options': ['Only the account owner’s job title', 'Only a screenshot of the alert colour', 'Related sign-in records, device details and subsequent account actions'], 'answer': 2,
     'feedback': ['A job title does not establish whether this event was legitimate.', 'An alert’s presentation is not sufficient investigation evidence.', 'Correct. Related records provide context about access, device and follow-on behaviour.']},
    {'id': 'location-limit', 'prompt': 'An alert shows an unexpected location. What is a defensible interpretation?',
     'options': ['Check it with device and activity evidence because routing, travel or VPNs may affect it', 'Treat the location alone as proof of a breach', 'Delete the event because location is never useful'], 'answer': 0,
     'feedback': ['Correct. Location is a signal to investigate in context, not conclusive attribution.', 'One location signal is insufficient proof. Correlate it with other records.', 'Location can add context; preserve the event and investigate it.']},
    {'id': 'confirmed-response', 'prompt': 'The team confirms unusual administrative activity. Which next action fits the mission?',
     'options': ['Disable monitoring to silence alerts', 'Follow incident procedures, preserve logs and coordinate authorised containment', 'Erase the evidence before escalation'], 'answer': 1,
     'feedback': ['Monitoring helps track scope and recurrence; disabling it removes visibility.', 'Correct. Coordinate the response under the plan and retain evidence for investigation.', 'Erasing logs prevents investigation and accountability. Preserve them.']},
    {'id': 'impact-evidence', 'prompt': 'Available logs do not confirm data extraction. What should the analyst report?',
     'options': ['There was certainly zero impact', 'The incident needs no further review', 'State the evidence and its limits, and continue the approved scope assessment'], 'answer': 2,
     'feedback': ['A lack of confirmed extraction is not proof of no impact.', 'The scope still needs assessment; incomplete evidence does not close the incident.', 'Correct. Distinguish what the records show from what remains unknown.']},
]
