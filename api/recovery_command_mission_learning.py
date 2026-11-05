"""Ransomware Recovery v1: fictional segment response and dependency-led recovery.

No ransom payment, real isolation, reimaging or service restoration is performed.
"""
MISSION_ID = 'ransomware-recovery'
REVISION = 'ransomware-recovery-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional response leader contain branch disruption, sequence limited recovery capacity and communicate evidence-based progress.',
    'objectives': [
        'Activate a scoped incident response without assuming a healthy core service settles all exposure.',
        'Sequence recovery using business impact, objectives and service dependencies rather than restore arbitrary systems.',
        'Report validated recovery progress and remaining risks while investigation continues.',
    ],
    'workflow': [
        'Read the command task and inspect every fictional service, recovery or status record.',
        'Select the finding most relevant to containment, recovery sequencing or communication.',
        'Commit a coordinated response recommendation and read the explanation.',
        'Complete three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Review is ungraded practice with no change to saved mission points.',
}
STAGES = [
    {'task': 'Activate the incident plan and contain affected branch segments while preserving evidence and validating service scope.',
     'hints': ['Healthy status for one service is a current observation, not a finding that the incident is harmless or fully scoped.', 'Coordinate approved isolation and evidence preservation rather than improvise mass reimaging or an immediate payment.'],
     'artifacts': [
         {'title': 'Affected branch devices', 'body': 'Several fictional branch endpoints show ransom notes. Activate the incident response process, assess scope and preserve relevant observations rather than continue routine use or assume all servers need the same action.'},
         {'title': 'Core service status', 'body': 'Core banking is currently healthy in the supplied status. Preserve and validate that observation as response planning context, but do not infer that every dependent service or access path is unaffected. Maintain needed oversight while the branch incident is assessed.'},
         {'title': 'Segmentation options', 'body': 'Network segmentation controls are available. Use approved, coordinated isolation of affected segments with appropriate business/service awareness and evidence preservation. Do not reimage every server without assessment or make unapproved payment decisions.'},
     ]},
    {'task': 'Use limited restoration capacity on the services and dependencies that support the agreed business priorities.',
     'hints': ['An objective sets a recovery target; it does not establish that available capacity can achieve it.', 'Use the BIA and dependency map to sequence the prerequisites, validate the recovery copy and coordinate owners/resources.'],
     'artifacts': [
         {'title': 'Recovery time objective', 'body': 'The fictional critical service has a four-hour RTO. An RTO is a recovery objective used for planning, not evidence that recovery has succeeded or a guarantee the target will be met. Assess capacity and escalation if the plan cannot meet the objective.'},
         {'title': 'Backup integrity result', 'body': 'A backup integrity test passed. Check that the copy, version and restoration approach are suitable for the required service. A validated backup supports recovery but does not supply unlimited restoration capacity or establish complete service recovery.'},
         {'title': 'Authentication dependency', 'body': 'The dependency map shows the critical service relies on authentication. Use business impact analysis priorities and verified service dependencies to sequence restoration, including necessary prerequisites, rather than restore random systems first. Confirm owners, resources and verification steps.'},
     ]},
    {'task': 'Communicate the established recovery position while the investigation and residual-risk work continue.',
     'hints': ['Some resumed branches do not prove that the full incident is over.', 'State validated progress, known impacts, remaining service limits and risks through approved channels; avoid unverified attribution or blanket closure.'],
     'artifacts': [
         {'title': 'Validated resumed services', 'body': 'The fictional team documents validation for some recovered branches. Report exactly which services resumed and what was checked rather than describe every branch as fully restored.'},
         {'title': 'Residual exposure', 'body': 'Some exposure remains and investigation continues. Keep responsible owners and follow-up clear; restored service is not proof that all causes, scope and remaining risks have been resolved.'},
         {'title': 'Customer service updates', 'body': 'Customers need accurate information about confirmed service availability and limitations. Coordinate approved communications using verified facts, recovery progress and remaining risks. Do not publish speculative attribution or declare full closure while known work remains.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The currently healthy core service is important scope and continuity context, not proof that the incident is over. Activate the plan, contain affected segments and preserve evidence while validating the wider position.',
    'The authentication dependency affects the recovery sequence. Use BIA priorities and prerequisites with tested backups and realistic capacity; the RTO alone does not supply the recovery plan.',
    'Documented recovery validation establishes what can responsibly be reported as resumed. Communicate that scope alongside confirmed impacts and remaining exposure, not unverified attribution or premature closure.',
]
REVIEW = [
    {'id': 'recovery-core-status', 'prompt': 'Core banking is currently healthy while branch endpoints show ransom notes. What should command infer?',
     'options': ['The incident needs no response', 'It is useful continuity context that still needs scope validation', 'Every other system is certainly unaffected'], 'answer': 1,
     'feedback': ['Branch disruption still warrants the incident process.', 'Correct. Preserve the observation while coordinating containment and checking scope.', 'One healthy status does not establish the state of every related system or access route.']},
    {'id': 'recovery-rto-limit', 'prompt': 'What does a four-hour recovery time objective establish?',
     'options': ['A guarantee every service will recover in four hours', 'Proof that restoration already succeeded', 'A planning objective against which capacity and recovery performance must be assessed'], 'answer': 2,
     'feedback': ['An objective is not a guarantee that resources or execution will achieve it.', 'A target time is not evidence of completed recovery.', 'Correct. Use the target with realistic plans, priorities and escalation where needed.']},
    {'id': 'recovery-sequence', 'prompt': 'Restoration capacity is limited and a critical service depends on authentication. Which sequencing approach is sound?',
     'options': ['Use BIA priorities and verified service dependencies, including prerequisites', 'Restore random systems first', 'Ignore the dependency map'], 'answer': 0,
     'feedback': ['Correct. Plan the services and prerequisites needed to achieve the business recovery priority.', 'Random order can consume capacity without restoring the required business service.', 'Ignoring prerequisites can leave a restored component unusable.']},
    {'id': 'recovery-backup-capacity', 'prompt': 'Why does a passed backup integrity test not settle recovery scheduling?',
     'options': ['A backup result removes every dependency', 'Capacity, suitable versions, prerequisites and service validation still matter', 'No restoration evidence should be reviewed'], 'answer': 1,
     'feedback': ['A usable recovery copy does not remove service dependencies.', 'Correct. Backup suitability is one input to the coordinated service-recovery plan.', 'Reviewing recovery evidence remains necessary.']},
    {'id': 'recovery-executive-update', 'prompt': 'Some branches have resumed service while investigation continues. What should leadership communicate?',
     'options': ['That the entire incident is closed', 'Unverified claims about the attacker', 'Confirmed impacts, validated progress, current limitations and remaining risks'], 'answer': 2,
     'feedback': ['Partial recovery does not establish full incident resolution.', 'Speculation is not an established incident finding.', 'Correct. Keep updates accurate, scoped and coordinated through approved channels.']},
]
