# Red/Blue Stage 2 — responsive active-match refresh

**Status:** development release candidate; requires GitHub CI, PR approval/merge and owner Beta rollout before calling deployed.  
**Owner direction:** each completed verified stage goes to the existing Beta; preserve all users and databases. Environment-aware restarts are mandatory: see [ENVIRONMENT_AWARE_RESTART.md](ENVIRONMENT_AWARE_RESTART.md).

## What this stage changes

- `web/app/red-blue/useArena.ts`: continue read-only polling every three seconds whenever an open match is **active**, even when this participant has not submitted an order. Formerly only a waiting match or a seat with a committed order was polled. An opponent could join/finish an action without the non-committed viewer receiving a refresh until reload.
- Preserve existing generation-ticket checks, in-flight request guards, visible-tab-only GETs, monotonic version checks, auth/session independence and no change to keyboard focus. Only authorised response projection from the existing API is used; no client mutation or more detailed opponent intelligence.
- `web/tests/browser/red-blue-real.test.cjs`: in an actual two-account, PostgreSQL-backed match, verify the active uncommitted Blue seat continues to issue GET updates while Red commits. Assert Blue receives no Red sealed order, observations or asset changes before resolution. The original two-seat flow continues through a resolved round.
- `docs/ENVIRONMENT_AWARE_RESTART.md`: explain fixed Beta vs Development env source files, ports, generated `next-env.d.ts` stashing, safe process ownership and local update/restart/readiness. The launchers already isolate their env files; **their behaviour is unchanged**.

## Important limitation

This is a bounded responsiveness stage in the **legacy sealed-round edition**. The UI receives already-authorised state sooner and the following resolved round updates become visible without an explicit refresh. It does **not** implement per-action alternating turns, the 90-second server clock, the 30-second reconnect grace, new V2 route integration or player-built networks. These remain tracked in [RED_BLUE_V2_REDESIGN.md](RED_BLUE_V2_REDESIGN.md). Do not report the turn model as delivered.

## Release and security gate

1. CI green for new authenticated two-seat actual-API/PostgreSQL assertion, existing Red/Blue browser gameplay, frontend type/build/unit, backend and V2 contract.
2. Verify no changes to API rules, engine digests, old replays, persisted learner data, schema or migration; current `api/.env.beta`, root `.env` and development `api/.env.development` remain private and untouched.
3. Merge the exact checked development commit to Beta using reviewed PR; record merge commit and final CI runs. Do not take an unchecked direct branch shortcut.
4. Owner safely updates existing Beta checkout and build, then restarts only the Beta API 8000 and web 3000 through `scripts/beta.py`; preflight verifies existing processes first. **No courses publisher or DB migration** for this stage.
5. Run `beta.py check`, verify public ngrok targets Beta frontend **3000**, test with two distinct users across desktop/mobile, and record user feedback. Continue dev only after preserving this handover.

## Owner acceptance

- Blue opens a human match, invites Red; joining becomes visible without refreshing.
- During an active match, neither participant needs a manual reload to see legal visible updates after the other participant finishes. A hidden sealed order remains hidden until resolution.
- Asset-specific observation counts update after both sides' orders resolve.
- Logout in one session does not log out the other; previous completed matches remain replayable.
- Check launcher's private beta mail origin and password reset (without printing tokens), restored data and existing courses.

## Release evidence

**Pending**: exact CI commit/runs; Beta PR/merge; laptop rollout; public test and feedback. Update these fields only after obtaining direct evidence.
