# Course-library beta release — 4 November 2026

The owner authorises the current 24 courses /192 lessons as a beta preview, deferring rewrites. This supersedes earlier editorial no-beta instructions for this snapshot. [Cleanup backlog and next-chat prompt](LESSON_CLEANUP_BACKLOG.md) preserve the unfinished work. The normal production publisher still requires genuine editorial approvals.

## Source and runtime

Beta head `c8e5fbc06c057b59ed70dc1d907b28b52fcaefeb` is an ancestor of development; source can fast-forward without discarding either history. The release includes eight saved manuscript edits, an exact-content beta manifest and an explicit `courses` action. Both branches should finish on the same checked revision. Source promotion does not operate the owner's laptop, PostgreSQL or ngrok.

`courses` validates all hashes, full 3×8 mapping and duplication guards; verifies the existing local private-beta target/current schema; creates a `pg_dump` backup with archive-list/checksum verification; then inserts all 24 courses atomically. It fingerprints every field of existing records, including old lesson text. A collision or changed prior course fails and rolls back. Repeating the same release is idempotent. It does not migrate, reseed, delete or update existing lessons. No fake editorial approvals are created. Backup listing/checksum verification is not a complete restore drill.

## Laptop PowerShell rollout

Stop **beta API and beta web only** using Ctrl+C in their terminals. Keep Docker/PostgreSQL and the separate development environment running. Start from the existing beta root, normally `C:\Users\dNA1991\University_All_In_One`:

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Use the beta checkout.' }
if (@(git status --porcelain).Count -ne 0) {
    git status --short
    throw 'Preserve and review local changes before updating; do not reset or clean.'
}
git fetch origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta fetch failed.' }
git merge --ff-only origin/feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta fast-forward failed.' }
$betaPython = Join-Path (Get-Location) 'api\.venv\Scripts\python.exe'
if (-not (Test-Path $betaPython)) { throw 'Existing beta api/.venv Python not found.' }
& $betaPython .\scripts\beta.py courses
if ($LASTEXITCODE -ne 0) { throw 'Publication stopped. Keep beta services stopped; inspect the snapshot, backup and configuration. No automatic restore.' }
& $betaPython .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta build failed. Keep the verified backup; no automatic restore.' }
Write-Host 'Restart beta API and web in separate terminals using the blocks below.'
```

Configuration uses the existing root `.env` and private mail settings without printing credentials. A schema/content collision is a diagnostic stop; never stamp migrations or delete enrolled courses to force publication.

**Beta API terminal**, from the beta root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped or could not start.' }
```

**Beta web terminal**, from the beta root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py web
if ($LASTEXITCODE -ne 0) { throw 'Beta web stopped or could not start.' }
```

**Readiness terminal**, from the beta root:

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py check
if ($LASTEXITCODE -ne 0) { throw 'Beta readiness failed.' }
Write-Host 'Open http://127.0.0.1:3000/learn and the current ngrok beta link.'
```

Publication must print `BETA COURSES READY: 24 courses / 192 lessons`. Verify eight courses per pathway, eight readable lessons each, enrollment/completion/resume, retained earlier progress/assessments/feedback and normal game/auth behaviour. Keep ngrok on beta port 3000. Source merge/build alone does not establish public runtime success.

**Development source update**, run from the beta root after readiness, locating its existing worktree rather than guessing a path:

```powershell
$ErrorActionPreference = 'Stop'
$devRoot = (& .\api\.venv\Scripts\python.exe .\scripts\beta.py development-path).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $devRoot)) { throw 'Existing development worktree not identified.' }
Push-Location $devRoot
try {
    if ((git branch --show-current).Trim() -ne 'feature/beta-continuous-improvement') { throw 'Wrong development branch.' }
    if (@(git status --porcelain).Count -ne 0) { git status --short; throw 'Preserve/review development local changes first.' }
    git fetch origin feature/beta-continuous-improvement
    if ($LASTEXITCODE -ne 0) { throw 'Development fetch failed.' }
    git merge --ff-only origin/feature/beta-continuous-improvement
    if ($LASTEXITCODE -ne 0) { throw 'Development fast-forward failed.' }
} finally { Pop-Location }
```

This updates development source only; it does not copy beta data or publish courses there.

## Evidence

Latest backend/frontend/browser-gameplay/real-API workflows on preceding `1741bfe` succeeded. An older duplicate real-API failure is superseded by the newer successful run. Current local checks and final-source CI are recorded in the handover with their actual state. Laptop publication, actual backup restoration and ngrok acceptance remain owner-operated.
