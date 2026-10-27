# Phase 4.2 — Account safety and SOC triage

Implemented 27 October 2026 after owner-reported Phase 4.1 acceptance and confirmation that beta access was restored. Addresses FB-02 (mission clarity), FB-04 (relevant evidence and usable 2D/3D interaction) and FB-05 (varied review). This is the next bounded improvement to existing missions, not a new catalogue expansion or completion of Phase 4.

## Scope and teaching alignment

| Mission | Pathway | Stage tasks | Review concepts |
| --- | --- | --- | --- |
| Password Fortress | Cyber Explorers | Limit reuse risk; choose MFA and handle prompts; investigate sessions and protect recovery | Reused credential exposure; factor types; unwanted approvals; sessions after password changes; recovery code secrecy |
| Midnight Login Alerts | Cyber Academy | Prioritise a suspicious sequence; correlate devices/logs/activity; escalate confirmed unusual activity | Prompt validation; relevant correlation; location-signal limits; authorised response/evidence preservation; known impact versus uncertainty |

Each mission has three goals, three stage tasks, six optional hints, a clear action/completion workflow, detailed fictional records in the same order as the original evidence, finding explanations after decisions and five explained optional review questions. Each review concept is taught in the corresponding stage records. Password/MFA and independent verification recur intentionally from the foundation courses, but the mission scenarios and review prompts differ. All 15 guided-mission review prompts are checked for accidental exact normalized duplication. This is not a claim that every other course/question bank has received a semantic duplicate review.

Password Fortress no longer relies on a generic branch-incident dashboard for this guided journey. Midnight Login Alerts uses stage-specific event records matching its 37-failure scenario rather than an unrelated fixed table. 2D and 3D open the same records and share inspected state within a stage; walking is optional. 2D remains the default lightweight route and the existing 3D error boundary remains available. Mobile viewports and reduced-motion browser fixtures do not prove actual device frame rates or accessibility conformance.

The Scholarship Email's accepted guide data is moved unchanged into `scholarship_mission_learning.py`. The static allowlisted registry in `mission_learning.py` serves all three guides. New source data lives in `account_mission_learning.py` and `soc_mission_learning.py`; future maintainers can add reviewed data modules without copying route or UI logic. The artifact panel has a generic Case artifacts accessible name.

## Security and data compatibility

Review is an authenticated student's repeatable practice on their own completed run. The server chooses the guide from the owned run's mission ID. Client-submitted mission IDs, scores and answer keys cannot select or grade a different mission. Cross-mission question IDs, non-students, another learner's run, unfinished runs and invalid bodies are rejected. Public guidance/review omits server answer keys and future-stage finding explanations. Static browser test fixture keys stay in the test process, not pre-answer browser responses.

No database migration, startup publication or curriculum apply command is required. Mission IDs, stages, finding keys, action points and 45-point maximums remain unchanged. Old partial/completed runs receive guidance when reopened without rewriting historic choices/feedback/scores. Optional review saves no grades, completion or new database rows. Existing courses and the separate beta branch are untouched. The catalogue remains 30 existing playable missions; three have the new guided pattern. Do not interpret catalogue count or automated checks as educational effectiveness.

Content is fictional, uses no live accounts/networks, accepts no actual passwords and executes no learner code. Keep the current guide revisions with their underlying unchanged mission definitions. Changing step order/count/scoring in a future release requires an explicit stored-run version/recovery design. This additive release can be recovered by reverting its source and restarting development; already published course markers have a separate recovery policy and must not be removed by that rollback.

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

## Acceptance

Open http://127.0.0.1:3010/missions. Choose Cyber Explorers for Password Fortress, then Cyber Academy for Midnight Login Alerts.

1. In each mission, check the role/goals, workflow, current task and both hint levels. A learner should know what to inspect, select and submit without developer coaching.
2. Inspect all stage-specific records, choose a finding, then choose and commit an action. Complete all three stages and read the finding/decision explanations, including a deliberately incorrect choice. Password Fortress must show account evidence; the SOC records must match the alert stage.
3. On supported devices, inspect records in 3D, switch to 2D and complete a stage. Confirm inspected evidence and the selected finding survive mode switching. Check keyboard operation, mobile width and reduced-motion settings. Use 2D if 3D is unavailable; record any device-specific issues.
4. After completion, try wrong/correct review answers in both missions. Check explanations, cleared old feedback, stable focus, duplicate blocking and retry after an error. The saved mission score must not change.
5. Reload and reopen completed results. Resume an existing unfinished account/SOC run, if available, and confirm its stage/score/history remain. Reopen The Scholarship Email and the accepted courses for regression checks.
6. With a beginner, record independent completion and whether they can explain reuse versus MFA, correlation versus proof and appropriate response. Owner test acceptance alone does not establish this wider educational gate.
7. Confirm beta remains reachable through its existing frontend entry page. The earlier /app link issue was resolved by using an implemented route; no beta port/tunnel or backend configuration changes are part of this release.

## Verification checkpoint

Assistant local checks: 217 backend tests and 11 subtests passed; 20 database-dependent tests skipped. These tests include actual mission/review HTTP handlers with synthetic SQLite and overridden identity, all three guides retaining historic runs/scores, all 45 review choices, per-guide role/ownership/completion/input checks, cross-mission rejection, public key non-disclosure, content-shape checks and all 30 missions completing. They do not establish full authentication or PostgreSQL locks.

All 15 frontend unit tests, TypeScript and production build passed; locked backend pip check passed. Existing TestClient deprecation and CSS compatibility warnings remain as applicable. Application dependency pins/lockfiles are unchanged.

The browser matrix now includes 12 journeys (three guided missions × desktop/mobile × 2D/3D) using stage text/shapes generated from static source modules. Replies are still intercepted synthetic API responses; this is not a real-backend browser journey. The browser job uses Python only to load pure source data, not to start an API or access a database. The execution workspace's known Chromium UNIX-socket blocker remains; no fresh local browser success is claimed. CI execution and owner acceptance are pending at this checkpoint. Record later CI evidence in DEVELOPMENT_STATUS.md.

The formal Cloudflare audit remains deferred to the end of development by owner instruction. No owner computer/database, beta services or mail provider was operated. Next: inspect CI, complete owner development acceptance and beginner/device evidence, then choose the next bounded mission improvement.
