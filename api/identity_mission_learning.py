"""Identity Lab v1: fictional role removal, policy exceptions and lifecycle checks.

No real directory role, session, account or access policy is changed.
"""
MISSION_ID = 'identity-lab'
REVISION = 'identity-lab-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional identity team remove unjustified privileges and prevent access-policy exceptions from being forgotten.',
    'objectives': [
        'Respond to privileged access that remains after a contractor’s engagement ends.',
        'Investigate a policy exclusion that bypasses expected MFA and restore approved controls.',
        'Use owned, periodic lifecycle reviews and tracked exceptions to reduce recurrence.',
    ],
    'workflow': [
        'Read the access task and inspect every fictional employment, role or policy record.',
        'Choose the finding most relevant to unjustified access or control bypass.',
        'Commit a proportionate access-governance recommendation and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the result. Review is repeatable practice with no saved grade or change to mission points.',
}
STAGES = [
    {'task': 'Remove unnecessary privileged access left assigned after a contractor’s engagement ended, and review its use.',
     'hints': ['The end date provides context; check what access remains and whether any current approval justifies it.', 'Use the approved removal process and investigate activity rather than share credentials or silently assume the account was unused.'],
     'artifacts': [
         {'title': 'Contract end', 'body': 'The fictional contractor’s engagement ended last month. Confirm the lifecycle event and responsible owner rather than rely on an assumption that all related access was automatically removed.'},
         {'title': 'Active privileged role', 'body': 'A privileged role remains assigned without a stated current need. Revoke unnecessary access through the approved process and review relevant activity. Ending the engagement does not prove the retained role was never used.'},
         {'title': 'Overdue review', 'body': 'The access review is overdue. Record and escalate the lifecycle gap, preserve relevant usage evidence and assign follow-up. Sharing the credentials with the team would create another access and accountability problem.'},
     ]},
    {'task': 'Explain why an expected MFA requirement was bypassed and correct the unauthorised exception through the approved process.',
     'hints': ['Review which account and conditions a policy exclusion actually matches.', 'Keep sign-in evidence, validate the effective policy and restore the approved requirement without accepting unknown logins.'],
     'artifacts': [
         {'title': 'Matching exclusion', 'body': 'A fictional policy exclusion matches the privileged account and bypasses its expected MFA requirement. Investigate the exclusion’s purpose, scope and approval, then enforce the approved policy and verify its effective result.'},
         {'title': 'Unfamiliar device sign-in', 'body': 'The affected sign-in came from an unfamiliar device. Correlate the event with policy evaluation and account activity. Device familiarity alone does not resolve why the expected control was bypassed.'},
         {'title': 'Unapproved policy change', 'body': 'The access-policy change was not approved in the case records. Preserve audit information, use the authorised correction process and review affected access. Do not disable auditing or approve every waiting login to clear the queue.'},
     ]},
    {'task': 'Turn the corrected role and policy issue into repeatable lifecycle and exception oversight.',
     'hints': ['Correcting today’s role does not ensure the next departure or policy exception is handled.', 'Combine ownership, lifecycle triggers, scheduled review and tracked approvals with verification; automation also needs oversight.'],
     'artifacts': [
         {'title': 'Role ownership', 'body': 'A responsible role owner is identified. Keep ownership and accountability clear so questions about continuing business need have a decision-maker rather than an informal shared assumption.'},
         {'title': 'Review frequency', 'body': 'The fictional team documents periodic access reviews alongside joiner, mover and leaver triggers. Automate appropriate checks and follow-up, but verify that events, reviews and removals actually complete. A scheduled job is not proof that every access decision is correct.'},
         {'title': 'Exception tracking', 'body': 'Exceptions require documented scope, owner, approval and review or expiry conditions. Track and monitor them so temporary access or exclusions do not persist silently. Verbal approval alone is not a durable review record.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The remaining privileged role is the unjustified access to address. Confirm ownership and lifecycle context, revoke under the process and investigate usage rather than assume it was harmless.',
    'The matching policy exclusion explains the bypass path. Review its approval and effective scope, correct the policy and retain the sign-in/audit evidence.',
    'A documented review frequency supports repeatable oversight, alongside lifecycle triggers and tracked exceptions. Automation and assigned owners still need completion checks and accountable decisions.',
]
REVIEW = [
    {'id': 'identity-departure', 'prompt': 'A former contractor’s privileged role is still assigned without a stated current need. What should the team do?',
     'options': ['Leave it indefinitely because it already exists', 'Remove unnecessary access under the approved process and review its use', 'Share the credentials so others can use the role'], 'answer': 1,
     'feedback': ['Past assignment is not justification for continuing access.', 'Correct. Address the retained privilege and assess relevant activity through the authorised process.', 'Sharing access creates further exposure and weakens individual accountability.']},
    {'id': 'identity-bypass', 'prompt': 'Expected MFA was bypassed and an exclusion matches the account. Which review is most relevant?',
     'options': ['Only the user’s display name', 'Whether alerts can be hidden', 'The exclusion’s scope, approval and actual policy evaluation'], 'answer': 2,
     'feedback': ['A display name does not explain control evaluation.', 'Hiding alerts removes visibility rather than correct the bypass.', 'Correct. Establish why the account was excluded and restore the approved effective control.']},
    {'id': 'identity-audit-retention', 'prompt': 'Why retain audit and sign-in records while correcting an unauthorised policy exclusion?',
     'options': ['They help assess changes, affected access and the correction', 'Correction makes all past activity irrelevant', 'Removing records is how MFA is enforced'], 'answer': 0,
     'feedback': ['Correct. The team still needs to understand the change and its consequences.', 'Restoring a control does not explain earlier access.', 'Deleting audit data does not enforce the intended authentication policy.']},
    {'id': 'identity-lifecycle', 'prompt': 'Which combination best reduces recurrence of forgotten privileged access?',
     'options': ['Only informal verbal reminders', 'Owned lifecycle triggers, periodic reviews and verified follow-up', 'Removing all review schedules'], 'answer': 1,
     'feedback': ['Informal reminders are difficult to track and verify.', 'Correct. Combine timely events with repeatable review and evidence that actions completed.', 'Eliminating review removes an important check on stale access.']},
    {'id': 'identity-exception', 'prompt': 'What makes a temporary access-policy exception reviewable?',
     'options': ['An undocumented promise to remember it', 'A permanent exclusion with no owner', 'Recorded scope, accountable owner, approval and review/expiry conditions'], 'answer': 2,
     'feedback': ['A promise alone does not provide a durable review trail.', 'Ownerless permanent exclusions are difficult to justify or revisit.', 'Correct. Make the decision, limits and follow-up visible and accountable.']},
]
