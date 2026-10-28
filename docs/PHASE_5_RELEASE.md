# Phase 5 — Combined progression and usability release

Owner direction, 28 October 2026: Phase 5.2 has **not** been installed locally. Complete the remaining Phase 5 implementation in one release with one update/acceptance cycle. This guide supersedes separate Phase 5.2 update instructions. Phase 5.1 has owner-reported local acceptance; it does not imply acceptance of this combined build.

## Release scope and evidence contract

| Phase 5 requirement | Combined implementation | Evidence / limit |
| --- | --- | --- |
| Useful assessment results (FB-03) | The accepted Phase 5.1 snapshots, 27 reviewed objectives, explanations, evidence limits and lesson links remain included | Original scores retained; old attempts are not retrospectively regraded; one-question samples never establish weakness/mastery |
| Dashboard previews and course progression | Uninstalled 5.2 changes included: published/enrolled course counts, first incomplete lessons, recent assessment links, empty/loading/retry states | Owned server data; three-item previews explicitly labelled; lesson completion is activity, not mastery |
| Mission progression | Distinct missions completed at least once, latest active attempt counts, three recent mission links, direct owned-run reopening | Replays do not inflate distinct completions; latest completed attempt supersedes older active attempts in the active count; no cross-learner records |
| Mission results and next steps | Original saved per-stage feedback and points, replay/review/next-scenario guidance, explicit missing-detail message | No historical regrading or retrospective objective mapping; simulation points and ungraded reviews do not establish mastery |
| Persistent history access | Assessment pages of 20 and mission pages of 50 with load-older controls; older mission results/resume buttons | Cursor queries remain owned; assessment ordering uses timestamp and ID, not ID alone; all original records retained |
| Onboarding | Existing password confirmation, visibility and sign-in instructions retained; focused errors/notices and appropriate autofill | Browser tests check mismatch before HTTP, registration/sign-in flow, keyboard feedback and real API persistence |
| Mobile and dark theme | Readable status colours, corrected preview-answer foregrounds, narrow form/fieldset/mission layout, reduced-motion focus | Targeted automated viewport/contrast checks; independent physical-device/accessibility evidence still required |
| Logout | Shared bounded request/local-clear function for home and dashboard; server revocation when reachable | Offline local token removal does not prove server revocation; ordinary expiry still applies |
| Recovery from data-fetch failures | Learning, assessments, mission board and dashboard retries; failed loads do not masquerade as zero/empty progress | Browser assertions test recovery and retained navigation; no service availability claim |

This completes the planned Phase 5 **implementation scope**, subject to CI results below and one combined owner acceptance. New feedback/defects can require fixes; they do not create a sequence of planned 5.3/5.4 releases. Broader independent learner/device evidence and agreed release/operational/security gates remain open. Phase 6 catalogue expansion is separate. The formal Cloudflare audit remains deferred until the end of development.

## Data and authorization

No new migration, content publication or dependency is introduced beyond the accepted Phase 5.1 schema (`0010_attempt_results`). The single update block below explicitly checks/applies the current migration head through the development-only guard; it is safe when already current. Startup still never migrates automatically. Development source and data remain separate from beta.

Mission activity projections use the authenticated student's runs and current fixed mission catalogue. Unknown/retired catalogue entries are excluded from current discovery counts but not deleted. Saved decision explanations are returned only through the existing owned-run endpoint; future/uncommitted stages are excluded. Legacy records without reliable stage/point details receive an unavailable-evidence message. Source labels/catalogue structure describe today's catalogue; no claim of frozen historic teaching objectives is made for mission records.

Assessment history cursors are scoped to the owned course/attempt and preserve timestamp/ID order. Mission history cursors filter the current student's records. Neither changes stored answers, scores, choices, completion timestamps or attempt IDs. Optional review/practice still awards no persistent mastery or score.

## One complete PowerShell update and check block

Stop only development API/frontend with Ctrl+C. Leave beta open. Run from the existing development worktree root; do not separately install 5.2 first.

```powershell
$ErrorActionPreference = 'Stop'
$phaseFiveBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $phaseFiveBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema verification/migration failed.' }

$phaseFivePreviousDatabaseUrl = $env:DATABASE_URL
$phaseFivePreviousTestUrl = $env:TEST_DATABASE_URL
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
    $env:DATABASE_URL = $phaseFivePreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $phaseFivePreviousTestUrl
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

## One combined acceptance checklist

1. Register/sign in with a synthetic account, check password confirmation/show-password and focused error/success instructions. Check at a narrow mobile viewport, with keyboard/reduced motion and readable dark-theme messages.
2. Compare dashboard course counts with My learning; resume the first incomplete lesson, complete it and reload the dashboard. Check completed and zero-lesson course behavior. A new learner should see useful first steps.
3. Take short and full assessments across the three reviewed courses; compare total/question count, topic evidence, mistakes and lesson recommendations. Reload and reopen a result from the dashboard. Historical results retain their scores and explicit evidence limits. Load older assessment history if enough records exist.
4. Resume a saved mission from the dashboard, finish and reopen it. Check original saved stage explanations, missing legacy details, optional review, replay and distinct mission counts. Load older mission history and reopen an older result. A replay must not inflate distinct completion counts.
5. Exercise failed-load retry on development only (for example, stop the development API, load a page, restart and retry). Verify navigation survives and a failed request is not presented as zero progress. Check both home/dashboard sign-out; with a stopped development API, local sign-out remains bounded. Restart and verify isolation afterwards.
6. Recheck representative 2D/3D missions, lesson practice and assessment lengths. Preserve independent learner understanding, physical-device/accessibility and full operational/security evidence as separate acceptance records. Report sanitised issues only.

This is one development release, not a beta promotion. Recovery for new additive source is a source fix/revert and restart; no new data rewrite needs reversal. Preserve existing records and local changes. Do not downgrade the accepted Phase 5.1 snapshot migration as routine recovery.

## Verification checkpoint

Assistant checks before CI: 574 backend tests and 11 subtests passed with 20 database-dependent skips; all 15 frontend unit tests, TypeScript, clean production build and pip check passed. Existing TestClient deprecation and CSS compatibility warnings remain. New HTTP regressions cover owned/distinct mission projections, saved original decision feedback/legacy limits, and complete nonduplicating owned history pages. Real-session endpoint boundaries remain in the PostgreSQL suite. Local synthetic HTTP fixtures override authentication; these alone do not prove full login or PostgreSQL behavior.

Seven new mock-API browser cases cover mission dashboard/result links and history at desktop/320px, learning/assessment retry, onboarding/focus/dark-error contrast and older assessment reopening. They join the eight earlier progression cases and 132 existing journeys. No new local browser assertions are credited under the previously observed socket restriction; CI must supply the browser results.

The real-API browser workflow now selects this development branch and includes two new desktop/mobile journeys through registration, enrolment, persisted lesson completion, assessment topic evidence, result reopening and reachable-server logout revocation. Its fixture explicitly permits only an isolated localhost PostgreSQL database named `educyber_test`; it publishes only synthetic reviewed Python teaching/questions there, not to development or beta. CI execution and combined owner acceptance are pending at this checkpoint.


### Subsequent CI evidence

Application source `c0d5e75` passed [backend/PostgreSQL run 40728223888](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40728223888): 594 tests and 11 subtests, plus unit and dependency checks. The suite includes the new real-session mission-progress boundaries; synthetic content fixtures deliberately remain SQLite/auth-overridden where defined.

[Real API browser run 40728223984](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40728223984) passed all three cases: the existing 30-game catalogue/persistent mission/2D–3D journey and both new desktop/mobile onboarding-to-progress/result/logout journeys. These use actual FastAPI/PostgreSQL and synthetic isolated accounts/content. This establishes those bounded journeys, not every real-backend mission/device/accessibility or operational scenario.

The first intercepted-API progression run passed 14/15 cases, including all seven new combined-release cases. An older dashboard fixture lacked the newly introduced mission-progress response and counted alerts across two panels sharing a CSS class. The fixture now supplies the new response and scopes the assertion by the saved-course-progress region's accessible name. Legacy dashboard/game fixtures were updated to the current read-only contracts. This correction changes no application source. Corrected source `def9fae` is being checked in runs 40728703388 (intercepted API) and 40728703380 (real API).


### Final combined-release result

Fixture correction `def9fae` passed [intercepted-API browser run 40728703388](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40728703388): 15 progression cases and 132 existing journeys, **147/147** total. It also passed all 15 frontend unit tests, TypeScript and production build. [Real API browser rerun 40728703380](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40728703380) passed all **3/3** actual FastAPI/PostgreSQL cases again. Backend/PostgreSQL run 40728223888 passed **594 tests and 11 subtests**; dependency checks passed. No application-source change was needed for the fixture correction. This supersedes the earlier pending/failed fixture checkpoints.

All planned Phase 5 implementation is now in this single release. Next: use the one combined update/check/restart sequence above, then complete one local acceptance pass. Phase 5.2 remains uninstalled separately; no intermediate installation/acceptance is required. Independent learner/device understanding and operational/final security assurance remain separate open gates.


### Owner local acceptance — 28 October 2026

After receiving handover `f081cb8` and this combined guide, the owner reported "all test passed". The combined Phase 5 build therefore has owner-reported successful local checks/acceptance; this supersedes the earlier pending-local-acceptance checkpoints. No separate 5.2 installation/acceptance cycle is needed. No detailed logs, independent learner/physical-device or operational/final-security evidence is inferred. Beta promotion is not claimed. The next source task is the Phase 6 catalogue/tutor gap inspection recorded in DEVELOPMENT_STATUS.md.
