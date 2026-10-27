"""Additive beginner mission guidance; existing steps and saved scores stay fixed.

Artifacts are fictional observations, not executable links. Review keys remain
server-owned. Review is repeatable, ungraded practice and never mutates a run.
"""
MISSION_ID = 'phishing-investigation'
REVISION = 'scholarship-guidance-v1'

BRIEFING = {
    'revision': REVISION,
    'role': 'You are a student helping a classmate assess a scholarship message.',
    'objectives': [
        'Recognise pressure and an unfamiliar destination without assuming every unexpected message is fraudulent.',
        'Verify a request through an independent school contact or portal.',
        'Respond promptly when a password may have been exposed.',
    ],
    'workflow': [
        'Read the stage briefing and open the evidence locker.',
        'Inspect every artifact, then choose the most important finding.',
        'Choose one response at the decision desk and commit it once.',
        'Read the feedback, repeat for all three stages, then try five review questions.',
    ],
    'completion': 'Finish all three decisions to save the mission result. Review questions are optional practice and do not change that result.',
}

STAGES = [
    {
        'task': 'Decide how to check the unexpected scholarship request without using its own verification route.',
        'hints': [
            'Compare the sender, deadline and destination. A familiar logo alone would not prove who sent it.',
            'Ask whether your check comes from the message itself or a route you already trust.',
        ],
        'artifacts': [
            {'title': 'Sender record', 'body': 'From: awards@scholarships-example.invalid. Ada has no previous verified contact with this address. An unfamiliar sender is a reason to check, not proof of fraud by itself. Receiving the message alone does not establish account compromise. Avoid engaging or forwarding its link; use the school’s approved reporting route.'},
            {'title': 'Message deadline', 'body': '“Your scholarship expires in 20 minutes. Verify your student account immediately.” The short deadline pressures Ada to act before checking.'},
            {'title': 'Destination preview', 'body': 'Displayed destination: student-grants-example.invalid/verify. It is not Ada’s previously verified school portal. This is fictional text, not a link to open.'},
        ],
    },
    {
        'task': 'Identify which observation most directly shows that the request risks exposing an account secret.',
        'hints': [
            'Separate the sensitive information being requested from how the message looks.',
            'A password entered into an unrelated site could be captured there; independently verify the service first.',
        ],
        'artifacts': [
            {'title': 'Requested information', 'body': 'The displayed form asks for Ada’s student portal password to release the award. No real form or password input is provided in this simulation.'},
            {'title': 'Website comparison', 'body': 'The request asks for the portal password at student-grants-example.invalid rather than the school portal Ada already knows. The requested secret and the unrelated destination must be considered together.'},
        ],
    },
    {
        'task': 'Choose a practical response after a classmate reports submitting a password.',
        'hints': [
            'The situation has changed from receiving a message to potentially exposing a credential.',
            'Use the real service’s security controls and trusted support, rather than asking the suspicious sender to fix it.',
        ],
        'artifacts': [
            {'title': 'Classmate report', 'body': '“I entered my portal password into the page from the message.” Treat that password as potentially exposed. Open the real portal independently, replace the password and any reused copies, review/revoke unfamiliar sessions where supported, enable MFA and report to trusted school support.'},
        ],
    },
]

REVIEW = [
    {'id': 'pressure', 'prompt': 'A message has a school logo and a ten-minute deadline. What can you conclude?',
     'options': ['The logo proves it is genuine', 'Pause and verify independently; appearance and urgency do not establish identity', 'Every short deadline proves fraud'], 'answer': 1,
     'feedback': ['A logo can be copied. It does not authenticate the sender.', 'Correct. Treat the signs as reasons to check through a trusted independent route.', 'Urgency is a warning sign, not conclusive proof. Verify the request.']},
    {'id': 'independent-route', 'prompt': 'Which check avoids relying on the suspicious message to verify itself?',
     'options': ['Call only the number inside it', 'Ask the sender whether it is real', 'Open the previously verified school portal and find support there'], 'answer': 2,
     'feedback': ['That number may belong to the same sender. Find contact details independently.', 'The sender can repeat the same claim. Use a separate trusted route.', 'Correct. The known portal provides an independent route to the school.']},
    {'id': 'secret', 'prompt': 'Why is an unrelated website requesting your portal password a strong warning?',
     'options': ['The secret could be captured by that site', 'Short messages cannot be genuine', 'A greeting always proves account theft'], 'answer': 0,
     'feedback': ['Correct. The password is an access secret; verify the real service before entering it.', 'Length does not determine trust. Focus on the requested secret and destination.', 'A greeting is not proof. The unrelated destination requesting a secret is the meaningful evidence.']},
    {'id': 'exposure', 'prompt': 'A classmate submitted a reused password. What addresses the remaining risk?',
     'options': ['Wait for another message', 'Secure the real account and every reused copy, review sessions and report through trusted support', 'Send the password to friends to test'], 'answer': 1,
     'feedback': ['Waiting leaves a potentially exposed password usable.', 'Correct. Use official controls promptly, replace reused passwords with unique ones and seek trusted support.', 'That exposes the secret again. Never send real passwords for investigation.']},
    {'id': 'received-only', 'prompt': 'You received the message but did not follow it or enter information. What is proportionate?',
     'options': ['Assume all your accounts are already lost', 'Forward the suspicious link to classmates to investigate', 'Avoid engagement and use the approved reporting route'], 'answer': 2,
     'feedback': ['Receiving a message alone does not establish account compromise.', 'Forwarding can spread the risk. Use approved reporting methods instead.', 'Correct. Avoid engaging and report safely; distinguish receiving a message from exposing credentials.']},
]

FINDING_EXPLANATIONS = [
    'The unfamiliar verification destination is the strongest finding for deciding how to check this request. The sender and deadline add context; an independently trusted portal avoids relying on the message’s own route.',
    'The unrelated website requesting the school portal password links a sensitive secret to an unverified destination. That combination is more specific than the password request alone.',
    'The classmate’s report of entering a password indicates potential credential exposure and calls for prompt action through the real service.',
]
