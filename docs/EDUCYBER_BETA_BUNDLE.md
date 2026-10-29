# EduCyber — bundled beta release and owner playthrough

29 October 2026 (Africa/Lagos). This single release combines the global EduCyber display name, navy/teal theme with scoped Red/Blue seat accents, deeper activities across the eight stages, the previously development-only journey/Red-Blue work, and guarded beta promotion. The owner explicitly authorised promotion and a development pause while completing a personal playthrough.

GitHub source promotion and the owner's laptop rollout are separate. Follow the complete blocks below to make the new source visible on the existing beta. No new hosting service, domain, account reset or external AI provider is required.

## Verified release evidence

Implementation `3f4d4ab26ca41f91f79e66c7664146c75721d705` passed [838 PostgreSQL backend tests plus 11 subtests and dependency gates](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40911328454), [150 browser regressions, 20 frontend unit tests, TypeScript and production build](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40911328726), and [27 real-API/PostgreSQL browser cases](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40911328515). Three backend SQLite lock cases intentionally skip; the PostgreSQL races execute. The beta source branch was advanced from `5824fb7` to this verified implementation with ancestry and expected-head checks. Final handover edits only documentation. The owner's laptop backup/migration/restarts and playthrough remain pending; follow the blocks below. Development is paused after this handover until explicit owner resumption.

## What is bundled

- **EduCyber** display branding, navigation, page metadata and recovery-mail wording. Session keys, account IDs, URLs, database identities and existing records retain their established identifiers. Geographic examples in existing teaching remain examples, not audience restrictions.
- Deep navy surfaces, teal accents and clear primary actions across the site. Active simulator workspaces use restrained crimson for Red and blue/teal for Blue; shared navigation remains navy/teal. Separate semantic warning/success colours and explicit seat labels are retained. This owner-requested correction supersedes the initial global crimson palette.
- **24 saved decision workshops, three per stage**, containing **72 decisions** with evidence, case consequences, unresolved decisions, simplified effort costs, saved resume and same-opening replay comparison. These are original guided cases, not 24 additional full network simulations. Existing 30 guided missions, four defender strategy scenarios, six Red/Blue scenarios, three foundation courses and the 500-question bank remain available.
- Six public introductory questions, topic practice, the existing lesson/reflection material and a solo role-reversal challenge at the final stage. Full two-human matches still need two distinct eligible student accounts; solo workshops and computer matches can be played independently.
- A workshop-to-feedback link carries only case/run/step context. Feedback remains learner-submitted. No passwords, session tokens, private seeds or invitation secrets belong in a report.

The new `/workshops` route is discoverable from every journey stage. Its public catalogue exposes summaries only. Saved cases use existing bearer/eligibility checks, ownership, bounded commands, UUID retry receipts, round/step preconditions and database row locking. No scores or state are accepted from the browser. Snapshot/rule revision `workshops-v1` preserves old attempts; replay compares a new run against the participant's own completed run. Counts/effort are teaching records, not a validated mastery or risk score.

## Migration and preservation

Beta may currently be at `0011_strategy_learning`. The explicit preparation upgrades through independent `0012_red_blue_matches` and **`0013_journey_workshops`**. No old table is dropped or rewritten by these migrations. The maintenance command creates/verifies a fresh binary logical backup and captures hashes/counts of existing records, including private Red/Blue and workshop records when present. It applies additive migrations and rechecks preservation around the established idempotent course publication. Preparation is never run on startup.

The beta readiness command now checks the actual source Alembic head rather than a hardcoded older revision. Head discovery uses absolute migration paths and does not require importing a database connection in the launcher. Existing beta/development database, interpreter, branch and port guards remain.

## 1. Stop the application terminals

Let active attempts finish. Use Ctrl+C in beta API, beta frontend and ngrok terminals, and development API/frontend terminals. Leave Docker Desktop and database containers running. Keep the source checkouts and data separate. Do not delete volumes, reset local source, copy development data to beta or use obsolete migration wrappers.

## 2. Update, check, back up and prepare beta once

Use the existing beta checkout. This block permits the known generated/local files but refuses unreviewed source edits; it never removes local changes. Use the normal existing verified recovery sender and HTTPS ngrok origin when private configuration needs completing. Existing accounts and invitations are retained; use your existing invited student account for the playthrough.

```powershell
$ErrorActionPreference = 'Stop'
$bundleBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $bundleBetaRoot
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') {
    throw 'Open the existing beta worktree; do not switch the development checkout to beta.'
}
$bundleChanges = @(git status --porcelain --untracked-files=normal)
$bundleUnsafe = @($bundleChanges | Where-Object {
    $_.Substring(3).Trim().Replace('\','/') -notin @(
        'web/next-env.d.ts','web/tsconfig.tsbuildinfo','compose.development.yaml'
    )
})
if ($bundleUnsafe.Count) { git status --short; throw 'Preserve and review local source edits before updating.' }
git pull --ff-only origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta update failed; do not force or reset.' }

& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-ci.lock
if ($LASTEXITCODE -ne 0) { throw 'Beta locked dependencies failed.' }
& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Beta local helper dependencies failed.' }
& .\api\.venv\Scripts\python.exe -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Beta dependency consistency failed.' }
Push-Location .\web
try {
    npm.cmd ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'Frontend dependencies failed.' }
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw 'Frontend typecheck failed.' }
}
finally { Pop-Location }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend build failed.' }

docker compose up -d --wait postgres
if ($LASTEXITCODE -ne 0) { throw 'Existing beta PostgreSQL startup failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py configure-mail
if ($LASTEXITCODE -ne 0) { throw 'Private recovery mail configuration failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py prepare
if ($LASTEXITCODE -ne 0) { throw 'Preparation failed; keep beta offline and retain the verified backup.' }
```

Expected preparation: `PROMOTION PREPARED: schema 0013_journey_workshops; all three course releases published; existing records preserved.` Retain the printed backup path, `.dump.sha256` and private preservation manifest. The dump contains private learner information; keep it protected. Archive/hash verification is not a fresh complete restore drill. If preparation stops, migrations may already have applied; retain the backup and inspect sanitised diagnostics. Do not delete learner records to pass a check.

## 3. Synchronise development separately

This discovers the already registered development worktree. No beta data or private mail settings are copied. The local development Compose file remains untouched. This keeps both environments ready while the owner plays on beta; it is not permission for more feature development.

```powershell
$ErrorActionPreference = 'Stop'
$bundleBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
$bundleDevRoot = & "$bundleBetaRoot\api\.venv\Scripts\python.exe" "$bundleBetaRoot\scripts\beta.py" development-path
if ($LASTEXITCODE -ne 0 -or -not $bundleDevRoot) { throw 'Cannot identify the existing development worktree.' }
Set-Location -LiteralPath $bundleDevRoot.Trim()
if ((git branch --show-current).Trim() -ne 'feature/beta-continuous-improvement') { throw 'Wrong development branch.' }
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Development update failed; preserve local changes.' }
& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development-only migration failed.' }
```

## 4. Start beta in separate terminals

Beta API:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped.' }
```

Beta frontend:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py web
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend stopped.' }
```

Verify beta, then open the **beta** journey (port 3000):

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py check
if ($LASTEXITCODE -ne 0) { throw 'Beta readiness failed; do not reopen tester access.' }
Start-Process 'http://127.0.0.1:3000/journey'
```

After the local smoke check, reopen the existing tunnel in its own terminal:

```powershell
$ErrorActionPreference = 'Stop'
ngrok http 3000
if ($LASTEXITCODE -ne 0) { throw 'Ngrok stopped.' }
```

If ngrok provides a changed HTTPS origin, stop only the beta API, update private mail configuration from the beta root with the full block below, then start the beta API again using its block above. Do not paste the key into chat. No database preparation is needed merely for an origin change.

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
$bundlePublicOrigin = Read-Host 'Current ngrok HTTPS origin (no trailing path)'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py configure-mail --public-url $bundlePublicOrigin
if ($LASTEXITCODE -ne 0) { throw 'Private recovery URL update failed.' }
```

Development may remain stopped during the beta playthrough. If needed, start it only with the existing `scripts/development.py api` and `web` guarded launchers from its own worktree, not the beta launchers or beta ports. No further feature work follows this release automatically.

## Owner playthrough and pause

Use [the stage-by-stage playthrough checklist](OWNER_BETA_PLAYTHROUGH.md). Check old account/progress first, then browse all eight stages, try the new cases and revisit the existing games. The six Red/Blue scenarios support solo computer play; the final stage includes solo role reversal and debrief. Two-human play requires another eligible account/session and remains optional for a solo tour.

Record page/case/run/step, the action, expected result, observed result, device and a sanitised screenshot. Workshop report links prefill only bounded case/run/step context. Do not include passwords, session tokens, private seeds, invitation codes or raw personal records.

**Development freeze:** after verified source promotion and this release handover, pause feature/content/theme redevelopment until Emmanuel completes the playthrough and explicitly resumes it. Respond to reported bugs and rollout blockers within their authorised scope; do not select a new phase, run a new redesign or promote further changes automatically.

Prefer a forward fix if rollback is needed. Preserve new match/workshop records and original engine versions. Do not drop the new tables or overwrite later feedback with an old backup without an explicit recovery decision. Functional checks do not close independent learning, physical-device, operational or deferred final formal security assurance gates.


## Applying only the palette correction

If the combined bundle has already been prepared and is running, this correction requires only a source update, frontend build and frontend restart. It adds no migration and needs no repeat content publication. Stop the beta **frontend** terminal with Ctrl+C; leave the API and database running. Use this complete block in the beta checkout, then start the frontend with its separate-terminal block in section 4:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Use the existing beta worktree.' }
git status --short
git pull --ff-only origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta update failed; preserve local changes and do not force.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend build failed.' }
```

After restarting the frontend, run the beta readiness block from section 4 and reload the browser. If the combined bundle has not yet been installed, use sections 1–4 in full instead. The development pause continues after this visual correction.
