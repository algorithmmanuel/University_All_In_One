# Phase 4.5 — Complete Cyber Academy and introduce Branch Resilience

Implemented 28 October 2026 after owner-reported Phase 4.4 acceptance and instruction to continue the approved six-game batches. Addresses FB-02, FB-04 and FB-05 on six existing games. This is not catalogue expansion or completion of the educational/operational/security gates.

## Scope and teaching alignment

| Game | Pathway | Three stage tasks | Five review concepts |
| --- | --- | --- | --- |
| Forensics Desk | Cyber Academy | Approved acquisition; image transfer; time reconstruction | Volatile evidence; hash limits; custody; raw timestamp limits; traceable normalisation |
| Malware Clues | Cyber Academy | Safe sample intake; static-clue correlation; detection update | Intake controls; hash versus safety; contextual validation; false positives; controlled release |
| Identity Lab | Cyber Academy | Stale privilege; MFA exclusion; repeatable oversight | Departure access; effective bypass; audit retention; lifecycle follow-up; exception records |
| Secure Code Review | Cyber Academy | Exposed credential; ignored scanner; mutable release reference | Secret copies; green-build limits; gate exceptions; immutable content; enforced signature/provenance policy |
| Threat Hunter | Cyber Academy | Testable DNS hypothesis; task provenance; confirmed outcome | Hypothesis quality; domain novelty limits; safe pivots; known scope; response/detection follow-through |
| Branch Resilience | Cyber Command | Workstation containment; spread/backups; planned recovery | First response; scope; backup protection; restore gates; verified service recovery |

Branch Resilience is the existing game card for mission `incident-response`, whose workspace title is **Ransomware at the Branch**. No ID or title is changed. Five Academy games and one professional game are improved; all ten Cyber Explorers and all ten Cyber Academy games now have guided content. Overall coverage is 21 of the existing 30 games, with nine professional games remaining. These are implementation counts, not independent evidence of educational effectiveness.

Each new game has three goals/tasks, six contextual hints, detailed fictional records matching each original evidence index, finding reasoning after a decision and five explained optional review questions. This batch adds 18 stage tasks, 36 hints and 30 review questions. The branch mission retains two records per stage rather than forcing a three-record template. Each review concept is taught in the stage records. Exact normalized prompt uniqueness is checked across all 105 guided-mission questions; intentional related-concept reinforcement does not imply a semantic review of every other course bank.

New modules: `forensics_mission_learning.py`, `malware_mission_learning.py`, `identity_mission_learning.py`, `delivery_mission_learning.py`, `hunt_mission_learning.py` and `response_mission_learning.py`. They register through the existing static allowlist and reuse the accepted route and UI. Previous guide modules remain unchanged.

## Compatibility and security

Existing mission IDs, step order/count, finding/action keys, points, 45-point maximums, saved choices/scores/stages and historic feedback are unchanged. No schema migration, seeding or content publication is required. Optional reviews save no grades, completion or new rows; guidance is additive when an old run is reopened. This source activates in development after update/restart, without changing beta. Rollback is reverting this additive source and restarting development; do not reverse separately published course markers as part of that action.

Review remains an authenticated student's practice on their own completed run. The server selects the guide from that owned run, rejects cross-mission IDs and invalid/forged inputs and omits grading keys from public guidance. Evidence inspection remains a client learning aid, not server proof that records were read.

2D is the default. Both modes open the same stage records and share inspected state/finding selection; walking is optional and the existing renderer failure boundary retains a 2D continuation path. No actual forensic images, malware, credentials, DNS queries, scheduled tasks, bank systems or branch files are provided or operated. Forensic actions remain subject to authorisation and preservation procedures, malware analysis is a supplied fictional case, and response/release actions are recommendations within the fictional approved processes. The exercise does not execute any acquisition, sample, injection, access removal or restoration.

## Complete PowerShell update and checks




Stop only development API/frontend using Ctrl+C. Leave beta open. Run from the existing development worktree root.

```powershell
$ErrorActionPreference = 'Stop'
$missionBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $missionBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

$missionPreviousDatabaseUrl = $env:DATABASE_URL
$missionPreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest test_mission_learning.py test_mission_contract.py test_foundations_courses.py test_python_foundations.py test_assessment_lengths.py test_development_isolation.py -q
        if ($LASTEXITCODE -ne 0) { throw 'Focused development checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $missionPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $missionPreviousTestUrl
}

Push-Location .\web
try {
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
}
finally { Pop-Location }
```

Start API in one terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Start frontend in another terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify in a third terminal from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
```

## Six-game acceptance checklist

Open http://127.0.0.1:3010/missions. Select Cyber Academy for Forensics Desk, Malware Clues, Identity Lab, Secure Code Review and Threat Hunter. Select Cyber Command for Branch Resilience; its mission workspace is titled Ransomware at the Branch.

For every game:

1. Confirm the role/goals, workflow, completion conditions and stage task are understandable. Use keyboard controls to open both hints. Each record must match the actual stage and learner task.
2. Inspect all records, choose a finding, choose an action and commit it. Complete all three stages and read explanations, including after an incorrect action. New stages reset inspection/selection; repeated submission must not score twice.
3. On a supported device, inspect in 3D, switch to 2D and confirm preserved inspected state and finding selection. Record contents must match; walking is optional and 2D must remain available if rendering fails.
4. After completion, try wrong/correct review options, read all five explanations, change an answer to clear old feedback, and check focus, duplicate blocking and error/retry. Saved mission scores must not change.
5. Reload/reopen completed results and resume an older unfinished run if available. Confirm saved stage/score/history remain. Reopen previously accepted games and foundation courses for regression checks.

Include desktop/mobile and reduced motion across the batch. Share only sanitised device/interaction failures, never credentials, files, images or learner records. Synthetic viewports and successful toggles do not establish actual-device frame rate or accessibility conformance.

With independent learners, check completion without developer coaching and one explanation per game: why acquisition must preserve state; why an unsigned file or hash is not a complete safety verdict; why access exceptions need tracking; why a mutable tag can break artifact identity; why a hunt hypothesis needs validation; and why restored files are not the same as complete service recovery. Independent educational/device evidence remains distinct from owner functional acceptance.

## Verification checkpoint

Backend tests cover all 21 guides using actual HTTP handlers with synthetic SQLite and overridden identity: correct stage scores, historic runs, all review options, ownership/role/completion/input boundaries, cross-mission rejection and public key non-disclosure. The legacy 30-mission completion case remains. Unsupported-review coverage now chooses an unregistered mission from source rather than assuming incident-response stays unguided; the ownership/role checks still run for every guide. These local tests do not establish full authentication or PostgreSQL locking.

The browser matrix automatically includes all 21 guides: 84 desktop/mobile × 2D/3D journeys with actual static content and catalogue-derived pathways, including the professional path. Contexts are isolated while the browser process is reused. API replies are intercepted synthetic responses, not a complete real-backend browser journey. Local checks passed: 433 backend tests and 11 subtests (20 database-dependent skips), 15 frontend unit tests, TypeScript, production build and pip check. Existing warnings remain as applicable. Local Chromium's known UNIX-socket restriction remains; no fresh local browser success is claimed. Verified local counts and CI evidence are recorded after execution in DEVELOPMENT_STATUS.md. Dependency pins are unchanged.

Owner acceptance of this batch, independent educational/actual-device evidence, complete real-backend browser journeys, production readiness and final security assurance remain separate gates. Formal Cloudflare audit execution remains deferred until the end of development by owner instruction. No owner computer/database, beta source/services or mail provider was accessed.

Next: verify CI and use the complete blocks above to update/restart development and accept all six games. Continue with the nine remaining professional games in the approved batch sizes after acceptance.
