# Phase 4.6 — Six Cyber Command games

Implemented 28 October 2026 after the owner instructed “go on” following the Phase 4.5 handover. This authorises continuing development; the owner did not separately report Phase 4.5 local test results, so that acceptance remains pending. This batch addresses FB-02, FB-04 and FB-05 on six existing professional games.

## Scope and teaching alignment

| Game | Three stage tasks | Five review concepts |
| --- | --- | --- |
| Risk Command | Unsupported payment service; interim treatment; residual decision | Evidence-based context; waiting-window exposure; management ownership; compensating-control limits; residual acceptance |
| Zero Trust Briefing | Device posture; workload identity; emergency path | Location limits; shared secrets; authorisation/lifecycle; narrow exception; tested emergency access |
| Cloud Incident | Consequential API changes; credential containment; recovery | Action context; continuity; effective reach; rotation versus configuration; verified follow-up |
| Supply Chain Watch | Supplier exposure; unexpected artifact; corrective assurance | Customer linkage; inventory limits; digest/provenance; milestone evidence; integration privileges |
| Ransomware Recovery | Segment response; recovery sequencing; leadership update | Healthy-service limits; RTO meaning; prerequisites; backup versus capacity; verified communication |
| Identity Crisis | Privileged anomaly; session response; bypass prevention | Unreachable administrator; sessions versus credentials; emergency protection; policy-path correction; effective enforcement |

Each game adds three goals/tasks, six contextual hints, detailed fictional records matching original evidence indices, finding reasoning after a decision and five explained optional review questions. This adds 18 tasks, 36 hints and 30 review questions. Every review concept is taught in its stage records. Related account/cloud/response concepts are reinforced with distinct command-level decisions rather than copied prompts. Exact normalized prompt uniqueness is checked across all 135 guided-mission questions; this does not establish semantic uniqueness across every other course bank.

Coverage becomes 27 of the existing 30 games: all ten Explorers, all ten Academy games and seven Cyber Command games. Boardroom Breach, AI Governance and Audit Trail remain to improve. These are source implementation counts, not independent proof of learning or actual-device performance. Neither Phase 4 nor wider assurance gates are complete.

The new modules are `risk_mission_learning.py`, `zerotrust_mission_learning.py`, `cloud_command_mission_learning.py`, `supplier_mission_learning.py`, `recovery_command_mission_learning.py` and `privileged_mission_learning.py`. They register through the existing static allowlist and reuse the accepted API/UI. All earlier guide modules and underlying mission definitions are unchanged.

## Compatibility, recovery and security

Mission IDs, stages, answer/finding keys, points, 45-point maximums, historical choices/feedback/scores and schema remain unchanged. Guidance is additive for existing runs. Reviews save no grade, completion or new database rows. No migration, seeding or content-publication command is needed. Development activates this source after update/restart without modifying beta. Reverting this additive source and restarting development is its recovery path; separately published course markers retain their own recovery procedure.

The server chooses review questions from the authenticated student's owned completed run. Cross-mission IDs, non-student roles, other learners, unfinished runs and invalid/forged inputs remain rejected. Public guidance omits answer keys; finding reasoning is returned after a decision. Inspection is a client learning aid, not server proof that a record was read.

2D remains the default. Both modes open the same stage records and share inspection/finding state within that stage. Walking is optional and the existing renderer error boundary preserves a 2D path. No actual business risk is accepted, identity policy changed, credential rotated, vendor package installed or service restored. Content uses fictional approved response/change processes, with no real secrets or personal records. It does not treat a signed notice, configured control, passing scan or recovered service as proof of universal safety or zero impact.

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

Open http://127.0.0.1:3010/missions and select Cyber Command. Test Risk Command, Zero Trust Briefing, Cloud Incident, Supply Chain Watch, Ransomware Recovery and Identity Crisis.

For every game:

1. Check the role/goals, workflow, stage task and completion condition. Open both hint levels using the keyboard. Records must fit the current professional scenario rather than repeat unrelated content.
2. Inspect each record, choose a finding, choose an action and commit it. Finish three stages and read the explanation, including after an incorrect action. New stages reset inspection/selection; repeated submission must not advance twice.
3. On a supported device, inspect in 3D, switch to 2D and verify preserved inspected state and finding selection. Record contents must match; walking is optional and 2D stays available if rendering fails.
4. Try wrong/correct options in all five review questions. Check explanations, clearing old feedback when changing a choice, stable focus, duplicate blocking and retry after an error. Saved mission scores must not change.
5. Reload and reopen a completed result; resume an old unfinished attempt if available. Confirm score/stage/history compatibility and reopen accepted games/courses for regression checks.

Include desktop/mobile and reduced motion. Report only sanitised device/interaction errors; do not share credentials, supplier records or learner data. Synthetic viewports and a working toggle do not establish actual-device frame rate or accessibility conformance.

Independent learners should be able to finish without coaching and explain one decision per game: why a future risk treatment date is not an interim control; why workload identity still needs authorisation; why rotation does not reverse configuration; why a corrective plan needs evidence; why an RTO is a target and dependencies matter; and why active sessions need separate containment. Keep this educational/device evidence distinct from functional acceptance.

Phase 4.5 owner acceptance is still unreported. When checking this updated development source, also complete or report the outstanding [Phase 4.5 checklist](PHASE_4_ACADEMY_AND_RESPONSE.md). The owner's instruction to continue did not assert that those tests ran or waive the wider gates.

## Verification checkpoint

Backend tests expand automatically to all 27 guides and exercise actual HTTP handlers with synthetic SQLite/overridden identity: correct stage scores, historical runs, every review option, role/ownership/completion/input boundaries, cross-mission rejection and key non-disclosure. The 30-mission completion case remains, as does unsupported-review coverage for the still-unregistered games. These local checks do not establish full authentication or PostgreSQL locking.

The browser matrix automatically includes 108 guided desktop/mobile × 2D/3D journeys with actual static content and catalogue pathways. Contexts are isolated while the process is reused. Replies are intercepted synthetic API responses, not a complete real-backend browser journey. Local checks passed: 505 backend tests and 11 subtests (20 database-dependent skips), 15 frontend unit tests, TypeScript, production build and pip check. Existing warnings remain as applicable. Local Chromium's known UNIX-socket limitation remains; no fresh local browser success is claimed. Verified counts and CI links are recorded after execution in DEVELOPMENT_STATUS.md. Dependency pins are unchanged.

Owner acceptance of Phases 4.5/4.6, independent educational/actual-device evidence, real-backend browser journeys, operational readiness and final security assurance remain separate gates. Formal Cloudflare audit execution stays deferred until the end of development by owner instruction. No owner computer/database, beta source/services or mail provider was accessed.

Next: verify CI, use the complete blocks above to update/restart only development and complete/report the outstanding acceptance checks. Then finish the three remaining command games before moving beyond the mission-content scope.
