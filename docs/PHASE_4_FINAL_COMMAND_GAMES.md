# Phase 4.7 — Final Cyber Command guidance upgrades

Implemented 28 October 2026 after owner-reported Phase 4.6 acceptance and the instruction to continue. Addresses FB-02, FB-04 and FB-05 on the final three existing games.

## Scope and teaching alignment

| Game | Three stage tasks | Five review concepts |
| --- | --- | --- |
| Boardroom Breach | First situation report; recovery trade-off; disclosure oversight | Facts and uncertainty; command ownership; recovery gates; notification assessment; population estimates |
| AI Governance | Model inventory; group error review; drift response | Data lineage limits; accountable registration; sample uncertainty; effective human oversight; controlled model changes |
| Audit Trail | Population and sampling; exception testing; verified closure | Population completeness; sample limits; emergency-policy applicability; timestamp limits; remediation evidence |

Each game adds three objectives/tasks, six hints, nine detailed fictional records, three post-decision finding explanations and five explained optional review questions. All review concepts are taught by the stage records. This adds nine tasks, 18 hints and 15 review questions. Across the catalogue there are now 30 guides and 150 optional questions, with exact normalized prompt uniqueness checked. This is not a claim of semantic uniqueness across all course banks.

All ten Explorer, ten Academy and ten Command games now have source guidance. Reaching 30 does not complete the Phase 4 gate: independent learner understanding, actual-device evidence and wider release assurance remain required.

The new modules are `board_mission_learning.py`, `ai_mission_learning.py` and `audit_mission_learning.py`, registered in the existing source allowlist. Previous guide modules and underlying mission definitions are unchanged.

## Compatibility and security

Mission IDs, stages, action/finding keys, score maximums, history and schema are preserved. Guidance applies additively to existing runs. Reviews are server-checked practice and save no grade or progress. No migration, seed or content-publication command is needed. Update/restart only development; beta remains separate. Reverting this additive source and restarting development is the recovery path.

The review API continues to require an authenticated student's owned completed run and server-selected questions. Invalid, cross-mission, forged, unfinished, other-owner and non-student requests remain rejected. Answer keys are not included in public guidance. Inspection is a client learning aid, not evidence of reading on the server.

2D is the default; both modes share records and preserve inspection/finding state within the stage. Walking remains optional with the existing 2D rendering fallback. Exercises use fictional records: no real customers, credit decisions, model deployments, board disclosures or audit conclusions are produced. Content does not supply jurisdiction-specific legal deadlines, infer fraud from a blank field, treat a model's prior approval as permanent suitability or equate a remediation promise with verified closure.

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
```## Three-game acceptance checklist

Open http://127.0.0.1:3010/missions and select Cyber Command. Test Boardroom Breach, AI Governance and Audit Trail.

1. Read each role/objective, workflow and stage task; open both hints by keyboard and inspect every record. Check that records match the stage and remain readable at mobile width.
2. Choose a finding and action, commit each of three stages and read the explanations, including after a wrong choice. A new stage resets selections; repeated submission must not advance twice.
3. On a supported device, inspect in 3D and switch to 2D. Contents must match and stage inspection/finding state must persist. Confirm a usable 2D path and optional walking, with reduced motion included.
4. Try incorrect and correct answers to all five review questions. Verify explanatory feedback, clearing stale feedback after a choice changes, stable focus, duplicate blocking and error retry. Saved mission scores must stay unchanged.
5. Reload/reopen a result and resume a pre-existing unfinished run if available. Check saved stage/history compatibility and open earlier games/courses for regression checks.

Independent learners should finish without coaching and explain a recovery trade-off, why subgroup sample uncertainty matters and why an owner/due date does not prove audit closure. Keep actual-device and educational evidence separate from functional acceptance. Report sanitised issues only; no real customer, model, audit or learner records.

Phase 4.6 has owner-reported local acceptance. Separate Phase 4.5 acceptance remains unreported; its checklist is in [the Phase 4.5 guide](PHASE_4_ACADEMY_AND_RESPONSE.md).

## Verification checkpoint

The backend suite automatically exercises all 30 guides: actual HTTP scoring, all review choices, historic runs, ownership/role/completion/input boundaries, cross-mission rejection and key non-disclosure. Browser fixtures derive actual source content/catalogue pathways, with desktop/mobile × 2D/3D journeys for every guide; API replies are intercepted synthetic responses. These are not complete real-backend browser journeys. Local Chromium remains blocked by the known UNIX-socket restriction; CI browser verification is recorded after execution.

Local checks passed: 541 backend tests and 11 subtests with 20 database-dependent skips; all 15 frontend unit tests, TypeScript, production build and pip check passed. The existing TestClient deprecation warning remains. Local HTTP tests use synthetic SQLite and overridden identity, not full authentication or PostgreSQL lock proof. CI results are pending at this implementation checkpoint. Formal audit remains deferred until the end of development. No owner computer/database, beta service or mail provider was accessed.

Next: verify checks, update/restart development and complete local acceptance. Then inspect actual progression/results/usability for Phase 5 gaps (FB-03) before implementing recommendations; retain outstanding educational/device, operational and final security gates.
