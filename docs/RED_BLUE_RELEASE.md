# Red/Blue simulator — development release

29 October 2026 (Africa/Lagos). Development branch only: `feature/beta-continuous-improvement`. Do not update, migrate, restart or promote `feature/secure-password-recovery` for this release.

## What is available

Open [the development simulator](http://127.0.0.1:3010/red-blue), or choose **Red / Blue** on the dashboard / **Red / Blue simulator** in Cyber Lab. Six scenarios, either seat, three computer difficulty levels and authenticated two-learner invitations use the original engine rules. Network and asset-list views expose only the selected seat's information. Plan one conceptual action with cost/prerequisites/explanation/mapping, seal it, and wait for the other seat. Read your evidence ledger and the participant-only terminal debrief. The action field guide is available without leaving the page.

Existing authentication, student/private-beta eligibility and logout apply. Human players need **different student accounts and separate browser sessions** (for example, a normal and private browser window). Red/Blue are match seats; do not create teacher/admin accounts to play. Instructor/spectator access is disabled. Computer policies are inspectable rules, not generative AI. No real scanning, exploit, payload or external AI integration exists.

The page checks waiting/sealed matches every three seconds while visible, with no background turn clock. Refresh checks saved state; reopening a saved match restores it after reconnect/sign-in. Interrupted command responses retain the same UUID/payload for safe retry. A stale/conflicting command reloads the authorized projection. Polling does not move keyboard focus or apply an old response to a different match. Deliberate start/resume/join uses the existing reduced-motion-aware focus helper.

## Complete PowerShell update, migration and checks

Stop **only development** API/frontend terminals with Ctrl+C. Keep beta running. Use the existing development worktree root, preserving any unrelated local changes. No dependency or content publication change is required. Migration `0012_red_blue_matches` adds independent simulator tables; the guard below refuses beta and requires development ports to be free. It does not migrate on ordinary startup.

```powershell
$ErrorActionPreference = 'Stop'
$redBlueBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $redBlueBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development migration failed; do not start services.' }

$redBluePreviousDatabaseUrl = $env:DATABASE_URL
$redBluePreviousTestUrl = $env:TEST_DATABASE_URL
try {
    $env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
    $env:TEST_DATABASE_URL = ''
    Push-Location .\api
    try {
        & .\.venv\Scripts\python.exe -m pytest -q
        if ($LASTEXITCODE -ne 0) { throw 'Backend synthetic checks failed.' }
    }
    finally { Pop-Location }
}
finally {
    $env:DATABASE_URL = $redBluePreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $redBluePreviousTestUrl
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

Start API in its own terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

Start frontend in another terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

Verify isolation/readiness in a third terminal, from the development root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation verification failed.' }
Start-Process 'http://127.0.0.1:3010/red-blue'
```

These local synthetic tests intentionally skip PostgreSQL-only checks. The CI PostgreSQL evidence in status is separate; neither providing these commands nor committing source establishes that they ran on the owner's laptop.

## One acceptance pass

1. Start a computer match as Blue, then another as Red. Review scenario objectives, difficulty descriptions, equal budgets and the action field guide. Compare the network with the asset list. Check a narrow screen, keyboard focus and reduced motion.
2. Select an asset and inspect known controls/weaknesses or dated Red intelligence. Choose a targeted action and read cost, prerequisites and public mapping before sealing. Confirm one choice only, Blue-first resolution and finite resources. Compare investigating with containment; isolation costs service availability.
3. Create a human match, generate an invitation and share it privately with a different synthetic learner in a separate session. Rotation invalidates the old code; it expires after 24 hours. The creator cannot claim both seats. Wait for automatic join recognition or refresh manually.
4. Seal only one seat's choice. That learner sees their own locked order. The other learner should see their own information, with no opponent choice, seed or full state. Submit the other seat for the same round; both should advance once. Leave/reload, resume from saved matches and confirm costs/evidence persist. No timeout forfeit is applied if a learner leaves.
5. Finish a match. Review Blue/Red decisions in resolution order, missed signals and affordable one-round alternatives. These are seeded examples, not guarantees of a different match winner or proof of learner mastery. Reopen the finished match and confirm the debrief is retained through recomputation.
6. Sign out of one session. It must lose access; the other learner's session remains independent. Recheck existing courses, assessments, practice, missions, Cyber Lab and old saved progress in development. Record confusing rules, learning gaps and balance/device observations.

## Evidence and recovery

[API contract](RED_BLUE_API.md) describes storage, ownership, secrecy, invitation and transaction boundaries. [Simulator plan](RED_BLUE_SIMULATOR_PLAN.md) describes pinned rules; [authoring guide](RED_BLUE_AUTHORING.md) covers extension. `DEVELOPMENT_STATUS.md` records exact verified source and results, including pending acceptance gates.

Prefer a forward fix. Preserve simulator transcripts and original engine editions. Ordinary downgrade to old application code leaves simulator tables unused; old readiness checks may reject a newer schema revision. Do not drop tables, rewrite saved editions or downgrade the database to make readiness green. Review compatibility and backups explicitly before any destructive recovery. This release makes no beta runtime/database changes. Independent content/learning/balance/device, operational retention/restoration and final formal security assurance remain open.


## Verified automated release evidence

Implementation `fe5de7570b44e1a5a1ddf9883ce273ee74672d72` passed [backend/PostgreSQL CI 40875345895](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40875345895): **805 tests plus 11 subtests**, migrated isolated PostgreSQL and dependency checks/audit. [Actual API/PostgreSQL browser CI 40875346015](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40875346015) passed **all 22 cases** (14 existing plus eight simulator). [Browser regression CI 40875346079](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40875346079) passed **147 existing journeys**, **15 frontend unit tests**, TypeScript and production build. The separate-session PostgreSQL gate was recorded and committed before interface implementation.

All automated gates for this release are green. Use the complete blocks above for one development update/migration/restart and the acceptance pass. Owner execution/acceptance and independent educational/balance/physical-device/operational/final-security evidence remain pending. Beta remains at `5824fb7b2ce309506e86b8fa0caeb9c5c339aedd`; no simulator promotion or beta runtime/database change was made.


## Windows symlink-test portability

If the previous suite stopped at `WinError 1314` in `test_cyber_warfare.py`, update the development branch and rerun the complete update/check block above in an ordinary PowerShell terminal. The corrected suite isolates the symlink test and skips it only when Windows denies symlink creation with error 1314. Size, filename and duplicate-intelligence checks still run. The actual symlink-rejection case runs on Linux CI using otherwise valid content. No application security guard, dependency, schema or beta configuration change is needed. This correction does not mark the owner's failed check block or later frontend checks as successful.
