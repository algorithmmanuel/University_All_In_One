"""Network Watch v1: fictional flow correlation and proportionate host response.

The documentation address is a training label, not a destination to contact.
"""
MISSION_ID = 'network-watch'
REVISION = 'network-watch-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional campus analyst assess unusual outbound traffic and recommend a scoped response.',
    'objectives': [
        'Compare current traffic with an asset baseline without treating volume alone as proof of compromise.',
        'Correlate recurring flows with destination, DNS and endpoint evidence.',
        'Recommend authorised host containment and preserve evidence when an unauthorised process is confirmed.',
    ],
    'workflow': [
        'Read the current network task and inspect every fictional baseline, flow or endpoint record.',
        'Choose the finding most relevant to the investigation stage.',
        'Commit a defensive recommendation and read the explanation.',
        'Complete three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Optional review is ungraded practice and does not change that result.',
}
STAGES = [
    {'task': 'Compare the outbound spike with the lab computer’s baseline before choosing a response.',
     'hints': ['A sudden change needs context about the asset and activity, not only a large number.', 'Check flows, destinations and expected use; preserve records instead of deleting them or disabling the whole campus.'],
     'artifacts': [
         {'title': 'Usual traffic', 'body': 'The fictional lab computer normally sends about 2 GB per hour. A baseline describes expected behaviour for this asset and time, not a universal threshold for every computer.'},
         {'title': 'Current volume', 'body': 'Current outbound volume is 24 GB per hour, a substantial change from the recorded baseline. Compare flows, destinations and expected activity to assess the cause. A legitimate transfer could also increase volume; the number alone does not prove theft.'},
         {'title': 'Routine printer job', 'body': 'A printer job completed normally. That background observation does not explain the lab computer’s outbound spike. Avoid indiscriminate campus shutdown or deletion of traffic records before a scoped assessment.'},
     ]},
    {'task': 'Correlate recurring connections with endpoint and DNS records to understand their source and purpose.',
     'hints': ['Look for records referring to the same asset and time window.', 'Regular timing is a useful pattern to investigate, but authorised software can also make periodic connections.'],
     'artifacts': [
         {'title': 'Destination review', 'body': 'Fictional flows reach 203.0.113.45, which is not on the available approved destination list. This reserved documentation address is only a training label. Check destination context and DNS records without contacting a live endpoint.'},
         {'title': 'Managed computer', 'body': 'The lab computer is managed. That status does not prove every running process or outbound connection is authorised. Use available endpoint evidence to identify the relevant process and activity.'},
         {'title': 'Recurring interval', 'body': 'Connections recur every 30 seconds. Correlate the timing with endpoint activity and DNS records to explain what initiated them. Regular intervals alone are not proof of malicious command traffic, and the investigation does not call for blocking all internet access indefinitely.'},
     ]},
    {'task': 'Recommend a scoped response after telemetry confirms an unauthorised process initiated the connections.',
     'hints': ['New confirming evidence changes the response from investigating an anomaly to handling known unauthorised activity.', 'Contain the affected host under the plan while retaining evidence and checking whether the scope extends further.'],
     'artifacts': [
         {'title': 'Process confirmation', 'body': 'Fictional endpoint telemetry confirms an unauthorised process started the recurring connections. This is more specific than a traffic anomaly. Recommend isolating the affected host under the authorised incident procedure and preserving investigation evidence.'},
         {'title': 'Known scope', 'body': 'One workstation is affected so far. That is the current known scope, not proof that all other assets are safe. Continue appropriate checks while avoiding an unjustified indefinite block of the entire campus.'},
         {'title': 'Evidence preservation', 'body': 'Relevant flow, DNS and endpoint snapshots are available. Retain them under the response procedure rather than erase logs while containing the host. Document the action, known scope and follow-up.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The current outbound volume is the change to explain against the asset baseline. Compare flows and destinations; unrelated normal activity and the volume alone do not settle the cause.',
    'The recurring interval provides a correlation lead across flows, DNS and endpoint activity. An unapproved destination adds context, while managed status does not establish legitimacy.',
    'The confirmed unauthorised process supports proportionate host isolation under the response plan. Preserve evidence and continue scoping rather than ignore or erase the finding.',
]
REVIEW = [
    {'id': 'network-baseline', 'prompt': 'A lab computer moves from 2 GB to 24 GB outbound per hour. What should the analyst establish?',
     'options': ['That any large transfer proves theft', 'How its flows, destinations and expected activity explain the change', 'That a normal printer job makes the spike irrelevant'], 'answer': 1,
     'feedback': ['Volume alone does not establish purpose or compromise.', 'Correct. Use the asset baseline and related records to explain the deviation.', 'An unrelated normal event does not explain the affected asset’s traffic.']},
    {'id': 'network-regularity', 'prompt': 'Connections recur every 30 seconds. Which conclusion is justified by that pattern alone?',
     'options': ['Malicious control is proven', 'The process must be authorised', 'The timing is a lead to correlate with endpoint and DNS evidence'], 'answer': 2,
     'feedback': ['Both legitimate and unauthorised activity can be periodic.', 'Regular timing does not grant authorisation.', 'Correct. Investigate the pattern with related evidence rather than treat timing as a verdict.']},
    {'id': 'network-managed-limit', 'prompt': 'Why still inspect endpoint evidence when the lab computer is managed?',
     'options': ['Management does not prove every process and connection is authorised', 'Managed computers cannot produce logs', 'Managed status explains every traffic spike'], 'answer': 0,
     'feedback': ['Correct. Use actual activity records to identify what initiated the connections.', 'Management does not make activity records impossible.', 'A management label is not an explanation of a particular event.']},
    {'id': 'network-host-scope', 'prompt': 'Telemetry confirms an unauthorised process on one host. Which response is proportionate?',
     'options': ['Ignore it because only one host is known', 'Isolate the affected host under the response plan, retain evidence and continue scoping', 'Erase the traffic records before acting'], 'answer': 1,
     'feedback': ['A limited known scope is not a reason to ignore confirmed activity.', 'Correct. Act on the confirmed host while preserving evidence and assessing scope.', 'Erasing records removes evidence needed for the response.']},
    {'id': 'network-scope-limit', 'prompt': 'The team has found one affected workstation so far. What should the report say?',
     'options': ['Every other asset is certainly unaffected', 'No follow-up is needed', 'State the known scope and which further checks remain'], 'answer': 2,
     'feedback': ['Current findings do not prove that every unchecked asset is safe.', 'The scope still needs appropriate assessment.', 'Correct. Distinguish current evidence from assumptions about unexamined systems.']},
]
