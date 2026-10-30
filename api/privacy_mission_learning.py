"""Privacy Patrol v1: fictional audience, location and permission records.

Evidence order and scoring remain aligned with the existing three-stage mission.
Never request a learner's real address, contacts, photos or location.
"""
MISSION_ID = 'privacy-patrol'
REVISION = 'privacy-patrol-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional school club member decide what to publish and which permissions to allow.',
    'objectives': [
        'Question why sensitive personal information is needed before sharing it.',
        'Limit who sees a photo album and what its location details reveal.',
        'Match app permissions to the task and decline unrelated access.',
    ],
    'workflow': [
        'Read the stage task and inspect every fictional profile, album or app record.',
        'Select the finding that matters most to the current privacy decision.',
        'Choose a protective action and commit it to read the explanation.',
        'Complete three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'All three committed decisions save the mission result. Review is repeatable practice and does not change that score.',
}
STAGES = [
    {'task': 'Decide whether a public club profile needs a student’s home address.',
     'hints': ['Consider who could search the profile, not only who runs the club.', 'Ask why an address is necessary and whether a less revealing option would meet the purpose.'],
     'artifacts': [
         {'title': 'Profile audience', 'body': 'The fictional club profile is public and searchable. People outside the club may find it. A school-themed page does not make its audience private.'},
         {'title': 'Address request', 'body': 'The profile form asks for the student’s home address. An address can reveal where someone lives. Keep it private and ask the club why it is needed, who would receive it and whether a less revealing option is available.'},
         {'title': 'Membership choice', 'body': 'Club membership is optional. Pressure to join quickly does not make publishing an address necessary. Do not substitute another person’s address; their privacy matters too.'},
     ]},
    {'task': 'Protect a photo album’s audience and reduce what it reveals about where the photos were taken.',
     'hints': ['A photo can reveal more than the people in it.', 'Combine an appropriate audience with removal of unnecessary location details; neither step guarantees that no copy will spread.'],
     'artifacts': [
         {'title': 'Album audience', 'body': 'The fictional album is visible to everyone, including strangers. Review whether that broad audience is needed before posting more photos.'},
         {'title': 'Sharing controls', 'body': 'A friends-only setting is available. Restrict the album to the intended audience and review who is included. Recipients can still copy or reshare images, so restricted visibility is not a guarantee of confidentiality.'},
         {'title': 'Location tags', 'body': 'Location tags identify where the photos were taken and may expose a home, school or routine. Remove unnecessary tags and inspect visible details in the image as well. Limiting the audience alone does not remove the location information already in the album.'},
     ]},
    {'task': 'Decide whether a quiz needs access to contacts or exact location.',
     'hints': ['Compare each requested permission with what the quiz actually does.', 'A permission request is not proof that access is needed. Decline unrelated access or use a suitable alternative.'],
     'artifacts': [
         {'title': 'Quiz purpose', 'body': 'The fictional quiz accepts answers and displays a result. No described feature needs to read a student’s address book or exact location.'},
         {'title': 'Contacts permission', 'body': 'Reading contacts would expose information about other people as well as the student. That access is unrelated to answering the quiz. Decline it rather than granting every request to proceed faster.'},
         {'title': 'Location choice', 'body': 'Exact location permission is optional in this scenario. Decline unnecessary access. If an app insists on unrelated permissions, stop and choose a trustworthy alternative or ask a trusted adult for help.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The home address is the sensitive information at stake. A public audience increases exposure; optional membership does not justify revealing where someone lives.',
    'Location tags add information about whereabouts beyond the album’s audience. Restrict visibility and remove unnecessary location details rather than relying on either measure alone.',
    'Contacts access is unrelated to the quiz and affects other people’s privacy. Match permissions to the task and decline unnecessary access, including optional location.',
]
REVIEW = [
    {'id': 'privacy-purpose', 'prompt': 'A public club page requests a home address for an optional badge. What should the student do first?',
     'options': ['Publish it because the page mentions school', 'Keep it private and ask why it is needed and who will see it', 'Use a classmate’s address instead'], 'answer': 1,
     'feedback': ['A school theme does not make a public page private or the request necessary.', 'Correct. Check purpose and audience before exposing sensitive information.', 'Substituting someone else’s details puts their privacy at risk.']},
    {'id': 'privacy-location', 'prompt': 'After restricting an album to friends, what other detail deserves review?',
     'options': ['Only the number of likes', 'Whether the photo is colourful', 'Location tags and visible clues about home, school or routines'], 'answer': 2,
     'feedback': ['Likes do not measure what location information the photo exposes.', 'Appearance does not determine privacy exposure.', 'Correct. Audience settings do not remove location details contained in the photo or its tags.']},
    {'id': 'privacy-resharing', 'prompt': 'Does friends-only visibility guarantee that an album cannot reach anyone else?',
     'options': ['No; recipients may still copy or reshare it', 'Yes; copying becomes impossible', 'Yes; every friend’s account is always secure'], 'answer': 0,
     'feedback': ['Correct. Limit the audience, but still consider what you are comfortable sharing.', 'Visibility controls do not make copying impossible.', 'An audience setting does not guarantee every recipient’s account is safe.']},
    {'id': 'privacy-contacts', 'prompt': 'Why decline contacts access for a quiz that only needs answers?',
     'options': ['Every quiz is necessarily malicious', 'The access is unrelated and exposes information about other people', 'Permissions are never useful for any app'], 'answer': 1,
     'feedback': ['An unnecessary permission is a reason to limit access, not proof about every quiz.', 'Correct. Grant only access needed for a justified feature; contacts contain other people’s information too.', 'Some features need permissions. Evaluate the particular purpose instead of granting or denying blindly.']},
    {'id': 'privacy-alternative', 'prompt': 'A quiz refuses to work unless you grant unrelated exact location access. What is a sensible next step?',
     'options': ['Grant it to finish faster', 'Tell classmates to grant it too', 'Stop, consider a trustworthy alternative and seek help if needed'], 'answer': 2,
     'feedback': ['Convenience does not establish that exact location is necessary.', 'Encouraging others to share does not resolve the unnecessary access.', 'Correct. You can decline the app rather than accept unrelated exposure.']},
]
