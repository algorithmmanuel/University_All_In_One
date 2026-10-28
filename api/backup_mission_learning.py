"""Backup Buddy v1: fictional project copies, restore checks and a lost device.

No learner files are uploaded, restored or deleted by this training content.
"""
MISSION_ID = 'backup-buddy'
REVISION = 'backup-buddy-guidance-v1'
BRIEFING = {
    'revision': REVISION,
    'role': 'Help a fictional student protect a school project and recover safely after a laptop is lost.',
    'objectives': [
        'Recognise the risk of keeping a project in only one place.',
        'Verify backup freshness and the ability to access or restore the intended file.',
        'Separate file recovery from securing accounts and reporting a missing device.',
    ],
    'workflow': [
        'Read the stage task and inspect each fictional copy, sync or device record.',
        'Select the finding that best explains the recovery risk.',
        'Commit a safer action and read the explanation.',
        'Finish three decisions to save your result, then try five optional review questions.',
    ],
    'completion': 'All three committed decisions save the mission result. Review saves no separate grade and does not change the score.',
}
STAGES = [
    {'task': 'Reduce the risk of losing a project that exists only on one laptop.',
     'hints': ['A deadline does not make the device immune to loss, failure or damage.', 'Create a separate, protected backup using an approved route rather than assume the only copy will survive.'],
     'artifacts': [
         {'title': 'Only project copy', 'body': 'The fictional laptop contains the project’s only copy. Device failure, loss or accidental deletion could remove the work. A separate protected backup reduces this single-copy dependency.'},
         {'title': 'Backup destination', 'body': 'An approved external or cloud backup route is available. Keep access protected and use a suitable independent copy or version history. A second folder on the same laptop does not protect against losing that laptop. Sync alone may also propagate unwanted changes or deletions.'},
         {'title': 'Deadline context', 'body': 'The project is due tomorrow. Create and verify the backup promptly rather than rely on the deadline or the laptop’s previous reliability. Never email an account password as a substitute for protecting project files.'},
     ]},
    {'task': 'Check that the available backup includes recent work and can actually be recovered.',
     'hints': ['A success indicator from last week says little about edits made today.', 'Check the required version and test access or restore to a separate safe location before deleting an original.'],
     'artifacts': [
         {'title': 'Old sync status', 'body': 'The fictional cloud service last reports a sync from a week ago. That status does not establish that the current project is backed up.'},
         {'title': 'Recent edits', 'body': 'The learner has made newer edits. Confirm that the intended file version and latest required changes reached a protected backup, not just that an account is connected to a sync service.'},
         {'title': 'Restore check', 'body': 'Test access or restoration of the intended version into a separate safe location and verify that it opens correctly. Do not delete the local original first or overwrite the only good copy during the test. Backups support recovery, but must be checked.'},
     ]},
    {'task': 'Respond to a lost laptop using both account-protection and verified file-recovery steps.',
     'hints': ['A backup restores files; it does not revoke sessions on a missing device.', 'Report the loss, secure affected access through trusted service/device controls and restore from the verified copy.'],
     'artifacts': [
         {'title': 'Possible account sessions', 'body': 'The fictional missing laptop may retain signed-in accounts. Use another trusted device and official controls to review or revoke sessions and secure affected accounts under the applicable procedure. A file backup does not end those sessions.'},
         {'title': 'Verified backup', 'body': 'The project backup was tested and contains the needed version. Restore through the trusted route to a suitable device and check the recovered file. A verified copy supports recovery, but does not by itself settle the security impact of losing the laptop.'},
         {'title': 'Device response route', 'body': 'Report the loss through the appropriate school or device-management process and follow authorised guidance about protection or recovery options. Do not publish passwords while asking for help, and do not assume every device supports the same remote controls.'},
     ]},
]
FINDING_EXPLANATIONS = [
    'The only copy on one laptop is the central loss dependency. A separate protected and usable backup is needed; a deadline or reliable history does not remove that risk.',
    'An old sync timestamp leaves newer work unverified. Confirm the intended version and test recovery safely before relying on the backup or deleting an original.',
    'The verified backup supports file recovery. It does not close possible account sessions or replace reporting and device-security steps after the loss.',
]
REVIEW = [
    {'id': 'backup-same-laptop', 'prompt': 'Why is a second project folder on the same laptop insufficient protection against losing the laptop?',
     'options': ['Folder names determine whether loss is possible', 'Both copies are lost with the same device', 'Every second folder is an independent off-device backup'], 'answer': 1,
     'feedback': ['A name does not change where the data is held.', 'Correct. Use a suitable separate protected copy so the same device loss does not remove both.', 'A second folder remains dependent on the same laptop.']},
    {'id': 'backup-sync-limit', 'prompt': 'Why consider version history or an independent protected copy alongside sync?',
     'options': ['Sync can never transfer a file', 'Connected accounts never lose data', 'Sync may carry unwanted changes or deletion to another copy'], 'answer': 2,
     'feedback': ['Sync can transfer files, but transfer is not the only recovery concern.', 'An account connection is not a guarantee of recoverable versions.', 'Correct. Consider whether a usable earlier version survives a mistake or unwanted change.']},
    {'id': 'backup-freshness', 'prompt': 'A backup indicator is from last week, but the project changed today. What should be checked?',
     'options': ['That the latest required file version is protected and recoverable', 'Only that the cloud account exists', 'Only that last week’s status was green'], 'answer': 0,
     'feedback': ['Correct. A stale status does not establish protection of recent edits.', 'Having an account does not show which version is available.', 'An old success does not verify today’s work.']},
    {'id': 'backup-safe-test', 'prompt': 'How can a restore check avoid risking the only good project copy?',
     'options': ['Delete the original before checking', 'Restore to a separate safe location and verify the intended version opens', 'Overwrite the original without inspecting the backup'], 'answer': 1,
     'feedback': ['Deleting first removes a recovery option before the backup is verified.', 'Correct. Validate the recovered file without destroying the current good copy.', 'Overwriting first can replace good work with the wrong or unusable version.']},
    {'id': 'backup-lost-sessions', 'prompt': 'A verified backup is available after a laptop goes missing. Which task still matters?',
     'options': ['Publish account passwords so others can help', 'Assume restored files end every device session', 'Report the loss and secure affected account/device access through trusted controls'], 'answer': 2,
     'feedback': ['Passwords should not be published during recovery.', 'Restoring files does not revoke sessions on another device.', 'Correct. File recovery and protecting access on the lost device are separate needs.']},
]
