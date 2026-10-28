"""Safe Social v1: fictional boundaries, bullying support and impersonation.

Do not request actual messages, personal routines or a victim's identifying data.
"""
MISSION_ID = 'safe-social'
REVISION = 'safe-social-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help fictional classmates maintain boundaries, support someone being targeted and verify an unusual request.',
    'objectives': [
        'Protect routine and location information from unverified contacts.',
        'Support someone facing repeated hurtful messages while preserving evidence and seeking trusted help.',
        'Verify an unusual money request outside a possibly impersonated account.',
    ],
    'workflow': [
        'Read the current social-safety task and open every fictional record.',
        'Choose the finding that best explains the risk or need for support.',
        'Commit a safe response and read the explanation before moving on.',
        'Finish three stages to save your result, then try five optional review questions.',
    ],
    'completion': 'All three committed responses save the mission result. Review is separate practice, with no saved grade or score change.',
}
STAGES = [
    {'task': 'Set a safe boundary when an unknown account asks about school and travel routines.',
     'hints': ['A friendly account can still be unverified.', 'Repeated details about place and time can reveal where to find someone; declining to share is a valid response.'],
     'artifacts': [
         {'title': 'Unknown follower', 'body': 'The fictional account’s identity is unverified. Do not treat friendliness, a shared interest or a profile picture as proof that it is safe to reveal personal routines.'},
         {'title': 'Routine request', 'body': 'The account asks which school the learner attends and when they travel home. Together, place and timing can reveal a routine. Do not share the route, travel times or live location.'},
         {'title': 'Boundary controls', 'body': 'The learner can restrict, block or report the account using the platform’s controls and ask a trusted adult for help if concerned. They do not owe a stranger personal details to be polite.'},
     ]},
    {'task': 'Support a classmate targeted by repeated cruel messages without spreading the abuse.',
     'hints': ['Support the person rather than reward the harmful group behaviour.', 'Preserve useful evidence privately and involve trusted help; do not repost identifying or humiliating material.'],
     'artifacts': [
         {'title': 'Repeated messages', 'body': 'The fictional classmate is repeatedly targeted. Do not join in or blame the person targeted. Offer support and help them use reporting or blocking controls.'},
         {'title': 'Private evidence', 'body': 'Screenshots can preserve relevant messages, dates and account details for a report. Keep them protected and share only with appropriate trusted support. Reposting the screenshots publicly can spread the harm.'},
         {'title': 'Trusted support', 'body': 'A trusted adult or school safeguarding contact can help the classmate respond. Persistent targeting should not be left for the learner to handle alone. Seek help promptly and follow the appropriate school/platform reporting route.'},
     ]},
    {'task': 'Check a friend’s unusual money request without trusting a copied profile.',
     'hints': ['A familiar picture does not show who controls an account.', 'Contact your friend through a separate route you already trust before sending money, then report impersonation if appropriate.'],
     'artifacts': [
         {'title': 'Copied profile', 'body': 'A fictional new account uses the friend’s photo and name. These details can be copied; even a familiar existing account can be compromised.'},
         {'title': 'Unusual money request', 'body': 'The account asks for an unexpected urgent transfer. The unusual financial request is the immediate reason to pause. Do not pay or forward the request to others for fundraising before verifying it.'},
         {'title': 'Independent friend contact', 'body': 'The learner can contact the friend through a previously known phone number or another trusted channel. Verify separately, then use platform reporting tools for an impersonating account. Do not rely only on replies from the suspect account.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The requested routine details can expose where and when to find the learner. Restricting an unverified contact and withholding those details protects a practical boundary.',
    'Trusted support is important when harmful messages persist. Preserve useful evidence privately and support/report rather than amplify the targeting.',
    'The unusual money request creates an immediate decision risk. A copied picture is not authentication; verify with the friend through an independent known route before acting.',
]
REVIEW = [
    {'id': 'social-routine', 'prompt': 'Which combination can expose a student’s routine to an unknown follower?',
     'options': ['A favourite colour alone', 'School location plus the usual journey-home time', 'A fictional nickname with no other details'], 'answer': 1,
     'feedback': ['A favourite colour alone does not provide the place-and-time routine in this scenario.', 'Correct. Place and timing together can reveal where someone may be found.', 'A non-identifying fictional nickname is different from sharing a real routine.']},
    {'id': 'social-boundary', 'prompt': 'A friendly stranger insists that refusing a live location is rude. What is appropriate?',
     'options': ['Share it to avoid offending them', 'Post it publicly instead', 'Keep the boundary and restrict or report the contact if needed'], 'answer': 2,
     'feedback': ['Politeness does not require exposing personal location.', 'Public sharing increases exposure rather than resolving the concern.', 'Correct. You may decline personal requests and seek trusted support.']},
    {'id': 'social-evidence', 'prompt': 'How should screenshots of repeated cruel messages be handled?',
     'options': ['Keep useful evidence protected for appropriate school/platform support', 'Repost them with the classmate’s details so everyone sees', 'Use them to join the teasing'], 'answer': 0,
     'feedback': ['Correct. Preserve the evidence without spreading identifying or humiliating content.', 'Public reposting can extend the harm to the person targeted.', 'Joining the behaviour harms the classmate and does not help reporting.']},
    {'id': 'social-help', 'prompt': 'A classmate remains the target of repeated hurtful messages. Which response is supportive?',
     'options': ['Tell them to handle it alone', 'Support them and involve trusted adult/school help through the reporting route', 'Blame them for being online'], 'answer': 1,
     'feedback': ['Persistent targeting is a reason to seek support, not leave someone isolated.', 'Correct. Trusted help can support a coordinated response while useful evidence is retained.', 'Blaming the person targeted adds harm rather than addressing the behaviour.']},
    {'id': 'social-money', 'prompt': 'An account using your friend’s photo asks for an urgent transfer. What should you verify?',
     'options': ['Whether the photo looks familiar enough to pay', 'Whether the suspect account repeats its claim', 'The request with your friend through a separately known contact route'], 'answer': 2,
     'feedback': ['Photos and names can be copied; familiarity does not authenticate this request.', 'The suspect source can repeat the same story.', 'Correct. A separate known route helps establish whether the friend actually made the request.']},
]
