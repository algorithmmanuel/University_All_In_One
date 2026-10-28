# Phase 5.1 — Assessment evidence and next steps (FB-03)

Implemented 28 October 2026 from `5567e76` after reading DEVELOPMENT.md, the current status and approved roadmap. This is the first bounded Phase 5 build; the wider progression/usability gate remains open.

## Source inspection and scope

Before this change, the assessment page displayed scores, immediate answer explanations and the latest 20 attempt summaries. Saved answers had no curriculum revision, objective evidence or original explanation snapshot. The learning page already persisted lesson completion; dashboard course/mission/assessment navigation, account onboarding and logout controls already exist. Global styling already uses a dark palette. Their existence is not evidence of mobile, accessibility, logout-provider failure or independent learner acceptance. This build adds the missing assessment evidence path; dashboard progress previews, mission-level recommendations and remaining usability verification are later work.

The three published foundations releases already define 27 stable objective IDs across Python, Cyber Safety and Digital Citizenship. New results map an item only when its course/academy, full published lesson markers, exact prompt, options, answer key and explanation match reviewed source. Customized/unpublished/unmapped items still contribute to the server-graded overall score, but do not acquire guessed topic labels. Duplicate reviewed prompts receive topic evidence once. Selection, grading and existing saved scores are unchanged.

Each new attempt stores a version-1 server-authored JSON snapshot: curriculum revision, objective/lesson identity and labels, counts, recommendations and original question/answer explanations. Snapshot creation and the attempt are committed together. The detail endpoint requires the current student's enrolment, published course and owned attempt; other-owner/wrong-course IDs return 404. Clients cannot submit a snapshot, score or objective label. Public question responses still omit answer keys. No new dependency or content publication is needed.

Historical attempts have NULL snapshots. Their answers, score, total, ID and submission time are preserved. No backfill regrades them against today's answer key. The UI explicitly says topic evidence is unavailable. Stored snapshots remain unchanged after question/lesson/course edits; a lesson link opens current teaching if that lesson still exists and the learner remains eligible. The list retains the existing latest-20 limit; this build does not add full-history pagination.

## Evidence contract

| Evidence in this attempt | Label | Next step |
| --- | --- | --- |
| No distinct mapped question for an objective | Not assessed | Study the lesson; sample it with a longer assessment |
| One distinct mapped question | Limited evidence | Review a mistake, or try another example/longer assessment |
| At least two mapped questions, at least 80% correct | Strength in this attempt | Apply it in another example; continue practising |
| At least two mapped questions, below 80% correct | Revisit this objective | Read the explanation and linked lesson, then practise |

These are transparent practice heuristics, not validated mastery/weakness diagnoses. Results describe one attempt. Repeating the deterministic bank does not add independent evidence; lesson completion, hints, optional mission review and guided checks are not merged into assessment evidence. Counts and unassessed objectives remain visible. No claim of long-term mastery, learning gain or adaptive personalization is made.

Results can be reopened after reload, including original selected/correct answers and explanations. Lesson recommendations open the enrolled course and focus the returned lesson using a reduced-motion-safe instant scroll. Completing the lesson does not intentionally refocus it. Saving a quiz has a synchronous client guard against duplicate in-flight submissions; this is not a server-side idempotency guarantee across retries/devices.

## Complete PowerShell update, migrate and check

Stop only the development frontend/API with Ctrl+C; leave beta open. Run this complete block from the existing development worktree root. This build **requires migration `0010_attempt_results` on development only** before API use. The new explicit migration command reuses the branch/interpreter/database/environment guards and refuses occupied development service ports. Ordinary service startup still does not migrate.

```powershell
$ErrorActionPreference = 'Stop'
$resultsBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $resultsBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development migration failed; do not start the updated API.' }

$resultsPreviousDatabaseUrl = $env:DATABASE_URL
$resultsPreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest -q
        if ($LASTEXITCODE -ne 0) { throw 'Backend checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $resultsPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $resultsPreviousTestUrl
}

Push-Location .\web
try {
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
    npm.cmd run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
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

The migration adds one nullable JSON column and performs no UPDATE/backfill. Do not run a downgrade as routine recovery: it removes new snapshots. If acceptance fails, stop development, preserve the database and inspect sanitised diagnostics before choosing a source fix or recovery. Do not migrate beta or switch its source for this development milestone. Existing backups/recovery and final release assurance gates remain required.

## Acceptance

1. Open assessments for each published foundations course. Take a one-question custom attempt: one objective should have limited evidence and the others should be not assessed. A wrong answer must recommend reviewing without diagnosing weakness from one item.
2. Take a 20-question attempt with some deliberate mistakes. Compare objective counts, overall score and answer explanations. Every counted question must belong to the reviewed objective and relevant lesson; the topic totals should account for mapped questions.
3. Reload, reselect the course and use View result. Check that the score, topic counts, selected answer and explanation persist. Open an older attempt if present: original score survives and topic evidence is unavailable.
4. Open a recommendation. The relevant course/lesson should load and receive keyboard focus. Complete it and verify saved lesson progress with no repeated focus jump. Repeat at mobile width and reduced motion, including keyboard operation and dark-theme readability.
5. Verify baseline course/mission/assessment/logout journeys still work. Independent learners should be able to explain the sample-size limitation and choose a suitable next lesson. Record this separately from functional acceptance.

## Verification checkpoint

Assistant checks: 560 backend tests and 11 subtests passed, with 20 database-dependent skips; a subsequent focused 22-test results/migration/launcher run passed including the three newly added launcher cases. Synthetic SQLite/overridden-auth HTTP checks cover all three curricula, correct/wrong/limited/unassessed evidence, repetitions, duplicated rows, forged payloads, snapshot stability, historical preservation and role/owner/course/enrolment boundaries. The migration test executes upgrade/downgrade against a populated old-schema SQLite table and verifies original answers/scores survive. Full PostgreSQL migration and real-session authorization assertions are delegated to the existing backend CI gate and are pending at this checkpoint.

All 15 frontend unit tests, TypeScript, production build and pip check passed. Existing TestClient deprecation and CSS compatibility warnings remain. Three new browser cases cover desktop/mobile result persistence, legacy limits, detail error/retry and focused lesson navigation; all failed to launch Chromium locally because its required UNIX socket was denied. No browser assertions executed locally. The existing browser CI gate now includes these cases; results are pending. Browser responses in that gate are synthetic, not a real-backend learner journey.

No owner computer/database, beta source branch, beta service or mail provider was accessed. Formal security-audit-skill execution stays deferred. Owner development migration/acceptance, independent learner/device evidence, wider Phase 5 usability and operational/final security gates remain open.
