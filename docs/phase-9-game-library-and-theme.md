# Phase 9.1 — Dark theme and game-library expansion

## Delivered
- Shared dark cybersecurity theme with accessible contrast-oriented colors and visible keyboard focus. Existing SOC workspace CSS modules and game logic are unchanged.
- Version 2 of `GET /api/v1/games` contains **exactly ten discoverable games per pathway** (30 entries total).
- The five existing playable games keep their IDs and mission mappings. The other **25 entries are explicitly marked `planned`** with no mission IDs; the UI labels them coming soon. This is a library roadmap, **not a claim of thirty playable simulations**.
- Backend catalogue tests enforce unique IDs, ten entries per pathway, honest availability, and correct mission/pathway mappings.
- GitHub backend and frontend quality gates now run on Phase 9 pushes, including locked dependencies and PostgreSQL integration.

## Security and architecture guardrails
- Planned games cannot start because they have no mission IDs. Existing mission authorization, scoring and concurrency protections remain server-side.
- Do not create placeholder mission mappings, expose scoring answers or weaken the learner access checks to fill catalogue counts.
- New playable games should be added incrementally as fictional defensive scenarios, each with three or more evidence-based stages, validated manifests, adversarial tests and user experience review.
- No new database tables, migrations, authentication flows or production services in this batch.
- For the next batch, add browser smoke tests for the dark theme and game-library status labels, and review mobile contrast and keyboard behavior.

## Verification
Pending latest Phase 9 CI and developer local build. From the project root, preserve local frontend edits before switching branches. Run `python -m pytest -q` in `api` with `DATABASE_URL=TEST_DATABASE_URL`, then `npm run typecheck`, `npm test`, and `npm run build` in `web`. Do not test against the development or production database.

## Next development batch
Convert planned titles into real playable scenarios in small tested groups, beginning with secondary learner digital safety and university network defense. Each published mission must have accurate age-appropriate content, meaningful feedback and server-owned grading.
