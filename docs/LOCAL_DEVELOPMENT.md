# Running development alongside beta

Use the `feature/beta-continuous-improvement` worktree. The launcher refuses other branches, other Python environments and database targets outside the dedicated development database. It does not run migrations, create users or change the beta checkout.

The local database and ignored configuration were created during Phase 1 setup. Keep the credential file private. Only its database setting is consumed by the launcher; application mode, origins and ports are explicitly set by the launcher. Inherited beta application, public API and mail configuration is discarded. Password reset delivery remains unavailable until an isolated mail-testing design is introduced.

## Prepare

From the development repository root in PowerShell:

```powershell
& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw "Development Python dependencies failed." }

Push-Location .\web
try {
    npm.cmd ci
    if ($LASTEXITCODE -ne 0) { throw "Frontend dependency installation failed." }
} finally { Pop-Location }
```

The existing local Compose definition remains pending review/commit. Do not overwrite it or publish its credential file. To start its existing database if needed, use its explicit development Compose project and file, never the beta Compose project.

## Start

In a terminal at the development root:

```powershell
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
```

In a second terminal at the same development root:

```powershell
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
```

Use the addresses reported/configured by the development launcher. Open the development frontend using its loopback address, not the beta tunnel. Keep all existing beta terminals running. Ctrl+C in each development terminal stops only that foreground development process.

The launcher uses explicit ports and refuses occupied ports instead of silently selecting an alternative. It does not automatically reload the API; restart that development terminal after backend source changes.

## Verify isolation

In a third terminal at the development root:

```powershell
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
```

The check compares a non-secret, process-specific identity from the development API directly and through the frontend proxy. It then checks direct/proxied database and schema readiness and performs a read-only database identity query. A generic HTTP 200 alone does not pass the check. The identity endpoint is absent unless isolated local mode is explicitly enabled with an approved development database target.

This check does not prove that all browser requests are correct or that beta remains healthy. Confirm beta's existing health separately and complete a synthetic learner journey in the development browser.

## Configuration design

- `EDUCYBER_API_ORIGIN` controls the server-side Next.js proxy. The existing beta default is preserved. Only HTTPS origins or loopback HTTP origins without credentials, query, fragment or path are accepted.
- Isolated mode requires its designated development API and same-origin browser requests.
- Home-page game fetching and logout now use same-origin browser requests by default.
- `EDUCYBER_WEB_ORIGIN` supplies the server-rendered pathway request's frontend origin. The beta fallback is preserved for ordinary runs.
- Existing reset-password cache and referrer headers are retained.
- Local startup validates configuration before launching either service; it does not use beta credentials from the current PowerShell session.

## Focused checks

```powershell
Push-Location .\api
try {
    & .\.venv\Scripts\python.exe -m unittest -v test_development_isolation
    if ($LASTEXITCODE -ne 0) { throw "Development isolation tests failed." }
} finally { Pop-Location }

Push-Location .\web
try {
    node --test tests/api-origin.test.cjs
    if ($LASTEXITCODE -ne 0) { throw "Proxy configuration tests failed." }
    npm.cmd run typecheck
    if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
    npm.cmd test
    if ($LASTEXITCODE -ne 0) { throw "Frontend tests failed." }
} finally { Pop-Location }
```

Do not use the old synchronisation wrapper blindly: its branch expectation predates this development branch. These commands run focused checks directly without synchronising or switching the beta worktree. Database-writing suites require separately reviewed isolated-test configuration.

## Remaining validation

Record actual Windows startup and runtime results in DEVELOPMENT_STATUS.md. The committed guard tests do not establish full application compatibility, frontend type correctness, browser success or a passing full database test suite. Broad dependency ranges and a different newly installed environment remain an explicit compatibility/reproducibility work item.


## V3 isolated Microfinance database backup and migration

**Only after final-head CI passes and after reviewing your local Development setup.**
V3 adds `0014_red_blue_v3_pilot` with two new match-related tables; ordinary
service startup never migrates. Preserve the Beta checkout, port 5433, ngrok and
all existing database volumes.

Stop **only** the Development frontend, API and timed worker (Ctrl+C).
From the Development checkout root in PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/beta-continuous-improvement') { throw 'Wrong checkout' }
git status --short
# Review tracked changes and backups before any git update.
& .\api\.venv\Scripts\python.exe .\scripts\backup_development.py
if ($LASTEXITCODE -ne 0) { throw 'Verified Development backup required before migration.' }
& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Migration stopped: inspect Development logs privately.' }
```

The backup command validates both the configured connection and actual
PostgreSQL server identity before creating a custom-format `pg_dump`
archive. It confirms `pg_restore --list`, SHA-256 and byte size in a
local, ignored `.local-development-backups/` manifest. It requires both
`pg_dump` and `pg_restore` installed on PATH. The migration script
refuses to run without a backup made within the last 24 hours for the
**same** Development database and **same** pre-migration Alembic revision.
This verifies archive integrity, but a separate restore rehearsal is still
recommended for production-grade assurance.

**Port discrepancy:** the source runtime guard currently requires
`127.0.0.1:5435`, database and user `educyber_dev`. Older planning
notes mention 5434. Do not override the launcher or change local database
ports blindly. If the existing dedicated database is still on 5434, the
new script will refuse to continue; resolve that isolation configuration
before migrating. Do not disclose the private connection password.

After a successful migration, start Development API on 8010, web on 3010
and the independent `development.py clock-worker` in separate terminals,
then run `development.py check`. Visit
`http://127.0.0.1:3010/red-blue/v3` with a Development learner account.
Test Blue vs computer first and then a separate second authenticated human
account. Never run these migration commands from the Beta checkout.
