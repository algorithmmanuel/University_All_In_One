"""Source-owned guidance for a fictional boardroom-breach decision exercise.

No live records, services, models or legal notifications are used.
"""
MISSION_ID = 'boardroom-breach'

REVISION = 'boardroom-breach-guidance-v1'

BRIEFING = {'revision': 'boardroom-breach-guidance-v1',
 'role': 'Help a fictional board oversee an uncertain cyber crisis, recovery trade-offs and '
         'responsible disclosure.',
 'objectives': ['Separate confirmed impact from uncertainty and require accountable, time-bound '
                'incident updates.',
                'Evaluate recovery gates and temporary alternatives before approving service '
                'reopening.',
                'Oversee accurate, timely disclosures and remediation using the completed '
                'notification assessment.'],
 'workflow': ['Read the stage task and inspect every fictional record before deciding.',
              'Select the finding most relevant to the decision and compare the available actions.',
              'Commit your recommendation and read the action and finding explanations.',
              'Finish three decisions to save the result, then try five optional review '
              'questions.'],
 'completion': 'Three committed decisions save the result. Optional review is separate practice '
               'with no saved grade or change to the score.'}

STAGES = [{'task': 'Request a verified first situation report without inventing attribution or impact '
          'certainty.',
  'hints': ['An activated commander establishes ownership, not a completed impact assessment.',
            'Ask for confirmed facts, unknowns, decisions, accountable owners and the next update; '
            'route possible notification duties to qualified advisers.'],
  'artifacts': [{'title': 'Incomplete impact assessment',
                 'body': 'The fictional service outage may involve a cyberattack, but impact '
                         'assessment is incomplete. Separate observed disruption from estimates '
                         'and unknowns. Request a verified situation report and a time-bound next '
                         'update; do not promise zero financial impact or identify an attacker '
                         'without evidence.'},
                {'title': 'Activated incident command',
                 'body': 'An incident commander is activated. Require clear response ownership, '
                         'decision requests and escalation. The board oversees priorities and '
                         'accountability; activation alone does not establish the cause, full '
                         'impact or successful containment.'},
                {'title': 'Possible notification duties',
                 'body': 'Notification timelines may apply. Have the authorised legal/compliance '
                         'team assess applicable obligations and track required decisions '
                         'promptly. This exercise provides no jurisdiction-specific deadline and '
                         'does not justify waiting for perfect certainty before seeking advice.'}]},
 {'task': 'Evaluate a proposed reopening using explicit recovery gates and executive '
          'accountability.',
  'hints': ['Revenue importance matters, but incomplete containment validation remains a decision '
            'risk.',
            'Compare temporary alternatives and documented validation criteria; executive approval '
            'should record residual exposure rather than replace technical checks.'],
  'artifacts': [{'title': 'Revenue-critical service',
                 'body': 'Operations needs the fictional service to support revenue. Include '
                         'business impact and urgency in the decision, but do not use urgency as '
                         'evidence that the service is contained or safe to reopen.'},
                {'title': 'Incomplete security validation',
                 'body': 'Containment validation is incomplete. Require risk-based recovery gates, '
                         'evidence of the necessary checks and documented executive approval of '
                         'remaining exposure before reopening. Record conditions and monitoring '
                         'rather than conceal the trade-off.'},
                {'title': 'Temporary alternatives',
                 'body': 'Temporary service alternatives are available. Compare their operational '
                         'limits and customer effects while validation proceeds. An alternative '
                         'can reduce pressure to reopen prematurely; it does not itself fix the '
                         'incident.'}]},
 {'task': 'Oversee disclosure and remediation after the notification assessment confirms a '
          'reportable incident.',
  'hints': ['Use the completed assessment and reviewed plan to coordinate timely factual '
            'disclosures.',
            'Estimated affected population must remain labelled as estimated; minimise disclosed '
            'personal information and track corrective actions.'],
  'artifacts': [{'title': 'Completed notification assessment',
                 'body': 'The fictional legal notification assessment is complete and confirms a '
                         'reportable customer data incident. Oversee timely action through the '
                         'authorised process using that assessment. Do not invent a universal '
                         'reporting deadline or delay all communications indefinitely.'},
                {'title': 'Estimated affected population',
                 'body': 'The number of affected customers is estimated. Clearly distinguish '
                         'confirmed facts, estimates and remaining uncertainty, updating '
                         'communications when verified information changes. Publishing raw '
                         'customer records would add exposure without proving responsible '
                         'disclosure.'},
                {'title': 'Reviewed communications plan',
                 'body': 'The communications plan has been reviewed. Oversee accurate, timely '
                         'disclosures and coordinated remediation, with accountable follow-up. A '
                         'reviewed plan is a basis for action, not evidence that notifications or '
                         'corrective actions have already been completed.'}]}]

FINDING_EXPLANATIONS = ['The incomplete impact assessment is the key uncertainty. A verified report, named ownership and '
 'next update support decisions without unsupported attribution or promises.',
 'Incomplete security validation is the central reopening risk. Use evidenced recovery gates, '
 'temporary alternatives and documented executive approval rather than let urgency substitute for '
 'validation.',
 'The reviewed communications plan supports coordinated disclosure after the completed assessment. '
 'Verify timely execution and remediation; keep population estimates explicit and protect customer '
 'records.']

REVIEW = [{'id': 'board-known-unknown',
  'prompt': 'What belongs in the first board update while incident impact remains incomplete?',
  'options': ['A guaranteed zero-loss figure',
              'Confirmed facts, explicit unknowns, owners and a scheduled next update',
              'A public accusation based on suspicion'],
  'answer': 1,
  'feedback': ['Incomplete assessment cannot support a zero-loss guarantee.',
               'Correct. This gives accountable decision support while making uncertainty visible.',
               'Suspicion alone does not establish attribution.']},
 {'id': 'board-command-role',
  'prompt': 'What does activation of an incident commander demonstrate in this scenario?',
  'options': ['Response ownership has been established',
              'Containment has been verified',
              'Every affected customer is known'],
  'answer': 0,
  'feedback': ['Correct. Ownership supports coordination; impact and containment still need '
               'evidence.',
               'Activation is not a containment test.',
               'The impact assessment is still incomplete.']},
 {'id': 'board-reopen-gate',
  'prompt': 'How should revenue urgency affect a reopening decision when security validation is '
            'incomplete?',
  'options': ['It proves reopening is safe',
              'It removes the need to document approval',
              'It informs a trade-off evaluated against recovery gates and temporary alternatives'],
  'answer': 2,
  'feedback': ['Revenue importance does not establish safety.',
               'Material trade-offs need accountable documented decisions.',
               'Correct. Urgency matters, alongside evidence, alternatives and residual risk.']},
 {'id': 'board-notification-assessment',
  'prompt': 'How should the board handle possible notification obligations before their '
            'applicability is settled?',
  'options': ['Ignore them until the annual review',
              'Promptly obtain and track the authorised legal/compliance assessment',
              'Assume one universal deadline applies everywhere'],
  'answer': 1,
  'feedback': ['Delay may undermine timely handling of applicable duties.',
               'Correct. Use qualified assessment and accountable follow-up without inventing a '
               'deadline.',
               'This exercise supplies no universal jurisdictional rule.']},
 {'id': 'board-population-estimate',
  'prompt': 'What is appropriate when disclosing an incident whose affected population is still '
            'estimated?',
  'options': ['Label the estimate, use verified facts and update through the reviewed plan',
              'Publish raw customer records to demonstrate transparency',
              'Present the estimate as a final confirmed count'],
  'answer': 0,
  'feedback': ['Correct. Accurate communication preserves uncertainty and protects personal '
               'records.',
               'Publishing personal records creates additional exposure.',
               'An estimate should not be misrepresented as final.']}]
