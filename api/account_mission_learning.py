"""Password Fortress guidance v1: fictional records, no real secret collection.

The evidence order matches the existing mission. Keep step/scoring changes out
of this content release so partial and historical runs retain their meaning.
"""
MISSION_ID = 'password-fortress'
REVISION = 'password-fortress-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional student protect a school account and respond to unfamiliar access.',
    'objectives': [
        'Choose a long, unique password and explain how reuse spreads risk between accounts.',
        'Explain what MFA adds and reject an approval request you did not initiate.',
        'Use official account controls to investigate sessions and protect recovery methods.',
    ],
    'workflow': [
        'Read the stage task, then open each record in the evidence locker.',
        'Select the most important finding for the current account-safety decision.',
        'Choose an action at the decision desk and commit it to see the explanation.',
        'Finish three stages to save the mission result, then try five review questions.',
    ],
    'completion': 'Commit all three stage decisions to save the result. Optional review does not save a separate grade or change the mission score.',
}
STAGES = [
    {
        'task': 'Choose a password strategy that keeps one website leak from unlocking a different account.',
        'hints': [
            'Consider what happens to the email account if its password is also used on a breached game.',
            'Length helps resist guessing; uniqueness limits reuse. A manager can help you keep both.',
        ],
        'artifacts': [
            {'title': 'Reuse risk note', 'body': 'A fictional game account and a school account use the same password. If that value is exposed at the game, someone may try it at the school. Choose a different long password for each account; changing only the game leaves the reused school password exposed.'},
            {'title': 'Passphrase workshop', 'body': 'A long, unique passphrase can be easier to remember than a short secret based on a birthday. Common quotations, names and predictable patterns can still be guessed. Do not enter or share an actual password in this training.'},
            {'title': 'Password manager plan', 'body': 'A reputable password manager can generate and store different long passwords. Protect the manager itself and follow its recovery guidance. A manager supports good password choices; it does not make every sign-in or download safe.'},
        ],
    },
    {
        'task': 'Choose how to add another kind of sign-in proof and handle an unexpected approval request.',
        'hints': [
            'Two ordinary passwords are both something you know; count kinds of proof, not screens.',
            'An approval prompt should correspond to a sign-in you started. Do not approve it merely to stop notifications.',
        ],
        'artifacts': [
            {'title': 'Password factor', 'body': 'A password is something you know. Adding a second ordinary password repeats the same type of proof and is not, by itself, multifactor authentication.'},
            {'title': 'Additional factor', 'body': 'The school supports an authenticator or security key as another type of proof alongside its password sign-in. Enable a suitable supported method through the real service’s settings. MFA adds protection but does not prove every session is legitimate.'},
            {'title': 'Unexpected prompt', 'body': 'A student receives an approval prompt while not signing in. Deny it, then review activity through the official service. Do not share one-time codes or approve a caller’s sign-in request. Repeated unwanted prompts are a reason to investigate, not approve.'},
        ],
    },
    {
        'task': 'Investigate an unfamiliar session through the real service and choose proportionate account protection.',
        'hints': [
            'A session is a signed-in connection that may continue after the original login.',
            'Use trusted service controls to review access and recovery. Do not hand the account to a classmate to investigate.',
        ],
        'artifacts': [
            {'title': 'Official session list', 'body': 'The school account’s verified settings show a session from an unfamiliar device. Check the listed activity and whether you recognise the access; do not ignore it or assume the entry alone proves theft. Use official controls and trusted support to secure the account.'},
            {'title': 'Session revocation', 'body': 'The service offers sign-out or revocation for unfamiliar sessions. If compromise is suspected, follow the real service’s recovery steps, change an exposed password and reused copies, and review active sessions. Do not assume a password change alone ends every existing session.'},
            {'title': 'Recovery settings', 'body': 'Check recovery contacts in the real account and keep recovery codes securely, separately from the device they recover. Recovery codes can grant access: do not send them to callers or classmates. Ask official support for help through independently verified contact details.'},
        ],
    },
]
FINDING_EXPLANATIONS = [
    'Password reuse links the safety of different accounts. A long, unique password limits that reuse path; the passphrase and manager records explain how to put the choice into practice.',
    'An authenticator or security key adds a different type of proof. Two passwords repeat a factor; an unexpected approval must still be denied and investigated.',
    'The real service’s session list is the starting evidence for unfamiliar access. Review it through official controls, revoke suspicious access where supported and protect recovery settings.',
]
REVIEW = [
    {'id': 'reuse-boundary', 'prompt': 'A gaming password leaks and also protects a school account. What leaves the school exposed?',
     'options': ['Replacing each reused copy with a unique value', 'Changing only the game password while retaining its old value at school', 'Protecting the password manager'], 'answer': 1,
     'feedback': ['Replacing every reused copy addresses that reuse path.', 'Correct. The school would still accept the leaked value. Replace reused copies with different long passwords.', 'Protecting the manager is useful, but the exposed reused school password still needs replacing.']},
    {'id': 'factor-types', 'prompt': 'Which combination adds a different kind of sign-in proof to a password?',
     'options': ['The same password typed twice', 'A second ordinary password', 'A supported authenticator or security key'], 'answer': 2,
     'feedback': ['Repetition does not add a different type of proof.', 'Both passwords are something you know. Two secrets do not by themselves create two factors.', 'Correct. A supported authenticator or security key supplies another kind of proof in the school’s MFA setup.']},
    {'id': 'unwanted-approval', 'prompt': 'Repeated approval requests arrive while you are studying offline. Which response fits the evidence?',
     'options': ['Deny them and check security activity through the real service', 'Approve one to stop the interruptions', 'Give a caller the next code'], 'answer': 0,
     'feedback': ['Correct. Do not authorise a sign-in you did not initiate; investigate through trusted service controls.', 'That may authorise someone else’s access. Repetition does not make approval safe.', 'A code is an access secret. A caller’s claim does not justify sharing it.']},
    {'id': 'session-follow-up', 'prompt': 'After suspected compromise, why review active sessions as well as changing an exposed password?',
     'options': ['Every unfamiliar entry proves theft', 'A password change may not end every existing session', 'Session logs should be deleted'], 'answer': 1,
     'feedback': ['Unfamiliar activity warrants checking; it is not automatic proof. Preserve and review the evidence.', 'Correct. Use the service’s session review and revocation controls where supported; do not assume every session has ended.', 'Logs help investigate. Deleting them removes useful evidence.']},
    {'id': 'recovery-secret', 'prompt': 'Where should a student keep recovery codes for a phone-based sign-in method?',
     'options': ['In a public class chat', 'With a caller who claims to be support', 'In protected storage separate from the phone they help recover'], 'answer': 2,
     'feedback': ['Public sharing can let someone else recover the account.', 'Recovery codes are access secrets. Do not hand them to an unsolicited caller.', 'Correct. Protect these access secrets and keep a usable recovery route if the phone is lost.']},
]
