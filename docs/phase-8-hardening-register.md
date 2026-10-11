# Phase 8 — Engineering hardening register

Baseline: `feature/phase-7-cyber-platform`. Working branch: `feature/phase-8-engineering-hardening`.

## Engineering rules
- OWASP Top 10 and API Security Top 10 controls are required where applicable.
- Preserve current API contracts, database records, and Android app.
- Favor modular monolith, stateless API, PostgreSQL migrations, and portable configuration.
- Add tests before changing security-sensitive behavior. Comments explain rationale and invariants, not obvious syntax.
- Do not merge until local regression, security, and concurrency checks pass.

## Findings and verification plan

| ID | Priority | Finding | Action | Evidence needed |
| --- | --- | --- | --- | --- |
| SEC-01 | High | Mission decision state was read without a row lock | Add PostgreSQL `SELECT ... FOR UPDATE` in decision transaction | Concurrent same-step submissions: exactly one succeeds, one gets 409; score increments once |
| SEC-02 | High | Login route has no abuse protection | Implement a distributed, privacy-conscious rate limit at ingress/shared store; do not use per-process memory | Repeated invalid login tests; multiple-instance behavior; legitimate user recovery |
| SEC-03 | Medium | Shared database dependency repeated in routes | Centralize with regression coverage | API behavior unchanged |
| SEC-04 | Medium | Development CORS origins hardcoded | Validate allowed origins from environment | Production allowlist test |
| SEC-05 | Medium | Dependency version ranges broad | Introduce reproducible lock/constraints and automated audits | Clean build and dependency scan |
| SEC-06 | Medium | Authentication/authorization and mission persistence coverage incomplete | Add adversarial API and database integration tests | CI evidence |
| MAINT-01 | Medium | Homepage combines networking, quiz state and rendering | Extract components and typed API client incrementally | Build and browser regression |
| OPS-01 | Medium | CI security and quality gates not verified | Establish GitHub Actions checks | Passing PR checks |
| PRIV-01 | High before public launch | Platform serves minors | Assess privacy, data minimization, retention, and child safety requirements | Documented review |

## Phase 8.1 first change
`api/mission_routes.py` now locks a mission-run row during a decision. This is intended to serialize concurrent scoring on PostgreSQL. It has **not** yet been verified by running concurrent integration tests; do not consider SEC-01 closed until that test passes.

## Next implementation sequence
1. Write PostgreSQL concurrency regression test for mission decisions.
2. Add shared configuration and DB dependency with tests.
3. Design shared-store/ingress authentication throttling and registration abuse protection.
4. Add automated CI and developer setup documentation.
5. Review remaining frontend, Android, and data flows before production readiness claims.

## Final review checkpoint — 2026-10-11

Verified locally by developer: 55 backend tests passed; `pip check` reports no broken requirements. Verified on GitHub: both backend-quality workflow runs for commit `ded337c` succeeded, including dependency audit and database-independent unit tests. PostgreSQL integration tests are **not** run by this CI workflow; local execution provides their evidence.

| ID | Review status | Evidence / remaining work |
| --- | --- | --- |
| SEC-01 | Verified locally | PostgreSQL concurrent mission decision test; one success, one conflict, score awarded once |
| SEC-02 | Partial | Persistent per-email login and registration buckets exist; still need trusted-edge IP quotas, bot protections, recovery and DoS assessment |
| SEC-03 | Open | Route modules still duplicate `get_db`; consolidate carefully without breaking dependency overrides |
| SEC-04 | Implemented and tested | `EDUCYBER_CORS_ORIGINS` validated; production origin values still need deployment review |
| SEC-05 | Partial | Dependency audit succeeds; broad version ranges remain, reproducible constraints/lockfiles not yet established |
| SEC-06 | Verified locally; CI gap | Authentication, BOLA, quiz, enrollment and mission HTTP tests pass against local PostgreSQL; add DB-backed CI |
| MAINT-01 | Open | Frontend component extraction, typed API client and build regression remain |
| OPS-01 | Partial | GitHub Actions quality and dependency audit succeed; integration CI, secret scanning and deployment checks remain |
| PRIV-01 | Open — public launch blocker | Child safety, age-appropriate flows, lawful basis, retention and deletion rights require product/legal review |

### Additional findings
- `/health/db` currently has no authentication; avoid exposing detailed infrastructure health to the public internet, or restrict it at the gateway.
- Quiz responses disclose answer keys after a submission by design. Before introducing high-stakes assessments, review attempt limits, question pools and answer-reveal policy.
- Authentication event logging records event names only. Centralized retention, security alerting and correlation remain operational tasks.
- Review authorization and personal-data handling in the web and Android clients; backend test coverage is not an end-to-end penetration test.

**Decision:** Do not declare Phase 8 production-ready or merge solely on the basis of the 55 passing tests. Continue with maintainability, dependency reproducibility and operational hardening in controlled batches.

## Shared database dependency refactor — pending verification
- Authentication, learning, quizzes and mission routes now import `get_db` from `api/db_dependencies.py` rather than defining duplicate generators. `api/main.py` already uses it.
- `api/auth.py` now receives the same request-scoped database session through FastAPI dependency injection for bearer-token lookup. This removes an additional implicit session and enables consistent dependency overrides.
- This changes authentication session lifecycle wiring and **requires** full isolated PostgreSQL integration tests before acceptance. Do not mark the refactor verified solely from successful import/unit checks.
- No schema migration is required. Confirm the backend GitHub quality workflow and rerun local isolated DB tests if CI reports errors.
