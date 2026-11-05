# Red/Blue Stage 1 — incremental Beta rollout (4 November 2026)

## Source promotion and acceptance evidence

Owner-approved release cadence: each **completed, independently verified** Red/Blue stage is source-promoted to the existing tester Beta. Stage 1 in [PR #6](https://github.com/algorithmmanuel/University_All_In_One/pull/6) merged into `feature/secure-password-recovery` at commit `c2e4ccc283b59a1ae511db7776983df540cf7c8b`, from exact checked PR head `3e4d9dae1ce4f1b8e742a7f7ae6e230e74a8a668`.

Five required workflows were **green on the checked PR head**:
- Backend quality gate: [41817028531](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41817028531) — success including PostgreSQL integration/dependency/unit jobs.
- Frontend quality gate: [41817028547](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41817028547) — success.
- V2 contract (six scenarios, bounds, projections and isolated transition tests): [41817028364](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41817028364) — success.
- Browser gameplay regression: [41817028610](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41817028610) — success.
- Real API/PostgreSQL browser: [41817028213](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/41817028213) — **initial attempt failed, rerun success**. Initial failure was a 30-second `page.waitForResponse` timeout in *existing unrelated* Cyber Lab Build C desktop integration test (`web/tests/browser/cyber-lab-real.test.cjs`, near line 489); mobile counterpart passed. Rerun completed successfully without changing application code. Treat intermittent test timing as a follow-up stability risk; do not claim proven root cause.

## What changes, and what does not

**Tester-visible now:** Existing Red/Blue `AssetBoard` shows authorised observations grouped by selected asset, an observed-event count in both network/list cards, and up to eight recent visible messages. It reads **only existing participant-filtered observations**. Actual network rules, original simultaneous sealed turns, original win conditions, resources, authentication, invitations, saved matches and all non-Red/Blue features remain unchanged.

**Scaffolding not yet wired to gameplay:** V2 `v2_state.py`, `v2_validation.py`, `v2_scenario.py`, `v2_events.py` and their tests. The V2 pure event simulations demonstrate controlled evidence projection, but production HTTP routes still use the existing engine. They are not proof of live alternating multiplayer. This release does not yet provide the 90-second timer, Blue-opening alternating turns, disconnection grace, new topology layout, learning/realistic modes or the new debrief. Future build-phase network/tool construction remains **unapproved for implementation**.

**Database and operations:** PR #6 changed no Alembic migration, no existing database schema, no content manuscript, no learner records and no private runtime secrets. No schema update or `beta.py courses` publication is required **for this Stage 1 release**. Existing 24-course publication on a particular laptop remains a separate historical task; do not assume it is complete based on source alone. This GitHub merge did **not** run commands on the owner's laptop or change Docker volumes, PostgreSQL, ngrok, or running API/web services. Keep current beta data and tester accounts. If there are uncommitted changes, stop and review; never reset/clean.

## Owner laptop rollout (Windows PowerShell)

Use the **existing beta root** (`feature/secure-password-recovery`) and stop only **beta frontend and beta API** terminals first with Ctrl+C; keep PostgreSQL, ngrok and independent development running. Do not use this code block from the development worktree.

**Terminal 1 — guarded source update and frontend build:**

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Use the beta checkout.' }
if (@(git status --porcelain).Count -ne 0) {
    git status --short
    throw 'Preserve and inspect local changes; do not reset or clean.'
}
git fetch origin feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta fetch failed.' }
git merge --ff-only origin/feature/secure-password-recovery
if ($LASTEXITCODE -ne 0) { throw 'Beta fast-forward failed; preserve local changes.' }
$betaPython = Join-Path (Get-Location) 'api\.venv\Scripts\python.exe'
if (-not (Test-Path $betaPython)) { throw 'Existing beta Python not found.' }
& $betaPython .\scripts\beta.py build
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend build failed; do not restart updated UI.' }
Write-Host 'Stage 1 beta source/build complete; start both services using separate terminals.'
```

**Terminal 2 — beta API, from same beta root:**

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Wrong checkout.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py api
if ($LASTEXITCODE -ne 0) { throw 'Beta API stopped or failed.' }
```

**Terminal 3 — beta web, from same beta root:**

```powershell
$ErrorActionPreference = 'Stop'
if ((git branch --show-current).Trim() -ne 'feature/secure-password-recovery') { throw 'Wrong checkout.' }
& .\api\.venv\Scripts\python.exe .\scripts\beta.py web
if ($LASTEXITCODE -ne 0) { throw 'Beta frontend stopped or failed.' }
```

**Terminal 4 — readiness, from beta root after both services are running:**

```powershell
$ErrorActionPreference = 'Stop'
& .\api\.venv\Scripts\python.exe .\scripts\beta.py check
if ($LASTEXITCODE -ne 0) { throw 'Beta readiness failed; investigate without resetting data.' }
Start-Process 'http://127.0.0.1:3000/red-blue'
```

Ngrok must still point to the existing Beta frontend port 3000. Avoid exposing development port 3010. No database migration or content publisher should be run solely for this release.

## Owner acceptance

1. As Blue, open a saved or new Red/Blue match, select several assets on network and asset-list views and confirm each displays only permitted alert/finding/own-action messages with correct per-asset counts. Assets without evidence should say they have no *observed* activity, not claim they are safe.
2. As Red, confirm its own known assets and action observations are shown, while Blue private investigations and controls do not leak.
3. Use two separate authenticated browser sessions, commit both sides in the existing sealed-round sequence, and verify evidence and counts update after resolution. Refresh and reopen match; confirm saved state remains.
4. Verify a completed match's old debrief, existing games/courses/assessments, user login/logout, password recovery and tutor-facing private beta are unchanged.
5. Confirm public ngrok and local beta show matching UI, then collect new tester comments. Do not mark local rollout or owner acceptance done without the actual owner's results.

## Follow-up / remaining work

- Monitor recurring flakiness of Cyber Lab Build C desktop response-wait test; rerun alone if it recurs and investigate event timing before changing application behaviour.
- **Next development stage:** V2 true server-authoritative per-action event integration + visibility update after every alternating action. Keep old match editions replayable, add live two-seat API/PostgreSQL/browser checks, then integrate 90-second server clock and one 30-second disconnect grace with bounded durable expiry.
- Record next development vs beta source commits, exact CI evidence and local deployment separately in `docs/DEVELOPMENT_STATUS.md`.
