# Phase 4.4 — Complete Explorers and extend Cyber Academy

Implemented 28 October 2026 after owner-reported Phase 4.3 acceptance. This is the next approved six-game batch for FB-02, FB-04 and FB-05. It improves existing games without expanding the 30-game catalogue or completing Phase 4.

## Scope and teaching alignment

| Game | Pathway | Stage learning | Five review concepts |
| --- | --- | --- | --- |
| MFA Guardian | Cyber Explorers | Unexpected approval; recovery codes; replacement phone | Prompt fatigue; recovery authority; independent recovery; tested transfer; old-device review |
| Backup Buddy | Cyber Explorers | Single project copy; stale sync; lost laptop | Shared-device dependency; sync/version limits; freshness; safe restore test; sessions versus file recovery |
| Operation Firewall | Cyber Academy | Privileged sign-in validation; device/action correlation; containment follow-up | Validation; irrelevant background events; MFA evidence limits; containment versus impact; documented uncertainty |
| Network Watch | Cyber Academy | Traffic baseline; recurring flows; confirmed process response | Baseline context; periodicity; managed-device limits; host containment; known scope |
| Web Defense | Cyber Academy | WAF lead; unsafe query construction; staging/release evidence | Alert versus proof; parameter values; server boundary; regression scope; change approval |
| Cloud Perimeter | Cyber Academy | Personal-data exposure; anonymous read grant; impact assessment | Prioritised containment; least privilege; effective permissions; current versus past access; evidence-based follow-up |

Each game adds three goals/tasks, six optional hints, detailed fictional records matching all original evidence indices, finding reasoning after a decision and five explained optional review questions. All reviewed concepts are taught in the stage records. This batch adds 18 stage tasks, 36 hints and 30 review questions. Fifteen of 30 games now use the guided pattern: all ten Cyber Explorers and five Cyber Academy games. Fifteen games remain to improve. These are implementation coverage counts, not proof of learning or device performance.

The six new modules are `mfa_mission_learning.py`, `backup_mission_learning.py`, `firewall_mission_learning.py`, `network_mission_learning.py`, `web_mission_learning.py` and `cloud_mission_learning.py`. They register through the existing source allowlist and reuse the accepted API and UI. Earlier guide modules are unchanged. Related concepts recur intentionally with distinct applied decisions: account protection versus MFA lifecycle; taking a backup versus restoring a current version; initial triage versus a confirmed response; a detector lead versus a verified application repair. Tests check exact normalized prompt uniqueness across all 75 guided-mission questions, not semantic duplication across every other course.

## Compatibility and security

Mission IDs, step order/count, finding and action keys, points and 45-point maximums are unchanged. Existing partial/completed runs retain saved stages, scores, choices and historic feedback; guidance is additive. No migration, seeding, content publication or new persisted review data is required. This development source activates after updating and restarting development services. The beta branch/services and accepted courses are untouched. Reverting this additive source and restarting development is the recovery path; do not remove separately published course markers as part of that rollback.

Reviews remain authenticated student practice scoped to an owned completed run. The server selects questions from that run's mission ID; cross-mission question IDs and forged/invalid bodies are rejected. No review answer saves a grade or changes mission completion/score. Public data omits grading keys and future finding reasoning. Evidence inspection is a client learning aid, not server proof that a record was read.

2D remains the default. Both modes present the same detailed records and share inspected state/finding selection in a stage. Walking is optional and the existing renderer failure boundary keeps the 2D route available. No real account codes, files, bank records, student data, query payloads or live systems are requested. No attachment, injection test, network request, account revocation or cloud-policy change is executed by the training content. Proposed actions follow the fictional response/change processes, and no guarantee is made that one control proves zero impact or eliminates all risk.

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

Open http://127.0.0.1:3010/missions. Select Cyber Explorers for MFA Guardian/Backup Buddy and Cyber Academy for Operation Firewall/Network Watch/Web Defense/Cloud Perimeter.

For every game:

1. Read the role/goals, workflow, completion condition and stage task; open both hint levels using keyboard controls. Records must refer to the actual stage, not a generic reused scene.
2. Inspect every record, select a finding, choose an action and commit it. Finish all three stages and read the explanation, including after a deliberately incorrect choice. Each new stage must reset inspection and selection. Repeated submission must not score or advance twice.
3. Use 3D on a supported device to open stage records, then switch to 2D and confirm preserved inspection/finding state. The record content must match in both modes; walking is optional and 2D remains usable if 3D is unavailable.
4. After completion, try wrong and correct review answers and read all five explanations. Check stable focus, cleared stale feedback when changing an answer, duplicate blocking and error/retry handling. The saved mission score must remain unchanged.
5. Reload and view the completed result; resume an older unfinished run if available. Confirm its saved stage/score/history remain. Reopen previously accepted games and courses for regression checks.

Across the batch, include desktop/mobile and reduced motion. Record actual device/interaction issues without sharing credentials, recovery codes, files or personal records. A synthetic viewport or successful toggle is not evidence of real-device frame rate or accessibility conformance.

With independent beginners, check whether they can finish without coaching and explain a key decision in each game: why unexpected prompts must be denied; why a backup needs a current restore check; why session revocation does not prove zero impact; why recurring traffic needs correlation; why parameterized values differ from query structure; why a private bucket does not settle historical access. These learning/device gates remain separate from automated checks and owner test acceptance.

## Verification checkpoint

The backend suite tests all 15 guides using actual HTTP handlers, synthetic SQLite and overridden identity: correct stage scoring, historical runs, every review option, ownership/role/completion/input boundaries, cross-mission rejection and public key non-disclosure. The 30-mission legacy completion case remains. This does not establish full authentication or PostgreSQL concurrency from local SQLite tests.

The browser matrix automatically covers every guide: 60 guided journeys across desktop/mobile and 2D/3D. Static fixture preparation now reads the literal existing game catalogue for the actual pathway mapping rather than defaulting unfamiliar mission IDs to Cyber Explorers. This uses only Python's standard library plus static content; it imports no database or application dependency. Browser contexts stay isolated while the process is reused. Responses remain intercepted synthetic replies, so these are not complete real-backend browser journeys.

Local checks passed: 361 backend tests and 11 subtests (20 database-dependent skips), 15 frontend unit tests, TypeScript, production build and pip check. Existing warnings remain as applicable. Local Chromium's known UNIX-socket limitation remains; no fresh local browser success is claimed. Test counts and CI links are added to DEVELOPMENT_STATUS.md after verified execution. Owner acceptance of this batch, independent educational/device evidence, operational readiness and the final security audit remain separate gates. Formal Cloudflare audit execution stays deferred until the end of development by owner instruction. No owner computer/database, beta source/services or mail provider was accessed.

Next: verify CI, update/restart only development with the complete blocks above, and complete this six-game checklist. Continue in approved five-to-six-game batches after acceptance.

### Subsequent CI verification

Implementation `ad8f244` passed [backend run 40661421407](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40661421407): 381 tests and 11 subtests against isolated PostgreSQL, plus unit and dependency checks. [Browser run 40661421374](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40661421374) passed all 72 browser cases (including 60 guided desktop/mobile × 2D/3D journeys), 15 frontend unit tests, TypeScript and production build. Browser API replies remain synthetic; this is not a complete real-backend browser journey. Owner acceptance of this six-game batch and independent beginner/actual-device evidence remain pending.
