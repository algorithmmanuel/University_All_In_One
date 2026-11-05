"""Branch Resilience v1: fictional ransomware containment, scope and recovery.

Uses the existing incident-response mission ID and two evidence records per stage.
No real device is isolated, file restored or operational system changed here.
"""
MISSION_ID = 'incident-response'
REVISION = 'branch-resilience-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional branch response team contain a disruption, protect recovery options and restore under an approved plan.',
    'objectives': [
        'Escalate a suspected ransomware disruption and isolate the affected workstation under the response plan.',
        'Assess possible spread while preserving evidence and safeguarding backups.',
        'Use verified containment and a validated recovery copy for controlled, monitored restoration.',
    ],
    'workflow': [
        'Read the branch task and inspect both fictional incident records for the stage.',
        'Select the finding most relevant to containment, scope or recovery.',
        'Commit a coordinated response recommendation and read the explanation.',
        'Complete three decisions to save the result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review changes neither the saved score nor completion.',
}
STAGES = [
    {'task': 'Handle the affected workstation under the incident plan rather than continue using it or dismiss the report.',
     'hints': ['Inaccessible files and a ransom message require prompt coordinated assessment, not routine continued use.', 'Follow the response procedure to isolate the affected workstation, notify the responsible team and preserve useful evidence.'],
     'artifacts': [
         {'title': 'Inaccessible files', 'body': 'The fictional branch workstation’s files are inaccessible. Treat the disruption seriously and report it through the incident process. Recommend isolation under the approved response plan to limit potential spread rather than continue normal use.'},
         {'title': 'Ransom message', 'body': 'A ransom demand is displayed in the case. Preserve relevant observations and coordinate with the response team. The display does not establish the full affected scope; do not improvise reinstalling, deleting evidence or changing other systems outside the plan.'},
     ]},
    {'task': 'Assess additional affected devices and protect backups before choosing a recovery path.',
     'hints': ['Unusual changes on additional devices are a scope lead to investigate.', 'Preserve records and recovery copies while checking affected assets; do not erase logs or assume backups are already safe.'],
     'artifacts': [
         {'title': 'Possible spread', 'body': 'Additional fictional devices show unusual file changes. Assess affected assets and related activity under the plan, retaining evidence. This is a reason to extend the scope check, not proof that every device is affected or that the first workstation was the only source.'},
         {'title': 'Backup protection', 'body': 'Recovery copies need protection from the ongoing incident and authorised review of integrity, freshness and restorability. Preserve usable versions and avoid overwriting good copies. Do not connect or use a backup blindly while the response team is still assessing spread.'},
     ]},
    {'task': 'Restore through the approved recovery process after containment and a clean recovery copy have been validated.',
     'hints': ['A recovery copy must be checked for suitability; availability alone does not establish that restoration will be safe.', 'Use the approved staged restoration, confirm service/data behaviour, communicate and monitor rather than reconnect everything without checks.'],
     'artifacts': [
         {'title': 'Containment verification', 'body': 'The fictional team verifies containment for the scoped incident. Use that finding as a prerequisite for the approved recovery decision, while recording the scope and any remaining uncertainty. Do not assume every unrelated asset is automatically safe.'},
         {'title': 'Validated recovery copy', 'body': 'The team validates a clean backup suitable for recovery. Restore under the approved plan, check recovered data and service behaviour, keep responsible stakeholders informed and monitor for recurrence. A successful file copy alone does not establish complete service recovery or prevent every future incident.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Inaccessible files are the operational disruption requiring a prompt planned response. A ransom message adds context; isolate under the incident procedure and preserve evidence rather than continue using the affected device.',
    'Possible spread means the affected scope needs assessment while backups are safeguarded. Erasing records or ignoring recovery copies would reduce both investigation and recovery options.',
    'The validated backup supports a controlled recovery decision after containment. Restore through the plan, verify data/services, communicate and monitor; a backup alone is not complete service recovery.',
]
REVIEW = [
    {'id': 'response-first-action', 'prompt': 'A branch workstation has inaccessible files and a ransom demand. Which action fits the response plan?',
     'options': ['Keep using it for normal work', 'Escalate and isolate the affected workstation under the approved procedure', 'Ignore the report until more users complain'], 'answer': 1,
     'feedback': ['Continued use may worsen exposure and alter evidence.', 'Correct. Coordinate containment and preserve observations rather than improvise.', 'The disruption already warrants prompt assessment.']},
    {'id': 'response-scope', 'prompt': 'Additional devices show unusual file changes. What should the team establish?',
     'options': ['That every device in the organisation is certainly affected', 'That logs can now be erased', 'Which assets and activities are affected while preserving evidence and recovery options'], 'answer': 2,
     'feedback': ['Additional signs justify scoping, not an unsupported conclusion about every asset.', 'Evidence remains important to understand scope and response.', 'Correct. Expand the assessment and protect recovery options without destroying records.']},
    {'id': 'response-backup-safety', 'prompt': 'Why safeguard backups while investigating possible spread?',
     'options': ['Usable recovery versions may otherwise be exposed or overwritten', 'Every backup is automatically immune to an incident', 'Keeping a backup makes containment unnecessary'], 'answer': 0,
     'feedback': ['Correct. Protect and assess recovery copies instead of assuming they remain usable.', 'Backups still require appropriate protection and validation.', 'Recovery data does not itself contain active exposure.']},
    {'id': 'response-restore-gate', 'prompt': 'Which evidence supports starting the approved recovery stage in this case?',
     'options': ['An untested file named backup', 'Verified containment and a validated clean recovery copy', 'A decision to reconnect everything immediately'], 'answer': 1,
     'feedback': ['A name or mere availability does not establish suitability.', 'Correct. Use established containment and recovery evidence within the approved plan.', 'Unverified reconnection can undermine recovery and create further exposure.']},
    {'id': 'response-service-recovery', 'prompt': 'After restoring files, what remains necessary for responsible recovery?',
     'options': ['Assume every service works because files copied', 'Skip communications and monitoring', 'Check data/service behaviour, inform responsible stakeholders and monitor recurrence'], 'answer': 2,
     'feedback': ['File copying is not the same as verified service recovery.', 'Communications and monitoring remain part of a coordinated response.', 'Correct. Validate the result and maintain visibility rather than equate copied files with complete recovery.']},
]
