"""Web Defense v1: fictional defensive review and release evidence.

No injection payload is generated or executed against an application or database.
"""
MISSION_ID = 'web-defense'
REVISION = 'web-defense-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional development team validate an injection concern, fix query construction and review release evidence.',
    'objectives': [
        'Treat a gateway alert as a lead to validate against request and application evidence.',
        'Explain how parameterized queries separate untrusted values from SQL structure.',
        'Review staging tests and change approval before a monitored production deployment.',
    ],
    'workflow': [
        'Inspect each fictional gateway, code-review or verification record for the current task.',
        'Select the finding that matters most to the stage’s defensive decision.',
        'Commit a remediation or release recommendation and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review saves no grade and does not change the mission score.',
}
STAGES = [
    {'task': 'Validate injection-like requests and the app’s input handling without treating a gateway alert as proof of exploitation.',
     'hints': ['A detector’s label is a reason to inspect evidence, not a complete application assessment.', 'Review relevant request logs and server-side input/query handling, preserving records and avoiding publication of sensitive request details.'],
     'artifacts': [
         {'title': 'Search parameter', 'body': 'Fictional request records show repeated unusual operators in a search parameter. Review the relevant request context and how the application handles the value. This exercise contains no executable payload or live target.'},
         {'title': 'Gateway alert', 'body': 'The WAF reports injection-like patterns. Such an alert is a lead for validation; it does not alone prove that the database executed an injected query. Review application input handling and relevant logs rather than disable monitoring.'},
         {'title': 'Continuing normal traffic', 'body': 'Normal search requests still occur. This does not establish that suspicious requests were safe. Keep the investigation scoped and preserve useful logs; do not publish potentially sensitive request details to users.'},
     ]},
    {'task': 'Recommend a server-side fix when untrusted input is concatenated into a database query.',
     'hints': ['Changing a visible form is different from changing how the server constructs SQL.', 'Use parameter binding so values are treated as data; validate other input requirements and test the actual server path.'],
     'artifacts': [
         {'title': 'Query construction', 'body': 'The fictional code review finds untrusted input joined directly into SQL text. That construction can let input affect query structure. Hiding the search field or adding only a client-side warning does not fix the server’s query handling.'},
         {'title': 'Parameter binding', 'body': 'The database interface supports parameterized queries for values. Bind values separately from the query structure rather than concatenate them. Dynamic identifiers or other query structure need constrained server-controlled choices; value binding is not a blanket solution to every dynamic SQL construction.'},
         {'title': 'Regression environment', 'body': 'A separate test environment is available. Add meaningful regression cases for the repaired query path and ordinary search behaviour, alongside appropriate server-side validation. A WAF may add protection but is not a replacement for correcting unsafe query construction.'},
     ]},
    {'task': 'Assess the staging fix and required approval before production deployment.',
     'hints': ['Passing a staging check and having authority to deploy are separate release requirements.', 'Review the fix and test evidence, obtain the applicable approval and monitor after deployment; do not claim all web risk is eliminated.'],
     'artifacts': [
         {'title': 'Fixed query review', 'body': 'The fictional team confirms the repaired path uses parameterized values. Review the actual change and its scope; one corrected path does not establish that every application query or input path is safe.'},
         {'title': 'Staging test evidence', 'body': 'Relevant security and ordinary behaviour tests pass in staging. Verify what they covered and any remaining gaps. These results support release assessment, not a claim that all web risks have disappeared.'},
         {'title': 'Production approval', 'body': 'Production change approval is still pending. Follow the applicable release process, review test evidence and obtain approval before deployment, then monitor the change. Do not bypass change control because the fix passed staging.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The injection-like gateway alert identifies what needs validation. Relevant request and application evidence must establish how input was handled; normal traffic does not dismiss the concern.',
    'Concatenated untrusted input is the unsafe server-side construction to fix. Parameterized values and meaningful regression checks address that path; hiding a field does not.',
    'Passing security tests in staging is relevant assurance evidence, but still requires scope review, applicable production approval and post-deployment monitoring. It does not eliminate every web risk.',
]
REVIEW = [
    {'id': 'web-alert-proof', 'prompt': 'A WAF labels search requests injection-like. What does this establish on its own?',
     'options': ['The database certainly executed injected SQL', 'A lead to validate using request logs and server-side handling', 'That normal searches must be disabled forever'], 'answer': 1,
     'feedback': ['A detector label alone does not demonstrate what the database executed.', 'Correct. Assess the actual handling and preserve evidence before concluding impact.', 'A scoped investigation is needed rather than an unsupported permanent disruption.']},
    {'id': 'web-bind-values', 'prompt': 'What is the main protection of parameterized query values in the reviewed path?',
     'options': ['They turn every dynamic query identifier into a safe value', 'They remove the need for all other checks', 'They separate supplied values from SQL structure'], 'answer': 2,
     'feedback': ['Identifiers and other query structure require separate constrained handling.', 'Other validation, authorization and query paths still need attention.', 'Correct. Binding values avoids constructing SQL structure by joining untrusted value text into it.']},
    {'id': 'web-client-limit', 'prompt': 'Why does hiding the search form not fix unsafe server-side query concatenation?',
     'options': ['The server still needs to handle received input safely', 'Every user interface change automatically rewrites SQL', 'Client visibility is the only input boundary'], 'answer': 0,
     'feedback': ['Correct. The server’s query construction must be corrected and tested.', 'A UI change does not itself change query construction.', 'Server-side requests cannot rely solely on what the normal page displays.']},
    {'id': 'web-regression-scope', 'prompt': 'Which tests best support the query fix?',
     'options': ['Only checking the colour of the search button', 'Relevant security regression cases plus normal search behaviour on the repaired server path', 'No tests because the WAF is installed'], 'answer': 1,
     'feedback': ['Appearance does not verify input handling or query behaviour.', 'Correct. Test the actual repair and ordinary behaviour, while recording coverage limits.', 'A WAF does not replace testing the corrected application path.']},
    {'id': 'web-release-gate', 'prompt': 'Staging tests pass, but production approval is pending. What should happen?',
     'options': ['Deploy immediately and skip approval', 'Declare all web risk eliminated', 'Review evidence, obtain the applicable approval and monitor the approved deployment'], 'answer': 2,
     'feedback': ['Passing staging does not waive the applicable change process.', 'A bounded fix does not settle every web risk.', 'Correct. Combine technical evidence with the required release decision and monitoring.']},
]
