# Phase 7 — Cybersecurity Learning and Simulation Platform

Status: Architecture baseline (implementation pending). Base: `feature/educyber-web-mvp`.

## Product scope
EduCyber is a cybersecurity-only learning platform for three pathways:
- **Cyber Explorers (secondary):** digital safety, phishing, identity, privacy and basic defensive reasoning. No live exploitation labs.
- **Cyber Academy (university):** networks, Linux, secure coding, incident analysis, forensics and supervised isolated labs.
- **Cyber Command (professional):** SOC triage, risk decisions, cloud security, business continuity and incident command.

Non-cyber general education features are out of scope for new development. Do not delete existing data or functionality without a migration and regression tests.

## Existing implementation and verification
The branch currently includes `web/` (Next.js), `api/` (FastAPI), `compose.yaml` (PostgreSQL), authentication, learning, quiz and mission modules. This document does not assert that the current implementation is production ready. Inventory routes, database models, tests and user flows before modifying them. Preserve the Android `app/` tree.

## Architecture decision records
1. **ADR-001: Modular monolith.** Keep FastAPI and PostgreSQL, separating identity, curriculum, mission definitions, attempts, scoring, achievements and audit events through module interfaces. Avoid premature microservices.
2. **ADR-002: Browser-based 3D.** Use React Three Fiber / Three.js for the first optional, lazy-loaded 3D SOC scene. Provide a 2D accessible fallback. Do not make authentication or course navigation dependent on WebGL.
3. **ADR-003: Data-driven missions.** Define immutable, versioned mission specifications; store attempts and authoritative scores server-side. The browser renders state but cannot award itself points.
4. **ADR-004: No untrusted execution in the application tier.** The first mission is a simulated investigation with synthetic logs and deterministic outcomes. Future executable labs require separate isolation, egress restrictions, resource quotas, expiry and abuse monitoring.
5. **ADR-005: Docker first, Kubernetes later.** Retain Compose for local testing. Introduce orchestration only after load, reliability and operational needs justify it.

## Mission contract (design, not yet API)
A mission specification includes:
- `id`, `version`, `pathway`, `title`, `learning_objectives`, `prerequisites`
- `scenario`, `stages`, `evidence`, `allowed_actions`, `scoring_policy`, `completion_rules`
- `content_rating`, `estimated_minutes`, `review_status`

A mission attempt includes `attempt_id`, `user_id`, `mission_id`, `mission_version`, `state`, `started_at`, `completed_at`, and a server-generated score/evidence trail. Authorization must bind each attempt to the authenticated user; never accept client-supplied owner IDs or scores as authority. Persist only necessary telemetry and apply retention limits.

## Security baseline and acceptance gates
- Threat-model account takeover, broken object-level authorization, scoring manipulation, prompt/content injection, child-safety abuse, denial of service and cyber-lab breakout.
- Enforce role and object authorization on every backend operation; server-side schema validation and rate limits; secure cookies/CORS/CSRF controls appropriate to the actual auth mechanism.
- Protect minors: age-appropriate content, minimal personal data, moderation/reporting, privacy notice and verified applicable legal requirements.
- Add automated backend/frontend tests, dependency checks, secret scanning and code scanning to CI; block merges on critical failures after baselining.
- No secrets in Git or example files. Public repository status requires extra care with synthetic data and infrastructure details.
- Keep game content, logs and all simulated incidents fictional; do not connect gameplay to production systems.

## Phase 7 work packages
| Package | Deliverable | Exit criterion |
| --- | --- | --- |
| 7.1 | Inventory and regression baseline | Existing flows documented; tests runnable |
| 7.2 | Cyber-only taxonomy | Three pathways available without deleting prior records |
| 7.3 | Versioned mission contract | Server-side validation and authorization tests |
| 7.4 | Security CI baseline | Checks run on pull requests; documented findings |
| 7.5 | Operation Firewall vertical slice | One complete simulated SOC mission with 3D and 2D modes |
| 7.6 | Acceptance and performance | Local test evidence, accessibility review, security regression |

## First playable mission: Operation Firewall
A synthetic bank SOC investigation: receive suspicious login alerts, examine simulated logs, correlate evidence, select containment decisions, and receive a learning-focused debrief. Scoring rewards justified decisions and evidence quality, not speed alone. No real attacks or live target infrastructure.

## Development and release workflow
- Implement on `feature/phase-7-cyber-platform`; do not modify `master` or the prior MVP branch.
- Commit small, reviewable increments; create a PR after code and tests are ready.
- Developer pulls the feature branch, runs local migrations and tests, and reports failures before merge.
- Never commit local `.env` files, credentials, production data or recordings with personal data.
