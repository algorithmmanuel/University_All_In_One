"""Wi-Fi Wise v1: fictional network choices and browser connection warnings.

No network is joined, credentials entered or certificate warning bypassed here.
"""
MISSION_ID = 'wifi-wise'
REVISION = 'wifi-wise-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional learner choose a connection and reach a school service safely.',
    'objectives': [
        'Verify an offered network rather than trust its name or signal strength.',
        'Distinguish HTTPS transit protection from proof that a site is honest.',
        'Stop at certificate warnings and verify through a trusted route before sharing secrets.',
    ],
    'workflow': [
        'Inspect each fictional network, browser or session record for the current stage.',
        'Select the finding that best explains the connection risk.',
        'Choose a safer next action, commit it and read the explanation.',
        'Complete three stages to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save your mission result. Optional review is practice only and does not change the saved score.',
}
STAGES = [
    {'task': 'Choose how to verify the cafe’s network before connecting to a lookalike hotspot.',
     'hints': ['Anyone controlling a hotspot can choose a convincing network name.', 'Ask staff for the official network details rather than using signal strength as proof of identity.'],
     'artifacts': [
         {'title': 'Unverified network', 'body': 'Two fictional free networks use similar cafe names. One is unverified. A name that sounds official is not proof of who controls the network.'},
         {'title': 'Staff confirmation', 'body': 'The learner can ask cafe staff to confirm the official network and connection procedure. This is a better first check than guessing from a name, though confirmation does not make every activity on a public network risk-free.'},
         {'title': 'Lookalike hotspot', 'body': 'A hotspot can copy a familiar name. A stronger signal does not prove legitimacy. Do not enter banking or school credentials simply to test a network; choose a trusted alternative connection if uncertain.'},
     ]},
    {'task': 'Reach the intended school service with appropriate connection and shared-device safeguards.',
     'hints': ['Check which service you reached, not just whether the connection is encrypted.', 'Use a previously verified school address or official app; avoid unnecessary sensitive activity and end any shared-device session.'],
     'artifacts': [
         {'title': 'HTTPS protection', 'body': 'HTTPS helps protect traffic between the browser and the site it connects to. A fraudulent site can also use HTTPS. Reach the intended school through an independently trusted address or app, and do not bypass browser warnings.'},
         {'title': 'Shared-device session', 'body': 'A shared device can retain a signed-in session. Sign out and end the session when finished. Network encryption does not prevent the next device user from using an account left open.'},
         {'title': 'Sensitive activity', 'body': 'On an unfamiliar public connection, avoid unnecessary sensitive actions and prefer a trusted alternative where available. A VPN can protect traffic in a tunnel to its endpoint, but it does not make a fraudulent site honest or an unsafe download harmless.'},
     ]},
    {'task': 'Handle an unverified certificate warning before entering a password.',
     'hints': ['A warning means a connection check failed; do not teach yourself to ignore it.', 'Stop, verify the intended service and use a trusted alternative route or support rather than submitting a secret through the warning.'],
     'artifacts': [
         {'title': 'Browser warning', 'body': 'The fictional browser says it cannot verify the site’s certificate. Do not click through automatically or enter a password to see whether the page works.'},
         {'title': 'Uncertain connection identity', 'body': 'The warning means the browser could not establish the expected connection assurances. It does not by itself prove an attacker is present, but it is not a safe basis for submitting secrets. Stop and verify the site or connection.'},
         {'title': 'Trusted alternative', 'body': 'Use an independently verified address and a trusted alternative connection or contact school IT through a known route. If the warning persists, seek help rather than bypass it. No real browser setting is changed in this lesson.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The unverified network name is the unresolved trust issue. Staff confirmation or a trusted alternative is preferable to choosing by name similarity or signal strength.',
    'HTTPS helps protect transit, which matters on this connection, but does not establish the honesty of the intended site. Combine a verified destination with careful sensitive activity and session handling.',
    'The failed certificate check leaves connection assurances uncertain. Stop and verify through a trusted route; neither blind bypass nor immediate claims of an attacker fit the evidence.',
]
REVIEW = [
    {'id': 'wifi-network-name', 'prompt': 'Two cafe hotspots have similar names. Why not simply choose the stronger signal?',
     'options': ['Strong signals always belong to the cafe', 'Signal strength does not establish who operates the hotspot', 'Any network with cafe in its name is official'], 'answer': 1,
     'feedback': ['Strength describes reception, not who controls the network.', 'Correct. Confirm the official network with staff or use a trusted alternative.', 'Network names can be chosen or copied by other operators.']},
    {'id': 'wifi-https-limit', 'prompt': 'What does HTTPS on a page establish about the connection, rather than the honesty of the site?',
     'options': ['The page cannot be fraudulent', 'Every file on it is safe', 'It helps protect data in transit to the site reached; the intended destination still needs checking'], 'answer': 2,
     'feedback': ['Fraudulent pages can also use HTTPS.', 'Transit protection does not assess whether every download is safe.', 'Correct. Verify the service independently as well as respecting connection safeguards.']},
    {'id': 'wifi-warning', 'prompt': 'A certificate warning appears on a school login page. What should the learner do before entering a password?',
     'options': ['Stop and verify the site/connection through a trusted route or support', 'Click through because the page has a school logo', 'Submit the password to test whether login succeeds'], 'answer': 0,
     'feedback': ['Correct. Do not submit secrets through an unresolved warning.', 'A copied logo does not resolve a failed certificate check.', 'Testing with a password exposes a secret before trust is established.']},
    {'id': 'wifi-session', 'prompt': 'Why still sign out on a shared computer even when the school page uses HTTPS?',
     'options': ['HTTPS automatically ends every login', 'Transit encryption does not prevent reuse of a session left open on the device', 'Signing out disables the network'], 'answer': 1,
     'feedback': ['Connection encryption does not automatically end the authenticated session.', 'Correct. Protect the device-side session as well as the network traffic.', 'Signing out ends account access; it does not disable the network.']},
    {'id': 'wifi-vpn-limit', 'prompt': 'A learner uses a VPN on public Wi-Fi. Which assumption remains unsafe?',
     'options': ['The intended website still needs verification', 'Downloads still need a trustworthy source', 'Every page is honest because a VPN is connected'], 'answer': 2,
     'feedback': ['Verification remains necessary, even when using a VPN.', 'A VPN does not establish that a downloaded file is safe.', 'Correct. A VPN tunnel does not make a fraudulent destination honest.']},
]
