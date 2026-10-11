# Phase 8 — Engineering acceptance and release-gate decision

Review date: 2026-10-11. PR #1: `feature/phase-8-engineering-hardening` → `feature/phase-7-cyber-platform`.

## Evidence verified at review
- GitHub PR #1 is open, draft, mergeable, with no merge conflicts at the reviewed SHA `97df31f`. 44 files changed; most added lines are dependency lockfile and test code.
- Developer reported **70 passed, 1 known deprecation warning**, `pip check` clean, using the isolated PostgreSQL test database.
- Backend GitHub Actions (unit, PostgreSQL integration, dependency audit) and frontend GitHub Actions (locked npm install, TypeScript, Node regression tests, Next.js build) succeeded at `97df31f`.
- Developer manually verified that the 2D/3D SOC switch remains available on an active Operation Firewall attempt. The homepage's outdated 3D-unavailable message was corrected after this review; its new commit requires frontend CI confirmation.

## Merge acceptance gates (Phase 8 → Phase 7.15)
| Gate | Decision | Evidence / caveat |
| --- | --- | --- |
| Backend regression, authorization and concurrent scoring | Pass | 70 local tests, PostgreSQL CI success |
| Frontend typecheck, tests and production build | Pass at reviewed SHA | Locked npm CI and developer build; rerun CI for homepage copy update |
| Dependency reproducibility | Partial | npm lockfile committed and `npm ci` verified; Python requirements remain version ranges |
| Database migrations and compatibility | Pass in CI | Alembic upgrade head with isolated PostgreSQL |
| Gameplay preservation | Pass for manually checked SOC path | 2D/3D switch confirmed; not a comprehensive browser E2E suite |
| Deployment safeguards | Prepared, not deployed | Production configuration validator and 15 tests; infrastructure controls not implemented |
| Pull request state | Not yet merged | Keep draft until final CI and owner approval |

## Before merge
1. Confirm CI on latest Phase 8 SHA and review PR diff for unrelated changes and secrets.
2. Decide whether Python constraints/lockfile reproducibility is required for this merge or tracked as a follow-on engineering issue; do not claim fully reproducible backend dependencies meanwhile.
3. Confirm the target branch is the intended Phase 7.15 baseline. Preserve the branch and tags as rollback points.
4. Review GitHub PR #1 and obtain repository-owner approval. Do not auto-merge from an acceptance note.
5. Optional but recommended: add a small browser E2E smoke suite for authentication, course access and 2D/3D SOC navigation.

## Public-launch blockers (not necessarily blockers for an internal engineering merge)
- Child privacy and safeguarding: age-specific UX, appropriate consent, lawful basis, deletion and retention, access rights, safeguarding escalation.
- Edge abuse prevention: IP/bot quotas and account recovery/DoS assessment; existing per-email buckets are insufficient for internet-scale abuse.
- Hosting/TLS/secrets and least-privilege production DB; backup restore drill, monitored scheduled cleanup, alerting, disaster recovery and incident response.
- Security verification: threat model, dependency review, secret scan, penetration test, browser accessibility and Android security review, load/capacity testing.
- Restrict `/health/db` at ingress; review quiz answer disclosure for graded assessments.

## Decision
**Engineering merge candidate, not public-launch ready.** Do not merge automatically. The final commit's checks and owner review are outstanding at time of writing. Deployment costs and public hosting are not prerequisites for an internal branch merge.

## Dependency lock follow-up
Python 3.13 lock inputs and generation instructions have been added in `api/requirements-ci.in`, `api/lock-requirements.sh` and `docs/phase-8-python-dependencies.md`. **The resolved lockfile has not been generated or committed yet.** This is a merge gate. After it is committed, update backend CI to install the lockfile and verify PostgreSQL integration, dependency audit and the complete frontend gate. Keep PR #1 in draft until then.
