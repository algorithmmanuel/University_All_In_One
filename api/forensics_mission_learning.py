"""Forensics Desk v1: fictional acquisition, transfer and timeline records.

No real device is acquired and no private file or forensic image is requested.
"""
MISSION_ID = 'forensics-desk'
REVISION = 'forensics-desk-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional authorised investigator preserve a workstation’s state and reason about evidence integrity and time.',
    'objectives': [
        'Document the current state and follow an authorised acquisition process that accounts for volatile evidence.',
        'Verify image integrity and maintain traceable evidence transfers.',
        'Correlate timestamps using documented clock offsets and uncertainty.',
    ],
    'workflow': [
        'Read the stage task and inspect every fictional device, transfer or event record.',
        'Choose the finding most relevant to preservation, integrity or timing.',
        'Commit an evidence-preserving recommendation and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'Three committed decisions save the mission result. Review remains separate practice without a saved grade or score change.',
}
STAGES = [
    {'task': 'Plan authorised acquisition without casually altering the suspected workstation or losing volatile evidence.',
     'hints': ['An acquisition decision depends on the device’s present state and the approved procedure.', 'Document what is observable, confirm authority and follow the trained acquisition plan; do not improvise browsing, reinstalling or power changes.'],
     'artifacts': [
         {'title': 'Powered-on state', 'body': 'The fictional workstation is powered on and suspected of unauthorised access. Record its observed state and follow the authorised procedure. Routine browsing, software installation or other changes could alter evidence.'},
         {'title': 'Volatile evidence', 'body': 'Some evidence, such as running activity and memory state, can change or disappear when the system state changes. Do not assume an immediate shutdown or reinstall is always the correct acquisition step. The trained investigator follows an approved plan that considers preservation and operational needs.'},
         {'title': 'Authority and scope', 'body': 'The forensic process requires appropriate authorisation and scope. Document the acquisition actions and handling. Suspicion does not authorise exploring unrelated personal files, and reinstalling the system would destroy useful state.'},
     ]},
    {'task': 'Transfer a forensic image with integrity checks and traceable handling.',
     'hints': ['A transfer should preserve the recorded evidence rather than modify the original image.', 'Compare the appropriate cryptographic hash values and record who transferred what, when and how; matching hashes do not establish every other fact about the evidence.'],
     'artifacts': [
         {'title': 'Recorded image hash', 'body': 'A cryptographic hash of the fictional image is recorded. Verify the expected hash before and after a transfer under the procedure. Matching hashes support byte-level integrity relative to that recorded reference; they do not alone prove who created the evidence or that acquisition was authorised.'},
         {'title': 'Custody log', 'body': 'A chain-of-custody log records identifiers, handlers and transfers. Keep it accurate and use the approved transfer channel. A matching hash does not replace knowing who handled the image or when.'},
         {'title': 'Secured original', 'body': 'The original device is secured. Preserve the original and use approved working copies for analysis. Do not edit the original image to make analysis easier or use an untracked sharing route.'},
     ]},
    {'task': 'Reconstruct the event sequence using clock context and independent records rather than sort raw times blindly.',
     'hints': ['Two displayed times may come from clocks with different offsets or time zones.', 'Apply documented time normalisation, retain the original values and uncertainty, and corroborate the sequence with independent evidence.'],
     'artifacts': [
         {'title': 'System event', 'body': 'A fictional system event is displayed at 10:04. Keep its original timestamp and source information; the displayed time alone does not prove its order relative to a record from a different clock.'},
         {'title': 'Authentication event', 'body': 'A related authentication event is displayed at 10:02. Compare its source, time zone, clock behaviour and event meaning before deciding the sequence. Do not delete a record simply because its displayed time appears inconsistent.'},
         {'title': 'Documented clock offset', 'body': 'The investigation records a clock offset. Normalise timestamps using that documented context, retain the transformation and any uncertainty, and correlate independent records. Normalisation helps comparison; it does not make every clock perfectly accurate or prove causation by itself.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'Potential loss of volatile evidence makes the current device state important. Document and follow authorised acquisition procedures rather than casually browse, reinstall or change power state.',
    'The recorded image hash supports checking integrity through the transfer. Record handling and protect the original too; a hash is not a substitute for authorisation or custody records.',
    'The documented clock offset is essential to a defensible time comparison. Preserve original values, normalise transparently and correlate sources instead of treating raw times as exact.',
]
REVIEW = [
    {'id': 'forensic-volatile', 'prompt': 'Why should acquisition of a powered-on suspected workstation follow a preservation plan?',
     'options': ['Reinstalling always preserves the most evidence', 'Changing system state can alter or remove volatile evidence', 'Suspicion permits browsing every private file'], 'answer': 1,
     'feedback': ['Reinstalling replaces valuable state rather than preserve it.', 'Correct. Document the current state and follow the authorised trained process.', 'Authority and scope still apply to the investigation.']},
    {'id': 'forensic-hash-limit', 'prompt': 'An image’s hash matches the recorded reference after transfer. What does that support?',
     'options': ['Proof that every acquisition action was authorised', 'Proof of who originally created every file', 'Byte-level integrity relative to the recorded reference'], 'answer': 2,
     'feedback': ['A matching hash does not establish authorisation.', 'A hash comparison alone does not identify who created the contents.', 'Correct. Integrity checking has a specific scope; retain the other acquisition and handling evidence too.']},
    {'id': 'forensic-custody', 'prompt': 'Which handling practice complements verifying an image hash?',
     'options': ['Record each authorised transfer and preserve the original', 'Use an untracked channel because the hash exists', 'Edit the original image before handing it over'], 'answer': 0,
     'feedback': ['Correct. Traceable handling and original preservation support the integrity check.', 'An integrity reference does not replace custody records or an approved channel.', 'Editing the original alters the evidence being preserved.']},
    {'id': 'forensic-raw-time', 'prompt': 'A system log shows 10:04 and a different source shows 10:02. What is needed before relying on that order?',
     'options': ['Assume both clocks are exact', 'Review clock offsets/time context and correlate the records', 'Delete whichever record disagrees'], 'answer': 1,
     'feedback': ['Different clocks and time settings can make raw ordering misleading.', 'Correct. Use documented normalisation and independent context before asserting a sequence.', 'Disagreement is a reason to investigate, not destroy a source.']},
    {'id': 'forensic-time-record', 'prompt': 'After normalising timestamps, what should the investigation retain?',
     'options': ['Only the adjusted values with no explanation', 'A claim that normalisation proves causation', 'Original values, transformation context and remaining uncertainty'], 'answer': 2,
     'feedback': ['Losing the original values and method makes the comparison harder to review.', 'A clearer time comparison does not alone prove one event caused another.', 'Correct. Keep the comparison traceable and its limits explicit.']},
]
