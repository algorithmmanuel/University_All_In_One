"""Zero Trust Briefing v1: fictional device posture, workload and emergency access.

No identity, policy, workload token or emergency account is operated here.
"""
MISSION_ID = 'zero-trust-briefing'
REVISION = 'zero-trust-briefing-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional architect assess privileged access and service identity while preserving controlled emergency access.',
    'objectives': [
        'Combine strong authentication and relevant device posture for privileged access instead of relying on location alone.',
        'Use scoped supported workload identities and manage remaining secrets deliberately.',
        'Test and monitor narrowly controlled emergency access rather than disable the general policy.',
    ],
    'workflow': [
        'Read the design task and inspect every fictional account, service or pilot record.',
        'Choose the finding most relevant to the access-design gap.',
        'Commit a scoped design recommendation and read the explanation.',
        'Finish three decisions to save the mission result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Optional review is practice only, with no saved grade or change to mission points.',
}
STAGES = [
    {'task': 'Improve privileged production access that currently permits unmanaged laptops.',
     'hints': ['Being on an office network does not prove the device or session meets the access requirements.', 'Use strong authentication and justified device-posture conditions, then test the effective access decision.'],
     'artifacts': [
         {'title': 'Privileged access', 'body': 'The fictional administrator has production privileges. Such access needs an appropriately scoped and verified access design; sharing the administrator password would weaken accountability and protection.'},
         {'title': 'Unenforced device posture', 'body': 'Production access is possible from any unmanaged laptop because device compliance is not enforced. Require relevant approved posture alongside strong authentication rather than use office-network location alone as a trust decision.'},
         {'title': 'Available access controls', 'body': 'Conditional access is available in this scenario. Design and test the relevant identity, device and access conditions, including expected authorised use. A configured control is not proof that every future session is safe.'},
     ]},
    {'task': 'Replace a long-lived shared service secret with a more scoped supported workload identity design.',
     'hints': ['A shared secret can make separate services depend on the same access material.', 'Use supported workload identities with least privilege and lifecycle controls, and rotate remaining secrets rather than assume an identity feature removes all credentials.'],
     'artifacts': [
         {'title': 'Shared service secret', 'body': 'Several fictional services share a long-lived secret. Exposure or rotation can affect more than one consumer, and attribution is harder than with distinct appropriately scoped identities. Do not distribute the secret further.'},
         {'title': 'Missing rotation record', 'body': 'No rotation record is available. Inventory legitimate consumers and manage the remaining secret’s replacement, permissions and verification through the approved process rather than leave it indefinitely or disable service logs.'},
         {'title': 'Supported workload identity', 'body': 'A managed workload identity option is supported in this case. Use appropriately scoped identities and permissions, validate which workload may obtain and use access, and manage token/credential lifecycle as applicable. Workload identity does not automatically provide correct authorisation or remove every remaining secret.'},
     ]},
    {'task': 'Handle a legitimate emergency workflow affected by the pilot without allowing all unmanaged devices permanently.',
     'hints': ['A pilot finding should lead to a controlled design adjustment, not indiscriminate removal of the policy.', 'Define accountable emergency access with narrow scope, suitable safeguards, testing and monitoring.'],
     'artifacts': [
         {'title': 'Pilot enforcement', 'body': 'The fictional pilot denies unmanaged devices as intended. Test expected authorised access as well as blocking behaviour. The result does not mean every exception should be granted or that the policy must be abandoned.'},
         {'title': 'Emergency workflow', 'body': 'One approved emergency workflow needs an exception. Define who may use it, under what conditions, with what safeguards and review. Keep scope and accountability tight rather than allow all devices permanently or distribute emergency credentials widely.'},
         {'title': 'Available audit events', 'body': 'Audit events support testing and oversight of emergency access. Monitor use, verify the approved process and review exceptions or access after use. A documented emergency path should be tested, not merely assumed to work when needed.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Unenforced device compliance is the gap in this privileged-access scenario. Combine relevant posture with strong authentication and test effective access rather than trust location alone.',
    'The supported workload identity option enables a scoped design instead of propagating a shared long-lived secret. Review authorisation and lifecycle, and rotate any remaining secrets with consumer coordination.',
    'The legitimate emergency need calls for a narrow, accountable tested exception. It does not justify disabling every policy or permanently admitting all devices; retain monitoring and review.',
]
REVIEW = [
    {'id': 'zt-location-limit', 'prompt': 'Why is office-network location alone insufficient for the privileged laptop scenario?',
     'options': ['Every office device is automatically compliant', 'Location does not establish device posture or session legitimacy', 'Strong authentication removes all need to review access'], 'answer': 1,
     'feedback': ['Being on that network does not demonstrate compliance.', 'Correct. Evaluate the relevant identity and device conditions rather than rely on location alone.', 'Authentication is one part of the access decision and still needs effective policy.']},
    {'id': 'zt-shared-secret', 'prompt': 'What is a concern with one long-lived secret shared by several services?',
     'options': ['It always gives perfect per-service accountability', 'It makes rotation irrelevant', 'Exposure or replacement can affect several consumers and blur attribution'], 'answer': 2,
     'feedback': ['Shared access material can make it harder to attribute activity to a specific consumer.', 'A secret still needs lifecycle management and safe replacement.', 'Correct. Use appropriately scoped supported identities and coordinate remaining secret management.']},
    {'id': 'zt-workload-scope', 'prompt': 'What remains important after adopting a supported workload identity?',
     'options': ['Appropriate authorisation scope and lifecycle verification', 'Assuming every permission is now correct', 'Removing service audit records'], 'answer': 0,
     'feedback': ['Correct. A supported identity mechanism does not automatically make its permissions or access conditions appropriate.', 'Identity features do not justify excessive permissions.', 'Audit records remain useful for verification and incident assessment.']},
    {'id': 'zt-emergency-design', 'prompt': 'A pilot blocks one approved emergency workflow. Which rollout response is sound?',
     'options': ['Disable all access policy', 'Define a narrow accountable emergency path, test it and monitor use', 'Allow every unmanaged device forever'], 'answer': 1,
     'feedback': ['One legitimate exception does not invalidate all policy requirements.', 'Correct. Preserve the intended controls while addressing the documented need with safeguards.', 'A permanent blanket bypass is much broader than the emergency requirement.']},
    {'id': 'zt-emergency-assurance', 'prompt': 'Why test and monitor emergency access before relying on it?',
     'options': ['Documentation guarantees it works and is never misused', 'Emergency activity needs no accountability', 'The path must be both usable when authorised and visible for oversight'], 'answer': 2,
     'feedback': ['A written design alone does not establish operational behaviour.', 'Emergency access still needs accountable use and review.', 'Correct. Verify the behaviour and retain evidence of how exceptional access is used.']},
]
