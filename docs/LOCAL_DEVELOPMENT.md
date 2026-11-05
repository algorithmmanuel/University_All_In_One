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
