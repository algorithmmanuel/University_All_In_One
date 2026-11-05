# Baseline security audit preparation

Prepared on 26 October 2026. This is a preparation package, not a completed vulnerability audit. No hunters or candidate verifiers have been launched, no application code was executed for this preparation, and no security finding or clean-coverage conclusion is asserted.

## Pinned inputs

| Input | Frozen reference |
| --- | --- |
| Application repository | algorithmmanuel/University_All_In_One |
| Development branch | feature/beta-continuous-improvement |
| Application baseline | `c1e494e533965cf10e701bd4b851cb4f3fb3b7db` |
| Cloudflare upstream | https://github.com/cloudflare/security-audit-skill |
| Upstream tool revision | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` |
| Local skill entry | `tools/security-audit-skill/SKILL.md` |
| Provenance/integrity manifest | `tools/security-audit-skill.lock.json` |
| Proposed profile | Standard, scoped to the maintained web/API platform and supporting operations/CI |

The tooling copy includes all 20 files from the upstream skill directory plus the upstream README and MIT license. All 22 files were checked against their upstream Git blob hashes before copying. The lock manifest also records SHA256 and byte length for each file. README is stored as README.upstream.md; the file contents are unchanged. No model/agent-client auto-discovery registration is claimed: future sessions must explicitly read the pinned entry point. Do not silently update upstream tooling during a run.

The baseline includes the accepted assessment-length and activity-navigation build. Later source changes require a new reviewed revision or explicit changed-source revalidation. Committing this preparation adds documentation/tooling but does not change application behaviour.

## Scope and initial source inventory

In scope: `api/`, `web/`, `scripts/`, `compose.yaml` and `.github/workflows/` at the frozen baseline. This is a scoped platform pass, not a claim to cover every historical project in the repository.

Out of scope for this first baseline: legacy Android sources under `app/`; the imported audit-tooling directory as an application target; other products/repositories; deployed hosting, identity/email-provider accounts and their control planes. Hosting configuration may become an owner-observed validation dependency, never an assumption that a control is present or absent.

The following is a planning inventory, not the skill's canonical coverage ledger and not proof that any unit has been audited. Full reconnaissance must expand each material surface/boundary/subsystem/attack-class combination into its own canonical unit.

| Planning group | Source entry points | Boundary/invariant to examine |
| --- | --- | --- |
| Identity and age/role transitions | api/auth_routes.py; api/age_policy.py; api/auth.py | Anonymous input must not grant unintended account activation, role authority, teacher approval or beta access. |
| Sessions and revocation | api/auth.py; api/auth_routes.py; api/security_maintenance.py; api/models.py | A token must bind to the intended active principal and respect expiry, logout and later revocation. |
| Recovery and mail delivery | api/password_recovery.py; web/app/forgot-password/page.tsx; web/app/reset-password/page.tsx | Reset authority, token lifecycle, concurrent use, leakage, throttling and session invalidation must follow the intended account boundary. Mail is mocked for local validation. |
| Learning and progress | api/learning_routes.py; api/models.py; web/app/learn/page.tsx | Publication, enrolment and authenticated ownership must apply to reads, completion writes and derived progress. |
| Assessments and saved results | api/quiz_routes.py; api/assessment_selection.py; web/app/assessments/page.tsx | Selected IDs, options, grading and denominator must be server-controlled; attempt history must remain owner-scoped, including the legacy full-bank path. |
| Missions and replay/concurrency | api/mission_routes.py; api/mission_contract.py; api/mission_data.py; web/app/missions/ | Mission ownership, allowed transitions, expected steps, score computation and concurrent/replayed actions must preserve the same authority boundary. |
| Private feedback and operator tools | api/beta_routes.py; api/create_beta_invites.py; api/list_beta_invites.py; api/reassign_beta_invite.py | Learners must not access another learner's feedback or operator authority. Invite lifecycle and CLI authority must be traced separately. |
| Browser rendering, storage and proxy | web/app/; web/components/; web/lib/; web/next.config.mjs; web/config/api-origin.mjs | Untrusted data must not gain browser execution, another account's session authority or an unintended proxy destination. Browser navigation is not an authorisation control. |
| Runtime and operational separation | api/main.py; api/production_config.py; api/development_runtime.py; scripts/development.py; compose.yaml | Development/test/runtime configuration must not silently cross environment or data boundaries. Inspect logging and diagnostic readers without collecting real secrets. |
| Data lifecycle and recovery | api/migrations/; api/request_telemetry.py; api/security_events.py; scripts/rehearse-database-recovery.sh | Protected fields, logs, migrations and restored copies must preserve stated ownership/lifecycle guarantees. Private backup artifacts are excluded. |
| Resource and abuse boundaries | api/login_limiter.py; api/password_security.py; api/quiz_routes.py; api/mission_routes.py | Source-visible work/limits must be examined with bounded dummy inputs. Never stress shared services or infer availability impact from an expensive-looking loop. |
| Dependencies and delivery | api/requirements*.txt; api/requirements-ci.lock; web/package*.json; .github/workflows/; scripts/*sync*.ps1 | Trace dependency provenance, workflow permissions, trigger/input trust, branch assumptions and release authority. Installing dependencies or publishing is not audit validation. |

Preliminary source facts: FastAPI routers are registered in api/main.py; authentication/session and published-course enrolment checks are present in route helpers; recovery includes a Brevo HTTPS delivery path; mission decisions contain ownership and locking logic; grading is server-side. These facts identify review starting points, not verified security conclusions. PostgreSQL-specific limiter/locking behaviour cannot be established by the earlier SQLite assessment tests.

No compatible prior Cloudflare coverage ledger or findings JSON was found in the tracked baseline. Historical hardening/acceptance documents under docs/ are context only and must be compared with current source; they do not constitute prior covered units. Private or untracked prior audit evidence has not been inspected.

## Companion selection

Use ordinary attack blocks where applicable: access control, injection, resource/file handling, cryptography/secrets, business logic, feature abuse/data leakage, chained trust boundaries, wildcard and obvious-things checks. Each future ledger unit must carry exact selected blocks and reasoned exclusions; this list is not a blanket assignment.

| Companion | Initial selection rationale |
| --- | --- |
| WEB-PROTOCOL-AND-AUTH.md | HTTP authentication, recovery, CORS and frontend/API proxy boundaries. |
| CLIENT-SIDE.md | React rendering, browser-held tokens, origin separation and browser lifecycle. |
| DATA-ISOLATION-AND-LIFECYCLE.md | Learner ownership, attempts/progress, feedback, diagnostics, migrations and recovery. |
| RESOURCE-EXHAUSTION-AND-AVAILABILITY.md | Authentication work, throttling and state/query growth; bounded fixtures only. |
| SUPPLY-CHAIN-AND-RELEASE.md | Dependencies, CI inputs/permissions and operational scripts. |
| CLOUD-AND-DEPLOYMENT.md | Compose/runtime configuration and ingress boundaries visible in source; no live provider probing. |

AI-AND-LLM.md is retained in the pinned toolset but not automatically selected: the inspected registered routers do not establish an active model/tool execution boundary. The product vision alone is insufficient. Reconnaissance must activate this companion if it discovers an in-scope AI path. Likewise, RPC/messaging, memory/native-binary and desktop/mobile companions require corresponding in-scope source evidence; the legacy Android application is excluded from this initial platform pass.

## Execution capability gate

Read-only source inspection can proceed. Execution-based validation is currently blocked.

Preparation probes found bubblewrap, unshare and prlimit available. A harmless user/network namespace probe failed with user-map permission denied. A bubblewrap probe using only system tools failed to create its loopback netlink socket. No target-controlled command was run in these probes. Available binaries are not evidence of a functioning sandbox.

| Required control | Preparation status |
| --- | --- |
| External networking disabled; isolated loopback when needed | Namespace probes denied; not established. |
| Empty environment with explicit allowlist; scratch-local home/temp/cache | Design requirement recorded; audited runner not established. |
| Read-only target and toolchain; scratch-only writable mount | Not established in an approved runner. |
| CPU, memory, process, file-size, disk and wall-clock bounds | prlimit availability observed; complete enforcement not established. |
| No host credentials, home, sockets or shared services exposed | Not established for a target-controlled process. |
| Parent-owned race-safe promotion of bounded regular files | Not implemented/verified for a full run. |

The pinned SKILL.md says: "If every control cannot be enforced, do not execute target code". Therefore do not run application tests, builds, browsers, fuzzers, fixture processors or services for audit validation in this workspace. Earlier functional tests are not retroactively treated as sandboxed audit reproduction evidence.

The source-only portions of a full audit may proceed with independent agents and honest coverage accounting. A lead needing unavailable runtime/deployment evidence must remain needs_validation with its exact blocker; it receives no severity. Do not treat this infrastructure limitation as a finding in the application.

## Full-run procedure to follow next

1. Re-read the pinned SKILL.md and relevant workflow files. Select standard scope as above unless the owner changes it. No strict agent budget has been set; record null rather than inventing one.
2. Resolve an absolute read-only target snapshot and a new output directory outside it, using the skill's default external run directory or another explicitly selected external location. Git documentation here is not the audit output directory.
3. Write run-metadata.json with actual source/worktree state, scope, execution policy, selected companions and ownership. State that this is a scoped platform pass and that no compatible prior ledger was available.
4. Run the four required independent reconnaissance assignments, then synthesise the bounded architecture summary and canonical coverage ledger. Reserve critics and independent verification before allocating hunter work. Validate the ledger after seeding and each update.
5. Run scoped hunters with unique scratch roots and exact block prompts. Never run target code without the full capability gate. Use post-wave critics plus a distinct final-clean critic for standard profile. Track every discovered/deferred/out-of-scope unit honestly.
6. Independently validate every candidate and separately verify final records, including needs_validation records. Do not confirm a runtime claim from source inspection alone, conflate hardening with vulnerabilities or infer deployed reachability.
7. Produce findings.json and the coverage ledger, validate both with the pinned validators, and derive REPORT.md, FINDINGS-DETAIL.md and NEEDS-VALIDATION.md from independently verified records. If the run cannot reach the required terminal state, record incomplete with the exact reason and disclose gaps.
8. Keep private evidence outside Git. Commit an appropriate sanitised summary and handover, then implement separately reviewed fixes and retest them. The audit workflow itself does not edit application source.

No agents have been launched and no full-run shared files have been created by this preparation. There are no findings to count or severity ratings to publish. A prepared toolset is not a passing audit.

## Engineering work carried forward

The missing ESLint flat configuration, broad dependency-range reproducibility work, full PostgreSQL regression and blocked automated browser verification remain open. Treat these as known engineering/assurance tasks unless an independently validated boundary violation establishes a security finding. Local-only Compose setup still needs deliberate source review before commitment.
