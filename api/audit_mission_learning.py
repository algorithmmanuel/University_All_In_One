"""Source-owned guidance for a fictional audit-trail decision exercise.

No live records, services, models or legal notifications are used.
"""
MISSION_ID = 'audit-trail'

REVISION = 'audit-trail-guidance-v1'

BRIEFING = {'revision': 'audit-trail-guidance-v1',
 'role': 'Help a fictional technology auditor evaluate change-control evidence and track verified '
         'remediation.',
 'objectives': ['Define scope and assess population completeness before selecting risk-based '
                'change samples.',
                'Corroborate missing approval evidence against policy criteria without assuming '
                'fraud.',
                'Report validated control gaps and distinguish remediation commitments from '
                'verified closure.'],
 'workflow': ['Read the stage task and inspect every fictional record before deciding.',
              'Select the finding most relevant to the decision and compare the available actions.',
              'Commit your recommendation and read the action and finding explanations.',
              'Finish three decisions to save the result, then try five optional review '
              'questions.'],
 'completion': 'Three committed decisions save the result. Optional review is separate practice '
               'with no saved grade or change to the score.'}

STAGES = [{'task': 'Plan evidence-based testing of management’s claim that every critical change was '
          'approved.',
  'hints': ['A stated total is not proof that the population includes all relevant changes.',
            'Obtain and reconcile the in-scope population, then select documented risk-based '
            'samples; incomplete approval evidence needs testing, not a prewritten conclusion.'],
  'artifacts': [{'title': 'Reported change population',
                 'body': 'The fictional team reports 240 change records. Define the audit period '
                         'and scope, obtain the full in-scope population and assess completeness '
                         'using available corroborating sources before selecting samples. The '
                         'reported count alone does not prove no changes are missing.'},
                {'title': 'Incomplete approval records',
                 'body': 'Approval evidence is incomplete despite the claim that every critical '
                         'change was approved. Seek corroborating records and test the claim. '
                         'Neither management’s verbal assurance nor missing evidence alone '
                         'supports a final conclusion about every change.'},
                {'title': 'Risk-based sampling option',
                 'body': 'Risk-based sampling is available. Document selection criteria and relate '
                         'them to the audit objective and population. A sample supports a '
                         'conclusion within its evidence limits; it does not establish that every '
                         'untested change complied.'}]},
 {'task': 'Evaluate one sampled change with a blank approval field using corroboration and policy.',
  'hints': ['A deployment timestamp shows timing, not independent approval.',
            'Inspect corroborating records and emergency-policy criteria; the existence of a '
            'policy does not prove this change qualified or complied.'],
  'artifacts': [{'title': 'Recorded deployment timestamp',
                 'body': 'The sampled fictional production change has a deployment timestamp. Use '
                         'timing to compare the sequence of approval, deployment and any required '
                         'follow-up. A timestamp alone does not establish independent '
                         'authorisation.'},
                {'title': 'Blank approver field',
                 'body': 'The approver field is blank. Seek corroborating independent approval '
                         'evidence, evaluate the applicable policy and assess impact. Do not '
                         'delete the sample or assume fraud solely from the missing field; record '
                         'a validated exception when supported.'},
                {'title': 'Emergency change policy',
                 'body': 'An emergency change policy exists. Check whether the change met its '
                         'criteria and required authorisation and follow-up, including any defined '
                         'retrospective review. A policy’s existence is not evidence that its '
                         'exception path applied or was followed.'}]},
 {'task': 'Report repeated validated exceptions while tracking management’s plan to verified '
          'closure.',
  'hints': ['An assigned owner and due date support accountability but do not prove the control '
            'now works.',
            'Retest implemented corrective actions with suitable evidence before closing the '
            'finding; distinguish planned, implemented and verified status.'],
  'artifacts': [{'title': 'Identified root cause',
                 'body': 'Management has identified a root cause for repeated change-control '
                         'exceptions. Evaluate the explanation against observed evidence and '
                         'whether proposed actions address it. A plausible cause is not itself '
                         'proof of effective remediation.'},
                {'title': 'Assigned owner and due date',
                 'body': 'A remediation owner and due date are assigned. Track milestones, '
                         'escalate overdue actions through the agreed process and keep management '
                         'accountable for implementation. The auditor verifies evidence rather '
                         'than takes over operational ownership.'},
                {'title': 'Missing retest evidence',
                 'body': 'Retesting evidence is not yet available. Report the validated gap and '
                         'track remediation, distinguishing the commitment from implemented and '
                         'independently verified correction. Do not close or remove the finding on '
                         'a promise alone.'}]}]

FINDING_EXPLANATIONS = ['Incomplete approval evidence is the key gap in management’s assertion. Define scope, assess '
 'population completeness and use documented evidence-based samples rather than accept the verbal '
 'claim.',
 'The recorded deployment timestamp helps corroborate the event sequence but does not prove '
 'approval. Evaluate the blank field with other records, policy criteria and impact without '
 'unsupported fraud attribution.',
 'Without retest evidence, a plan and assigned owner do not justify verified closure. Report the '
 'validated gap and track implementation and suitable retesting.']

REVIEW = [{'id': 'audit-population-completeness',
  'prompt': 'What should be established before drawing samples from the reported 240 changes?',
  'options': ['That 240 is a sufficiently large number by itself',
              'The defined scope and completeness of the in-scope population using available '
              'corroboration',
              'That management’s statement needs no evidence'],
  'answer': 1,
  'feedback': ['A count alone does not establish completeness.',
               'Correct. Sampling a population with unknown omissions can miss relevant activity.',
               'The assertion is what testing must evaluate.']},
 {'id': 'audit-sample-limit',
  'prompt': 'What can risk-based sampling support when its selection and testing are documented?',
  'options': ['A conclusion within the scope and limits of the evidence',
              'Proof that every untested change was approved',
              'A conclusion written before any evidence is reviewed'],
  'answer': 0,
  'feedback': ['Correct. Explain selection and limitations rather than claim universal compliance.',
               'Untested records are not individually proven compliant by sampling.',
               'Conclusions must follow the evidence.']},
 {'id': 'audit-emergency-evidence',
  'prompt': 'How should an existing emergency change policy affect review of a missing approval?',
  'options': ['It automatically excuses every missing approval',
              'It proves fraud occurred',
              'Its applicability and required authorisation and follow-up must be checked against '
              'records'],
  'answer': 2,
  'feedback': ['A policy is not evidence that the change qualified or complied.',
               'Missing approval alone does not establish fraud.',
               'Correct. Corroborate the event and evaluate the actual policy criteria.']},
 {'id': 'audit-timestamp-limit',
  'prompt': 'What does a deployment timestamp establish on its own?',
  'options': ['Independent approval',
              'Timing evidence that can be compared with authorisation and follow-up records',
              'That the emergency policy was followed'],
  'answer': 1,
  'feedback': ['Timing is not authorisation.',
               'Correct. It supports chronology, while approval requires separate evidence.',
               'Policy compliance needs its own supporting evidence.']},
 {'id': 'audit-closure-evidence',
  'prompt': 'Why keep a validated finding open when management assigns an owner and due date but '
            'no retest evidence exists?',
  'options': ['A commitment does not yet demonstrate effective correction',
              'Auditors should permanently own the operational control',
              'Root cause and a promise prove successful remediation'],
  'answer': 0,
  'feedback': ['Correct. Track implementation and obtain suitable retest evidence for verified '
               'closure.',
               'Management owns remediation; auditors evaluate evidence.',
               'A plan is not evidence that the revised control works.']}]
