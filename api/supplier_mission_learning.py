"""Supply Chain Watch v1: fictional supplier exposure, package and assurance records.

No vendor package is downloaded, installed or sent to another party here.
"""
MISSION_ID = 'supply-chain-watch'
REVISION = 'supply-chain-watch-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional customer organisation assess a supplier build incident and verify corrective assurance.',
    'objectives': [
        'Assess customer exposure to supplier-produced releases and pause unverified updates through the response process.',
        'Quarantine a package with unexpected identity and verify provenance instead of testing it by installation.',
        'Track corrective evidence and reduce unnecessary supplier privileges after containment.',
    ],
    'workflow': [
        'Read the supplier task and inspect every fictional notice, package or assurance record.',
        'Choose the finding most relevant to exposure or trust in the supplied artifact.',
        'Commit a defensive customer response and read the explanation.',
        'Finish three decisions to save the result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save your result. Optional review is separate ungraded practice and does not change the score.',
}
STAGES = [
    {'task': 'Assess whether the supplier’s build incident affects the customer and hold unverified releases while seeking evidence.',
     'hints': ['A supplier issue can cross into the customer through releases or integration access.', 'Map affected products and versions to actual customer use; an inventory or signed notice is useful context, not complete assurance.'],
     'artifacts': [
         {'title': 'Supplier notification', 'body': 'The fictional supplier reports suspicious build-environment activity in a signed notification. Verify the communication through established trusted channels and assess the evidence; a notice alone does not establish the customer’s impact or that all releases are safe.'},
         {'title': 'Production update link', 'body': 'This supplier deploys production updates for the customer. Assess potentially affected products, versions, deployments and integration access. Freeze unverified releases under the approved response while obtaining evidence rather than ignore the incident because it began outside the organisation.'},
         {'title': 'Software inventory', 'body': 'A software bill of materials is available to help map components and exposure. Check its relevance, completeness and version context against actual deployed use. An inventory helps ask better questions; it does not prove no affected component is present.'},
     ]},
    {'task': 'Handle a new package whose digest differs from the expected value and whose signature verification is unresolved.',
     'hints': ['An unexpected digest means the package is not the exact content represented by that expected reference.', 'Quarantine and resolve provenance through a trusted supplier route; do not install it to discover whether the mismatch matters.'],
     'artifacts': [
         {'title': 'Digest mismatch', 'body': 'The fictional new package’s digest differs from the expected reference. It may represent a legitimate new build or an unauthorised change, but its identity is not yet resolved. Quarantine it and obtain verified release/provenance evidence before approval.'},
         {'title': 'Inconclusive signature', 'body': 'Signature validation is inconclusive. Do not turn off signature checks to force installation or interpret uncertainty as a verified result. Resolve the trust, identity and release context under the applicable verification process.'},
         {'title': 'Previous approved version', 'body': 'A previous approved package is available as a continuity option for assessment. Check whether it is suitable and whether the supplier incident affects it too; prior approval is not proof of indefinite safety. Do not install the new package merely to see whether it works.'},
     ]},
    {'task': 'Turn the supplier’s containment and corrective plan into tracked customer assurance and least-privilege follow-up.',
     'hints': ['A corrective plan is a commitment to verify, not evidence that every action has completed.', 'Track the evidence and milestones, retain supplier oversight and address unnecessary integration privileges.'],
     'artifacts': [
         {'title': 'Root-cause report', 'body': 'The fictional supplier provides a root-cause report. Review its evidence, scope, remaining uncertainty and customer relevance instead of accepting only a verbal assurance that everything is fixed.'},
         {'title': 'Corrective milestones', 'body': 'Remediation milestones are documented. Assign customer follow-up, review supporting completion evidence and test relevant outcomes under the assurance process. Keep monitoring and escalation for missed or inadequate actions.'},
         {'title': 'Excessive integration access', 'body': 'Supplier access remains broader than the justified integration need. Reduce unnecessary privileges through an approved coordinated change and verify required legitimate functions. Containment at the supplier does not justify retaining every customer-side privilege indefinitely.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The supplier’s production-update relationship is the route that makes customer exposure important. Map actual use and hold unverified releases while obtaining and checking evidence.',
    'The unexpected digest leaves package identity unresolved. Quarantine and verify provenance; an inconclusive signature or available prior version does not justify installing the unverified package.',
    'Excessive integration privileges remain a customer-side issue after supplier containment. Track corrective evidence and reduce unneeded access while preserving justified operations and oversight.',
]
REVIEW = [
    {'id': 'supplier-customer-link', 'prompt': 'Why does a supplier build incident matter to a customer receiving its production updates?',
     'options': ['External incidents can never affect a customer', 'Supplier releases and integration access can connect the incident to customer exposure', 'A signed notice proves every installed version is safe'], 'answer': 1,
     'feedback': ['Dependencies and access can carry consequences across organisation boundaries.', 'Correct. Map the affected supplier activity to actual customer use and access.', 'A notice’s authenticity does not settle the state of every release or deployment.']},
    {'id': 'supplier-inventory-limit', 'prompt': 'What is a sensible use of the available software bill of materials?',
     'options': ['Assume it guarantees no exposure', 'Stop checking deployed versions because an inventory exists', 'Use it with version and deployment evidence to assess relevant components'], 'answer': 2,
     'feedback': ['An inventory has scope, freshness and completeness limits.', 'Actual deployed use still needs verification.', 'Correct. Component information supports exposure analysis rather than replace it.']},
    {'id': 'supplier-digest-action', 'prompt': 'A package digest differs and signature validation is inconclusive. Which response fits the case?',
     'options': ['Quarantine it and verify provenance through a trusted supplier route', 'Install it to see whether it works', 'Disable validation checks'], 'answer': 0,
     'feedback': ['Correct. Resolve artifact identity and release trust before approval.', 'Successful execution would not resolve whether the supplied content is trusted.', 'Removing the check does not resolve the mismatch or uncertainty.']},
    {'id': 'supplier-plan-evidence', 'prompt': 'The supplier offers a corrective plan after containment. What should customer assurance track?',
     'options': ['Only whether the plan sounds confident', 'Milestones, accountable follow-up and evidence that relevant outcomes were achieved', 'The removal of all supplier monitoring'], 'answer': 1,
     'feedback': ['Confidence is not completion evidence.', 'Correct. Verify commitments and outcomes rather than treat a plan as proof of remediation.', 'Monitoring and escalation remain useful during follow-up.']},
    {'id': 'supplier-access-followup', 'prompt': 'Why review excessive integration privileges even after the supplier contains its incident?',
     'options': ['Containment authorises every existing privilege permanently', 'Access scope is unrelated to future exposure', 'Unnecessary customer-side permissions remain a risk requiring justified reduction'], 'answer': 2,
     'feedback': ['A response action does not justify indefinite excessive access.', 'The integration’s privileges affect its possible reach.', 'Correct. Retain only justified access and verify legitimate functions after the approved change.']},
]
