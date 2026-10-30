"""Digital citizenship: audience, consent, privacy and respectful participation.

Distinct from the technical cyber-safety bank. Scenarios are fictional; exercises
never ask for a learner's address, school, contacts, credentials or real incident.
"""
REVISION = 'digital-citizenship-v1'
COURSE_TITLE = 'Digital Citizenship Essentials'
ACADEMY_ID = 'secondary'
MARKER = 'educyber.lesson:' + REVISION + ':'

LESSONS = [
    {
        'key': 'footprint', 'title': 'Your digital footprint',
        'legacy_content': 'Online posts can persist. Think before sharing information about yourself or others.',
        'objectives': [
            {'id': 'DC-F1', 'text': 'Explain how online actions leave records and copies.'},
            {'id': 'DC-F2', 'text': 'Choose an appropriate audience and seek consent before sharing about others.'},
            {'id': 'DC-F3', 'text': 'Pause and check a claim before forwarding or publishing it.'},
        ],
        'sections': [
            {'title': 'Actions leave a trail', 'body': 'Your digital footprint is the record left by online activity: a post, comment, photo, message or other interaction. A message intended for a small group can be copied or shown elsewhere. Deleting your original post may reduce exposure, but does not guarantee that every screenshot or saved copy disappears. Think about what someone could learn from the whole trail, not just one post.'},
            {'title': 'Worked scenario: celebrating an award', 'body': 'Emeka wants to post an award photo. The picture also shows his friend, a school badge and a certificate number. He first asks whether his friend wants the photo shared. They choose a version that hides identifying details and an audience appropriate for the celebration. Consent to take a photo is not automatically consent to publish it; a celebration does not need every detail of the certificate.'},
            {'title': 'Choose the audience before posting', 'body': 'Ask who needs to see this and whether you would be comfortable if it reached a wider audience. A private group is not a promise that nobody can copy a post. Avoid publishing another person’s location, contact information or embarrassing moment without permission. You can change your mind about your own post and ask for unwanted copies to be removed, while recognising that removal may not be complete.'},
            {'title': 'Pause before you pass it on', 'body': 'A dramatic claim in a class group is not confirmed just because many people forward it. Check its original source, date and context through a reliable independent route. An old notice can be misleading when shared as today’s news. If you cannot establish that a claim is reliable, do not present it as fact or forward it merely “just in case”. Correct a mistaken post and tell the people you shared it with.'},
        ],
        'exercises': [
            {'id': 'award-photo', 'objective': 'DC-F2', 'prompt': 'Your award photo includes a friend and an identity number. What is a thoughtful publishing choice?',
             'options': ['Post the original because awards are good news', 'Ask the friend, hide identifying details and choose an appropriate audience', 'Tag everyone so the photo spreads faster'], 'answer': 1,
             'feedback': ['Good news can still expose someone’s information. Check consent and what the photo reveals.', 'Correct. The celebration can be shared without assuming permission or exposing unnecessary identifying details.', 'Wider distribution increases exposure; it does not solve consent or privacy.']},
            {'id': 'old-notice', 'objective': 'DC-F3', 'prompt': 'A forwarded school-closure notice has no clear date or source. What should you do before spreading it?',
             'options': ['Forward it because many people have', 'Add “confirmed” to help classmates decide', 'Check the current official school notice through a trusted route'], 'answer': 2,
             'feedback': ['Repeated sharing is not independent confirmation. Check the source and date.', 'Adding a label cannot establish that the notice is current or genuine.', 'Correct. Verify the current source and date. If uncertain, do not spread the claim as established fact.']},
        ],
    },
    {
        'key': 'privacy', 'title': 'Privacy basics',
        'legacy_content': 'Limit sharing of personal details, review privacy settings and ask a trusted adult when uncertain.',
        'objectives': [
            {'id': 'DC-P1', 'text': 'Identify personal information and share only what a task genuinely needs.'},
            {'id': 'DC-P2', 'text': 'Use audience and permission settings without treating them as guarantees.'},
            {'id': 'DC-P3', 'text': 'Choose trusted help when information is requested or exposed unexpectedly.'},
        ],
        'sections': [
            {'title': 'Notice what identifies you', 'body': 'Personal information can identify or reveal something about a person: a full name, home address, phone number, school, exact location or identity document. Several small details can reveal more when combined. A public comment or profile usually does not need your home address or daily timetable. Use fictional details in learning exercises; do not put your own private information into an example.'},
            {'title': 'Worked scenario: a group study form', 'body': 'A class organiser needs to know which study session students can attend. A form also asks for a home address and a photo of an identity document, with no explanation. Ada does not submit those extra details. She checks with a trusted teacher through an established route and asks whether a session choice alone is enough. Sharing only information genuinely needed is called data minimisation.'},
            {'title': 'Settings help you choose access', 'body': 'Review who can see your profile, contact you, tag you or view a post. The exact setting names differ across services. Restrict access to the intended audience and check after an update or change. Review device/app permissions too: a study timer may not need your contacts or precise location. You can deny unnecessary access. Privacy settings reduce exposure, but another person may still copy information they can see.'},
            {'title': 'You can stop and ask for help', 'body': 'An online stranger does not gain a right to private details by claiming to be a friend, sponsor or school official. If a request feels pressured or confusing, pause, do not send the information, and ask a trusted adult or appropriate support contact using an established route. If private information was posted by mistake, limit/remove the post where possible, report unwanted exposure and seek help. Do not respond by publishing more identifying details to explain it.'},
        ],
        'exercises': [
            {'id': 'study-form', 'objective': 'DC-P1', 'prompt': 'A study-session poll asks publicly for your home address. Which response best limits unnecessary exposure?',
             'options': ['Ask a trusted organiser why it is needed and provide only an appropriate session choice', 'Post your address so others can copy the form', 'Send an identity document instead of an address'], 'answer': 0,
             'feedback': ['Correct. Check the purpose and share only what is genuinely needed through an appropriate route.', 'A public address is unnecessary for choosing a session and creates avoidable exposure.', 'An identity document reveals more information, not less. Check the request before sharing.']},
            {'id': 'timer-permission', 'objective': 'DC-P2', 'prompt': 'A simple study timer asks for precise location and all contacts. What should you consider?',
             'options': ['Every permission is harmless if an app is free', 'Whether those permissions are needed; deny unnecessary access', 'Grant access first and post your location to test it'], 'answer': 1,
             'feedback': ['Price does not explain why access is necessary. Review the purpose of each permission.', 'Correct. Match permissions to the task and decline access the timer does not reasonably need.', 'That exposes more information. You can review or refuse access without publishing it.']},
        ],
    },
    {
        'key': 'respect', 'title': 'Respectful online conduct',
        'legacy_content': 'Communicate respectfully, avoid cyberbullying and report threatening behaviour.',
        'objectives': [
            {'id': 'DC-R1', 'text': 'Recognise harmful online conduct and avoid amplifying it.'},
            {'id': 'DC-R2', 'text': 'Choose safe support, blocking and reporting actions.'},
            {'id': 'DC-R3', 'text': 'Disagree respectfully and acknowledge other people’s work.'},
        ],
        'sections': [
            {'title': 'A real person reads the message', 'body': 'Repeated insults, threats, humiliating posts, impersonation and sharing private information can harm someone online. Calling something a joke does not cancel the harm. Do not join a pile-on, react to encourage it or forward an embarrassing screenshot. Disagree with an idea without attacking a person. It is possible to challenge a claim while using calm words and evidence.'},
            {'title': 'Worked scenario: a class-group pile-on', 'body': 'A classmate’s mistake becomes a series of mocking posts. Emeka does not forward the screenshot or add a laughing reaction. He checks privately whether the classmate wants support and asks a trusted teacher for help. If safe and appropriate, ordinary message details can be kept privately for a report; they should not be spread around the class. The targeted person is not to blame and does not have to handle it alone.'},
            {'title': 'Get support without spreading the harm', 'body': 'Use available platform reporting and blocking controls and talk to someone you trust, such as a parent, caregiver, teacher or counsellor. If collecting evidence would put you at risk, seek help rather than doing it alone. Blocking can limit contact; reporting tells the service about the problem. A threat to immediate safety needs urgent help from a trusted person and appropriate local emergency support. Do not arrange a confrontation or retaliate with someone’s private information.'},
            {'title': 'Respect also includes credit and repair', 'body': 'When discussing a different opinion, address the point and explain your reason instead of insulting the author. Use material you are allowed to reuse and acknowledge its source as appropriate; credit alone does not mean you have permission for every use. Do not submit a classmate’s work as your own. If you posted something hurtful or inaccurate, remove/correct it where possible, acknowledge the mistake and avoid repeating the harm in your apology.'},
        ],
        'exercises': [
            {'id': 'group-pile-on', 'objective': 'DC-R1', 'prompt': 'A class group is repeatedly mocking someone. Which action supports the person without widening the harm?',
             'options': ['Forward the posts to another group for entertainment', 'Add laughing reactions but avoid typing', 'Do not amplify it; offer support privately and seek trusted help'], 'answer': 2,
             'feedback': ['Forwarding gives the harmful posts a wider audience.', 'Reactions can encourage the pile-on even without another message.', 'Correct. Avoid spreading the content, support the person and involve appropriate trusted help.']},
            {'id': 'respectful-reply', 'objective': 'DC-R3', 'prompt': 'You disagree with a classmate’s explanation. Which reply addresses the idea respectfully?',
             'options': ['“I read it differently; can we compare the examples?”', '“You are too stupid to understand this.”', 'Post the classmate’s private details to win the argument'], 'answer': 0,
             'feedback': ['Correct. You invite discussion of the evidence without attacking the person.', 'An insult targets the person instead of explaining your reason.', 'Private information is not a debating tool. Do not expose it to pressure someone.']},
        ],
    },
]

QUESTIONS = [
    ('DC-F1', 'What is an example of a digital footprint from everyday online participation?', ['A comment you leave in a discussion', 'Only the physical size of your phone', 'Only a password you never use online'], 0, 'Posts, messages and other online interactions can leave records. A footprint is broader than a single device detail.'),
    ('DC-F1', 'You delete an embarrassing post. What can you reasonably conclude?', ['Every screenshot elsewhere must disappear too', 'The original may be removed, but other people may retain copies', 'The post can never have been seen'], 1, 'Deletion can reduce exposure without erasing every saved or copied version.'),
    ('DC-F2', 'A friend agrees to be in a photo. What should you check before publishing it?', ['Whether the friend also agrees to that sharing and audience', 'Whether a popular filter removes the need for consent', 'Whether enough people have already been tagged'], 0, 'Permission to take a photo is not automatically permission to publish it. Check the intended sharing.'),
    ('DC-F2', 'Why is a private class group not a complete guarantee of privacy?', ['Group members cannot ever copy text', 'The word private prevents screenshots', 'A member may copy or show a post elsewhere'], 2, 'An access setting limits an audience, but a person who can see content may still copy it.'),
    ('DC-F2', 'An award photo reveals an identity number and another person. Which revision best reduces avoidable exposure?', ['Keep all details because the achievement is positive', 'Hide identifying details, check consent and choose the audience', 'Publish the home address as extra context'], 1, 'A celebration can keep its meaning without disclosing unnecessary information or assuming another person’s permission.'),
    ('DC-F3', 'A school notice is being forwarded with no reliable source or date. Which check matters before sharing?', ['The number of times it was forwarded', 'Whether its headline is dramatic', 'Its original source, date and current context'], 2, 'Popularity and dramatic language do not establish that a notice is current and reliable.'),
    ('DC-F3', 'You discover that a claim you posted was wrong. What is a responsible response?', ['Correct it and notify the people you shared it with', 'Keep repeating it to avoid embarrassment', 'Label it confirmed without evidence'], 0, 'Repair includes correcting the record and helping the earlier audience understand the mistake.'),
    ('DC-P1', 'Which detail normally deserves protection in a public study-group profile?', ['A general interest in science', 'Your home address and daily travel timetable', 'A fictional example name used in an exercise'], 1, 'An address combined with a timetable can reveal where someone lives and when they travel. A public study profile rarely needs that.'),
    ('DC-P1', 'What does sharing only information genuinely needed for a task mean?', ['Data minimisation', 'Sending every available document', 'Publishing the same details in more places'], 0, 'Data minimisation limits disclosure to the purpose instead of collecting or spreading extra identifying details.'),
    ('DC-P1', 'A session-choice form requests a public identity-document photo without an explanation. What should you do?', ['Supply it automatically because it is a form', 'Ask a trusted organiser about the purpose and avoid unnecessary disclosure', 'Post a second identity document to be helpful'], 1, 'Check the need through a trusted route before providing sensitive information. More documents do not make the request appropriate.'),
    ('DC-P2', 'A study app requests contacts it does not need for its task. Which decision matches privacy-aware use?', ['Allow it because the app is free', 'Publish contacts yourself to save time', 'Deny unnecessary access or choose a suitable alternative'], 2, 'App permissions should match a real need. Free access does not justify every data request.'),
    ('DC-P2', 'What can audience settings help you control?', ['Who can view or contact you through the service', 'Whether every viewer can be prevented from taking a copy', 'Whether a rumour becomes true'], 0, 'Settings can restrict access and contact. They do not guarantee that visible content cannot be copied or that a claim is correct.'),
    ('DC-P3', 'Someone online pressures you for private details while claiming to represent your school. What is a safe first response?', ['Send the details before the deadline', 'Post the request together with your address', 'Pause and verify with a trusted adult or school contact through an established route'], 2, 'A claimed role does not establish authority. Stop and check without revealing the requested details.'),
    ('DC-P3', 'Your private contact details were posted by mistake. What reduces further exposure?', ['Limit/remove the post where possible, report unwanted sharing and seek trusted help', 'Publish more private details to explain the mistake', 'Ask everyone to forward the post so they can warn others'], 0, 'Reduce distribution and use support/reporting channels. Spreading the original information further can worsen exposure.'),
    ('DC-R1', 'Repeated mocking posts target a classmate. What is a helpful bystander response?', ['Add reactions to fit in', 'Do not amplify the posts; offer support and seek appropriate help', 'Forward screenshots for entertainment'], 1, 'Bystanders can reduce harm by not rewarding or spreading it and helping the person reach support.'),
    ('DC-R1', 'A hurtful post is described as “only a joke”. What is the best reason to reconsider sharing it?', ['A joke label guarantees nobody is harmed', 'More shares always solve a conflict', 'The effect on the targeted person matters, not just the label'], 2, 'Calling a post a joke does not erase its impact. Avoid amplifying humiliating or threatening content.'),
    ('DC-R2', 'If safe and appropriate, how should ordinary message details needed for a report be handled?', ['Keep them privately for a trusted reporting route', 'Share them in every class group', 'Use them to threaten the other person'], 0, 'Evidence can support a report without broadening the audience for harmful material. Seek help if saving it would create risk.'),
    ('DC-R2', 'Which combination can help when unwanted online contact continues?', ['Retaliate with private details', 'Use platform block/report controls and talk to a trusted adult', 'Arrange a confrontation alone'], 1, 'Blocking can limit contact, reporting raises the issue with the service, and trusted support helps you respond safely.'),
    ('DC-R3', 'Which reply challenges an explanation without attacking its author?', ['“You are useless at this.”', '“I will share your private messages unless you agree.”', '“Here is a different example; can we compare the results?”'], 2, 'A respectful disagreement addresses reasons and evidence. Insults or threats target the person.'),
    ('DC-R3', 'You want to include someone else’s image in a school project. Which plan respects their work?', ['Assume being online permits every use', 'Check that the use is allowed and acknowledge the source as appropriate', 'Remove the creator’s name and claim you made it'], 1, 'Use material you are allowed to reuse and give appropriate credit. Attribution alone is not permission for every use.'),
]
