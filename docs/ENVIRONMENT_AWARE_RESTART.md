# EduCyber environment-aware restart and release runbook

**Owner instruction 4 November 2026:** Every stage rollout must account for the **separate environment files**, preserve existing beta learner data, and avoid accidentally starting two copies of the API on the same port. Read with [development status](DEVELOPMENT_STATUS.md).

## Authoritative environment sources

| Environment | Checkout | Ports | Files consumed by existing launcher | Command |
| --- | --- | --- | --- | --- |
| **Beta** | `feature/secure-password-recovery` (`University_All_In_One`) | API **8000**, web **3000**, existing PostgreSQL **5433** | Root `.env` supplies **only** beta `POSTGRES_PASSWORD`; `api/.env.beta` supplies `BREVO_API_KEY`, `EDUCYBER_EMAIL_SENDER`, `EDUCYBER_PUBLIC_WEB_URL` | `api/.venv/Scripts/python.exe scripts/beta.py api\|web\|build\|check` |
| **Development** | `feature/beta-continuous-improvement` (`University_All_In_One_Development`) | API **8010**, web **3010**, isolated PostgreSQL **5434** | `api/.env.development` provides the isolated `DATABASE_URL`; never copy Beta recovery-mail settings | `api/.venv/Scripts/python.exe scripts/development.py api\|web\|check` |

Both launchers rebuild a fixed, **sanitised** application process environment and ignore inherited beta/dev app settings. Beta launcher requires its private recovery-mail values for API startup, and validates the precise beta DB address. Development checks its own DB address and denies beta credentials. **Do not commit, print, paste or transfer the contents of these .env files**. The `EDUCYBER_PUBLIC_WEB_URL` must remain the current correct public Beta origin for password-reset emails when ngrok URLs change; use the existing private `beta.py configure-mail --public-url https://<current-host>` to update it, not a copy from development.

No application feature stage should rewrite these environment files, run `beta.py prepare`, run `beta.py courses`, apply Alembic migrations, recreate Docker volumes, reseed accounts or alter beta records unless a separately reviewed stage explicitly requires it.

## Safe preflight before any restart (Windows PowerShell)

**From the Beta repository root only**, inspect current listeners **before** launching new processes. Recent owner diagnostics confirmed multiple Python wrapper/Uvicorn processes and an occupied port 8000; the launcher's `OSError` was a normal conflict rather than a broken Beta database. Prefer **Ctrl+C in the terminal that started each Beta process**. If it remains stuck, identify its **exact executable path and port** before stopping; never stop by broad `python`, `uvicorn` or port alone because development is also running.

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = 'C:\Users\dNA1991\University_All_In_One'
Set-Location $betaRoot
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Expected beta checkout.' }
$betaPython = (Resolve-Path '.\api\.venv\Scripts\python.exe').Path
Write-Host 'API listeners (beta 8000; dev 8010):'
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in @(8000, 8010, 3000, 3010) } |
    Select-Object LocalAddress, LocalPort, OwningProcess
Get-CimInstance Win32_Process |
    Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'uvicorn main:app' } |
    Select-Object ProcessId, ExecutablePath, CommandLine | Format-List
```

After reviewing process ownership, stop old **Beta** API/web via their original terminal with Ctrl+C. To release a proven **Beta 8000 Uvicorn** process only (never dev), use the following *optional targeted recovery* after normal shutdown fails:

```powershell
$betaPython = (Resolve-Path '.\api\.venv\Scripts\python.exe').Path
$matches = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'python.exe' -and
    $_.ExecutablePath -eq $betaPython -and
    $_.CommandLine -match 'uvicorn main:app' -and
    $_.CommandLine -match '\-\-port 8000'
})
foreach ($process in $matches) {
    Write-Host "Stopping verified beta Uvicorn PID $($process.ProcessId)"
    Stop-Process -Id $process.ProcessId -ErrorAction Stop
}
if (Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue) {
    throw 'Beta port still in use. Inspect its owner; do not blindly kill other processes.'
}
```

Existing wrapper processes may remain after a child Uvicorn exits. Confirm original terminals have stopped before restarting. For web port **3000**, identify its **exact Next.js process and checkout** rather than killing generic Node processes.

## Beta source update and build — only after a green stage release

1. Stop only beta API/web. Keep both databases, development and ngrok untouched. Preserve any uncommitted files first. A Next.js build may modify `web/next-env.d.ts`; inspect `git diff -- web/next-env.d.ts` and stash **only this known generated-file change** if no other unreviewed changes exist. Never run `git reset --hard` or `git clean`.
2. From Beta root: `git fetch origin feature/secure-password-recovery`, then `git merge --ff-only origin/feature/secure-password-recovery`. Do not force a merge or operate on the dev checkout.
3. Ensure the existing private beta root `.env` and `api/.env.beta` are **present**; do not display values. If a public ngrok origin has changed, update only the public origin through `configure-mail`. **Do not run migration or courses for a source-only stage.**
4. Run `& .\api\.venv\Scripts\python.exe .\scripts\beta.py build`. Keep output/error logs; a build may regenerate `web/next-env.d.ts`.
5. In two separate **Beta root** terminals, run `& .\api\.venv\Scripts\python.exe .\scripts\beta.py api` and `& .\api\.venv\Scripts\python.exe .\scripts\beta.py web`. **These are foreground processes**; keep terminals open. Do not run another copy if port 8000/3000 already listens. The API launcher validates beta mail and database target.
6. In a **third** terminal run `& .\api\.venv\Scripts\python.exe .\scripts\beta.py check`. Expect `BETA READY: direct/proxied API and schema checks passed; development identity is absent.`. Confirm public ngrok points to beta **3000**, not development **3010**; test password-reset origin without exposing a real token.
7. Record beta Git revision, runtime health, browser gameplay, private tester feedback and any issue separately from the CI source merge. If the build fails, **do not** claim deployment or silently restore/migrate data.

## Development restart (separate checkout)

Use `C:\Users\dNA1991\University_All_In_One_Development`. Check its branch, retain its existing `api/.env.development`, and ensure API 8010 and web 3010 are free. From two different terminals run:
- `& .\api\.venv\Scripts\python.exe .\scripts\development.py api`
- `& .\api\.venv\Scripts\python.exe .\scripts\development.py web`

After both start: `& .\api\.venv\Scripts\python.exe .\scripts\development.py check`. This must verify direct/proxied development identity and the **isolated** database. Do not use `beta.py`, root beta `.env` or `api/.env.beta` in development. Do not restart the beta merely to test development.

## Git workflow when Beta is ahead

Beta merges may create a merge commit. Development is updated **only** using a verified fast-forward from the existing Beta ancestor when the development tree has no pending changes; otherwise integrate with review. Never reset a worktree to force synchronisation. Record exact source hashes and CI results; a GitHub merge does not restart local services.
