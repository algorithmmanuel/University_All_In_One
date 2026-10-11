# Phase 9 — Platform expansion plan

Starting baseline: Phase 8 merge commit `226ac2292e286287425a767e07333d93c9afe423` on `feature/phase-7-cyber-platform`.
Development branch: `feature/phase-9-platform-expansion`.

## Non-negotiable engineering rules
- Preserve the working Phase 7.15 SOC 2D/3D experience, authentication, enrollment, quiz and scoring contracts.
- Keep changes modular, reviewed and covered by automated tests. Preserve Python 3.13 backend dependency locking and the npm lockfile.
- Run integration tests only against isolated `educyber_test`; do not alter the developer's application database or local uncommitted files.
- No production deployment or public launch until operational, privacy and child-safety gates are met.

## Proposed delivery sequence
1. **P9.1 Baseline acceptance:** local checkout, backend tests, frontend typecheck/tests/build, and a manual 2D/3D SOC smoke test. Record the baseline without committing generated files.
2. **P9.2 Learner progression:** mission completion history, achievements and learner dashboard; enforce per-user authorization and idempotent award logic.
3. **P9.3 Instructor capabilities:** role-scoped progress overview, assignment and feedback workflows; enforce least privilege and privacy boundaries.
4. **P9.4 Immersive gameplay:** expand scenario content and UX while keeping existing 2D/3D SOC mechanics stable and accessible.
5. **P9.5 Browser E2E:** automate login, enrollment, mission navigation, and 2D/3D switch regression with test data isolation.

## Acceptance for each batch
- Document the user-visible behavior and API/data changes.
- Add adversarial tests for authorization and scoring integrity when applicable.
- Pass backend and frontend CI on the feature branch and run the agreed local checks.
- Do not merge Phase 9 until the developer approves its acceptance review.

## Initial local synchronization
From the project root, stash local frontend modifications and untracked build artifacts with `git stash push -u`, fetch origin, switch to the new feature branch, and restore the stash. If the stash restore conflicts, stop and resolve without discarding work. Keep `web/tsconfig.tsbuildinfo` out of commits.
