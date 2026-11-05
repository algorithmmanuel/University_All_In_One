"""Digital Footprints v1: fictional consent, old-profile and correction records.

Learners do not submit real photos, search results or personal contact details.
"""
MISSION_ID = 'digital-footprints'
REVISION = 'digital-footprints-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional student consider another person’s consent and manage their own public traces.',
    'objectives': [
        'Ask permission before publishing an identifying photo and respect a refusal.',
        'Reduce unnecessary public contact and routine details on old profiles.',
        'Preserve evidence and seek correction or reporting of misleading posts without amplifying harm.',
    ],
    'workflow': [
        'Read the current publishing or correction task and inspect every fictional record.',
        'Choose the finding that matters most to consent, exposure or accuracy.',
        'Commit one respectful protective response and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Optional review remains repeatable practice, with no saved grade or score change.',
}
STAGES = [
    {'task': 'Decide whether to publish an identifying, embarrassing photo when permission has not been obtained.',
     'hints': ['Taking or receiving a photo does not settle whether you may publish it.', 'Ask permission before sharing and respect a refusal; consider the person and audience, not just your intent.'],
     'artifacts': [
         {'title': 'Identifying photo', 'body': 'The fictional image identifies a classmate and could embarrass them. Owning a copy or finding it funny does not remove the need to consider the person’s privacy and wishes.'},
         {'title': 'Missing consent', 'body': 'The classmate has not agreed to publication. Ask permission before sharing and respect a refusal or uncertainty. Agreement to take a photo is not automatically agreement to publish it to any audience.'},
         {'title': 'Persistent copies', 'body': 'Public recipients may save or reshare the image. Later deletion may reduce exposure but cannot guarantee that every copy disappears. Do not tag more people or publish first and ask afterwards.'},
     ]},
    {'task': 'Review an old public profile and reduce unnecessary contact and routine exposure.',
     'hints': ['An account you no longer use may still reveal current or useful personal details.', 'Review the schedule as well as the phone number; combining time and place can expose a routine.'],
     'artifacts': [
         {'title': 'Public phone number', 'body': 'An old fictional profile displays the learner’s phone number. Review whether it needs to be public and remove unnecessary contact details rather than add further personal information.'},
         {'title': 'School schedule', 'body': 'The profile lists school times and activities. A schedule can reveal when and where someone is likely to be found. Removing only the phone number leaves this routine exposure in place.'},
         {'title': 'Profile controls', 'body': 'The learner can remove unnecessary details, tighten the audience or close an unused account through official settings. Review other old profiles too. Changes reduce available information but do not guarantee removal of every past copy.'},
     ]},
    {'task': 'Respond proportionately to a misleading post without threatening its author or spreading more private information.',
     'hints': ['Establish what is inaccurate before treating the post as confirmed fact.', 'Save relevant evidence privately, then use correction/reporting and trusted support rather than public retaliation.'],
     'artifacts': [
         {'title': 'Accuracy check', 'body': 'A fictional friend finds a potentially misleading post about the learner. Check what it claims and which parts are inaccurate; another person repeating the claim does not make it true. Preserve relevant evidence before requesting correction.'},
         {'title': 'Correction and reporting', 'body': 'Use the platform’s reporting tools or an appropriate safe correction request. Keep a protected record of the post and relevant context. Do not threaten the poster, spread the misleading claim or reveal additional personal information to retaliate.'},
         {'title': 'Escalation support', 'body': 'A trusted adult or appropriate school/platform support can help if the post persists or causes concern. Save evidence without publicly amplifying identifying content. The simulation does not promise that a report will remove every copy.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Missing consent is the central decision point. An identifying image and potentially persistent copies make it important to ask first and respect refusal.',
    'The schedule exposes a routine even if a phone number is removed. Review the full profile, remove unnecessary details and tighten the audience.',
    'Potential inaccuracy is the basis for checking and seeking correction. Preserve evidence and use appropriate reporting/support without threats or extra privacy exposure.',
]
REVIEW = [
    {'id': 'footprint-photo-permission', 'prompt': 'A classmate agreed to be photographed but has not agreed to a public post. What follows?',
     'options': ['Permission to take the photo covers every future use', 'Ask before publishing and respect their refusal or uncertainty', 'Post first because deletion always removes all copies'], 'answer': 1,
     'feedback': ['Taking a photo and publishing it to an audience are different decisions.', 'Correct. Check permission for the intended sharing before posting.', 'Deletion cannot guarantee that saved or reshared copies disappear.']},
    {'id': 'footprint-persistence', 'prompt': 'Why consider the audience before posting an identifying image publicly?',
     'options': ['A public post is visible only to friends', 'A tag makes all copies temporary', 'Other people may save or reshare it beyond the intended audience'], 'answer': 2,
     'feedback': ['Public visibility can reach people outside the friend group.', 'Tagging does not limit copying or make every copy temporary.', 'Correct. Consider possible onward sharing before publication, not only after.']},
    {'id': 'footprint-old-profile', 'prompt': 'An old account lists a phone number and school timetable. What should a privacy review cover?',
     'options': ['Both unnecessary contact details and the schedule that reveals routines', 'Only the profile’s colour scheme', 'Only the number of followers'], 'answer': 0,
     'feedback': ['Correct. Review the information exposed as well as the audience and unused account settings.', 'Appearance does not remove contact or routine information.', 'Follower count does not show whether sensitive routine details remain public.']},
    {'id': 'footprint-correction', 'prompt': 'Which response best fits a post that appears to misrepresent you?',
     'options': ['Threaten the author publicly', 'Check the claim, preserve evidence and use an appropriate correction/reporting route', 'Publish the author’s private details'], 'answer': 1,
     'feedback': ['Threats escalate harm rather than establish accuracy or a safe remedy.', 'Correct. Use evidence and a proportionate reporting or correction process.', 'Exposing another person’s details adds a privacy harm and does not correct the claim.']},
    {'id': 'footprint-removal-limit', 'prompt': 'After tightening an old profile’s privacy settings, which statement is accurate?',
     'options': ['Every past copy is certainly gone', 'No future privacy review will ever be needed', 'Exposure is reduced, but earlier saved copies may still exist'], 'answer': 2,
     'feedback': ['Settings cannot guarantee removal of copies already made elsewhere.', 'Other accounts, settings or circumstances may still need review.', 'Correct. Privacy changes help, while their limits should remain clear.']},
]
