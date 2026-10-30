# Three pathways + detailed Help — development and beta laptop release

30 October 2026. The owner explicitly authorises synchronising both source branches before testing locally and through ngrok. This supersedes earlier development-only promotion restrictions for this release. The owner has **not yet tested** the distinct pathway allocation. Source promotion is separate from updating the laptop; no laptop services are operated by the assistant.

## Delivered scope

- Three pathways with distinct core materials across eight shared stage names. [The exact matrix](PATHWAY_CONTENT_RELEASE.md) lists teaching, topics, ten guided missions/eight workshops per pathway, and scenario allocations. General browsing and earlier saved history remain accessible.
- Detailed `/help`: ten chapters, contents links, three entry routes and all 24 stage/pathway links. Explains every activity, actual controls, evidence, costs/turns, hidden commitments, computer/human play, invitations, save/resume/replay, 2D fallback and troubleshooting. Available publicly through Start here / Help in either environment.
- Final-stage onward invitation: Explorers → Academy → Command. Moving between pages does not award pathway completion, mastery or a certificate. Explorer/Command stage six are explicitly focused workshops; Academy stage six is full Branch Siege.
- Existing account/session identifiers, databases, schemas, game rules, authored workshop/mission content, published banks and dependencies are unchanged. This is frontend/content organisation and Help. **Do not run migrations, prepare/publish content, reseed, reset data or copy a database for this update.** Already-installed bundle schema remains required; if readiness reports an older installation, use the earlier bundle runbook rather than treating this update as a migration.
- Future enrichment should add depth within these three eight-stage routes. No further gameplay/content expansion starts automatically while the owner tests.

Beta had independent documentation-only commits after PR #4. Preserve that history through the combined merge; do not force beta backwards. Exact verification/promotion evidence is recorded in DEVELOPMENT_STATUS.md after checks.

## 1. Stop only the frontend terminals

Use Ctrl+C in the **beta frontend (3000)** and **development frontend (3010)** terminals. Leave their API processes and database containers running if healthy. The APIs have no changes. An already-running ngrok tunnel to port 3000 can stay running; it will briefly be unavailable while beta rebuilds. Do not launch a second API or duplicate tunnel merely for this update.

## 2. Update and check both existing worktrees

Run this from an ordinary PowerShell terminal. The known beta folder is under your Windows profile; the registered development path is discovered rather than guessed. The block preserves the known generated/local files, refuses unexpected source edits, never force-resets and saves a local rollback reference for each current source revision. If a pull refuses a locally modified generated file, stop and inspect it; no local change is automatically removed or stashed.

```powershell
$ErrorActionPreference = 'Stop'
$releaseBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $releaseBetaRoot
$releaseBetaBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $releaseBetaBranch -ne 'feature/secure-password-recovery') {
    throw 'Open the existing beta worktree; do not switch the development worktree to beta.'
}
$releaseDevRoot = & .\api\.venv\Scripts\python.exe .\scripts\beta.py development-path
if ($LASTEXITCODE -ne 0 -or -not $releaseDevRoot) { throw 'Could not locate the existing development worktree.' }
$releaseDevRoot = ($releaseDevRoot | Select-Object -Last 1).Trim()
$releaseTargets = @(
    @{ Root = $releaseBetaRoot; Branch = 'feature/secure-password-recovery'; Label = 'beta' },
    @{ Root = $releaseDevRoot; Branch = 'feature/beta-continuous-improvement'; Label = 'development' }
)
$releaseStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
foreach ($releaseTarget in $releaseTargets) {
    Set-Location -LiteralPath $releaseTarget.Root
    $releaseBranch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $releaseBranch -ne $releaseTarget.Branch) {
        throw "Unexpected branch in $($releaseTarget.Label) worktree."
    }
    $releaseChanges = @(git status --porcelain --untracked-files=normal)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect local source changes.' }
    $releaseUnsafe = @($releaseChanges | Where-Object {
        $_.Substring(3).Trim().Replace('\','/') -notin @(
            'web/next-env.d.ts','web/tsconfig.tsbuildinfo','compose.development.yaml'
        )
    })
    if ($releaseUnsafe.Count) { git status --short; throw 'Preserve and review unexpected local changes before continuing.' }
    $releaseRollbackRef = "rollback/pathways-help-$($releaseTarget.Label)-$releaseStamp"
    git branch $releaseRollbackRef HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Could not save the pre-update source reference.' }
    git pull --ff-only origin $releaseTarget.Branch
    if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve local files and investigate without force/reset.' }
    git log -1 --oneline
    Push-Location .\web
    try {
        npm.cmd test
        if ($LASTEXITCODE -ne 0) { throw 'Frontend unit checks failed.' }
        npm.cmd run typecheck
        if ($LASTEXITCODE -ne 0) { throw 'TypeScript check failed.' }
    }
    finally { Pop-Location }
}
# Build beta using its guarded configuration; beta frontend must be stopped.
Set-Location -LiteralPath $releaseBetaRoot
& .\api\.venv\Scripts\python.exe .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta build failed; do not start the old frontend against an incomplete build.' }
# Development uses its existing guarded dev launcher in the next section.
Set-Location -LiteralPath $releaseDevRoot
Write-Host 'Source updated. Start each frontend in its own terminal using the blocks below.'
```

No dependency files changed; installation is unnecessary for an already working setup. If the checks identify missing packages, stop and resolve that concrete installation issue rather than changing API/database settings.

## 3. Start beta frontend — its own terminal

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py web
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend stopped.' }
```

## 4. Start development frontend — another terminal

```powershell
$ErrorActionPreference = 'Stop'
$releaseBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $releaseBetaRoot
$releaseDevRoot = & .\api\.venv\Scripts\python.exe .\scripts\beta.py development-path
if ($LASTEXITCODE -ne 0 -or -not $releaseDevRoot) { throw 'Development worktree discovery failed.' }
Set-Location -LiteralPath (($releaseDevRoot | Select-Object -Last 1).Trim())
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

## 5. API startup only if you had stopped it

If API health already responds, keep the existing process. A second process on the same port produces the port-in-use error encountered previously. If an API terminal was stopped, use the matching complete block in its own terminal.

Beta API:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped; check its existing private configuration and port.' }
```

Development API:

```powershell
$ErrorActionPreference = 'Stop'
$releaseBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $releaseBetaRoot
$releaseDevRoot = & .\api\.venv\Scripts\python.exe .\scripts\beta.py development-path
if ($LASTEXITCODE -ne 0 -or -not $releaseDevRoot) { throw 'Development worktree discovery failed.' }
Set-Location -LiteralPath (($releaseDevRoot | Select-Object -Last 1).Trim())
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

## 6. Verify both local environments

Use a separate terminal after both frontends/APIs are ready:

```powershell
$ErrorActionPreference = 'Stop'
$releaseBetaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $releaseBetaRoot
& .\api\.venv\Scripts\python.exe .\scripts\beta.py check
if ($LASTEXITCODE -ne 0) { throw 'Beta readiness failed; retain current data and inspect sanitised diagnostics.' }
$releaseDevRoot = & .\api\.venv\Scripts\python.exe .\scripts\beta.py development-path
if ($LASTEXITCODE -ne 0 -or -not $releaseDevRoot) { throw 'Development worktree discovery failed.' }
Set-Location -LiteralPath (($releaseDevRoot | Select-Object -Last 1).Trim())
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation/readiness failed.' }
foreach ($releaseOrigin in @('http://127.0.0.1:3000','http://127.0.0.1:3010')) {
    $releaseHelp = Invoke-WebRequest -UseBasicParsing -Uri "$releaseOrigin/help"
    if ($releaseHelp.StatusCode -ne 200 -or $releaseHelp.Content -notmatch 'How to play') {
        throw "Detailed Help was not served by $releaseOrigin."
    }
    Write-Host "$releaseOrigin/help - detailed guide available"
}
Start-Process 'http://127.0.0.1:3010/help'
Start-Process 'http://127.0.0.1:3010/journey?stage=discover&pathway=secondary'
```

## 7. Expose only beta through ngrok

Reuse your existing tunnel if it already forwards to beta port 3000. If it is stopped, run this in its own terminal:

```powershell
$ErrorActionPreference = 'Stop'
ngrok http 3000
if ($LASTEXITCODE -ne 0) { throw 'Ngrok stopped.' }
```

Use the current HTTPS origin displayed by ngrok. Open `/help` and `/journey`; do not append the nonexistent `/app` route. Development remains local on port 3010; do not point this beta tunnel at it.

Check and open the public beta in a separate terminal:

```powershell
$ErrorActionPreference = 'Stop'
$releasePublicInput = (Read-Host 'Current ngrok HTTPS origin only, without a path').Trim().TrimEnd('/')
$releasePublicUri = [uri]$releasePublicInput
if (-not $releasePublicUri.IsAbsoluteUri -or $releasePublicUri.Scheme -ne 'https' -or
    $releasePublicUri.UserInfo -or $releasePublicUri.Query -or $releasePublicUri.Fragment -or
    $releasePublicUri.AbsolutePath -ne '/') {
    throw 'Enter only the current HTTPS ngrok origin.'
}
$releasePublicHelp = Invoke-WebRequest -UseBasicParsing -Uri "$releasePublicInput/help" -Headers @{'ngrok-skip-browser-warning'='true'}
if ($releasePublicHelp.StatusCode -ne 200 -or $releasePublicHelp.Content -notmatch 'How to play') {
    throw 'Public beta did not return the detailed guide. Check the tunnel forwards to port 3000.'
}
Start-Process "$releasePublicInput/help"
Start-Process "$releasePublicInput/journey?stage=discover&pathway=secondary"
```

If the public origin changed, update password-recovery links without altering databases. Stop only beta API with Ctrl+C, then use this complete block before restarting it with section 5. Skip this if the configured origin is still current.

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
$releasePublicOrigin = (Read-Host 'Current ngrok HTTPS origin only').Trim().TrimEnd('/')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py configure-mail --public-url $releasePublicOrigin
if ($LASTEXITCODE -ne 0) { throw 'Private mail-origin update failed.' }
```

## 8. One playthrough in each environment

Use separate browser profiles or windows for local development and public beta; private learner records remain in separate databases. Localhost/127.0.0.1 and public ngrok are separate browser origins. Do not assume an account created only in development exists in beta; use an existing invited beta learner.

- Open Start here / Help; test the contents links, pathway entries and relevant activity instructions. On mobile, confirm no horizontal page overflow.
- Compare all eight stages across the three pathways against the matrix. Complete each six-question introduction and inspect its explanation/onward suggestion.
- Open an allocated workshop, finish it and reopen its saved result. Compare a replay. Reopen an earlier saved mission/assessment/game to check continuity.
- Try the pathway defender scenario and Red/Blue computer match; for human play use two distinct eligible accounts in separate sessions. Review the debrief and stage-eight next-pathway invitation.
- Confirm beta uses its existing accounts/progress and development remains isolated. Record which environment, pathway, stage and activity had an issue. No completion or acceptance is recorded merely because commands were supplied.

Rollback: prefer a forward fix and retain the local rollback refs. If the frontend build/start fails, stop that frontend and retain the error without changing databases. A maintainer can use the preserved source ref in a separate worktree or a reviewed revert; do not reset a checkout containing local edits or roll back the database for a frontend change.

## Verification checkpoint

Local 24 frontend unit tests, TypeScript and production build passed. New desktop/mobile Help cases cover all contents targets, 24 stage/pathway links, narrow layout, public entry and no POSTs. Final current-head browser/real-API CI and source promotion are pending at this implementation checkpoint. Earlier pathway verification remains tied to its recorded SHA. No laptop runtime, database, private mail or ngrok operation was performed here.


## Final verified source promotion

Verified implementation `168b55a` passed [browser CI 41055336307](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41055336307): 158 browser cases, 24 frontend unit tests, TypeScript and production build. [Actual-API/PostgreSQL CI 41055336706](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41055336706) passed all 30 cases. These supersede the pending checkpoint above.

The reconciled commit preserves beta's independent documentation history. Beta was advanced from `0d13fc5` to this exact checked implementation using an expected-head lease, with both parents/ancestry and unchanged backend/schema/dependencies confirmed. Final documentation is synchronised to both source branches. **Both branches are ready to pull; the laptop update and playthrough above remain pending.** No owner processes, data or ngrok settings were operated by this release. The owner has not yet supplied local/public acceptance.
