"""Identity Crisis v1: fictional privileged-session and exception response.

No real directory, credentials, emergency account or authentication policy is used.
"""
MISSION_ID = 'identity-crisis'
REVISION = 'identity-crisis-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional identity responder validate unusual privileged changes, contain confirmed access and remove a recurring bypass.',
    'objectives': [
        'Validate unexplained privileged changes and invoke approved containment without deleting evidence or assuming authorisation.',
        'Revoke confirmed unauthorised sessions and coordinate credential response while protecting emergency access.',
        'Remove unjustified legacy exceptions and monitor effective privileged authentication and access.',
    ],
    'workflow': [
        'Read the current identity-response task and inspect every fictional change, session or exception record.',
        'Choose the finding most relevant to the current privilege or bypass risk.',
        'Commit a controlled response recommendation and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Optional review is separate practice with no saved grade or change to the score.',
}
STAGES = [
    {'task': 'Validate unusual overnight privilege changes and initiate the approved response while the administrator is unreachable.',
     'hints': ['Missing change evidence and new privilege need investigation; inability to contact the admin does not prove either guilt or legitimacy.', 'Preserve directory/sign-in records and use the authorised privileged-account response rather than erase history or simply assume approval.'],
     'artifacts': [
         {'title': 'Missing change ticket', 'body': 'The fictional team cannot find the expected change ticket for unusual directory-policy changes. Check available approval and change evidence, but do not treat a missing record alone as complete attribution of the activity.'},
         {'title': 'New privileged role', 'body': 'A new privileged role was assigned overnight. Validate the assignment and related policy/sign-in activity and initiate approved privileged-account containment as required. The added privilege is a direct access consequence to assess.'},
         {'title': 'Unreachable administrator', 'body': 'The administrator cannot currently be reached. Use the approved escalation and continuity process rather than assume all activity is authorised or invent an attribution. Retain evidence and document what remains unverified.'},
     ]},
    {'task': 'Contain a confirmed unauthorised privileged session without exposing the separate emergency account.',
     'hints': ['A password change and ending an already authenticated session are distinct controls.', 'Use supported session revocation and coordinated credential replacement, preserve logs and keep emergency access tightly controlled.'],
     'artifacts': [
         {'title': 'Active sessions', 'body': 'The fictional investigation confirms an unauthorised privileged session and detects active sessions. Revoke unauthorised sessions through supported official controls and coordinate affected credential rotation. Do not assume changing a password ends every active session.'},
         {'title': 'Separate emergency account', 'body': 'A separate break-glass account exists for approved emergency access. Protect its credentials and accountable use. Do not share them widely as a shortcut to containment; verify the authorised emergency process if it is needed.'},
         {'title': 'Supported revocation', 'body': 'Session revocation is supported in this scenario. Use it under the response plan, verify the effective containment result and preserve investigation evidence. Waiting for the next audit would leave confirmed unauthorised access unresolved.'},
     ]},
    {'task': 'Remove unnecessary legacy authentication exceptions and verify ongoing privileged-access controls.',
     'hints': ['The immediate session response does not fix the policy path that allowed it.', 'Use owned, approved exception removal with effective MFA/access testing and monitoring rather than keep permanent bypasses.'],
     'artifacts': [
         {'title': 'Unbounded legacy exception', 'body': 'The fictional attacker used a legacy authentication exception that lacked expiry. Review purpose, approval, scope and continued need, and remove unnecessary exceptions through the approved change process. Correcting one session does not remove the underlying bypass.'},
         {'title': 'Privileged MFA enforcement', 'body': 'Privileged MFA enforcement is available in this case. Apply the approved policy, verify effective evaluation and relevant access behaviour, and monitor privileged activity. Merely configuring a requirement is not proof it applies to every intended path.'},
         {'title': 'Accountable review owner', 'body': 'A review owner is assigned. Track remaining justified exceptions, review/expiry conditions and follow-up evidence. Preserve auditing and verify actions completed rather than treat an assigned name as closure.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The new privileged role is the direct access change to validate alongside missing approval and policy/sign-in evidence. An unreachable administrator is uncertainty to manage, not grounds for erasing records or assuming legitimacy.',
    'Confirmed unauthorised active sessions require supported revocation and coordinated credential response. Protect the separate emergency account, retain evidence and verify the result.',
    'Effective privileged MFA enforcement addresses the approved control requirement after removing unnecessary bypasses. Pair it with owned exception review, monitoring and verification rather than rely on configuration alone.',
]
REVIEW = [
    {'id': 'privileged-unreachable', 'prompt': 'An administrator is unreachable during unusual privileged changes. What does that establish?',
     'options': ['Every change is authorised', 'A verification gap requiring approved escalation, evidence preservation and validation', 'Proof identifying who performed the changes'], 'answer': 1,
     'feedback': ['Lack of contact does not establish approval.', 'Correct. Continue through the authorised response and document uncertainty.', 'Unreachability alone does not establish attribution.']},
    {'id': 'privileged-session-vs-secret', 'prompt': 'Why address both active sessions and affected credentials after confirmed unauthorised privileged access?',
     'options': ['Rotating a password always ends every session automatically', 'Existing sessions are irrelevant', 'Credential replacement may not terminate every already authenticated session'], 'answer': 2,
     'feedback': ['Do not assume universal session termination from a password change.', 'An active unauthorised session remains an access path to contain.', 'Correct. Use supported revocation and coordinated replacement, then verify the actual result.']},
    {'id': 'privileged-breakglass', 'prompt': 'How should the separate emergency account be handled during containment?',
     'options': ['Keep credentials protected and use the approved accountable emergency process if needed', 'Share its password with everyone responding', 'Assume separate means it needs no oversight'], 'answer': 0,
     'feedback': ['Correct. Emergency availability must still preserve controlled access and accountability.', 'Broad sharing creates further privileged-access exposure.', 'A separate account still requires protection, authorised use and review.']},
    {'id': 'privileged-bypass-root', 'prompt': 'Why review the legacy authentication exception after revoking the suspect session?',
     'options': ['Session revocation removes every policy exception', 'The bypass path may remain unless its purpose, scope and necessity are corrected', 'Legacy exceptions should always be permanent'], 'answer': 1,
     'feedback': ['A session action does not automatically change policy configuration.', 'Correct. Address the access path as well as the immediate confirmed session.', 'Exceptions need justification and follow-up, not indefinite retention by default.']},
    {'id': 'privileged-effective-policy', 'prompt': 'What demonstrates more than merely configuring a privileged MFA requirement?',
     'options': ['Turning off sign-in logs', 'Assigning an owner but checking nothing', 'Testing effective policy/access behaviour and monitoring exceptions with accountable follow-up'], 'answer': 2,
     'feedback': ['Removing logs weakens visibility into whether the requirement works.', 'Ownership without verification does not show completion.', 'Correct. Verify the intended access result and keep exception oversight active.']},
]
