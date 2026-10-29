# Red/Blue simulator — approved direction and staged delivery

Owner instruction: 29 October 2026. English only. An original educational browser strategy game inspired by ThreatGEN: Red vs. Blue; no copied product assets, real exploitation, attack payloads or external AI calls. Preserve existing courses, 500-question practice, missions, Cyber Lab, saved progress and authentication.

## Architecture inspection before implementation

| Area | Existing architecture and consequence |
| --- | --- |
| Languages | Python API; TypeScript/React web client. Keep the simulation authoritative in Python. |
| Frameworks | FastAPI/Pydantic, SQLAlchemy 2/PostgreSQL/Alembic; Next.js 15 App Router, React 19; optional Three.js/React Three Fiber for existing 3D views. No additional dependency is needed for this engine checkpoint. |
| Structure | `api/` routes, SQL models, engines, content, Alembic migrations and colocated pytest files; `web/app/` pages, `web/components/`, `web/lib/`, global CSS and module styles; `scripts/`, `docs/`, CI workflows. Legacy Android `app/` is outside this work. |
| Data models | User/AuthSession, Academy/Course/Lesson/Enrollment/LearnerProgress, QuizQuestion/QuizAttempt, MissionRun, StrategyRun/StrategyCommand, CyberPracticeSession/CyberStudyProgress, invite/recovery/feedback and security records. StrategyRun owns one user's JSON state; it cannot securely represent two independent seats by changing a client label. |
| Routes | FastAPI `/api/v1` routers; Next.js filesystem pages with same-origin API rewriting. Additive routes will be introduced only after the engine review. |
| State | Server-authoritative persisted game state; owner-scoped commands, versions, command IDs and locking in existing strategy APIs. React hooks/fetch for client interactions, not Redux. Opaque bearer sessions are hashed on the server; this is not JWT authentication. |
| Styling | Global CSS and CSS Modules; dark navy/teal, responsive controls, focus management and reduced-motion support. Reuse these conventions in the later UI. |
| Tests | Pytest synthetic SQLite and isolated PostgreSQL/concurrency suites; Node frontend tests, TypeScript, production builds, Playwright intercepted-API regression and real-API/PostgreSQL browser tests. Engine tests use no learner database. |

The inspection and the need for a separate match model were summarised to the owner before code was written. No incompatible framework or authentication replacement is required. Red/Blue match seats are not student/teacher/admin account roles. Existing private-beta eligibility remains authoritative. An instructor must not acquire private match access merely by selecting a role.

## Delivery gates

1. **Engine checkpoint (this build):** isolated `api/cyber_warfare/` package, strict loader, six separate configurations, bounded action catalogue, fixed resolver, sealed two-seat commands, observations, deterministic replay, readable opponent rules at three levels, debrief, unit/regression evidence and authoring documentation. **Stop and present results before any interface.**
2. **Persistence/authentication/API:** additive match/seat/order/receipt storage and migration, existing bearer authentication and beta eligibility, participant binding, invite/join/expiry policy, transaction/CAS locking, command UUIDs, deduplication, stale requests, simultaneous submissions, disconnect/resume and owner-scoped history. Prove with separate actual sessions on isolated PostgreSQL. Keep old strategy tables/routes/rules unchanged. Define instructor-review consent/ownership explicitly before enabling it. A pure domain test is not proof of live multiplayer authorization or concurrency.
3. **Interface:** scenario/role/difficulty choice; responsive network/asset-list view; one-round action planning with cost, prerequisites, explanation and mapping; locked-choice waiting/resume; side-filtered evidence; accessible wiki and post-game debrief. Reuse account/session helpers, CSS and navigation. Add desktop/mobile/reduced-motion and real-API journeys. No UI in checkpoint 1.
4. **Educational/balance acceptance and release:** review beginner comprehension, scenarios, counterfactual explanations, Red/Blue balance and opponent challenge using seeded playthroughs. Final security assurance, recovery/retention and operational checks remain required. Promote to beta only by a separately authorised, tested rollout; never copy beta learner data to development.

## Rules and assumptions for review

- Two distinct seats. Either may be a human or a policy-controlled opponent. Human identity strings in the engine are domain bindings, **not** authenticated sessions; the next adapter must obtain these from existing authentication.
- One action per side per round. Both get the scenario's AP allowance afresh each round; unused AP do not carry over. Each also has a finite, equal starting budget. An action deducts its cost from both the per-round allowance and remaining budget; with one action, the AP check is a simple cap. Waiting costs zero. No purchases, real money or asymmetric economy yet.
- Choices lock on commit; no editing or revealing the other choice. Resolution waits for both seats. Round number is the command precondition; a first commitment does not invalidate the other's same-round request. The future storage adapter must still atomically CAS/lock the full match. Same command ID and payload is idempotent, including after replay.
- Fixed order: Blue protection/investigation/recovery, then Red action, then victory/deadline checks. Effects use current truth at resolution, not obsolete commit-time truth. A blocked action still spends committed resources. Public legality uses only the seat projection, preventing an error message from exposing a hidden control change.
- Directed connections represent allowed trust paths. Privileged footholds cross one edge at a time; segmentation at either endpoint blocks lateral crossing. Isolation blocks actions and costs business availability. Retained access can survive containment in a dormant state; access review/recovery removes it.
- Red starts with limited inventory and explicitly configured starting footholds; recon reveals outgoing neighbours and a dated assessment. Red's intelligence can become stale. A failed session check can establish loss of connectivity without naming the defender's action. Blue knows its inventory, controls and health, but not hidden compromises or Red's exact orders. Alerts identify suspicious activity, not whether an attack succeeded; targeted investigation can find evidence. Monitoring alone does not reveal access.
- Victory uses per-scenario target value, irreversible fictional leakage/fraud, or consecutive critical-service unavailability. Isolation counts as downtime in the hospital scenario. Recovery cannot reverse historical leakage/fraud. Red wins if its objective is met on the final turn; otherwise Blue wins at the deadline. No draws, timeout forfeits or early elimination rule yet.
- Counter-based SHA256 pseudorandom fractions depend on a private seed, engine revision, round and phase. No wall clock, Python process hash or global random state. Outcomes and detection are independently keyed. Scenario snapshot/digest, rule digest and private command transcript support exact recomputation, including pending orders. Preserve old engine versions for existing matches; do not silently replay them under changed rules.
- Seeds, full state, sealed commands and private trace remain server-only. The replay format supports debugging, **not cryptographic proof of authenticity**; hashes detect accidental/mismatched content, not maliciously rewritten imports. No untrusted import endpoint is provided.
- Easy prioritises scouting/basic hygiene. Standard prioritises objectives and alert-led containment/recovery. Hard additionally ranks critical targets, known weaknesses and trust boundaries. Policies consume exactly the same projection as a human and never access seed, hidden orders or hidden compromise state. Difficulty does not improve resources or probabilities. Balance/challenge need human evaluation.
- Post-game participants may see the full action timeline, missed alerts and alternative Blue orders that were affordable at that round's opening. Counterfactuals rerun that single round with the same seed and Red choice; report only improvements actually observed, never guarantee a changed match winner. No instructor endpoint exists yet.
- ATT&CK mappings are conceptual educational associations. Red actions represent techniques; Blue actions address them; wait actions have planning context. These are not certifications or full emulations. The AI scenario models instruction-boundary failure and data access only; it does not introduce an LLM/provider dependency.

## Six initial scenarios

| Config ID | Industry / challenge | Difficulty | Turns / budget per side | Red objective |
| --- | --- | --- | --- | --- |
| `microfinance` | Phishing-led banking fraud | Beginner | 12 / 24 | Alter the 80-value ledger |
| `hospital` | Ransomware and clinical availability | Intermediate | 14 / 30 | At least 60 critical value unavailable for two consecutive rounds |
| `software_cloud` | Public cloud configuration breach | Beginner | 10 / 21 | Copy at least 70 sensitive value |
| `payment_insider` | Trusted payment-operations session | Advanced | 10 / 24 | Alter approval and settlement records, combined value 155 |
| `trusted_vendor` | Supply-chain trust crossing | Intermediate | 14 / 30 | Copy the 80-value shipment database |
| `ai_service` | Untrusted retrieved instructions and data leakage | Advanced | 12 / 27 | Copy the 90-value restricted knowledge store |

Each JSON file owns its network, controls, weaknesses, starter intelligence, objective, turn limit and budget. The loader discovers bounded local files without dynamic imports or executable configuration.

## Public framework sources

Verified against MITRE's primary public pages on 29 October 2026. Original explanations in the catalogue intentionally omit payloads and operational procedures. The wiki may link to these public reference pages; learners need not read them to play.

- [T1595 reconnaissance](https://attack.mitre.org/techniques/T1595/), [T1566 phishing](https://attack.mitre.org/techniques/T1566/), [T1190 public-facing application boundary](https://attack.mitre.org/techniques/T1190/).
- [T1068 privilege escalation](https://attack.mitre.org/techniques/T1068/), [T1021 remote services](https://attack.mitre.org/techniques/T1021/), [T1098 retained account access](https://attack.mitre.org/techniques/T1098/).
- [T1041 exfiltration](https://attack.mitre.org/techniques/T1041/), [T1486 ransomware impact](https://attack.mitre.org/techniques/T1486/), [T1565 integrity manipulation](https://attack.mitre.org/techniques/T1565/), [T1698 indirect prompt injection](https://attack.mitre.org/techniques/T1698/).

The owner permitted ATT&CK **or** ISO 27001 mappings per action. This build uses ATT&CK throughout, with explicit relation labels, and does not reproduce licensed ISO control text.
