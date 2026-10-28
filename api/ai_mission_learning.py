"""Source-owned guidance for a fictional ai-governance decision exercise.

No live records, services, models or legal notifications are used.
"""
MISSION_ID = 'ai-governance'

REVISION = 'ai-governance-guidance-v1'

BRIEFING = {'revision': 'ai-governance-guidance-v1',
 'role': 'Help a fictional AI risk team govern a credit-assessment pilot from inventory to ongoing '
         'monitoring.',
 'objectives': ['Register a consequential AI use case and clarify accountability and training-data '
                'lineage before scaling.',
                'Investigate group error differences with attention to sample representativeness '
                'and customer impact.',
                'Respond to drift and complaints using approved protective thresholds, review and '
                'controlled model changes.'],
 'workflow': ['Read the stage task and inspect every fictional record before deciding.',
              'Select the finding most relevant to the decision and compare the available actions.',
              'Commit your recommendation and read the action and finding explanations.',
              'Finish three decisions to save the result, then try five optional review '
              'questions.'],
 'completion': 'Three committed decisions save the result. Optional review is separate practice '
               'with no saved grade or change to the score.'}

STAGES = [{'task': 'Bring an unregistered lending model under accountable governance before expansion.',
  'hints': ['The model influences lending, so deployment consequences matter alongside technical '
            'performance.',
            'Missing data lineage limits assessment of suitability; assign an owner and document '
            'the use case rather than scale an unassessed pilot.'],
  'artifacts': [{'title': 'Lending decision influence',
                 'body': 'The fictional model influences lending decisions. Register its intended '
                         'use, decision role and affected users, assign an accountable owner and '
                         'assess risk before scaling. A working pilot is not evidence that '
                         'expansion is appropriate.'},
                {'title': 'Incomplete training-data lineage',
                 'body': 'Training-data lineage is incomplete: the team cannot fully trace the '
                         'origin and preparation of training data. Document and investigate these '
                         'gaps when assessing suitability and limitations. Lineage evidence helps '
                         'review but does not alone prove accuracy or fairness.'},
                {'title': 'Unassigned model owner',
                 'body': 'No model owner is assigned. Establish accountability for approval, '
                         'monitoring and corrective decisions. Registration and an owner are '
                         'starting controls, not substitutes for validation or evidence of '
                         'acceptable customer impact.'}]},
 {'task': 'Investigate different group error rates without hiding metrics or overclaiming what '
          'they prove.',
  'hints': ['A measurable gap deserves investigation; unequal sample sizes affect confidence and '
            'representativeness.',
            'Overall accuracy and the presence of human review do not settle subgroup impact; '
            'document limitations and verify how oversight works.'],
  'artifacts': [{'title': 'Measured performance gap',
                 'body': 'Validation shows different error rates across fictional customer groups. '
                         'Investigate the size and consequences of those differences, document '
                         'appropriate fairness and impact checks and select controls. A measured '
                         'gap warrants review; it does not alone identify its cause.'},
                {'title': 'Unequal evaluation samples',
                 'body': 'Evaluation sample sizes differ between groups. Examine '
                         'representativeness and uncertainty before drawing broad conclusions. Do '
                         'not suppress subgroup metrics or claim a small sample establishes a '
                         'reliable population-wide result.'},
                {'title': 'Human review process',
                 'body': 'Human review exists, but its effectiveness must be checked: what '
                         'reviewers see, when they can intervene and whether corrections are '
                         'tracked. A human in the process does not automatically eliminate unfair '
                         'outcomes or replace model validation.'}]},
 {'task': 'Use changed inputs and rising complaints to trigger review of the approved model.',
  'hints': ['Prior approval describes an earlier decision, not permanent suitability after '
            'conditions change.',
            'Review drift and customer effects using protective thresholds and the available '
            'rollback plan; retraining needs controlled approval and validation.'],
  'artifacts': [{'title': 'Shifted input distributions',
                 'body': 'Input distributions shifted after a fictional market change. This is a '
                         'drift signal for review of continued suitability, not proof by itself of '
                         'the cause of every prediction error. Compare current evidence with '
                         'approved monitoring thresholds.'},
                {'title': 'Increasing complaints',
                 'body': 'Complaint rate increased. Investigate customer impact alongside drift '
                         'and performance evidence, escalating through the model owner and '
                         'applying approved protective thresholds. Do not dismiss concerns merely '
                         'because the model was previously approved.'},
                {'title': 'Available rollback plan',
                 'body': 'A rollback plan exists. Assess it as a controlled protective option '
                         'under the approved process, including operational effects. Retraining or '
                         'replacement needs approval and validation before release; the presence '
                         'of a plan is not evidence it has been exercised.'}]}]

FINDING_EXPLANATIONS = ['Incomplete training-data lineage is a material evidence gap for the lending use case. Register '
 'the model, assign ownership and assess its risks and limitations before scaling.',
 'The measurable group performance gap requires investigation of representativeness, uncertainty '
 'and customer consequences. Overall accuracy and nominal human review cannot settle those '
 'questions.',
 'Rising complaints provide an impact signal alongside changed inputs. Trigger accountable drift '
 'review and approved protective measures; validate and approve any retraining before release.']

REVIEW = [{'id': 'ai-lineage-gap',
  'prompt': 'Why investigate incomplete training-data lineage before expanding the lending pilot?',
  'options': ['It guarantees a particular fairness result',
              'It reveals data origin and preparation gaps that limit suitability assessment',
              'It replaces the need for a model owner'],
  'answer': 1,
  'feedback': ['Lineage alone cannot guarantee fairness.',
               'Correct. Traceability helps the team evaluate limitations and obtain missing '
               'evidence.',
               'Accountability is still required.']},
 {'id': 'ai-register-limits',
  'prompt': 'What does registering a model and assigning its owner achieve?',
  'options': ['Proof that all lending outcomes are fair',
              'Permission to skip validation',
              'Visibility and accountability as a starting point for risk assessment'],
  'answer': 2,
  'feedback': ['Registration does not establish outcome fairness.',
               'Validation remains necessary.',
               'Correct. These controls make the use case governable; they do not prove '
               'suitability.']},
 {'id': 'ai-sample-confidence',
  'prompt': 'Why examine unequal evaluation sample sizes when comparing group error rates?',
  'options': ['Representativeness and uncertainty affect how confidently results can be '
              'interpreted',
              'Small samples always prove there is no issue',
              'Overall accuracy makes group samples irrelevant'],
  'answer': 0,
  'feedback': ['Correct. Investigate the gap and its limits rather than suppress or overstate it.',
               'A small sample limits certainty; it does not establish absence of harm.',
               'Overall results can obscure group differences.']},
 {'id': 'ai-human-effectiveness',
  'prompt': 'What must be checked beyond the existence of human review in the AI pilot?',
  'options': ['Whether reviewers can identify and correct issues and whether interventions are '
              'tracked',
              'Only whether the process is called human review',
              'Nothing, because a person always removes model error'],
  'answer': 0,
  'feedback': ['Correct. Oversight needs effective intervention and evidence of follow-through.',
               'A label does not demonstrate useful oversight.',
               'Human involvement does not guarantee correct or fair outcomes.']},
 {'id': 'ai-drift-response',
  'prompt': 'What should follow changed model inputs and increasing complaints after approval?',
  'options': ['Ignore both until the annual review',
              'Retrain and release immediately without validation',
              'Review impact and drift, apply approved protective measures and control any model '
              'change'],
  'answer': 2,
  'feedback': ['Changing conditions require timely review.',
               'Retraining is a controlled change requiring approval and validation.',
               'Correct. Prior approval does not establish continuing suitability.']}]
