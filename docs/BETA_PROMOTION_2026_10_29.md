# Beta promotion and separate development restart — 29 October 2026

The owner reported Branch Siege tests passed and explicitly authorised merging all completed development into the tester-facing beta before the next major development area. The source merge is complete. This guide covers the separate local rollout. A GitHub merge does not restart the owner's laptop or modify its database.

## Source and data contract

- Source before promotion: beta `531017d8b978d43f6c781a73d13a86d0aec9b2d2`; accepted development `dbf6eeee35c6a9bf1f307a30ead1f865593e6c0a`.
- Beta was the development ancestor: 52 development commits ahead, zero beta-only commits. A leased fast-forward preserves the full history and requires no conflict resolution or force push. New rollout helpers are verified on development before promotion. Final merge/CI evidence belongs at the end of this guide and in the status document.
- Included: expanded foundation courses, improved 30 case-study missions, persistent progression/results, 500-question Cyber Lab, four strategy scenarios including Branch Siege, and the accepted usability work. English only; AI/languages remain deferred.
- **Beta must apply `0010_attempt_results` and `0011_strategy_learning`** from the previously accepted `0009_password_reset`. They add nullable attempt evidence and separate strategy/practice/study tables. Development already uses `0011`; do not assume beta does because development passed.
- Source alone does not publish the three foundation courses. The explicit preparation command preflights and publishes Python, Cyber Safety and Digital Citizenship in one transaction. It updates only the expected legacy/current lesson markers and appends missing questions. It refuses custom/duplicate/missing content rather than overwriting it. No broad seeding or startup publication occurs.
- Preparation creates a fresh PostgreSQL custom-format backup inside the verified local beta container, lists its archive, copies it with Docker (binary-safe in PowerShell), compares SHA-256 and retains the dump/hash under ignored `local-backups/`. This is archive/copy verification, not a fresh full recovery rehearsal.
- It fingerprints existing accounts, sessions, invitations, feedback, progress, attempts, missions, courses, lesson identity/ordering and old question rows. Only expected lesson content changes and appended questions are allowed; mismatches abort/roll back publication. Existing strategy/practice/study rows are included when already present. A hash/count manifest is retained privately without raw row contents.
- No beta data is copied into development. No account, invitation, feedback, old question key or saved result is reset. Existing testers should continue signing in with their existing accounts; do not regenerate invites merely for this release.

## 1. Stop application terminals

Allow active assessments to finish, then use **Ctrl+C** in the existing beta API, beta web and ngrok terminals, and in development API/web terminals. Leave Docker Desktop and both database containers running. Do not use `docker compose down -v`, restore a development database into beta or run the obsolete `prepare-beta-migration.ps1` / `sync-before-test.ps1` wrappers; those target earlier branches/schema revisions.

Prefer to run the next block in the existing beta API PowerShell window after Ctrl+C: its working Brevo settings can be retained. If using a fresh window, `configure-mail` asks for missing existing settings; the API key is entered without echo and no settings are printed. It saves only the three mail variables to ignored `api/.env.beta`, so future fresh terminals can restart reliably. Use the existing verified sender and current public ngrok HTTPS origin; do not paste credentials into chat.

## 2. Update and prepare beta once

The default beta checkout is the existing `University_All_In_One` under your Windows profile. Stop on any error; preserve local source edits rather than resetting them.

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
Set-Location -LiteralPath $betaRoot
$betaBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $betaBranch -ne 'feature/secure-password-recovery') {
    throw 'Open the existing beta worktree; do not switch the development worktree to beta.'
}
$betaChanges = @(git status --porcelain --untracked-files=normal)
$betaUnsafe = @($betaChanges | Where-Object {
    $_.Substring(3).Trim().Replace('\','/') -notin @('web/next-env.d.ts','web/tsconfig.tsbuildinfo')
})
if ($betaUnsafe.Count) { git status --short; throw 'Preserve and review local source changes before updating.' }
git pull --ff-only origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta update failed; do not force or reset.' }

& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-ci.lock
if ($LASTEXITCODE -ne 0) { throw 'Beta locked dependency installation failed.' }
& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Beta local helper dependencies failed.' }
& .\api\.venv\Scripts\python.exe -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Beta dependency consistency failed.' }

Push-Location .\web
try {
    npm.cmd ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'Beta frontend dependencies failed.' }
}
finally { Pop-Location }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend build failed.' }

docker compose up -d --wait postgres
if ($LASTEXITCODE -ne 0) { throw 'Beta database startup failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py configure-mail
if ($LASTEXITCODE -ne 0) { throw 'Beta recovery mail configuration failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py prepare
if ($LASTEXITCODE -ne 0) { throw 'Beta preparation stopped; keep services offline and retain the backup.' }
```

Expected final preparation message: `PROMOTION PREPARED: schema 0011_strategy_learning; all three course releases published; existing records preserved.` Retain its backup path and private dump/hash/manifest. Keep backups protected; they contain sensitive learner data. If content preflight refuses a course, no course publication commits; migrations may already have applied. Stop and resolve that condition with sanitised diagnostics. Do not delete/custom-reset records to get past the guard.

## 3. Update the existing development worktree once

This discovers the already-registered development path rather than guessing its folder name. It keeps its own virtual environment, `.env.development`, database and Git branch.

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
$devRoot = & "$betaRoot\api\.venv\Scripts\python.exe" "$betaRoot\scripts\beta.py" development-path
if ($LASTEXITCODE -ne 0 -or -not $devRoot) { throw 'Cannot identify the existing development worktree.' }
Set-Location -LiteralPath $devRoot.Trim()
if ((git branch --show-current).Trim() -ne 'feature/beta-continuous-improvement') { throw 'Wrong development branch.' }
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Development update failed; preserve local changes.' }
& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-ci.lock
if ($LASTEXITCODE -ne 0) { throw 'Development locked dependencies failed.' }
& .\api\.venv\Scripts\python.exe -m pip install -r .\api\requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Development helper dependencies failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema check failed.' }
```

Both databases were deliberately left running. If the dedicated development database is stopped, start it using its existing private Compose configuration; do not use beta's Compose file for it. No development content re-publication is needed for the already accepted setup.

## 4. Start beta terminals

**Beta API — terminal 1:**

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped.' }
```

**Beta frontend — terminal 2:**

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py web
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend stopped.' }
```

Beta now runs the built frontend via `next start`. The guarded build/start explicitly target API 8000 and exclude development overrides; the frontend child receives no database or mail credentials. Private-beta invitation/adult/student rules remain enabled. Services bind to loopback and refuse occupied ports. API startup never migrates or publishes content.

**Beta readiness — a separate check terminal:**

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
& .\api\.venv\Scripts\python.exe .\scripts\beta.py check
if ($LASTEXITCODE -ne 0) { throw 'Beta readiness failed; do not reopen the tunnel.' }
```

Open [local beta](http://127.0.0.1:3000). Sign in with an existing beta account and check the smoke pass below before reopening the tunnel.

**Ngrok — terminal 3:**

```powershell
ngrok http http://127.0.0.1:3000
```

Share/use the HTTPS origin that ngrok actually prints, not the local development URL. If it is unchanged, existing tester links to that origin continue. Testers should refresh the page and sign in normally; they should not register again. The new game is at `PUBLIC_HTTPS_ORIGIN/cyber-lab?scenario=siege` and the bank at `PUBLIC_HTTPS_ORIGIN/cyber-lab?tab=practice`.

If ngrok prints a different origin, stop **only beta API** with Ctrl+C, then update the reset-link origin and restart it in that API terminal:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $env:USERPROFILE 'University_All_In_One')
$betaPublicOrigin = Read-Host 'Paste the current ngrok HTTPS origin, without a path'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py configure-mail --public-url $betaPublicOrigin
if ($LASTEXITCODE -ne 0) { throw 'Beta public origin update failed.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped.' }
```

## 5. Start development terminals

**Development API — terminal 4:**

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
$devRoot = & "$betaRoot\api\.venv\Scripts\python.exe" "$betaRoot\scripts\beta.py" development-path
if ($LASTEXITCODE -ne 0 -or -not $devRoot) { throw 'Development worktree not found.' }
Set-Location -LiteralPath $devRoot.Trim()
& .\api\.venv\Scripts\python.exe .\scripts\development.py api
if ($LASTEXITCODE -ne 0) { throw 'Development API stopped.' }
```

**Development frontend — terminal 5:**

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
$devRoot = & "$betaRoot\api\.venv\Scripts\python.exe" "$betaRoot\scripts\beta.py" development-path
if ($LASTEXITCODE -ne 0 -or -not $devRoot) { throw 'Development worktree not found.' }
Set-Location -LiteralPath $devRoot.Trim()
& .\api\.venv\Scripts\python.exe .\scripts\development.py web
if ($LASTEXITCODE -ne 0) { throw 'Development frontend stopped.' }
```

**Development isolation — check terminal:**

```powershell
$ErrorActionPreference = 'Stop'
$betaRoot = Join-Path $env:USERPROFILE 'University_All_In_One'
$devRoot = & "$betaRoot\api\.venv\Scripts\python.exe" "$betaRoot\scripts\beta.py" development-path
if ($LASTEXITCODE -ne 0 -or -not $devRoot) { throw 'Development worktree not found.' }
Set-Location -LiteralPath $devRoot.Trim()
& .\api\.venv\Scripts\python.exe .\scripts\development.py check
if ($LASTEXITCODE -ne 0) { throw 'Development isolation check failed.' }
```

| Environment | Frontend | API | Database |
| --- | --- | --- | --- |
| Tester beta | 127.0.0.1:3000, exposed through existing ngrok | 127.0.0.1:8000 | educyber on 127.0.0.1:5433 |
| Further development | 127.0.0.1:3010, local only | 127.0.0.1:8010 | educyber_dev on 127.0.0.1:5435 |

## 6. Beta smoke pass before inviting testers back

1. Existing account sign-in/logout works and its prior enrollments, completion, attempts, missions and feedback remain. Check stored records rather than interpreting changed active course bank sizes as historical loss.
2. Open the three foundation courses: structured lessons should render, with no raw curriculum markers. Existing completions remain. Old attempt scores/totals remain; new results use the new snapshots.
3. Cyber Lab shows 500 questions and four scenarios. Start/reopen a synthetic practice session; complete a game action and reload. Try Branch Siege and its replay when convenient.
4. Open representative older case-study missions, progress/results and feedback. Check a narrow viewport and logout.
5. Test password recovery through the owner's existing beta delivery arrangement. Verify the received reset link uses the current public origin; do not publish real tokens/logs. No email is sent by preparation itself.
6. Re-run beta readiness and development isolation. Confirm from another device/network through the ngrok HTTPS origin. The tunnel exposes only beta 3000, never development 3010 or either database.

## Recovery and verification limits

Prefer a forward fix. After new schemas/content/run editions exist, source rollback alone is not a complete recovery plan. Do not downgrade migrations, delete new records, automatically restore the pre-promotion dump or copy databases between environments. Restoring an old dump can discard later tester activity. If preparation fails, keep beta offline and retain its backup; resolve the bounded failure before restart.

Functional CI and owner-reported checks are not independent educational, physical-device, operational-recovery or final formal-security clearance. Formal Cloudflare audit remains deferred. The merge is an authorised temporary-beta rollout, not a production-hosting launch. The assistant has not restarted the owner's laptop, made its backup or migrated its live database; those occur only when the owner runs the blocks above.


## Promotion-candidate verification — 29 October 2026

Candidate `8c939eef0480a28f72751040feefa76de58b0840` passed [backend/PostgreSQL run 40858554393](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40858554393): **685 tests plus 11 subtests**, including populated PostgreSQL course publication with retained learner/session/invite/feedback/mission/assessment state. Unit and dependency-audit jobs passed. [Real API/PostgreSQL browser run 40858554381](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40858554381) passed **all 14 cases**. The 147-case existing-gameplay regression and source promotion remain pending at this checkpoint. Local focused rollout checks passed 16 cases with the PostgreSQL case skipped locally; local full earlier checkpoint passed 661 tests plus 11 subtests with 22 skips. CI supersedes that earlier partial local checkpoint. No actual owner beta data, backup, migration, provider or restart was operated here.


## Completed source promotion — 29 October 2026

Verified candidate `8c939eef0480a28f72751040feefa76de58b0840` also passed [browser regression run 40858554387](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40858554387): **147 browser journeys** (15 progression plus 132 gameplay), frontend **15 unit tests**, TypeScript and production build. Together with the **685 PostgreSQL backend tests plus 11 subtests**, dependency audit and **14 actual-API/PostgreSQL browser cases** above, all promotion gates passed. This supersedes the earlier pending checkpoints.

Remote beta was then rechecked at `531017d8b978d43f6c781a73d13a86d0aec9b2d2`, development at the verified candidate, and ancestry confirmed (53 commits ahead, zero behind). The beta ref was advanced with an expected-head lease to that candidate; a subsequent read verified the promoted SHA. No force push, conflict resolution, history rewrite or merge into the legacy default branch was used. Both source branches retain their separate roles; the final documentation checkpoint is shared between them.

**Owner runtime rollout is still pending.** No laptop service, beta database, backup, migration, mail provider or tunnel was operated by the assistant. Run sections 1–6 above to make the merged source visible to testers. Then provide local readiness/isolation and beta smoke results before beginning the next major development area, whose scope remains to be chosen.
