"""Threat Hunter v1: fictional hypotheses, task provenance and response records.

No DNS query, scheduled task execution or live host investigation runs here.
"""
MISSION_ID = 'threat-hunter'
REVISION = 'threat-hunter-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional hunt team move from a recurring DNS pattern to a tested explanation and scoped defensive response.',
    'objectives': [
        'Form a testable hypothesis from unusual DNS activity without declaring a breach from novelty alone.',
        'Validate scheduled-task provenance and related endpoint activity without executing an unknown task.',
        'Turn confirmed findings and known scope into an owned response and tested detection improvement.',
    ],
    'workflow': [
        'Read the hunt task and inspect each fictional DNS, process or outcome record.',
        'Choose the finding most useful for the current hypothesis or response decision.',
        'Commit a defensive next step and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review is ungraded practice with no change to the saved score.',
}
STAGES = [
    {'task': 'Turn periodic DNS activity into a testable hypothesis rather than a premature breach declaration.',
     'hints': ['A regular interval and a newly registered domain are clues, not a complete verdict.', 'State an explanation you can test with related endpoint events, and consider legitimate alternatives while preserving the records.'],
     'artifacts': [
         {'title': 'Minute-by-minute queries', 'body': 'Fictional DNS queries repeat every minute. Form a testable hypothesis about what process or task could cause the pattern and correlate related endpoint events. Regular activity can come from legitimate services too.'},
         {'title': 'New domain context', 'body': 'The domain was registered recently in the case evidence. Newness adds context to investigate, not proof of malicious ownership or behaviour. The exercise supplies no live domain to query.'},
         {'title': 'Three managed endpoints', 'body': 'The pattern is present on three managed endpoints. Compare expected software, processes and timing across them. Managed status does not establish that every task is authorised; retain DNS and host evidence for validation.'},
     ]},
    {'task': 'Validate an unfamiliar scheduled task linked to the queries without running it on a live server.',
     'hints': ['The task’s creation time is a lead for correlation, not by itself proof of who created it or why.', 'Check provenance, approval, expected software and related host events; do not execute the unknown task to see what happens.'],
     'artifacts': [
         {'title': 'Task creation timing', 'body': 'A fictional task was created shortly before the first observed DNS query. Check time context and related host events to test the link. Timing alone does not establish causation, so validate task provenance and activity.'},
         {'title': 'Service account context', 'body': 'The task runs under a service account. That can describe a legitimate operating pattern or inappropriate use; the account label alone does not prove authorisation. Review the intended purpose, approved ownership and relevant activity.'},
         {'title': 'Inventory mismatch', 'body': 'The available endpoint inventory has no matching approved software. Confirm inventory context and the task’s expected origin rather than simply ignore the discrepancy. Do not run the unknown task on a live server as a test.'},
     ]},
    {'task': 'Respond to the confirmed unauthorised task and preserve what the hunt established and did not establish.',
     'hints': ['The case has moved from an unexplained signal to a confirmed unauthorised task with identified hosts.', 'Assign response ownership, preserve evidence, contain through the plan and test detections; the current host list is not a guarantee about unexamined systems.'],
     'artifacts': [
         {'title': 'Identified affected hosts', 'body': 'The fictional hunt confirms the task is unauthorised and identifies three affected hosts. Escalate and coordinate containment under the response plan. State this as the known affected scope and record any remaining checks, not proof that no other host could be affected.'},
         {'title': 'Preserved hunt evidence', 'body': 'Relevant DNS, task and endpoint evidence is retained. Document the hypothesis, checks, findings and limits so another team can review the conclusion. Do not stop without a record or disable telemetry that can reveal recurrence.'},
         {'title': 'Response and detection owners', 'body': 'Containment owners are assigned. Coordinate their actions and convert the validated findings into detection improvements with appropriate tests and review. Confirm actions completed and monitor for recurrence rather than assume assigning a name finishes the response.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The repeating DNS pattern provides a testable lead. Correlate it with endpoints and expected behaviour rather than treat regularity or a new domain as proof of a breach.',
    'Task creation before the observed queries is a useful pivot to validate with provenance and related activity. Service-account execution or inventory absence alone does not establish the full explanation.',
    'The three identified affected hosts provide an actionable known scope for response. Preserve the hunt record, coordinate assigned owners and build tested detections without assuming every unexamined system is safe.',
]
REVIEW = [
    {'id': 'hunt-testable', 'prompt': 'What makes a response to minute-by-minute DNS queries a useful hunt step?',
     'options': ['Declaring a breach because repetition exists', 'Forming an explanation that can be tested against related endpoint evidence', 'Deleting the queries to remove noise'], 'answer': 1,
     'feedback': ['Periodic activity can have legitimate causes and needs validation.', 'Correct. A hypothesis should lead to evidence that can support or challenge it.', 'Deleting records prevents useful comparison and validation.']},
    {'id': 'hunt-domain-newness', 'prompt': 'A queried domain was registered recently. What does that fact establish on its own?',
     'options': ['Confirmed malicious behaviour', 'That every related process is authorised', 'Context to investigate, rather than a complete trust verdict'], 'answer': 2,
     'feedback': ['Domain age alone does not prove malicious activity.', 'A domain’s age does not authorise the endpoint process using it.', 'Correct. Evaluate the signal with process, task and other relevant evidence.']},
    {'id': 'hunt-task-provenance', 'prompt': 'An unfamiliar scheduled task precedes the DNS activity. Which next step fits the case?',
     'options': ['Review provenance and related host events without running the unknown task on a live server', 'Execute it on a live server to test it', 'Assume the service-account label proves approval'], 'answer': 0,
     'feedback': ['Correct. Validate source, expected purpose and related activity while preserving evidence.', 'Running the unknown task could create exposure instead of safely validating it.', 'An account label does not establish why a task was created or whether it was approved.']},
    {'id': 'hunt-known-scope', 'prompt': 'Three affected hosts are confirmed. Which scope statement is defensible?',
     'options': ['Every other host is certainly safe', 'Three are established so far, with remaining checks and limits recorded', 'Known scope should not be documented'], 'answer': 1,
     'feedback': ['Current findings do not settle the state of unexamined systems.', 'Correct. Separate established scope from assumptions and follow-up.', 'The response needs a clear record of what was found.']},
    {'id': 'hunt-follow-through', 'prompt': 'What should follow a confirmed unauthorised task and assigned containment owners?',
     'options': ['Stop because assigning owners completes the response', 'Disable the telemetry that found it', 'Verify response actions and use the documented findings for tested detection improvements'], 'answer': 2,
     'feedback': ['Ownership needs completed actions and verification.', 'Telemetry can support scope assessment and recurrence monitoring.', 'Correct. Follow through on containment and translate validated learning into reviewed defensive coverage.']},
]
