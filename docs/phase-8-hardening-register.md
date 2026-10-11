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
