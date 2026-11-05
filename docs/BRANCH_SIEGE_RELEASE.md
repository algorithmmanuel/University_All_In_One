# Branch Siege — consequential gameplay release

29 October 2026 (Africa/Lagos). Branch: `feature/beta-continuous-improvement`. The owner accepted Build C and instructed further work on deeper decisions, consequences and interaction. This is a gameplay iteration after Build C, not the proposed later AI/multiplayer build. No new independent learner observations were supplied; scope follows the owner's direction and source review, with educational/device validation still separate.

## Delivered experience

**Branch Siege** is a new advanced capstone in Cyber Lab, with eight assets, an active opening foothold, uncertain incident reports, an opponent that selects remaining reachable entry paths, limited staff/credits, delayed maintenance/recovery, operational dependencies and an after-action comparison. Previous scenarios remain selectable with unchanged rules. The 500-question bank and learning edition are unchanged.

Open **Cyber Lab → Scenario → Branch Siege**, or [the direct development entry](http://127.0.0.1:3010/cyber-lab?scenario=siege). The link selects the scenario; starting remains a deliberate action.

| Change | Consequence for the player | Verification |
| --- | --- | --- |
| Investigation queue | Spending staff establishes a current finding; a report can describe benign activity. Reviewed reports retain their original finding and observation turn. | Both initial findings, repeat rejection, observations and saved reopening |
| Adaptive entry | Every second turn the opponent chooses among still-reachable password, application and supplier entry paths. One closed path leaves others. | Forced remaining-path cases; deterministic replay; six opening seeds |
| Work orders | Patching, recovery verification and restoration take two turns, with explicit completion turns and unavailable service. | Delays, restored pending work after reopening, action legality |
| Service dependencies | Application/database service depends on identity, application and database being online together. Isolation/maintenance may stop more than the selected asset. | Dependency outages, threshold loss, decision ledger |
| Emergency staffing | Six credits buy two extra actions for the current turn, once per shift. Those credits cannot fund other controls. | Once-only, affordability and expiry checks; browser use |
| Controlled restoration | Isolation and a verified copy precede restoration. A separate clean validation is required before reconnection. | Failed/early reconnect rejection and full recovery journeys |
| Same-incident replay | A completed owned capstone can be restarted with the same private seed/rule edition; choices change subsequent paths. | Ownership, edition/terminal/strict-input checks, persisted comparison |
| Outcome review | Turn history, resource/service decision ledger and side-by-side prior/current metrics show tradeoffs rather than inventing a mastery score. | Desktop/mobile two-strategy wins, comparison and reopening |

This supports FB-02/FB-04/FB-05 and the current Phase 6 consequential-play loop. It does not relabel all existing 30 case studies as new strategy games or establish ThreatGEN parity. Four selectable strategy scenarios are now present, with the new capstone using a distinct eight-asset board.

## Rules and learning contract

Start with **38 credits and three staff actions**. One opening foothold is present in the workstation or broker; initial report ordering varies, so the first report is not a guaranteed culprit. Investigation costs one action. The opponent chooses from reachable open entry paths every second turn; spread uses a pre-spread snapshot and can traverse at most one graph edge per turn. Spread pressure increases at turns 6 and 10. The private seed makes matching choices reproducible, not omniscient or externally intelligent.

| Action | Credits | Staff | Duration / effect |
| --- | ---: | ---: | --- |
| Investigate asset/report | 0 | 1 | Current observation; report review is retained |
| Deploy monitoring | 4 | 1 | Observations require the asset and a functioning collector to be reachable |
| Patch | 3 | 1 | Two turns; asset offline while pending; no compromise removal |
| Isolate | 0 | 1 | Disconnect immediately; remove service and invalidate prior reconnection validation |
| Validate recovery | 0 | 1 | Record current result; affected assets fail validation |
| Reconnect | 0 | 1 | Requires a clean validation after containment and no pending work |
| Strengthen sign-in | 4 | 1 | Identity only; close the password entry path |
| Revoke supplier access | 4 | 1 | Broker only; close credential reuse, without cleaning existing compromise |
| Segment database | 5 | 1 | Restrict modeled spread while retaining approved application communication |
| Verify recovery copy | 4 | 1 | Vault only, two turns; fails if the vault is affected at completion |
| Restore asset | 4 | 1 | Isolated asset plus verified copy, two turns; validate afterwards |
| Emergency staff | 6 | 0 | Once per shift, two additional actions this turn only |

Normal non-turn actions are bounded by available staff; advancing resets staff to three. Unavailable controls explain their visible prerequisites. The broker and collector have no direct service weight, but remain important access/telemetry dependencies. Application and database contribute their service weights only when all three core dependencies (identity, application, database) are online. The collector can itself be affected, so quiet monitoring is not a clean-state guarantee; manual inspection remains possible. Observations and validations are dated records rather than secret-state meters.

Victory can occur from turn 10 through turn 18 when all compromise is cleared, password/supplier/application entry paths are closed, recovery is verified, application/database clean validations are recorded and at least 80% service is available. Lose at 100 exposure, after two turn advances below 25% service, or at turn 18 if the victory conditions remain unmet. Database compromise while online adds 20 exposure points per turn. Exposure is an explicit fictional indicator, not evidence of real-world data theft.

The briefing is specific to this capstone: the older scenarios still have their own original timings/rules. No clock advances while the learner is deciding. Animated dashed lines show configured links, not hidden attacker traffic; reduced-motion disables animation. Asset-list and keyboard controls remain available. The latest report finding can open the asset controls without spending a staff action.

## Replay, evidence and authority

Rule revision is **`branch-siege-v1`** in `api/strategy_siege.py`. Future rule changes require retaining this implementation for saved runs and pinning a new edition deliberately. The scenario catalog composes metadata without changing the old rule modules. Existing v1/v2 games keep dispatching to their original modules.

Replay is a server-owned operation on a completed run owned by the current student. The request supplies only the parent run ID and selected scenario; it cannot supply seed, budget, score, comparison data or resulting state. Replay of another student's run is hidden with 404; active runs, other editions/scenarios and invalid IDs are rejected. Parent terminal state is immutable through game commands. Each replay copies only a safe terminal metric baseline and its original private seed into the new owned run. The public active response does not expose either the seed or the private baseline; a terminal debrief shows the safe metrics.

All mutation still uses the shared ownership checks, row locks, expected versions and command UUID deduplication. Emergency staffing and signal review use the same command path, so duplicate requests do not spend or grant resources twice. Creation limits still apply to replays. IDs are strict bounded integers, unknown request fields are rejected, and there is no client achievement write endpoint. All effects are simulated: no live scanning, malware, external targets, model/provider calls or host changes.

The campaign gains a fourth freely playable chapter; existing markers and wins are not rewritten. Campaign markers remain activity guidance, not qualifications. No schema migration beyond accepted `0011_strategy_learning`, new app dependencies, publisher step, AI or languages. Existing 500 question objects/files, module editions, course/mission/assessment records and original strategy-rule files remain intact. Beta is not promoted or operated.

## Complete PowerShell update, checks and restart

Stop **only development** frontend/API with Ctrl+C. Leave beta running. Run from the existing development worktree root. Preserve local changes. The schema check below uses the existing development-only guard; it is a no-op when the accepted Build A schema is already current. No separate content publication is needed.

```powershell
$ErrorActionPreference = 'Stop'
$siegeBranch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $siegeBranch -ne 'feature/beta-continuous-improvement') {
    throw 'Open the existing development worktree first.'
}
git status --short
git pull --ff-only origin feature/beta-continuous-improvement
if ($LASTEXITCODE -ne 0) { throw 'Update failed; preserve and inspect local changes.' }

& .\api\.venv\Scripts\python.exe .\scripts\migrate_development.py
if ($LASTEXITCODE -ne 0) { throw 'Development schema verification/migration failed.' }

$siegePreviousDatabaseUrl = $env:DATABASE_URL
$siegePreviousTestUrl = $env:TEST_DATABASE_URL
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
    $env:DATABASE_URL = $siegePreviousDatabaseUrl
    $env:TEST_DATABASE_URL = $siegePreviousTestUrl
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

## One Branch Siege acceptance pass

Use a synthetic student in development.

1. Open the direct link above; confirm **Branch Siege** is selected and all older scenarios remain available. Inspect its briefing and eight-asset map, then compare the map with the asset list. Reduced motion should stop route animation.
2. Start a shift. Review the two reports, investigate and read the dated findings; one initial asset is affected. Open the relevant controls from the latest-finding panel. Verify credits/staff are unchanged by navigation. Decide whether to contain broadly or investigate and target the affected system.
3. Try emergency support and observe the six-credit cost and two extra actions. It is once-only and extra actions expire at the next turn. Close relevant entry paths, queue work and compare due turns. Isolate identity or maintain the application in a separate run to observe dependency effects; do not assume only the selected service stops.
4. Restore deliberately: isolate, verify a copy, queue restoration, advance to completion, validate and reconnect. Early or failed-validation reconnection must be unavailable. Reload mid-job and confirm due turn, resources, reports and saved state remain intact. Compare ignoring the incident with deliberate response.
5. Finish a run and inspect metrics, turn history and the resource/service ledger. Choose **Replay the same incident** and use another strategy. Check the same opening reports and a separate saved run. At its conclusion, compare recorded prior/current measures. Neither fewer actions nor fewer alerts alone should be interpreted as mastery.
6. Reload both outcomes, check another student's isolated history, resume an old scenario and verify existing learning/practice history. Check keyboard, narrow viewport, logout and error recovery. Record confusing signals, unclear dependencies or control explanations for revision.

An automated targeted strategy investigates both initial signals, contains the affected asset, schedules the application patch and closes the other reachable entry path, then completes the remaining controls, recovery and validation. A broader strategy contains both possible opening assets before recovery. Both can win under the tested openings; the broader strategy spends four additional restoration credits. These are regression examples, not a claim that they are the only good strategies. Metrics count actual decisions and service effects, including temporary within-turn outages that differ from the turn-boundary chart.

## Verification checkpoint

Local full backend checkpoint: **643 passed, 11 subtests passed, 21 PostgreSQL-dependent skips**, before the final input-bound/monitoring-isolation/legacy-replay checks. Subsequent focused checks passed all 71 cases after those fixes. An additional PostgreSQL case now exercises concurrent emergency-support deduplication. Frontend **15 unit tests**, TypeScript, production build, dependency consistency and whitespace checks passed. Previous v1/v2 rule files and all 500-question teaching/bank files were compared unchanged.

All **11 Cyber Lab actual-API/SQLite browser journeys** passed, without response interception. The two new desktop/mobile journeys each investigate, contain, recover, reopen queued work, win, replay with the same opening, win using another strategy, compare costs and reopen the comparison. The original nine journeys remain. Command-console and review screenshots were inspected. Final CI supplies PostgreSQL and Chromium browser regression coverage; those checks are pending at this checkpoint. Owner acceptance of this gameplay release remains pending.

Local and automated functional results do not establish independent learning effectiveness, complete assistive-technology coverage, physical-device performance, operational restoration or final security clearance. No beta or owner runtime/data was accessed. The formal Cloudflare audit remains deferred by owner instruction; normal secure implementation/review/tests continue.

## Recovery and next action

Prefer a forward fix. No database downgrade is required. Older source cannot continue `branch-siege-v1` runs; preserve the new module/run data and review rollback compatibility rather than deleting new records or changing a saved revision. Replay parents and safe baselines remain as saved evidence.

Next: all required automated gates passed as recorded below. Use this single complete development update/check/restart/acceptance guide. Collect independent beginner/device observations of investigation clarity, dependency tradeoffs and replay understanding. Use those observations for the next gameplay refinement; AI, multiplayer, languages, beta promotion and production readiness remain separate.


## Subsequent CI evidence — source `1de2713`, 29 October 2026

Implementation `1de2713981b477c5a26e3c7ef8f8d2ae8984d095` passed [backend/PostgreSQL run 40852352681](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40852352681): **668 tests and 11 subtests**, including actual-session concurrent emergency-support deduplication and conflicting-command checks. Unit and dependency-audit jobs passed. [Real API/PostgreSQL browser run 40852352571](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40852352571) completed successfully, including both capstone desktop/mobile same-opening replay/comparison journeys. These supersede the earlier pending PostgreSQL/actual-API checkpoint for this source. The 147-case older-gameplay regression remains pending here. Owner acceptance and independent learner/content/device/operational/final-security gates remain open.


## Launch-label follow-up — source `bc9c871`

Final review corrected the launch text to show eight assets for Branch Siege and six for the earlier scenarios. Commit `bc9c871ebb8753cb855bac9bb02141c46f5e4681` changes only that frontend display; API/rule files remain identical to the 668-test PostgreSQL checkpoint. Local TypeScript passed. [Updated real API/PostgreSQL browser run 40853151148](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40853151148) passed all 14 cases on this revision. The updated 147-case browser regression remains pending at this checkpoint.


## Final automated handover — 29 October 2026

The final frontend revision `bc9c871ebb8753cb855bac9bb02141c46f5e4681` passed [browser regression run 40853151159](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40853151159): **147 existing browser journeys** (15 progression plus 132 gameplay), **15 frontend unit tests**, TypeScript and production build. Its [actual-API/PostgreSQL browser run 40853151148](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40853151148) passed **all 14 cases**. Backend/rule source is unchanged from the **668-test plus 11-subtest PostgreSQL**, concurrent-command and dependency-audit checkpoint above. The original implementation regression also passed [run 40852352602](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40852352602). These verified results supersede all earlier pending CI checkpoints.

Use the complete blocks in this guide for one development update/check/restart, then perform its six-step acceptance pass. Open [Branch Siege](http://127.0.0.1:3010/cyber-lab?scenario=siege), or choose it in **Cyber Lab → Scenario**. Owner acceptance of this gameplay release remains pending; earlier Build C acceptance does not cover it. Independent learner/content/device/operational/final-security gates remain separate. No beta promotion or owner runtime operation was performed.
