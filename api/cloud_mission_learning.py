"""Cloud Perimeter v1: fictional storage exposure, identity grants and impact review.

No student records are retrieved, copied or exposed during this exercise.
"""
MISSION_ID = 'cloud-perimeter'
REVISION = 'cloud-perimeter-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional cloud team contain a student-record storage exposure and assess what remains unknown.',
    'objectives': [
        'Prioritise exposed personal information and restrict public access under the approved response.',
        'Replace anonymous broad grants with access scoped to justified identities and needs.',
        'Distinguish restoring privacy settings from establishing data-access impact and preventive assurance.',
    ],
    'workflow': [
        'Read the storage task and inspect every fictional inventory, policy or response record.',
        'Choose the finding most relevant to the current protection or assurance decision.',
        'Commit a defensive recommendation and read the explanation.',
        'Complete three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Optional review is separate practice with no saved grade or change to that score.',
}
STAGES = [
    {'task': 'Prioritise an apparently public storage location containing student records without copying the exposed data.',
     'hints': ['Consider both the access setting and the sensitivity of what is stored.', 'Use the approved response to restrict public exposure while preserving relevant access evidence and involving the owner.'],
     'artifacts': [
         {'title': 'Public access setting', 'body': 'The fictional storage inventory shows a public-access flag. Validate the effective exposure through the approved process; a single inventory field may not describe every control. Do not download records or publish a link to demonstrate the concern.'},
         {'title': 'Personal information', 'body': 'The dataset is described as student records containing personal information. Its sensitivity makes potential public readability urgent to assess and contain. Restrict public access through the approved response, preserve logs and do not copy the data to another public location.'},
         {'title': 'Identified owner', 'body': 'The bucket owner is known. Involve the responsible owner and response team to protect the data, maintain needed authorised access and assess scope. Do not wait for an external complaint before addressing the exposure.'},
     ]},
    {'task': 'Replace a broad anonymous read policy with justified access to approved identities.',
     'hints': ['Identify who receives the grant as well as what actions it permits.', 'Remove the public grant, scope identity/resource/action permissions to the need and verify effective access across relevant controls.'],
     'artifacts': [
         {'title': 'Anonymous principal', 'body': 'The fictional policy grants a wildcard principal broad read access. In this scenario that includes anonymous readers. Remove public grants and identify which approved identities actually need access; a wildcard must be interpreted in its full policy context.'},
         {'title': 'Read scope', 'body': 'The read action applies broadly to the storage contents. Limit resources and actions to the justified need. Making the location writable or disabling monitoring would increase exposure rather than correct the read policy.'},
         {'title': 'Least-privilege check', 'body': 'Apply least privilege and verify effective access, including other relevant policies or sharing controls. A policy edit alone is not proof that every public access path is gone. Check that required authorised access still works through an approved test without exposing real records.'},
     ]},
    {'task': 'Complete an evidence-based impact assessment after public access is removed.',
     'hints': ['Making the location private again changes current exposure, not what happened earlier.', 'Assess the exposure window and available access evidence, involve responsible teams and test prevention without assuming zero impact.'],
     'artifacts': [
         {'title': 'Exposure window', 'body': 'The fictional team identifies when the storage was exposed. Use that window to scope the access review and record how it was established, including any uncertainty.'},
         {'title': 'Retained access records', 'body': 'Relevant access logs are preserved. Review their coverage and what they show about the exposure window. Retained logs support investigation but may not record every access path; do not delete them after changing the policy.'},
         {'title': 'Impact not established', 'body': 'The location is private again, but the effect of earlier access remains unknown. Assess evidence and limits, notify the responsible incident/privacy teams under the applicable process and test preventive controls. Restoration alone does not prove no one read the data.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The personal information raises the consequence of public readability. Contain through the approved response and retain evidence; copying the records publicly or waiting for a complaint would add risk.',
    'The anonymous wildcard principal is the broad grant needing correction in this policy. Scope justified access and verify effective permissions, not only the edited text.',
    'Unknown data-access impact remains an assurance gap after access is restricted. Assess the window and logs with responsible teams and test prevention rather than assume no impact.',
]
REVIEW = [
    {'id': 'cloud-exposure-priority', 'prompt': 'A storage location may publicly expose student records. What should the team prioritise?',
     'options': ['Copying records into another public bucket', 'Approved exposure restriction with evidence preservation and owner involvement', 'Waiting until an outsider complains'], 'answer': 1,
     'feedback': ['Copying into another public location spreads the exposure.', 'Correct. Protect the data through the response process and preserve evidence for assessment.', 'A known potential exposure needs prompt assessment, not reliance on a later complaint.']},
    {'id': 'cloud-principal', 'prompt': 'In the reviewed policy, a wildcard principal grants anonymous broad reads. What change fits least privilege?',
     'options': ['Grant public writes too', 'Disable access monitoring', 'Remove public grants and scope required actions/resources to approved identities'], 'answer': 2,
     'feedback': ['Public writes add privileges rather than constrain the exposure.', 'Monitoring supports assessment and does not remove the anonymous grant.', 'Correct. Justify who needs access, what they need and which resources are in scope.']},
    {'id': 'cloud-effective-access', 'prompt': 'Why verify effective access after editing the bucket policy?',
     'options': ['Other policies or sharing controls may still affect who can read', 'One policy edit automatically proves every route is private', 'Authorised access no longer matters'], 'answer': 0,
     'feedback': ['Correct. Evaluate the combined relevant controls and retain required authorised access.', 'The final access result depends on more than assuming an edit worked everywhere.', 'A safe change should also preserve the intended legitimate access.']},
    {'id': 'cloud-current-vs-past', 'prompt': 'The storage is private again. What does that not establish?',
     'options': ['That current exposure has been addressed', 'That no one accessed the data during the earlier exposure window', 'That the policy changed'], 'answer': 1,
     'feedback': ['The current restriction is relevant, but it does not answer the historical impact question.', 'Correct. Earlier access and its consequences still require evidence-based assessment.', 'A recorded policy change is distinct from proving what happened before it.']},
    {'id': 'cloud-impact-followup', 'prompt': 'Data-access impact remains unknown after containment. Which follow-up is appropriate?',
     'options': ['Delete logs because the policy is fixed', 'Assume no one read anything', 'Assess the exposure window and evidence limits with responsible teams and test prevention'], 'answer': 2,
     'feedback': ['Logs remain useful for impact assessment and accountability.', 'Current privacy settings do not prove absence of earlier access.', 'Correct. Complete the scoped assessment and relevant follow-up without unsupported assurances.']},
]
