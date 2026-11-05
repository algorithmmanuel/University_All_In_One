"""Device Defender v1: fictional update, shared-session and permission records.

No software is downloaded, installed or elevated by this training content.
"""
MISSION_ID = 'device-defender'
REVISION = 'device-defender-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional student maintain a device and leave shared computers safely.',
    'objectives': [
        'Use the operating system’s trusted update route rather than an unsolicited updater.',
        'End a signed-in session before handing a shared computer to another person.',
        'Pause an unexpected download requesting administrator rights and seek trusted support.',
    ],
    'workflow': [
        'Read the device task and inspect every fictional update, session or download record.',
        'Choose the finding most relevant to the current device risk.',
        'Commit one protective action and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review has no saved grade and does not alter the result.',
}
STAGES = [
    {'task': 'Handle a security update through the device’s official update settings.',
     'hints': ['Open the normal update settings independently if you are unsure about a notification.', 'Updates may fix security weaknesses; an unsolicited download calling itself an updater is a different source.'],
     'artifacts': [
         {'title': 'Operating system notice', 'body': 'The fictional device reports an available update in its operating system settings. Use the normal official update route. If a pop-up or message is uncertain, independently open those settings rather than following its download link.'},
         {'title': 'Security fixes', 'body': 'Updates can fix known weaknesses and improve reliability, though no update removes every risk. Disabling updates permanently leaves supported fixes unapplied. Do not replace the official route with a random updater sent in chat.'},
         {'title': 'Restart planning', 'body': 'This update may require a restart. Save work and follow school IT guidance about timing and power before installing through the official settings. A restart prompt is not a reason to disable updates indefinitely.'},
     ]},
    {'task': 'Leave a shared school computer without leaving your account available to the next student.',
     'hints': ['A browser tab and an authenticated session are different things.', 'Use the service’s sign-out controls and close the session; do not assume that shutting a tab ends every login.'],
     'artifacts': [
         {'title': 'Active session', 'body': 'The fictional school account remains signed in. A session can let another person use the account without entering its password again. Closing only a tab may leave the authenticated session available.'},
         {'title': 'Next computer user', 'body': 'Another student will use this shared computer next. Do not leave personal account pages open, save an actual password in a shared browser or share credentials to let the next person continue.'},
         {'title': 'Sign-out control', 'body': 'Use the account’s sign-out control, finish the shared-computer session according to school procedure and close the browser. A screen lock can protect a temporary absence, but is not a substitute for ending your session when handing the device over.'},
     ]},
    {'task': 'Stop an unexpected attachment that asks for administrator permissions until it can be assessed safely.',
     'hints': ['Look at both the source and how much control the file requests.', 'Do not grant elevated rights or switch off protection just to discover what the file does.'],
     'artifacts': [
         {'title': 'Unknown sender', 'body': 'An unexpected fictional download comes from a sender the learner has not verified. Do not open or forward it to friends to test. An attractive filename or icon does not establish trust.'},
         {'title': 'Administrator request', 'body': 'The download asks for administrator rights, which can permit broad device changes. Grant only justified, authorised access. In this unverified situation, stop rather than approve elevation or disable security protection.'},
         {'title': 'Trusted IT assessment', 'body': 'School IT support can assess the request through its approved reporting process. Report what happened without running the file to gather more evidence. No actual attachment is present or executed in this simulation.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The update’s security-fix purpose explains why it matters. Use the official settings and plan any restart; a random chat download or permanently disabled updates does not meet that need.',
    'The active authenticated session is the exposure on the shared device. Sign out and end it before handing over, rather than relying on a closed tab or shared password.',
    'Requested administrator access raises the possible impact of an unverified download. Stop and seek trusted IT assessment without granting elevation or disabling protection.',
]
REVIEW = [
    {'id': 'device-update-route', 'prompt': 'A chat message offers an updater while your operating system also has an update setting. Which route should you use?',
     'options': ['The chat download because it promises speed', 'Independently open the official update settings and follow school guidance', 'Disable updates to avoid choosing'], 'answer': 1,
     'feedback': ['A promise does not verify the download source.', 'Correct. Reach the trusted update route independently and follow the applicable procedure.', 'Disabling updates leaves supported fixes unapplied.']},
    {'id': 'device-restart', 'prompt': 'An official security update needs a restart while schoolwork is open. What is sensible?',
     'options': ['Ignore every future update', 'Install a random tool to avoid restarting', 'Save work and plan the official update/restart under school IT guidance'], 'answer': 2,
     'feedback': ['Restart timing can be planned without permanently ignoring updates.', 'An unrelated tool introduces an unverified source instead of resolving the update safely.', 'Correct. Protect your work and use the official process at an appropriate time.']},
    {'id': 'device-shared-session', 'prompt': 'Why may closing a tab be insufficient before another student uses the computer?',
     'options': ['The authenticated session may remain available', 'Closing a tab always erases every session', 'The next student needs your password to use any open session'], 'answer': 0,
     'feedback': ['Correct. Use sign-out and end the shared-computer session rather than assume a tab closure logs you out.', 'Tab closure does not guarantee every session is erased.', 'An existing authenticated session can allow use without another password entry.']},
    {'id': 'device-elevation', 'prompt': 'What makes an unknown attachment’s administrator request especially concerning?',
     'options': ['It has an interesting filename', 'Elevated rights can permit broad changes to the device', 'Administrator requests are proof that all software is malicious'], 'answer': 1,
     'feedback': ['A filename does not justify access or establish the file’s behaviour.', 'Correct. Unverified software should not receive broad privileges; stop and seek approved assessment.', 'Some authorised tasks need elevation. Assess the purpose and source rather than treating every prompt as proof.']},
    {'id': 'device-report-file', 'prompt': 'How should a student seek help with an unverified file without increasing the risk?',
     'options': ['Run it first to see what it does', 'Forward it to friends to test', 'Stop and use school IT’s approved reporting process'], 'answer': 2,
     'feedback': ['Executing it may cause the very harm you are trying to assess.', 'Forwarding spreads the potential exposure to other people.', 'Correct. Trusted IT can guide assessment without asking you to execute the file.']},
]
