# Red/Blue B2 — server-clock groundwork and release blockers

**Status:** Development only; NOT merged to Beta, NOT connected to authenticated routes, no worker or production timer yet.  
**Owner-approved rules:** human actions have **90 seconds**, Blue opens, one **30-second** grace per human seat per match when server-observed liveness indicates a likely disconnection; timeout produces an authoritative no-cost wait/pass; bots act server-side without browser polling. The original sealed-match engine and historical saved transcripts remain unchanged.

## Source commits and deterministic tests

- `api/cyber_warfare/v2_clock.py` (`e632a50`, hardening `2b8faac`): bounded immutable clock with 90-second deadline, 15-second stale-presence threshold, active-seat-only authenticated heartbeat interface and once-per-human-seat 30-second extension. Late action/heartbeat cannot revive an expired deadline. Clock projection hides timestamps describing individual player check-ins.
- `api/cyber_warfare/test_v2_clock.py` (`18fff50`): eight server-time simulations for boundary times, unverified disconnect claims, grace once per seat, bot exclusion, stale presence and worker delay; no real sleeps, no dependence on user device clock.
- `api/cyber_warfare/v2_timed.py` (`d28e52d`): pure wrapper for active V2 matches. Checked actions resolve immediately before server deadline; expired turns result in a trusted `wait_blue` or `wait_red` committed as a deterministic server timeout, with next turn opening immediately. Server clock state has no browser-time dependency.
- `api/cyber_warfare/test_v2_timed.py` (`5eb7411`): eight time-advance tests, replay safety, deadline protection and grace/timeout no-duplicate transitions.
- `.github/workflows/red-blue-v2-contract.yml` (`89b6fc3`): contract CI includes both clock and timed-match tests plus syntax checks.

## Security and release blockers

1. **Absence of heartbeat is not proof of a transport disconnect.** This is a *server-observed inactivity heuristic* used to gate an optional grace. A final reconnect design must explicitly define authenticated heartbeat cadence, multiple simultaneous devices, revoked sessions, stale browser tabs, last-seen consistency and whether a *true* server-side socket disconnection is necessary. Never accept a caller-supplied `disconnected=true` or browser timestamp as authority.
2. **Persist clock and last-seen data transactionally** with the exact edition-tagged match, in a schema/migration that is reviewed separately. Current pure clock is not durable across restarts. Clock must survive browser closes, server restarts, races and multi-worker scheduling. Do not append untrusted timing fields to old replay envelopes or reinterpret old V1 records.
3. **Build an independent server worker** that scans due active V2 deadlines under PostgreSQL row lock / CAS and commits timeout moves without browser polling; handle bot turns without client intervention and ensure background tasks cannot reveal private match truth.
4. **Prove concurrent action versus timeout boundaries** at 89/90/120 seconds; consume grace only once, use actor-scoped idempotent receipts and keep original replay deterministic and verifiable. Ensure no action submitted after its deadline can win a race against a background pass. Test one delayed worker invocation, restart recovery, and simultaneous duplicated workers.
5. Expose a server-owned `deadline_at` to seat view, display an accessible countdown in Development, prevent browser clocks from granting extra time, and test as two separate authenticated real browser sessions.
6. Complete all existing backend/frontend/real-API/browser gameplay/V2 security CI on the exact PR head, preserve learner data, and promote each completed user-testable stage to Beta. The current source modules alone must **not** activate a premature timer or change existing Beta gameplay.

## Environment configuration

All owner restart commands must follow [ENVIRONMENT_AWARE_RESTART.md](ENVIRONMENT_AWARE_RESTART.md): Beta root `.env` and `api/.env.beta`, API/web 8000/3000; Development `api/.env.development`, API/web 8010/3010. Leave PostgreSQL volumes, learner records, courses, mail keys, ngrok and running Beta untouched until verified. Do not copy credentials between checkouts or kill unrelated Uvicorn processes.

## Evidence

First check exact CI on the stage branch/PR and record runs in [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md). The owner has confirmed earlier Beta tests passed, but has NOT yet tested any B2 timer implementation. No Beta rollout for B2.
