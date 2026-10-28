"""MFA Guardian v1: fictional approvals, recovery codes and device replacement.

No real sign-in, recovery code, phone enrollment or account change is requested.
"""
MISSION_ID = 'mfa-guardian'
REVISION = 'mfa-guardian-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional learner use MFA safely and keep a usable recovery route when changing phones.',
    'objectives': [
        'Deny an approval request that does not match a sign-in you initiated.',
        'Treat recovery codes as account access secrets and store them privately.',
        'Transfer or re-enrol an MFA method using official account procedures before losing access to the old device.',
    ],
    'workflow': [
        'Read the stage task and inspect each fictional sign-in, recovery or device record.',
        'Choose the finding most relevant to the current access decision.',
        'Commit a protective action and read the finding explanation.',
        'Complete three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review is repeatable practice and does not change the saved score.',
}
STAGES = [
    {'task': 'Handle an unexpected approval without authorising someone else’s sign-in.',
     'hints': ['Check whether you actually started the login that this approval is meant to confirm.', 'Deny a request you did not initiate, then review security through the real service rather than a caller’s link.'],
     'artifacts': [
         {'title': 'No initiated sign-in', 'body': 'The fictional learner is not signing in to the service. An approval needs to correspond to an action the learner actually initiated; the arrival of a prompt is not a reason to accept it.'},
         {'title': 'Unexpected approval', 'body': 'A phone prompt asks for sign-in approval unexpectedly. Deny it. Repeated prompts do not become safe through repetition, and approving to stop interruptions could complete an unauthorised login.'},
         {'title': 'Official security page', 'body': 'Open the real service independently to review sign-in activity, active sessions and account protection. Follow its recovery/support guidance if suspicious activity is found. Do not send a one-time code or approve a login because an unsolicited caller asks.'},
     ]},
    {'task': 'Store recovery codes so they remain usable without exposing account access to other people.',
     'hints': ['Think about what someone who obtains a recovery code may be able to do.', 'Keep a protected recovery copy separate from the phone it helps recover, not in a public chat or with an unsolicited helper.'],
     'artifacts': [
         {'title': 'Recovery authority', 'body': 'The fictional service issues one-time recovery codes after MFA setup. Such codes may restore access when the normal method is unavailable. Treat them as access secrets, not harmless reference numbers.'},
         {'title': 'Confidential handling', 'body': 'Do not post recovery codes in a group chat or send them to classmates or callers. A screenshot exposes the codes just as readable text does. No actual code is shown or entered in this exercise.'},
         {'title': 'Protected storage', 'body': 'Use protected private storage and keep a usable recovery route separate from the device it recovers. Follow the service’s instructions about used/replaced codes. Do not assume an old code remains valid after recovery methods are changed.'},
     ]},
    {'task': 'Prepare MFA on a replacement phone before the old phone is unavailable.',
     'hints': ['A new phone does not automatically inherit every authenticator enrollment or device-bound method.', 'Use official transfer or re-enrollment steps, verify the new method works and review old-device access before retiring it.'],
     'artifacts': [
         {'title': 'Old-device dependency', 'body': 'The fictional learner is replacing a phone currently used for MFA. Losing that phone before checking the transfer and recovery process could leave the learner locked out.'},
         {'title': 'Official transfer process', 'body': 'Use the service’s official account settings and guidance to transfer or re-enrol the supported MFA method. Methods differ; do not assume copying an app transfers every account. Confirm that the new method works before retiring the old one.'},
         {'title': 'Trusted settings review', 'body': 'Review enrolled devices, recovery options and sessions in the real service. Remove old-device access where appropriate after verifying replacement access. Avoid permanently disabling MFA as a shortcut; use official recovery or trusted support if already locked out.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The unexpected approval is an authorisation request that does not match the learner’s activity. Deny it and investigate through the real service rather than approve to silence prompts.',
    'Recovery codes can restore account access. That authority is why they require confidential, protected storage and a recovery route independent of the phone.',
    'The service’s official transfer or re-enrollment process determines how to move the method safely. Verify replacement access and recovery before retiring the old device.',
]
REVIEW = [
    {'id': 'mfa-prompt-fatigue', 'prompt': 'An approval request repeats while you are not logging in. What should repetition change?',
     'options': ['It makes approval safe', 'Nothing about authorisation: deny the unknown request and investigate', 'It means you should share the next code'], 'answer': 1,
     'feedback': ['Repeated requests do not prove you initiated the sign-in.', 'Correct. Repetition does not grant permission; use official controls to investigate.', 'The code remains an access secret even after repeated prompts.']},
    {'id': 'mfa-code-authority', 'prompt': 'Why protect one-time recovery codes like other account secrets?',
     'options': ['They are only decorative setup information', 'They are safe once sent as an image', 'They can provide a route back into the account'], 'answer': 2,
     'feedback': ['Their recovery role can carry account access authority.', 'A readable image exposes the same secret.', 'Correct. Someone obtaining a usable recovery code may gain a recovery route into the account.']},
    {'id': 'mfa-independent-recovery', 'prompt': 'Which recovery arrangement best helps if the MFA phone is lost?',
     'options': ['Protected recovery information accessible independently of that phone', 'The only recovery copy saved on the lost phone', 'Recovery codes posted publicly'], 'answer': 0,
     'feedback': ['Correct. Protect the information while keeping a usable route independent of the failed or missing device.', 'A recovery copy available only on the missing device may be unusable when needed.', 'Public exposure could give others account access.']},
    {'id': 'mfa-phone-transfer', 'prompt': 'Before retiring an old MFA phone, what should be verified?',
     'options': ['Only that the new phone has a similar wallpaper', 'The official transfer/re-enrollment succeeded and the replacement method works', 'That MFA has been permanently disabled'], 'answer': 1,
     'feedback': ['Appearance says nothing about account enrollment.', 'Correct. Check the supported process and working replacement access before losing the old method.', 'Permanent removal weakens protection rather than establishing a safe transfer.']},
    {'id': 'mfa-old-device', 'prompt': 'After verifying replacement access, what else belongs in the account review?',
     'options': ['Leave every old device trusted indefinitely', 'Send recovery codes to anyone offering help', 'Review old-device access, recovery options and sessions through official settings'], 'answer': 2,
     'feedback': ['Old access should be reviewed rather than retained blindly.', 'Unsolicited helpers should not receive recovery secrets.', 'Correct. Replacement includes reviewing what old access remains, not just installing an app.']},
]
