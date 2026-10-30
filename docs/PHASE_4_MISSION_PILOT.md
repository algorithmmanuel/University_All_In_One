# Phase 4.1 — The Scholarship Email beginner pilot

Implemented 27 October 2026 for FB-02 (mission clarity), FB-04 (meaningful evidence interaction and lightweight fallback), and FB-05 (varied post-mission checks). This is one bounded pilot, not completion of Phase 4 or proof of educational effectiveness.

## Learner contract

The Scholarship Email now explains the learner's role, three learning goals, exact workflow and completion conditions. Every stage has a specific task and two optional nested hints. Stage-specific fictional sender/message/destination records replace the repeated generic mail display for this pilot. Inspecting records enables finding selection; committing a response advances the mission. Finding reasoning appears after the decision, alongside existing scoring feedback.

2D remains the default and needs no WebGL. Optional 3D artifact controls open the same detailed records; switching mode retains inspected indices and the selected finding in the current stage. Walking is optional. An error boundary keeps a failed 3D renderer from taking down the whole mission; the learner can switch to 2D. This does not establish responsiveness, frame rate or device compatibility by itself.

After all three decisions, five distinct review questions check pressure versus proof, independent verification, secret exposure, response to reused credentials and proportionate handling of a received message. Each option has an explanation. Checks require an authenticated student owning a completed pilot run. Invalid/forged inputs, unfinished runs, other learners and unrelated missions are rejected. Checks are repeatable, do not save grades/progress, and do not change the completed mission score. Review answers reset on workspace exit/reload. Completed results can now be reopened from the mission board.

All content is fictional text. The pilot collects no real passwords or reports and follows no external links. No learner code executes. The optional notebook/correlation board remain local scratchpads. Evidence inspection is a UI learning aid, not server proof that a learner read a record. Do not treat points as demonstrated understanding.

## Compatibility and release

No migration or content publication command is needed. Existing mission IDs, step order/count, finding keys, answer points and 45-point pilot maximum are unchanged. Historic scores/choices remain stored unchanged. Old partial/completed pilot runs receive the additive guidance/review when opened; historic feedback is not rewritten. Other missions retain their investigation UI; completed-result reopening, submission guard and renderer error boundary are shared improvements. The API returns an optional `learning` field; clients without it keep the previous workflow.

Keep `mission_learning.py` alongside the current mission revision. Future changes to underlying steps/scoring need explicit versioning/recovery decisions before editing stored-run semantics. Updating source and restarting this development build activates the guidance; it does not publish to beta. Recovery is a source rollback/restart of these additive changes; review has no saved records to reverse. Never revert previously published course markers without their separate curriculum recovery procedure.

## Complete PowerShell update and tests

Stop only the development API and frontend with Ctrl+C; leave beta open. Run from the existing development worktree root.

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
        if ($LASTEXITCODE -ne 0) { throw 'Focused development tests failed.' }
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
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit tests failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
}
finally { Pop-Location }
```

Restart the API from the development root in one terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Restart the frontend from the development root in another terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify from the development root in a third terminal:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
```

## Acceptance checklist

Open http://127.0.0.1:3010 and find The Scholarship Email in Cyber Explorers.

1. Start a new attempt. Confirm the workspace scrolls into view; role, goals, workflow, completion and stage task are clear. Open both hint levels using the keyboard.
2. Inspect every record, select a finding, choose an action and commit it. Repeat all three stages; artifacts must match each stage, not repeat the same inbox. Try an incorrect choice and read the reasoning.
3. Confirm progression requires a finding and action. If opening the decision desk early, follow its return-to-evidence guidance. Repeated submission must not advance or score a stage twice.
4. In a separate attempt, inspect records in 3D, switch to 2D and finish the stage. Check preserved inspection/selection, keyboard controls and mobile width. If 3D is unavailable, confirm 2D remains usable. Report actual device/interaction details; a toggle alone is not acceptance.
5. Finish the mission. Try wrong and correct review answers; check each explanation, cleared stale feedback on a new choice and retry after an error. The mission score must not change. Review does not save a separate grade.
6. Reload the board and choose View result for The Scholarship Email. The score remains saved and all five review questions return. Resume an old unfinished attempt; its saved stage/score remain and the current task is shown. Inspect other missions and the accepted courses for regressions.
7. Confirm beta availability. Use a beginner who has not seen the implementation: record whether they independently finish and can explain the verification/exposure decisions. Keep names, private records and secrets out of Git.

## Verification

Assistant workspace: full backend collection passed with 191 tests, 20 database-dependent skips and 11 subtests. New actual HTTP tests use disposable synthetic SQLite with overridden identity; they cover every mission finishing, pilot scoring, historic runs, all 15 review choices, ownership/role/completion boundaries and malformed inputs. They do not establish PostgreSQL locking, full authentication or concurrency.

All 15 frontend unit tests, TypeScript and production Next.js build passed. Existing CSS compatibility warnings and a TestClient deprecation warning remain. The installed locked backend environment passes pip check. No dependency versions changed in this build.

Four new browser cases cover desktop/mobile 2D/3D, stage transitions, hints, shared evidence, review focus/duplicate guarding, failure/retry, result reopening and partial resume with synthetic API responses. Chromium installation succeeded, but launch failed before assertions because its required UNIX socket is denied in this workspace. These cases are not counted as passed locally. They are included in the browser CI job; CI results must be checked separately.

No owner computer, development database, beta database, mail provider or beta service was accessed. Formal Cloudflare security-audit-skill execution remains deferred until the end of development. Next: owner pilot acceptance and independent beginner/device evidence, then extend proven patterns to the next representative missions.

### Subsequent CI evidence

Implementation `277164e` passed the backend workflow: 211 tests and 11 subtests against isolated PostgreSQL, plus independent-unit and dependency audit jobs. Initial browser execution passed the four new pilot cases but exposed an older assertion expecting a dashboard greeting heading that no longer exists. Test-only commit `bfacb11` asserts the actual greeting paragraph and dashboard heading. [Browser run 40468828728](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40468828728) then passed all 16 browser cases, 15 frontend unit tests, TypeScript and production build. [Backend run 40468541737](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40468541737) supplies the separate PostgreSQL/API evidence. Browser API responses are synthetic, not the real PostgreSQL-backed API. Owner pilot acceptance and independent beginner/device walkthroughs remain pending.
