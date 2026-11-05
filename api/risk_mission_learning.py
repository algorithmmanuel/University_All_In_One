"""Risk Command v1: fictional ownership, interim treatment and residual decisions.

No real risk is accepted, downtime approved or committee decision issued here.
"""
MISSION_ID = 'risk-command'
REVISION = 'risk-command-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional business risk owner assess an unsupported payment service and make traceable treatment decisions.',
    'objectives': [
        'Assess an unsupported critical service using likelihood, impact and accountable ownership.',
        'Manage continuing exposure with approved interim controls and a funded remediation plan.',
        'Document residual risk, authorised acceptance and exception review or expiry.',
    ],
    'workflow': [
        'Read the current risk task and inspect every fictional service, treatment or exception record.',
        'Select the finding most relevant to the decision and continuing exposure.',
        'Commit a defensible treatment recommendation and read the explanation.',
        'Complete three decisions to save the result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review saves no grade and does not change the score.',
}
STAGES = [
    {'task': 'Assess the unsupported payment service and assign accountable treatment rather than hide or informally accept it.',
     'hints': ['Consider the service’s business impact, exposure and actual control evidence together.', 'Record likelihood, impact, ownership and proposed treatment; undocumented safeguards should not be assumed effective.'],
     'artifacts': [
         {'title': 'Payment service importance', 'body': 'The fictional internet-facing service processes payments and is business-critical. Consider availability, data and business consequences in the impact assessment rather than evaluate the operating system without service context.'},
         {'title': 'Ended vendor support', 'body': 'Vendor support ended last quarter in this fictional case. Assess the implications of unsupported software, the relevant exposure and treatment options. Do not hide the asset or treat an informal decision as documented risk acceptance.'},
         {'title': 'Undocumented safeguards', 'body': 'Compensating controls are not documented. Identify and assess what actually exists, including evidence and limits, rather than crediting assumed protections. Assign the responsible risk owner and propose a traceable treatment decision.'},
     ]},
    {'task': 'Control exposure during the proposed six-week remediation period while keeping business accountability clear.',
     'hints': ['An approved future fix does not protect the service during the waiting period.', 'Use justified time-bound interim measures with owners, evidence and a funded plan; the auditor does not become the business risk owner.'],
     'artifacts': [
         {'title': 'Continuing exposure', 'body': 'The fictional service remains exposed during the proposed six-week treatment period. Evaluate the interim risk and required decision authority rather than delay without controls or assume a planned date is protection.'},
         {'title': 'Temporary segmentation', 'body': 'Temporary segmentation is feasible in this case. Review its scope, effectiveness and operational effects, obtain appropriate approval and monitor it as a time-bound compensating measure. It is not automatically equivalent to remediating the unsupported platform.'},
         {'title': 'Business maintenance decision', 'body': 'The business owner can approve the necessary downtime under the applicable process. Assign treatment actions, resources and dates to accountable owners. An auditor can provide assurance and challenge, but treatment responsibility should not be transferred to the auditor.'},
     ]},
    {'task': 'Close the treatment decision with a documented residual-risk assessment and monitored exception.',
     'hints': ['Completing remediation and eliminating every remaining risk are different conclusions.', 'Use the required acceptance authority, retain the exception and monitor its review/expiry rather than erase the remaining issue.'],
     'artifacts': [
         {'title': 'Remediation evidence', 'body': 'The fictional team reviews patch/remediation evidence. Assess what was actually changed and verified. A completed action does not establish that every risk or remaining exception disappeared.'},
         {'title': 'Thirty-day exception', 'body': 'One exception expires in 30 days in the case. Retain its scope, owner and conditions, track the deadline and require review or further treatment if it is not resolved.'},
         {'title': 'Residual-risk authority', 'body': 'The risk committee requires approval of residual risk. Document the remaining exposure, evidence, accountable acceptance and conditions using that authority. Do not mark all risk eliminated or delete an exception merely to close an action.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Ended support is the platform condition needing assessment in this critical payment service. Use exposure, impact and control evidence with a responsible owner, not hidden assets or informal acceptance.',
    'Continuing exposure during the wait requires an interim decision, not only a future remediation date. Approve and verify time-bound controls alongside a resourced accountable treatment plan.',
    'The required residual-risk approval determines how the decision closes. Preserve the exception and its expiry monitoring; completing remediation is not proof that all remaining exposure vanished.',
]
REVIEW = [
    {'id': 'risk-context', 'prompt': 'What belongs in assessing an unsupported internet-facing payment service?',
     'options': ['Only whether the asset is easy to hide', 'Likelihood, business impact, exposure, control evidence and accountable ownership', 'An undocumented assumption that compensating controls work'], 'answer': 1,
     'feedback': ['Hiding the asset does not reduce or govern the exposure.', 'Correct. A defensible risk decision connects the technical condition to business consequences and evidence.', 'Undocumented assumptions should not receive the same credit as verified controls.']},
    {'id': 'risk-waiting-window', 'prompt': 'A remediation plan needs six weeks. Which conclusion is unsafe?',
     'options': ['The interim exposure should be assessed', 'Time-bound controls may need approval and monitoring', 'A future completion date itself protects the service now'], 'answer': 2,
     'feedback': ['Risk can remain active while treatment is pending.', 'Interim measures need justification, accountability and verification.', 'Correct. Planning a fix is not the same as controlling the exposure during the wait.']},
    {'id': 'risk-auditor-owner', 'prompt': 'How should the business handle responsibility while an auditor reviews the treatment?',
     'options': ['Keep treatment and risk ownership with the accountable management roles', 'Transfer the risk to the auditor', 'Leave ownership blank until the next audit'], 'answer': 0,
     'feedback': ['Correct. Assurance and challenge do not replace management’s responsibility for treatment decisions.', 'An audit role does not become the owner of the business exposure merely by reviewing it.', 'An undefined owner makes timely treatment and acceptance harder to govern.']},
    {'id': 'risk-compensating-limit', 'prompt': 'Temporary segmentation is feasible during remediation. How should it be treated?',
     'options': ['As an automatic permanent substitute for every missing fix', 'As a scoped, approved, verified and time-bound measure with documented limits', 'As a reason to cancel all follow-up'], 'answer': 1,
     'feedback': ['A compensating measure needs an effectiveness assessment and does not automatically replace remediation.', 'Correct. Record what it achieves, what remains and who monitors it.', 'Interim measures still need treatment follow-through.']},
    {'id': 'risk-residual-close', 'prompt': 'Remediation is complete but an exception remains. What supports responsible closure?',
     'options': ['Delete the exception record', 'Declare all risk eliminated', 'Document residual risk, obtain the required acceptance and monitor exception conditions/expiry'], 'answer': 2,
     'feedback': ['Deleting a record does not remove the underlying exposure.', 'A remaining exception requires assessment rather than an unsupported zero-risk claim.', 'Correct. Use the authorised decision process and retain reviewable follow-up.']},
]
