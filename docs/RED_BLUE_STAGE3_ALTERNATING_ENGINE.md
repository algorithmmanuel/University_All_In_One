# Red/Blue B1 — Versioned alternating engine checkpoint

**Date:** 4 November 2026. **Development:** `feature/beta-continuous-improvement`. **Beta:** `feature/secure-password-recovery`.  
**Status:** isolated alternating **domain** engine implemented; not integrated into HTTP/DB/browser and not deployed.  
**Scope:** new Blue-first alternating rules edition; 90-second server deadline and one-time 30-second disconnect grace to be implemented as B2, not in this checkpoint. Old sealed rounds/replays must remain unchanged.

## Code and decisions

- `api/cyber_warfare/v2_alternating.py` (initial commit `ad5ca1a`): new `red-blue-alternating-v2-1` domain edition wraps the existing battle-resolver's private scenario/effects. A new match starts with Blue; only the active side can submit a legal order; Blue immediately resolves the defensive effect, Red then sees its own authorised projection; Red action resolves and closes one complete Blue+Red round. Enemy action details remain hidden through existing seat-specific `engine.view` projection. Each action increments version; actor-scoped UUID/command IDs return unchanged state on identical replay and reject repurposing.
- Private edition-tagged canonical event-sourced replay saves seat IDs, seed, scenario digest and ordered individual commands, fully reconstructed by the V2 engine. Historic v1 replay envelope is still handled by the **unchanged** original engine, not reinterpreted. V2 rule digest and edition pin compatibility.
- `api/cyber_warfare/test_v2_alternating.py` (commit `e77ac30`): tests Blue first, immediate state effects, hidden orders, idempotency, deterministic replay and tamper detection, completion across six scenarios, legacy sealed-order/replay compatibility and outsider denial.
- `.github/workflows/red-blue-v2-contract.yml` (commit `626e64c`): adds V2 alternating tests and syntax compilation.
- All new code is **not imported into the existing Red/Blue FastAPI route**, so current Beta gameplay, auth, match rows, records, lessons and scenarios are unaffected.

## Before B1 can count as a *tester-visible completed milestone*

1. Verify dedicated V2 contract CI; fix any failures, rerun on exact final PR head.
2. Create edition-selective authenticated HTTP start/resume/command/replay integration and DB transaction/persistence; protect seats and idempotent receipts under real PostgreSQL concurrency and retain old unfinished/finished saved matches. Do not accidentally change current match default before full V2 support.
3. Offer new engine edition only for **new** matches and show each side's true active turn in UI. Both human and bot games, current role limits, commands and debrief need explicit alternate-edition semantics; provide tests with two distinct authenticated accounts and client UI.
4. Decide and verify objective checks when Red finishes each full round versus irreversible immediate effects. Check difficulty and fairness for Blue-first on all six scenarios, and preserve budgets and deterministic roll streams.
5. B2 separately adds server-owned 90-second deadline, durable expiry processing, one 30-second presence-based grace per seat, and bot deadline policy. Do not ship unbounded, untimed competitive V2 matches as if timer existed.
6. Stage a complete, useful, secure Beta-visible release and pass frontend/backend, V2, browser, real API/PostgreSQL integration gates; provide environment-aware owner Beta rollout. If not ready, keep draft PR and development branch only.

## Operational configuration policy

Use [environment-aware restart](ENVIRONMENT_AWARE_RESTART.md). **Beta** launcher reads root `.env` for `POSTGRES_PASSWORD`, `api/.env.beta` for mail and current `EDUCYBER_PUBLIC_WEB_URL`, API 8000/web 3000; **Development** launcher reads `api/.env.development`, API 8010/web 3010. Never copy the private env files between checkouts, force-stop all Python processes or apply a migration without a separate reviewed/backup step. Keep the two working trees and databases separate.

## Current acceptance and evidence

Initial code and test commits are named above; **GitHub CI status and any live Beta promotion must be recorded from observed workflow results, not inferred.** The owner reported Stage 2 tests passed locally. This does not establish B1 verification. Next action: inspect workflow run, fix failures, then implement authenticated edition-specific rules before Beta-facing release.
