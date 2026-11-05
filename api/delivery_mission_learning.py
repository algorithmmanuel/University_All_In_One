"""Secure Code Review v1: fictional credential, pipeline and artifact records.

No real secret is shown, repository history rewritten or release deployed here.
"""
MISSION_ID = 'secure-code-review'
REVISION = 'secure-code-review-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional delivery team respond to a committed credential and preserve the connection between a verified artifact and deployment.',
    'objectives': [
        'Revoke or rotate an exposed credential and assess exposure beyond the current source file.',
        'Enforce policy-based security gates with accountable exception handling.',
        'Deploy the validated immutable artifact and verify required provenance or attestations under a trusted policy.',
    ],
    'workflow': [
        'Inspect every fictional repository, pipeline or release record for the current task.',
        'Select the finding most relevant to credential exposure, gating or artifact identity.',
        'Commit a defensive improvement and read the explanation.',
        'Complete three decisions to save the mission result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Review is separate practice and changes neither the score nor saved completion.',
}
STAGES = [
    {'task': 'Respond to a credential in commit history rather than only erase its latest visible line.',
     'hints': ['A credential can remain usable after the source line is deleted.', 'Revoke/rotate under the response procedure, investigate possible use and copies, and clean up exposure safely without destroying the investigation record.'],
     'artifacts': [
         {'title': 'Visible commit history', 'body': 'A fictional API credential is visible in repository history. Removing its latest line does not necessarily remove earlier commits, clones, logs or other copies. The exercise contains no actual credential.'},
         {'title': 'Scanning alert', 'body': 'Secret scanning flags the exposure. Treat the alert as something to investigate and resolve, not hide. Follow the approved response for evidence handling and safe cleanup of exposed material.'},
         {'title': 'Potentially valid credential', 'body': 'The credential may still be valid. Revoke and rotate it using the authorised service process, update legitimate consumers safely and investigate exposure and usage. Deleting source text alone does not revoke access.'},
     ]},
    {'task': 'Make the required security scanner outcome matter to release approval, while keeping exceptions controlled.',
     'hints': ['A successful pipeline can hide a failed check if that failure was configured to be ignored.', 'Enforce the applicable blocking policy and record approved exceptions with scope and follow-up rather than disable checks.'],
     'artifacts': [
         {'title': 'Ignored scanner failure', 'body': 'The fictional workflow allows the security scanner to continue on error. A failed or unavailable required check can therefore be hidden behind a successful release result. Review the policy and make required outcomes enforceable.'},
         {'title': 'Successful build result', 'body': 'The pipeline still reports success. That describes the configured workflow outcome, not proof that required security checks passed or that the application is secure.'},
         {'title': 'Gate and exception policy', 'body': 'Policy requires a blocking gate for the relevant check. Enforce it and handle exceptions through accountable approval, documented scope and time/review conditions. Review scan coverage too; an enforced scanner is not complete security assurance.'},
     ]},
    {'task': 'Deploy the same artifact that was validated, with the required verification of integrity and provenance.',
     'hints': ['An image tag can be moved to different content after the original validation.', 'Reference the verified digest and check required signatures/attestations against trusted policy; configuration alone is not completed verification.'],
     'artifacts': [
         {'title': 'Validated digest', 'body': 'The fictional team records the content digest of the artifact it validated. Deploying that immutable reference connects the release decision to those specific bytes. A digest identifies content, not whether it is free of vulnerabilities.'},
         {'title': 'Mutable deployment tag', 'body': 'The deployment references the mutable tag latest. That tag could resolve to different content after verification. Use the validated immutable digest rather than assume the tag still names the artifact that passed review.'},
         {'title': 'Signing configuration', 'body': 'Image signing is configured, but the release still needs to verify required signatures and attestations under trusted identity/provenance policy at the applicable boundary. A signature is not proof of harmless content, and merely enabling signing is not proof that deployment enforces verification.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Visibility in commit history means removing the newest line is insufficient. Revoke/rotate the credential, investigate usage and copies, and clean up through a safe response process.',
    'The continue-on-error setting breaks the required scanner gate in this workflow. Enforce the approved blocking policy and manage exceptions rather than interpret a green pipeline as proof of security.',
    'The mutable deployment tag can break the link to the validated artifact. Deploy the recorded digest and verify the required attestations/signatures under policy; signing configuration alone does not settle integrity enforcement.',
]
REVIEW = [
    {'id': 'delivery-secret-history', 'prompt': 'Why is deleting a credential from the newest source file insufficient after it was committed?',
     'options': ['Deleting text automatically revokes the credential', 'Earlier history or copies may retain it, and it may still grant access', 'A scanner alert makes revocation unnecessary'], 'answer': 1,
     'feedback': ['Source editing and service-side revocation are different actions.', 'Correct. Revoke/rotate through the authorised process and assess exposure beyond the latest line.', 'An alert identifies a concern; it does not invalidate the credential.']},
    {'id': 'delivery-green-pipeline', 'prompt': 'A pipeline is green while a required scanner can continue on error. What can the green result prove?',
     'options': ['Every required security check passed', 'All vulnerabilities have been removed', 'Only that the configured workflow allowed success, not that the ignored check passed'], 'answer': 2,
     'feedback': ['An ignored failed check may not affect the final result.', 'A build result does not establish complete vulnerability absence.', 'Correct. Required check outcomes need enforceable gates and reviewable exceptions.']},
    {'id': 'delivery-exception', 'prompt': 'Which handling fits a justified exception to a required release gate?',
     'options': ['Accountable approval with recorded scope and review/time conditions', 'An undocumented permanent bypass', 'Disabling every scan to keep the build green'], 'answer': 0,
     'feedback': ['Correct. Keep exceptions explicit, limited and reviewable under the applicable policy.', 'A hidden permanent bypass undermines the gate and its oversight.', 'Removing the checks is not controlled exception handling.']},
    {'id': 'delivery-mutable-tag', 'prompt': 'Why deploy a validated image digest rather than rely on latest after verification?',
     'options': ['Tags can never change', 'The digest ties deployment to the specific content that was validated', 'A digest guarantees there are no vulnerabilities'], 'answer': 1,
     'feedback': ['A mutable tag can resolve to different content later.', 'Correct. Preserve the link between the reviewed artifact and deployment.', 'Content identity is not a claim that the content is free of vulnerabilities.']},
    {'id': 'delivery-signature-policy', 'prompt': 'Signing is enabled for images. What further assurance still matters?',
     'options': ['Assume every signed image is harmless', 'Skip deployment verification because a setting exists', 'Verify required signatures/attestations against trusted policy at the release boundary'], 'answer': 2,
     'feedback': ['A valid signature does not establish that every behaviour is safe.', 'Configuration alone does not show that verification occurred or was enforced.', 'Correct. Check actual identity/provenance requirements and enforcement rather than only the presence of signing.']},
]
