# Phase 5.2 — Saved progress previews and dashboard usability

Implemented 28 October 2026 after owner-reported Phase 5.1 local acceptance ("All tests pass"). Addresses the Phase 5 progression/usability scope and FB-03 by making saved learning records and suitable next steps visible on the dashboard. This is a bounded build, not completion of the full Phase 5 gate.

## What changed and why

Source inspection found that the dashboard offered navigation cards but no learner progress previews. Existing course enrolment/completion and assessment history were already persistent. Onboarding already has password confirmation, visibility and post-registration sign-in instructions; the site already has a dark palette. Their source existence does not establish broader device/accessibility or independent learner acceptance. The dashboard's sign-out request also lacked the five-second bound already used by home navigation.

The new authenticated student-only `/api/v1/learning/overview` endpoint returns counts for enrolled published courses, up to three course previews (unfinished first) and three most recent assessment attempts. Aggregation filters by the current learner. Each preview shows actual completed/total lessons and the first incomplete lesson in position/ID order. Courses with no lessons remain incomplete. Draft and unenrolled courses are excluded, including from recent assessment previews. Scores retain their stored denominators; chronological recent results are not replaced with a learner's best score. Responses select only summary columns, not answers, topic snapshots or other learners' records. Reads save no progress and award no grade.

The student dashboard displays progress, resume-lesson links, completed-course assessment links, recent-result links, loading/empty states and a retry action for failed progress requests. It shows the three-item preview limit and directs learners to My learning for all courses. It does not present a failed request as zero progress. Teacher/admin dashboards do not request student overview data.

Recent-result links now open the enrolled course and owned saved attempt directly in assessments, with heading focus after loading. Existing legacy results retain the Phase 5.1 evidence-unavailable message. The existing server detail route remains the authorization boundary; URL IDs do not confer access. Lesson links reuse Phase 5.1's course/lesson opening behavior. Completion measures recorded activity, not mastery; assessment scores describe separate practice samples. This build does not introduce adaptive recommendations, aggregate strengths, mission progress scoring or learning-gain claims.

Dashboard sign-out has a disabled pending state and five-second request timeout before clearing the local token and returning to account entry. If the server cannot be reached, local sign-out does not establish server-side token revocation; ordinary session expiry remains applicable. No authentication lifetime or storage model changed.

No database migration, seed, content publication or dependency change is introduced. Keep the accepted `0010_attempt_results` schema from Phase 5.1. Beta source/services/data are untouched.

## Complete PowerShell update and checks

Stop only development API/frontend with Ctrl+C; leave beta open. Run from the existing development worktree root.

```powershell
$ErrorActionPreference = 'Stop'
$dashboardBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $dashboardBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

$dashboardPreviousDatabaseUrl = $env:DATABASE_URL
$dashboardPreviousTestUrl = $env:TEST_DATABASE_URL
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
    $env:DATABASE_URL = $dashboardPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $dashboardPreviousTestUrl
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

## Acceptance

1. Open the development dashboard with an existing student account. Compare course/lesson counts with My learning. Use Continue to open the first incomplete lesson, complete it, then return/reload the dashboard: saved counts and next lesson should update. A course with all lessons complete should offer assessment practice; a course with no lessons should not be labelled complete.
2. Open a recent assessment result. Confirm its score, original question count and saved explanation/topic evidence, or the explicit historical-evidence limit. Complete another assessment and return/reload: the new recent attempt should appear chronologically. Ordinary course/length selection must still work.
3. With synthetic accounts where available, verify empty progress offers first-course/assessment links, another account shows only its own data, and teacher accounts do not show student progress. A failed progress fetch should show retry while keeping dashboard navigation available.
4. At mobile width, with keyboard and reduced motion, verify readable dark-theme progress cards, no horizontal overflow, lesson/result focus and usable links. Verify registration/login baseline and home/dashboard logout flows. With only development API stopped, dashboard sign-out should still clear local sign-in after about five seconds; restart and run the isolation check afterwards.
5. Check earlier lessons, assessment length/grading, saved results and representative missions for regression. Independently ask a learner to select a next step and explain why lesson completion is not proof of mastery. Keep independent learner/device evidence separate from functional acceptance.

Recovery for this additive build is a source fix/revert on development followed by restart; no new schema/data change needs reversing. Preserve local modifications and saved records. Operational recovery, privacy/accessibility targets, broader real-backend browser journeys and final security assurance remain open.

## Verification checkpoint

Assistant checks passed: 570 backend tests and 11 subtests, with 20 database-dependent skips; seven new HTTP cases exercise owned/read-only aggregation, correct completion/next lesson, zero-lesson behavior, chronology/limits, drafts/unenrolled courses and student role boundaries using synthetic SQLite and overridden identity. Real-session overview access checks were added to the existing isolated-PostgreSQL integration suite; CI results are pending at this checkpoint.

All 15 frontend unit tests, TypeScript, production build, pip check and diff whitespace checks passed. Existing TestClient deprecation and CSS compatibility warnings remain. Five new browser cases cover desktop/mobile previews, result deep links/focus, error retry and empty state, teacher isolation, and stalled logout. No local browser assertions are credited; the preceding local Chromium socket restriction remains an execution limitation. The early progression CI step now includes these five cases and the three accepted Phase 5.1 cases, followed by the 132 existing browser journeys. CI and owner acceptance remain pending.

No owner computer/database, beta branch/services or mail provider were accessed. Formal security-audit-skill execution remains deferred until final development assurance. Separate Phase 4.5 acceptance and independent learner/device evidence remain outstanding.
