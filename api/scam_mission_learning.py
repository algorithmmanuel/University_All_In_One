"""Scam Spotter v1: fictional prize, impersonation and marketplace evidence.

No payment, bank contact or live marketplace action is executed by this lesson.
"""
MISSION_ID = 'scam-spotter'
REVISION = 'scam-spotter-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional learner assess an unexpected prize, a claimed bank call and a risky sale.',
    'objectives': [
        'Recognise advance-payment pressure and verify a prize independently.',
        'Keep one-time codes secret and verify a claimed bank contact through a separate trusted route.',
        'Recognise attempts to bypass marketplace protections and decline unsafe deals.',
    ],
    'workflow': [
        'Inspect the claim and each supporting fictional record at the current stage.',
        'Choose the strongest finding for the payment or account risk.',
        'Choose a safe response, commit it and read the finding explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Optional review is ungraded and does not change your saved mission score.',
}
STAGES = [
    {'task': 'Decide how to handle an unexpected prize that requires an urgent upfront fee.',
     'hints': ['Separate the promised reward from what the sender wants you to send now.', 'A small test payment is still a payment. Verify independently before sending money or financial details.'],
     'artifacts': [
         {'title': 'Prize claim', 'body': 'A fictional stranger says the learner won a phone, but the learner recalls no entry. An unexpected prize needs independent verification; the claim alone does not create an obligation to pay.'},
         {'title': 'Delivery fee demand', 'body': 'The sender demands payment before releasing the phone. This advance-payment request is the immediate financial risk. Do not send a small fee to test it or disclose card details. Verify through the claimed organiser’s independently found official channel.'},
         {'title': 'Time pressure', 'body': 'The sender says the prize expires immediately and discourages questions. Slow down. Pressure and a reward can distract from the payment request, and a logo or polished message does not verify the sender.'},
     ]},
    {'task': 'Protect a one-time code when a caller claims to be a bank agent.',
     'hints': ['A caller’s claimed role is not the same as verified identity.', 'A one-time code can authorise access or a transaction. End the call and use a contact route you find separately.'],
     'artifacts': [
         {'title': 'Caller claim', 'body': 'The fictional caller says they work for the bank. A convincing voice or displayed caller name does not independently establish that identity.'},
         {'title': 'One-time code', 'body': 'The caller asks the learner to read a one-time code aloud. The code protects sign-in or another sensitive action. Keep it private: reading it aloud or sending a screenshot exposes the same access secret.'},
         {'title': 'Separate bank contact', 'body': 'The learner can end the call and contact the bank using its official app, verified card contact details or another independently trusted route. Do not rely solely on a new number supplied by the caller.'},
     ]},
    {'task': 'Choose whether to proceed when a seller avoids the marketplace’s payment and delivery safeguards.',
     'hints': ['A low price is not compensation for losing the safeguards you intended to use.', 'Use the marketplace’s applicable protections and verify the transaction terms; decline if the seller insists on bypassing them.'],
     'artifacts': [
         {'title': 'Off-platform request', 'body': 'A fictional seller insists on direct payment outside the marketplace. That may remove the platform’s applicable payment or dispute protections. Use verified platform procedures or decline the deal; no platform guarantees that every transaction is safe.'},
         {'title': 'Delivery uncertainty', 'body': 'The seller offers no verified delivery or collection arrangement. Resolve the terms through trusted platform processes before committing. A receipt screenshot alone does not establish that an item exists or will arrive.'},
         {'title': 'Unusually low price', 'body': 'The price is far below comparable offers. It is a reason to scrutinise the deal, not conclusive proof by itself. Never share an account password to let a seller arrange a purchase for you.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The demanded upfront fee is the immediate risk: the learner is being asked to pay before an independently verified prize exists. An unsolicited claim and urgency reinforce the need to stop and verify.',
    'The one-time code is the access secret the caller wants. Protect it regardless of the caller’s story and verify through a separate trusted bank contact.',
    'Avoiding platform protections changes the transaction’s safeguards. Uncertain delivery and a low price add context, but bypassing protections is the central finding for this decision.',
]
REVIEW = [
    {'id': 'scam-test-payment', 'prompt': 'Why is sending a small delivery fee a poor way to test an unexpected prize?',
     'options': ['Small transfers are always reversible', 'It exposes money before the claim has been independently verified', 'Paying proves that the organiser exists'], 'answer': 1,
     'feedback': ['Do not assume a transfer can be recovered.', 'Correct. A test payment still gives money to an unverified recipient.', 'Receiving a payment does not verify a recipient’s prize claim.']},
    {'id': 'scam-screenshot', 'prompt': 'A claimed bank caller says a screenshot of the one-time code is safer than reading it aloud. What is true?',
     'options': ['A screenshot removes the code’s value', 'A caller’s title makes sharing safe', 'Both methods reveal the access secret'], 'answer': 2,
     'feedback': ['The code remains visible and potentially usable.', 'A claimed title does not authorise receiving your code.', 'Correct. Keep the code private and use an independently trusted bank route.']},
    {'id': 'scam-contact-route', 'prompt': 'After ending a suspicious bank call, which contact route is more reliable?',
     'options': ['The bank’s independently verified app or contact details', 'Only the new number the caller supplied', 'A reply to the caller’s message asking whether they are genuine'], 'answer': 0,
     'feedback': ['Correct. A separately trusted route avoids asking the same source to authenticate itself.', 'That number may be controlled by the same caller.', 'The caller can simply repeat the claim. Verify separately.']},
    {'id': 'scam-platform', 'prompt': 'A seller demands direct payment outside the marketplace. Which issue matters most?',
     'options': ['The seller used short sentences', 'Applicable payment and dispute protections may be bypassed', 'Every low-cost item is necessarily fake'], 'answer': 1,
     'feedback': ['Writing style does not establish transaction safeguards.', 'Correct. Follow verified platform procedures or decline the deal if the seller refuses them.', 'Price is a signal to assess, not proof about every item.']},
    {'id': 'scam-urgency', 'prompt': 'A prize sender says independent checking will make you lose the offer. What should you do?',
     'options': ['Pay before thinking about it', 'Send card details instead of money', 'Pause and verify or decline rather than let pressure decide'], 'answer': 2,
     'feedback': ['The deadline is part of the pressure; it does not verify the offer.', 'Card details are also sensitive and do not resolve the unverified claim.', 'Correct. Losing an unverified offer is preferable to exposing money or financial information under pressure.']},
]
