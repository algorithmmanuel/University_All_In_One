# Build A — Operation Firewall: Branch Defender

28 October 2026 (Africa/Lagos). First playable strategy foundation under the [approved direction](PHASE_6_GAMEPLAY_PLAN.md). Development branch: `feature/beta-continuous-improvement`. Keep the tester-facing beta running separately.

## Delivered scope

- New `/cyber-lab` with Play, Learn and Practise, linked from home, dashboard and My learning.
- Original top-down six-asset strategy scenario: three staff actions per turn, 30 credits, simulated stolen-password/application entry, seeded spread, hidden compromise, monitoring/investigation, patching, isolation/reconnection, database segmentation, verified recovery and restoration. Turn-dependent effects and availability/exposure tradeoffs produce explicit win/loss outcomes and a saved timeline/debrief.
- Server-owned, version-pinned runs and UUID command deduplication; stale/conflicting commands are refused. Reopening and history pagination are owned-user scoped. No change to existing three-stage missions or their scoring/history.
- Three original English supporting modules: Protect the branch; Defend connected services; Respond, recover and assure. Ten topic sections include objectives, substantive explanations, 100 worked decisions, game applications, optional NIST/OWASP/MITRE public references and saved module completion. This is a new Cyber Lab curriculum; the three accepted foundations courses remain available unchanged. Module completion is a learner-marked reading record, not mastery.
- **100 new cybersecurity practice questions**, ten per topic family, separate from the existing course banks and 150 mission reviews. Topic/difficulty/count selection, fresh/least-recent selection, mixed-topic balancing, shuffled options, server-pinned private snapshots, grading/explanations, source/module references and saved results/history. Sessions contain 1–20 questions. In-progress answer choices are page-local; selected questions persist. Submitted results and original answer explanations persist.
- Rules-based opponent, English only. No AI/model integration, Nigerian-language additions, multiplayer, live-target operations, new app dependencies or content-publisher command.

This is one beginner strategy scenario with a shared map and programmed rules, not ThreatGEN feature parity or a completed multi-scenario campaign. The first entry events occur at turns 2 and 4; seeded spread depends on the state and controls. Protecting the relevant entry paths early is intentionally a valid beginner strategy. More scenarios/difficulty, richer presentation/audio and extensive independent educational testing remain future work. No 10–20-minute session length or hardware frame-rate target is claimed as measured.

## Data and implementation contract

Migration **`0011_strategy_learning`** adds four tables: strategy runs, deduplicated commands, pinned practice sessions/results and versioned study completion. Existing tables/rows are not rewritten. The guarded development migrator still refuses occupied development ports and selects only the dedicated development configuration; normal service startup never migrates automatically. New lessons/questions are versioned source data, not modifications to old course rows.

The browser submits only an action, asset, expected state version and command UUID. Row locks serialize a run's changes on PostgreSQL; a repeated UUID cannot spend resources twice. Only allowlisted public state is exposed during play; seed and compromise flags remain private until the scoped debrief. Investigation observations expire on the next turn unless monitoring is installed. The attacker advances one graph hop per turn from a pre-spread snapshot. Patching reduces this model's exploit/spread paths but does not remove existing compromise. A restore clears compromise on the next turn and leaves the asset isolated.

Practice grading uses the session's stored questions/options/keys, not a freshly sampled bank. Keys and explanations are withheld from the active practice response; feedback becomes available after submission. Retries return the saved result; different resubmissions cannot overwrite it. Practice/source revisions remain part of snapshots. New activity creation is bounded to 100 per user per type in 24 hours, serialized through the user row. These application bounds supplement, not replace, the existing production operational/edge-rate-limit work.

## Complete PowerShell update and checks

Stop **only development** API/frontend with Ctrl+C. Run from the existing development worktree root. Preserve local changes; do not reset them. This build needs the additive development migration before restart. Retain an appropriate development backup under your existing local procedures before applying schema changes. No beta commands or credentials are needed.

```powershell
$ErrorActionPreference = 'Stop'
$buildABranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $buildABranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema verification/migration failed.' }

$buildAPreviousDatabaseUrl = $env:DATABASE_URL
$buildAPreviousTestUrl = $env:TEST_DATABASE_URL
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
    $env:DATABASE_URL = $buildAPreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $buildAPreviousTestUrl
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

## Development acceptance

After update/checks, start and verify the separate services using the full blocks above. Open the development frontend and sign in with a synthetic adult student account.

1. Use dashboard **Play Branch Defender**, or open `/cyber-lab`. Start a shift, select assets and verify budget/staff/service changes. In one run protect sign-in, patch the application and verify recovery before advancing. Check delayed effects, progress through turn 8 and inspect the debrief. In another run investigate/monitor and allow an entry event; compare spread, isolation/service cost and recovery. Record whether the choices and consequences are understandable without developer coaching.
2. Reload mid-shift, reopen the same saved shift and confirm state/credits/timeline. Completed shifts reopen their own debrief. Try a stale second tab on development; it must refuse a conflicting action and allow reloading current state. For a network failure, retry the same command or reload the saved run before choosing another action.
3. Read all three learning modules, expand worked decisions, open optional public references and mark a module complete. Reload and confirm that completion belongs to this student. Check the game applications and that the assessed concepts are actually explained; report factual ambiguity or confusing distractors for editorial correction.
4. Start mixed and focused practice at valid sizes, vary difficulty, submit answers and inspect explanations/module links. Reopen a result after reload. Start another session and check fresh selection; repetition is expected once that eligible pool is exhausted. Incomplete choices reset on page reload, but the selected questions remain saved.
5. Check keyboard focus, reduced-motion setting, desktop and a narrow viewport. The network panel pans horizontally on small screens; asset controls remain ordinary buttons. Check map/legend readability and that the page itself does not overflow. No WebGL is required for this mode.
6. Recheck existing course enrolment/completion/assessment, a saved legacy mission and logout. Keep independent beginners, physical devices/performance, accessibility and final operational/security assurance as separate open evidence gates. Report sanitised diagnostics only.

## Verification and limits

Local assistant checks at implementation checkpoint: 595 backend tests plus 11 subtests passed, 21 PostgreSQL-dependent cases skipped; 21 focused new rules/HTTP/migration cases passed. Frontend 15 unit tests, TypeScript and production build passed; dependency consistency (`pip check`) passed. Existing TestClient deprecation and global CSS alignment warnings remain. The populated old-schema SQLite migration test preserves historic mission rows and checks new-table downgrade separately.

Both new desktop/mobile browser journeys passed against real FastAPI and a disposable SQLite database with a real synthetic bearer session (no intercepted API responses). They cover game actions/delayed effects, save/reload, a winning debrief, module completion, practice submission and result reopening; screenshots were inspected. Earlier connection/setup and test-locator failures were corrected and are superseded by the passing runs. This establishes those bounded journeys; SQLite does not establish PostgreSQL row locking. New guarded PostgreSQL real-session/duplicate/conflicting-command tests and both browser journeys are included in CI. CI, the existing 147-case browser regression and owner local acceptance remain pending at this drafting checkpoint.

Content is original source-authored material with structural/coverage checks and factual review during implementation. No independent educator/content review, measured learning gain, representative-device performance benchmark or security clearance is claimed. The 100-question milestone does not complete the proposed 500-question bank.

## Recovery and next action

Prefer a forward fix while retaining new run/practice data. Do not run Alembic downgrade as routine recovery: dropping the four tables loses new strategy/practice/study records. Preserve source and backup state before any recovery decision. Earlier foundation course/question rows, scores, progress and legacy mission histories were not changed by this build.

Next: use this single guide for development migration/update/restart and local acceptance; all automated CI gates passed as recorded below. Tune the first game using learner feedback before expanding to more scenario variants and 250/500 questions. Keep beta separate and the final formal audit deferred under the recorded owner direction.


## Final automated gates — source `718dc9b`, 28 October 2026

All three CI workflows passed for implementation `718dc9b5fc795dd50cb4a6e5ab4ba3227f550212`:

| Gate | Observed result | Evidence |
| --- | --- | --- |
| Backend/PostgreSQL | 616 tests and 11 subtests passed; unit/dependency jobs passed too | [Backend run 40739042384](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40739042384) |
| Existing browser regressions | 15 progression + 132 existing gameplay/learning cases passed (147 total); frontend 15 unit tests, typecheck and production build passed | [Browser run 40739042859](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40739042859) |
| Actual API/PostgreSQL browser | All five cases passed, including new desktop/mobile Branch Defender → saved run/debrief → learning completion → saved practice/result journeys, plus the three existing cases | [Real API run 40739042498](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40739042498) |

The PostgreSQL gate includes real bearer-session ownership/revocation and concurrent duplicate/conflicting-command tests; it verifies those specific boundaries rather than all possible concurrency schedules. The 147 existing cases also passed locally using the supported headless shell. Full Chromium's local process-singleton socket remained denied, so the local harness selected headless shell without changing test assertions; normal CI Chromium passed independently. These results supersede the earlier pending and interrupted local-browser checkpoints.

The final evidence update changes documentation only. **Owner development installation and local acceptance are still pending.** No beta source/service/database, owner runtime or external mail/model provider was accessed. Independent content/learner/physical-device/accessibility/performance, operational recovery and final formal security gates remain open.

**Immediate next action:** stop only development services, follow the complete update/migration/check/restart blocks above, verify isolation, then complete the single acceptance checklist at `/cyber-lab`. No separate content publication is required.


## Dashboard navigation correction — 28 October 2026

The original dashboard card was mistakenly rendered only in the dashboard error view. The correction puts **Play Branch Defender →** on the normal student dashboard, above **Your saved progress**, and adds **Cyber Lab** to its top navigation. The direct destination remains `/cyber-lab`. Update using the complete existing blocks above; no additional schema change is needed beyond `0011_strategy_learning`.

Seven focused local browser cases passed after this correction (desktop/mobile dashboard discovery and both actual-API/SQLite game/practice journeys included); production build/type validation passed. Real-API CI now starts the new game journeys by clicking the dashboard link. Correction CI is pending at this checkpoint; this note does not replace the original Build A CI results or infer owner installation.
