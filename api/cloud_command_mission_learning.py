"""Cloud Incident v1: fictional service-credential containment and recovery.

No real credential is retrieved, rotated or used against a cloud resource.
"""
MISSION_ID = 'cloud-incident'
REVISION = 'cloud-incident-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional incident commander validate cloud access changes and coordinate credential containment with service continuity.',
    'objectives': [
        'Validate unusual service-credential actions using retained cloud evidence.',
        'Coordinate scoped restriction and credential replacement while assessing legitimate consumers.',
        'Reconcile affected configuration and effective access before improving detections and closing the response.',
    ],
    'workflow': [
        'Read the command task and inspect every fictional cloud activity, scope or recovery record.',
        'Select the finding most relevant to the current response decision.',
        'Commit a coordinated defensive action and read the explanation.',
        'Complete three decisions to save the result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review saves no grade and does not change that result.',
}
STAGES = [
    {'task': 'Validate unusual access-rule changes and initiate the approved service-credential response.',
     'hints': ['The action performed matters as well as the unfamiliar region.', 'Correlate the calls with expected use, preserve audit evidence and invoke the approved containment process rather than wait for routine review.'],
     'artifacts': [
         {'title': 'Expected region', 'body': 'The fictional credential normally operates in one region. New-region activity is a lead to investigate, not by itself proof of compromise. Compare expected service behaviour, sources and timing.'},
         {'title': 'Access-rule modifications', 'body': 'The new API calls modify access rules. These potentially consequential actions need prompt validation against expected activity and change evidence, followed by the approved credential-containment response where warranted.'},
         {'title': 'Retained cloud audit', 'body': 'Audit logs are retained. Preserve and correlate relevant access and configuration events rather than delete all cloud accounts or wait until a monthly review. Record both established findings and uncertainty.'},
     ]},
    {'task': 'Contain a broad credential with coordinated restriction and replacement instead of creating unnecessary production disruption.',
     'hints': ['Assess both the credential’s possible reach and which legitimate services depend on it.', 'Use approved scoped restrictions and coordinated rotation, verify consumers and retain audit evidence throughout.'],
     'artifacts': [
         {'title': 'Broad credential scope', 'body': 'The fictional service credential can modify several storage resources. Assess and limit its effective reach under the response plan rather than treat a single observed resource as the only possible exposure.'},
         {'title': 'Production consumers', 'body': 'Rotating the credential can interrupt legitimate production services. Identify consumers and coordinate the replacement and verification with responsible owners. Continuity concerns require planning, not indefinite tolerance of suspect access.'},
         {'title': 'Temporary role restriction', 'body': 'An approved temporary restriction is available. Use justified scoped containment and rotate affected access material under the coordinated response. Do not publish the secret or stop collecting audit logs. Verify effective permissions and service behaviour after the changes.'},
     ]},
    {'task': 'Reconcile affected resources and access after rotation, then record findings and improve monitoring.',
     'hints': ['A replaced secret does not automatically reverse access rules changed while it was usable.', 'Review configuration differences against approved known-good state, validate effective access and turn confirmed findings into tested detections.'],
     'artifacts': [
         {'title': 'Access-change review', 'body': 'The fictional team reviews access changes on identified resources. Reconcile what was modified, restore only approved settings and validate effective access. Credential rotation alone does not undo configuration changes or prove every resource was unaffected.'},
         {'title': 'Known-good templates', 'body': 'Approved infrastructure templates are available as a recovery reference. Review differences and the template’s suitability before applying it through the change process. Do not blindly restore unreviewed permissions simply because a template exists.'},
         {'title': 'Detection follow-up', 'body': 'Monitoring needs updates based on the validated findings. Test relevant detections, retain an incident record and monitor restored services/access. Closing without a report or restoring unreviewed permissions would leave important assurance gaps.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The access-rule modifications make the unusual credential activity consequential. Validate the events with retained evidence and invoke the approved response rather than rely only on region or delay.',
    'Broad modification scope defines the containment reach that needs assessment. Coordinate restriction and rotation with legitimate consumers while preserving visibility and verifying the effective result.',
    'Detection follow-up is part of completing recovery after access and configuration reconciliation. Rotation is not proof that prior changes were undone; record findings, validate access and test monitoring improvements.',
]
REVIEW = [
    {'id': 'cloud-command-action', 'prompt': 'Which observation makes the unfamiliar-region activity especially important to validate?',
     'options': ['Any region change automatically proves compromise', 'The calls modify access rules using a service credential', 'Audit logs exist so no review is needed'], 'answer': 1,
     'feedback': ['Location alone does not establish the full explanation.', 'Correct. Evaluate the consequential actions with expected activity and change evidence.', 'Retained records enable investigation rather than replace it.']},
    {'id': 'cloud-command-continuity', 'prompt': 'Credential rotation can interrupt production. What should incident command do?',
     'options': ['Publish the credential to reduce coordination work', 'Leave suspect access indefinitely', 'Coordinate scoped containment and replacement with legitimate service owners'], 'answer': 2,
     'feedback': ['Sharing the secret creates additional exposure.', 'Service continuity needs a planned response, not indefinite acceptance of suspect access.', 'Correct. Address risk while identifying, updating and verifying legitimate consumers.']},
    {'id': 'cloud-command-reach', 'prompt': 'A credential can modify multiple storage resources. What should containment assessment consider?',
     'options': ['Its effective reach beyond the single observed resource', 'Only the first resource mentioned in the alert', 'Whether audit collection can be stopped'], 'answer': 0,
     'feedback': ['Correct. Scope the permission and potential affected resources before assuming the observed event is the full exposure.', 'One observed action may not represent the credential’s full reach.', 'Removing audit visibility would hinder assessment.']},
    {'id': 'cloud-command-rotation-limit', 'prompt': 'After rotating a credential, why review affected resource configuration?',
     'options': ['Rotation automatically reverses all policy edits', 'Earlier access-rule changes may remain in place', 'Resource settings no longer affect access'], 'answer': 1,
     'feedback': ['Secret replacement and configuration repair are different actions.', 'Correct. Reconcile approved state and validate effective permissions after the response.', 'Configuration still determines who can access or modify resources.']},
    {'id': 'cloud-command-recovery', 'prompt': 'Which follow-up supports evidence-based cloud recovery?',
     'options': ['Restore permissions without reviewing them', 'Close the incident without a record', 'Reconcile approved configuration, validate access and test detection improvements'], 'answer': 2,
     'feedback': ['Unreviewed permissions can recreate exposure.', 'A response needs a reviewable record of findings, actions and limits.', 'Correct. Recovery includes the actual access result and monitoring follow-through, not only a new secret.']},
]
