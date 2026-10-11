# Phase 9.3 — Cyber Explorers dual-mode expansion

## Scope
Ten secondary-school Cyber Explorers games are now mapped to real server-scored missions. Eight new games each contain three fictional stages, evidence, three response options, feedback, and a server-owned best-evidence finding key. Together with Scholarship Detective and Password Fortress, this makes ten playable Explorer games; the university and professional pathways still contain three playable games and seventeen planned titles.

## Dual-mode presentation
The eight new games now open purpose-labelled 2D evidence simulators with inspectable case artifacts. The 3D scene reuses the existing procedural investigation room and assigns a themed HUD label and accent color per game. These are **shared environments**, not eight custom-built 3D worlds. Scoring and run state remain on the server, not in either renderer.

## Security and data integrity
- Never send option points, finding keys or feedback to the client before a decision.
- Maintain row-locked server scoring, per-user run ownership and stage concurrency guards.
- Mode changes only affect rendering; there is no score-changing mode endpoint.
- The read-only `/health/schema` endpoint checks whether expected tables exist without applying schema changes. Schema migrations and startup/deployment gating remain follow-up work.

## Local acceptance
1. Pull the Phase 9 branch and run backend tests against the **isolated test PostgreSQL database**.
2. Run `npm run typecheck`, `npm test`, `npm run build` in `web`.
3. Restart FastAPI with the development `DATABASE_URL`, and keep Next.js running.
4. Confirm `/health/schema` returns `{"schema":"ready"}`.
5. Log in as a student and verify ten Cyber Explorers cards say playable.
6. Open each new game. Inspect artifacts in 2D, switch to 3D, inspect another artifact, and verify the shared inspected count persists.
7. Complete a mission and confirm score is at most 45, history is updated, and stale/repeated submissions cannot award additional points.
8. Confirm all seventeen unimplemented university/professional titles still say coming soon.

CI runs may lag behind commits. Do not treat unverified local interactions as passed acceptance tests.
