"""Operation Firewall v1: fictional bank identity investigation and follow-up.

No bank service, real account or session is queried or contained by the lesson.
"""
MISSION_ID = 'operation-firewall'
REVISION = 'operation-firewall-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional bank response team validate a privileged session and document proportionate follow-up.',
    'objectives': [
        'Validate a suspicious successful sign-in without prematurely dismissing or broadly disrupting services.',
        'Use device and privileged-action evidence to recommend authorised containment.',
        'Distinguish confirmed containment from established impact and document what remains unknown.',
    ],
    'workflow': [
        'Read the stage task and inspect every fictional sign-in or response record.',
        'Choose the finding most relevant to the current response decision.',
        'Commit a defensive recommendation and read its explanation.',
        'Complete three decisions to save the mission result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save your result. Optional review is separate practice with no saved grade or score change.',
}
STAGES = [
    {'task': 'Validate the successful privileged sign-in following repeated failures before deciding the response scope.',
     'hints': ['The success after the failures is important, but the alert alone does not identify who performed it.', 'Correlate the events and verify with the owner through a trusted route; do not delete evidence or shut down every service without justification.'],
     'artifacts': [
         {'title': 'Failure burst', 'body': 'The fictional monitoring record shows 42 failed sign-ins in six minutes. Preserve and correlate the account, time, source and related events. A high failure count alone does not prove successful access.'},
         {'title': 'Privileged success', 'body': 'A successful privileged sign-in occurs at 02:14 after the failures. Validate promptly using related logs and trusted owner verification. Do not ask the suspect session or an unverified new contact to establish its own legitimacy.'},
         {'title': 'Routine backup', 'body': 'A nightly backup completed normally. It may matter to later recovery planning, but it does not authenticate the privileged sign-in or justify dismissing the alert. Broad shutdown requires an evidence-based response decision, not the alert alone.'},
     ]},
    {'task': 'Recommend proportionate containment when an unfamiliar device reaches a privileged configuration screen.',
     'hints': ['Compare the device and action records, not unrelated healthy equipment.', 'MFA status alone does not establish that this session is legitimate; follow the approved escalation and containment plan.'],
     'artifacts': [
         {'title': 'Unapproved device', 'body': 'The fictional session’s device is absent from the available approved inventory. Validate inventory context and correlate the access; the unfamiliar device is a direct investigation lead, not conclusive attribution by itself.'},
         {'title': 'Printer status', 'body': 'An office printer is online. That healthy device is not evidence that the privileged session was authorised. Separate relevant observations from background activity.'},
         {'title': 'Privileged screen access', 'body': 'The unfamiliar device’s session accessed a privileged configuration screen. Recommend escalation and authorised, proportionate containment of the suspect access under the response plan while retaining logs. MFA being enabled is not a reason to ignore contradictory session evidence.'},
     ]},
    {'task': 'Document the revoked session and remaining impact uncertainty before completing this response stage.',
     'hints': ['Stopping a session and proving no harmful activity occurred are different conclusions.', 'Record available evidence and its limits, monitor for recurrence and review affected controls rather than promise zero impact.'],
     'artifacts': [
         {'title': 'Revocation record', 'body': 'The response team confirms the suspect session was revoked. Document the action and continue to assess related access and activity. Revocation does not retroactively prove that no impact occurred.'},
         {'title': 'Unverified rumour', 'body': 'A fictional social-media rumour alleges a large breach. Do not present it as a confirmed finding or publish unverified details. Follow approved incident communications and distinguish the rumour from evidence.'},
         {'title': 'Impact evidence limit', 'body': 'Available logs do not confirm data extraction. This is not proof of zero impact or proof that all relevant activity was logged. Document what is established and unknown, assess the affected scope, monitor recurrence and review the relevant controls.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The successful privileged event after the failure burst is the access event needing validation. A routine backup does not establish its legitimacy; correlate and verify before choosing a wider response.',
    'The unapproved device is a direct lead linked to privileged access. Correlate it with the action evidence and recommend authorised containment, rather than rely on MFA status or unrelated printer health.',
    'No confirmed extraction in the available logs is an evidence limit, not proof of zero impact. Record containment, continue scoped assessment and monitoring, and review affected controls.',
]
REVIEW = [
    {'id': 'firewall-validate', 'prompt': 'What does a privileged success after 42 failures justify first in Operation Firewall?',
     'options': ['Deleting the alert as a false positive', 'Prompt correlation and trusted owner verification', 'An automatic shutdown of every bank service'], 'answer': 1,
     'feedback': ['The success remains unexplained; deleting the alert removes useful evidence.', 'Correct. Establish whether the access was authorised before choosing the full response scope.', 'A blanket shutdown without validation may be disproportionate.']},
    {'id': 'firewall-background', 'prompt': 'Why does the completed nightly backup not settle the suspicious login?',
     'options': ['Backups prove the identity of every user', 'Any normal event cancels an alert', 'Recovery readiness and sign-in legitimacy are different questions'], 'answer': 2,
     'feedback': ['A backup does not authenticate a user or session.', 'Normal background activity does not cancel contradictory access evidence.', 'Correct. Keep the observations relevant to the decision being made.']},
    {'id': 'firewall-mfa-context', 'prompt': 'MFA is enabled, but an unfamiliar device reaches privileged configuration. Which interpretation is sound?',
     'options': ['Correlate the evidence and follow the response plan; MFA alone does not prove legitimacy', 'Ignore the access because MFA exists', 'Turn off logging to reduce noise'], 'answer': 0,
     'feedback': ['Correct. Evaluate the actual session and action evidence, not only the presence of a control.', 'A configured control does not independently validate every event.', 'Logging is needed to assess scope and support the response.']},
    {'id': 'firewall-containment-limit', 'prompt': 'The team has revoked the suspect session. What does that establish?',
     'options': ['No harmful action could have happened earlier', 'That containment action was confirmed; prior impact still requires assessment', 'All other accounts and sessions are certainly safe'], 'answer': 1,
     'feedback': ['Revocation does not erase or explain earlier activity.', 'Correct. Separate a confirmed response action from the remaining impact and scope questions.', 'One revoked session does not establish the state of every other access route.']},
    {'id': 'firewall-report-evidence', 'prompt': 'A breach rumour appears, but available logs do not confirm extraction. What belongs in the response record?',
     'options': ['The rumour as proven fact', 'A guarantee of zero impact', 'Verified findings, evidence limits and the planned follow-up'], 'answer': 2,
     'feedback': ['An unverified rumour is not a confirmed finding.', 'No confirmed extraction is not proof that no impact occurred.', 'Correct. Communicate through approved channels and keep uncertainty explicit while assessing scope.']},
]
