# Phase 9.2 — Shared dual-mode mission workspace

## Delivered
All **currently playable** missions can now switch between the existing 2D investigation workstation and the existing interactive 3D investigation environment. The 3D scene is shared, dynamically labels the active mission, and uses the same evidence and tab state as the 2D workstation. No separate mission run is created when switching, and all decisions remain server-scored through the existing authenticated API.

The existing 3D room layout remains a generic security operations room. **This is a reusable dual-mode foundation, not yet a unique immersive 3D environment for every game.** The 25 planned titles are still not playable. We will add thematic rooms and mission-specific interactions incrementally, without duplicating scoring logic.

## Invariants
- Switching modes changes only the frontend renderer. No client-controlled score, award, or mission advancement.
- Shared evidence-inspection state persists across mode changes; stages still reset evidence and decision selection.
- 2D is always available, and the 3D scene loads only when requested.
- Existing backend concurrency, authentication, authorization, idempotency and mission history controls remain untouched.
- No migrations, package changes, or API contract changes in this batch.

## Acceptance checklist
1. Run locked backend tests with the isolated PostgreSQL test DB.
2. Run frontend typecheck, unit tests and production build.
3. In a fresh authenticated run, open each of the five playable games and verify that 3D can be opened and closed.
4. Inspect an artifact in 3D, switch to 2D, verify the same artifact is marked inspected, then submit through the existing decision desk.
5. Verify a completed mission cannot submit a second decision and switching modes does not duplicate points.
6. Check 2D fallback when 3D is unsupported, keyboard access and mobile performance.

Do not advertise thirty fully playable dual-mode games until all planned games are implemented and tested.
