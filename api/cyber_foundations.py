"""Cyber safety curriculum: fictional scenarios, no live links or secret collection.

Keep this revision available while stored lesson markers reference it. Assessment
items link to taught objective IDs; practice is explanatory and has no saved grade.
"""
REVISION = 'cyber-foundations-v1'
COURSE_TITLE = 'Cyber Safety Foundations'
ACADEMY_ID = 'cyber'
MARKER = 'educyber.lesson:' + REVISION + ':'

LESSONS = [
    {
        'key': 'phishing', 'title': 'Recognising phishing',
        'legacy_content': 'Phishing messages may impersonate schools, banks or employers. Verify requests through independently located official channels. Never enter passwords through unfamiliar links.',
        'objectives': [
            {'id': 'CS-P1', 'text': 'Spot pressure, impersonation and requests for secrets.'},
            {'id': 'CS-P2', 'text': 'Verify a request using an independent, trusted route.'},
            {'id': 'CS-P3', 'text': 'Choose a safe reporting or recovery action after a suspicious message.'},
        ],
        'sections': [
            {'title': 'Read the request, not just the logo', 'body': 'Phishing uses a misleading message to persuade someone to reveal information, install something or make a payment. It can arrive by email, text, chat or a QR code. A familiar display name, copied school crest or convincing grammar does not prove who sent it. Slow down when a message creates urgency, secrecy or an unexpected reward.'},
            {'title': 'Worked scenario: a scholarship deadline', 'body': 'Ada receives: “Your scholarship expires in ten minutes. Use this link and send your password and one-time code.” She stops before opening the link. She opens the school portal from a bookmark she previously verified, then contacts the scholarship office using details found there. The office says no password is needed. The deadline and logo were distractions; the independent check settled the request without exposing a secret.'},
            {'title': 'Change the channel to verify', 'body': 'Use the official app, an already verified bookmark or contact details you find independently. Do not use the phone number, reply address or link inside the suspicious message as your only check. A familiar sender account can itself be compromised. Before opening an unexpected attachment, verify that the person really intended to send that file. A shortened link or QR code can hide the destination; neither proves trust.'},
            {'title': 'Report, then respond to what happened', 'body': 'Use your school or employer’s approved reporting method, or the platform’s report feature. Do not forward a suspicious file to friends to investigate. If you already entered a password, open the real service independently, change that password and any reused copies, review account activity and use the service’s sign-out/recovery controls. Tell the appropriate support team promptly. If you only received the message, you have not necessarily lost the account; report it and avoid engaging.'},
        ],
        'exercises': [
            {'id': 'scholarship-route', 'objective': 'CS-P2', 'prompt': 'A scholarship message demands your login today. Which next step gives an independent check?',
             'options': ['Call only the number inside the message', 'Open the verified school portal and contact its office', 'Reply with your password to prove your identity'], 'answer': 1,
             'feedback': ['That number may be controlled by the same sender. Find contact details independently.', 'Correct. You reached the school through a route you already trust rather than following the message.', 'A password is a secret, not evidence to send to a message sender. Verify through the real service.']},
            {'id': 'submitted-secret', 'objective': 'CS-P3', 'prompt': 'You entered a password into a page reached from a suspicious text. What should you do now?',
             'options': ['Wait for another message before acting', 'Send the page to friends with your password', 'Open the real service independently, secure the account and report it'], 'answer': 2,
             'feedback': ['Waiting can leave the exposed password usable. Use the real service’s recovery controls promptly.', 'That shares the secret again and spreads the unsafe page. Do not ask friends to log in to test it.', 'Correct. Change the exposed password through the real service, review access and tell the appropriate support team.']},
        ],
    },
    {
        'key': 'accounts', 'title': 'Protecting your accounts',
        'legacy_content': 'Use a unique long password for every account, preferably with a password manager. Enable multifactor authentication where available.',
        'objectives': [
            {'id': 'CS-A1', 'text': 'Explain why long, unique passwords and a password manager reduce reuse risk.'},
            {'id': 'CS-A2', 'text': 'Recognise MFA as another factor and handle unexpected approval requests.'},
            {'id': 'CS-A3', 'text': 'Keep recovery methods private and reduce exposure after device loss.'},
        ],
        'sections': [
            {'title': 'One leak should not open every account', 'body': 'A long, unique password belongs to one account only. If a website loses reused credentials, an attacker may try the same email/password pair elsewhere; this is credential stuffing. A reputable password manager can generate and store different passwords so you do not need to memorise each one. Secure the manager itself carefully. Never use real passwords in a learning exercise.'},
            {'title': 'Worked scenario: a leaked game password', 'body': 'Emeka used one password for a game and his email. After the game reports a leak, he changes the game password but realises the email still uses the exposed value. He opens his email service directly, sets a different long password and turns on MFA. Changing only the game would leave the email at risk. Using unique passwords limits this reuse path; it does not guarantee an account can never be compromised.'},
            {'title': 'MFA is more than a second password', 'body': 'Multifactor authentication adds another type of proof, such as an authenticator or security key, to a password-based sign-in. Two ordinary passwords are still the same type of factor. Enable a suitable supported MFA method and follow the service’s setup guidance. Never approve a sign-in you did not start, or give a caller a one-time code. An unexpected prompt is a reason to deny it and investigate through the real service.'},
            {'title': 'Keep a safe way back in', 'body': 'Where offered, store recovery codes securely and separately from the device they help recover. They are account access secrets, not items to send to support callers or classmates. If a phone is lost, use another trusted device and official service controls to secure affected accounts, revoke sessions where supported and report the loss. Do not assume a screen lock alone ends every existing session. Give people only the access they need; do not share your account to grant access.'},
        ],
        'exercises': [
            {'id': 'reused-login', 'objective': 'CS-A1', 'prompt': 'A shopping password was exposed and is also used for your email. Which plan reduces the remaining reuse risk?',
             'options': ['Change both affected passwords to different long values', 'Change only the shopping password and keep reusing the email password', 'Use the exposed password for every account to remember it'], 'answer': 0,
             'feedback': ['Correct. Each affected account needs its own new password; a manager can help keep them different.', 'The email account would still accept the exposed value. Address every account using it.', 'Reuse makes one leak useful on more services. Choose unique passwords instead.']},
            {'id': 'unexpected-mfa', 'objective': 'CS-A2', 'prompt': 'An approval prompt appears when you are not signing in. What is the safest response?',
             'options': ['Approve it so notifications stop', 'Deny it and review security through the official service', 'Send the approval code to the caller asking for it'], 'answer': 1,
             'feedback': ['Approval may complete someone else’s sign-in. Do not approve a request you did not start.', 'Correct. Deny the unknown request, review activity and secure the account using trusted service controls.', 'The code is a sign-in secret. A caller’s claim does not make sharing it safe.']},
        ],
    },
    {
        'key': 'browsing', 'title': 'Safer browsing',
        'legacy_content': 'Check website addresses carefully, install updates, and avoid downloading files from untrusted sources.',
        'objectives': [
            {'id': 'CS-B1', 'text': 'Distinguish an encrypted connection from a trustworthy website.'},
            {'id': 'CS-B2', 'text': 'Make safer download, extension and update decisions.'},
            {'id': 'CS-B3', 'text': 'Explain how limited permissions, backups and safer network choices reduce harm.'},
        ],
        'sections': [
            {'title': 'A secure connection is only one check', 'body': 'HTTPS protects data in transit between your browser and the site it connects to. A fraudulent site can also use HTTPS. Check that you reached the intended service using a trusted address or official app, not merely that the connection is encrypted. In a training example, school.example and school.example.attacker.example are different hosts; adding familiar words does not make the second one the school. These are fictional addresses, not links to visit.'},
            {'title': 'Worked scenario: an urgent video update', 'body': 'A pop-up says a lesson video needs an urgent player download and asks Ada to disable security software. She closes the pop-up and checks updates in the device or application’s normal settings. The trusted update route is separate from the advertisement. She does not disable protection or install the offered file just because the page claims urgency.'},
            {'title': 'Downloads, updates and permissions', 'body': 'Use trusted stores or the publisher’s verified route for downloads. Apply supported software updates through normal settings; many updates fix security weaknesses, but no update removes every risk. Review why an extension needs access before installing it. A simple calculator asking to read all browser pages deserves scrutiny. Decline unnecessary permissions. Do not connect an unknown USB drive to your trusted device just to discover its owner.'},
            {'title': 'Limit harm and prepare to recover', 'body': 'Use only the access needed for a task and share files through an approved access-controlled route. Keep important files backed up in a protected copy you can restore; a backup supports recovery but does not stop every attack. On an unfamiliar public Wi-Fi network, prefer a trusted alternative for sensitive activity. A VPN can protect a tunnel to its endpoint, but does not make a phishing page safe or remove malicious downloads. Choose several complementary safeguards rather than trusting one badge or tool.'},
        ],
        'exercises': [
            {'id': 'https-promise', 'objective': 'CS-B1', 'prompt': 'A sign-in page has HTTPS but came from an unexpected message. What does HTTPS alone establish?',
             'options': ['The site must be the real bank', 'Every download on the page is harmless', 'The connection is encrypted; the site still needs an independent trust check'], 'answer': 2,
             'feedback': ['A fraudulent site can also have HTTPS. Verify the intended service independently.', 'Connection encryption does not assess downloaded files.', 'Correct. Encryption protects transit to that site, not the honesty or identity you intended.']},
            {'id': 'update-route', 'objective': 'CS-B2', 'prompt': 'A pop-up asks you to disable protection to install a “required update”. What should you choose?',
             'options': ['Close it and check the normal app/device update route', 'Disable protection because the warning is urgent', 'Download it first and ask a friend to test it'], 'answer': 0,
             'feedback': ['Correct. Check for a real update using settings or the verified publisher route.', 'Urgency does not justify disabling safeguards for an unverified download.', 'That still downloads and spreads an unverified file. Verify the source first.']},
        ],
    },
]

QUESTIONS = [
    ('CS-P1', 'A message uses a familiar school logo and demands a secret code immediately. Which is the strongest warning sign?', ['The request for a secret under pressure', 'The presence of any school logo', 'The use of complete sentences'], 0, 'Pressure plus a request for an access secret calls for a pause. A logo or polished writing does not authenticate a sender.'),
    ('CS-P1', 'A friend’s usual account sends an unexpected payment request. Which assumption is unsafe?', ['The request still needs checking', 'A familiar account cannot have been compromised', 'Use a known independent contact route'], 1, 'A real account can be taken over. Familiar sender details alone do not prove that the current request is legitimate.'),
    ('CS-P2', 'An email gives a new phone number to confirm its own banking link. What is a safer verification route?', ['Call only the supplied number', 'Reply to the same email', 'Use the official app or previously verified bank contact details'], 2, 'The email’s link and number may share the same source. An independently trusted route avoids that circular check.'),
    ('CS-P2', 'What should you do before opening an unexpected document sent through a class chat?', ['Open it because it is in a class group', 'Verify separately that the sender intended this file', 'Forward it to others to test first'], 1, 'Check the expected file with the sender through a trusted route. Group membership does not guarantee a safe attachment.'),
    ('CS-P2', 'A QR code promises a prize. What makes scanning or following it trustworthy?', ['Being printed on a colourful poster', 'An independent check of the source and intended destination', 'The square shape of the code'], 1, 'A QR code can carry a destination without showing it clearly. Its shape or presentation is not a trust decision.'),
    ('CS-P3', 'You entered a reused password on a suspicious login page. Which response addresses the exposed credentials?', ['Secure the real account and other accounts using that password, then report', 'Wait to see whether money disappears', 'Send the password to a friend for testing'], 0, 'Use official service controls promptly and replace each reused copy with a unique password. Report through an appropriate trusted route.'),
    ('CS-P3', 'You receive a suspicious attachment but have not opened it. What is a proportionate next action?', ['Assume every account has already been lost', 'Report it through the approved method without forwarding the file to friends', 'Open it to collect more evidence'], 1, 'Receiving a file does not establish compromise. Avoid opening it and use the approved reporting process.'),
    ('CS-A1', 'Why does using a different password for email and shopping help after a shopping-site leak?', ['It makes the two websites the same account', 'It means MFA is never useful', 'It limits reuse of that leaked password on the email account'], 2, 'Unique passwords restrict the credential-reuse path; other safeguards still matter.'),
    ('CS-A1', 'What practical problem can a reputable password manager help solve?', ['Generating and keeping different passwords for many accounts', 'Making every downloaded file safe', 'Removing the need to protect the manager account'], 0, 'A manager helps with unique passwords. Its own access must be protected, and it does not inspect every threat.'),
    ('CS-A2', 'Why are two ordinary passwords not normally two authentication factors?', ['Both are the same kind of proof: something you know', 'Two passwords automatically prove possession of a device', 'Factors are just the number of screen pages'], 0, 'MFA combines different types of proof; repeating knowledge-based secrets does not by itself add another type.'),
    ('CS-A2', 'A sign-in approval arrives when you made no login attempt. Which action protects the boundary?', ['Approve it to stop the reminders', 'Give the caller your one-time code', 'Deny it and investigate through the real service'], 2, 'Do not approve or share proof for an unknown sign-in. Review activity through trusted service controls.'),
    ('CS-A2', 'A caller says your one-time login code is needed to cancel a scam. What is the safer choice?', ['Read the code because the caller claims to be support', 'Keep the code private and contact the service independently', 'Post the code in a group for advice'], 1, 'A code may authorize access. The caller’s explanation does not make disclosure safe.'),
    ('CS-A3', 'What is an appropriate way to keep account recovery codes?', ['In a public group message', 'Only on the device you would need them to recover', 'In a protected place separate from that device'], 2, 'Protect recovery codes as access secrets and keep a usable recovery copy separate from the device at risk.'),
    ('CS-A3', 'Your signed-in phone is lost. What should you do from another trusted device?', ['Use official controls to secure accounts and revoke sessions where supported', 'Assume its screen lock has ended every session', 'Publish passwords so someone can help'], 0, 'A device lock and server sessions are different controls. Use supported recovery/sign-out features and report the loss.'),
    ('CS-B1', 'What does HTTPS primarily protect on a website connection?', ['The truth of every statement on the page', 'Data travelling between browser and that site', 'The safety of every file offered'], 1, 'HTTPS protects transit. The intended site and content still require separate trust decisions.'),
    ('CS-B1', 'A fictional service uses school.example. Which displayed host is a different host despite containing those words?', ['school.example', 'The same trusted bookmark', 'school.example.attacker.example'], 2, 'Extra words in a host do not make it the intended service. Use independently verified addresses; these examples are not links to visit.'),
    ('CS-B2', 'Where should you check an urgent browser pop-up claiming a security update is required?', ['By disabling security software first', 'Only through the pop-up download button', 'In normal device/app settings or the verified publisher route'], 2, 'A normal verified update route is independent of the untrusted pop-up. Keep safeguards enabled.'),
    ('CS-B2', 'A simple extension requests access to every page you visit. What should you consider before installing it?', ['Whether that access is necessary and the source is trusted', 'Only whether the icon looks professional', 'Whether every permission can be approved quickly'], 0, 'Permissions determine exposure. Review the need and source, and decline unnecessary access.'),
    ('CS-B3', 'Which statement correctly describes a protected backup you can restore?', ['It stops all phishing attempts', 'It supports recovery after data loss but does not prevent every attack', 'It replaces access controls'], 1, 'A usable backup helps restore data. Prevention and access protection remain separate responsibilities.'),
    ('CS-B3', 'You use a VPN on public Wi-Fi. Which risk still needs a separate decision?', ['Whether a login page is fraudulent or a download is malicious', 'Whether the tunnel alone proves every site trustworthy', 'Whether passwords can now be shared publicly'], 0, 'A VPN protects a tunnel to its endpoint; it does not validate every website or file.'),
]
