# Development handover

**Last updated:** 27 October 2026 (Africa/Lagos).  
**Checkpoint:** Phase 3.2 owner-reported local checks passed; Phase 4.1 Scholarship Email pilot implemented, owner acceptance and beginner/device evidence pending. Python pilot acceptance remains recorded. The formal audit remains deferred until the end of development.
**Roadmap:** [approved plan](DEVELOPMENT_ROADMAP.md).

## How to resume

Read this file and the roadmap, select `feature/beta-continuous-improvement`, inspect current Git status and relevant source, and continue from the next action below. Do not assume that the default branch represents the current web/API project.

- Development branch: `feature/beta-continuous-improvement`.
- Tester-facing beta branch: `feature/secure-password-recovery`.
- The development worktree was created from the same committed source as beta.
- The owner has verified the local setup through terminal output. The assistant inspected repository code but did not directly operate the owner's computer.
- Local development setup files have not yet been uploaded merely by creating this documentation.
- Treat runtime locations, connection details, credentials, backup metadata and raw feedback as private local information. Ask for fresh, sanitised diagnostics when needed rather than recording these details in Git.

## Completed with owner-supplied evidence

- [x] Exported all feedback in a consistent read-only snapshot and reconciled the record count.
- [x] Reviewed feedback and approved the revised eight-phase roadmap.
- [x] Checked beta application and database readiness.
- [x] Created a logical database backup and verified its checksum.
- [x] Restored that backup into a temporary isolated database.
- [x] Verified restored migration and representative aggregate counts against the baseline.
- [x] Removed the temporary recovery container and retained the backup locally.
- [x] Created a separate development Git worktree and branch.
- [x] Added local Git exclusions for backup, export and generated build directories.
- [x] Created a separate development database, credentials and persistent volume.
- [x] Created a separate development Python environment.
- [x] Applied database migrations to the expected source revision.
- [x] Seeded demonstration courses, lessons and quizzes.
- [x] Confirmed development contains no copied beta learner accounts, feedback or mission records.
- [x] Owner ran the development isolation check successfully: frontend and API process identities matched; database identity and schema readiness passed.
- [x] Owner confirmed the existing beta frontend and API health still returned HTTP 200.

Recovery evidence establishes successful logical snapshot restoration and the stated checks. It does not establish off-site retention, encryption, point-in-time recovery, service recovery time or a complete application recovery drill.

## Latest approved build

After reporting all baseline learner checks passed, the owner requested two additions for the next build: selectable assessment lengths and automatic scrolling/focus when opening courses, missions and assessments. The owner approved proceeding. This is a bounded addition before the planned baseline security audit; it does not cancel the audit or replace the approved roadmap.

Implemented:
- Quick, Standard, Extended and Custom practice lengths, limited to the available unique question bank and a server-side maximum.
- Server-recomputed question selection and grading; persisted attempt totals reflect the selected length. Legacy full-bank requests remain supported. No database migration.
- Automatic scrolling and keyboard focus after successful course/mission/assessment opening, with reduced-motion support. Lesson completion and answer changes do not deliberately refocus the workspace.
- [Feature contract and acceptance checklist](ASSESSMENTS_AND_ACTIVITY_NAVIGATION.md).

Verification in the assistant workspace:
- 21 actual quiz HTTP tests passed using a disposable in-memory SQLite database, with authentication overridden. They cover chosen sizes, real grading, persisted totals, backwards compatibility, eligibility and forged/invalid submissions. They do not establish PostgreSQL concurrency or full authentication behaviour.
- TypeScript typecheck passed; all 15 frontend unit tests passed.
- Production Next.js build passed, with pre-existing CSS alignment compatibility warnings.
- Standalone lint is blocked by the repository's missing ESLint flat configuration.
- Four new Playwright browser cases were added, but the browser could not start because the execution workspace denies a required local socket. Browser assertions therefore remain unverified.
- No beta database, beta source branch or running owner services were changed by this build.

Local acceptance on 26 October 2026: after receiving the update, test, restart and feature-check instructions for source commit `adc2f4c`, the owner reported no errors and that all tests passed. Record this as owner-reported acceptance, without claiming independently observed logs, a full regression result or execution of the blocked Playwright cases. Specific mobile and reduced-motion evidence was not separately supplied.

## Baseline audit preparation

- Pinned upstream Cloudflare security-audit-skill revision: `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`.
- Prepared application baseline: `c1e494e533965cf10e701bd4b851cb4f3fb3b7db`, including the accepted assessment/navigation build.
- Added an unchanged project-local reference copy at `tools/security-audit-skill/`, including the MIT license and upstream README. All 22 files matched their upstream Git blob hashes; SHA256 and byte lengths are recorded in `tools/security-audit-skill.lock.json`. This does not claim client auto-discovery registration.
- [Preparation, scope and capability gate](security/BASELINE_AUDIT_PREPARATION.md) maps the web/API, learner-data, browser, operations and CI trust boundaries. Legacy Android and other products are outside the initial scoped pass.
- Required user/network namespace probes were denied in this execution workspace. A complete read-only/scratch-only, empty-environment and resource-bounded runner with safe evidence promotion has not been verified.
- Preparation initially launched no audit agents. The subsequent audit attempt is recorded below; it remains incomplete and is not a passing audit.
- Source-only review can proceed. Runtime-dependent claims require exact needs_validation blockers and no severity until independently established under the skill's contract.

## Interrupted baseline audit checkpoint

The owner authorised the source-first audit. The prior-session handover reports four reconnaissance assignments completed and six hunters launched. Several hunters reported workspace-credit errors before the workflow finished. The original external run directory and structured agent results are unavailable after the session transition.

A [recovered incomplete checkpoint](security/baseline-run-1/REPORT.md) preserves the frozen source revision, architecture summary, deterministic coverage plan and exact resumption steps. The ledger was reconstructed from the surviving parent-owned planning script; no missing evidence or candidate fingerprints were invented. All 33 in-scope units are deferred; two units are out of scope. No unit receives coverage credit.

The empty findings array and 35-unit ledger pass the pinned structural validators. These passes establish format only. No independently validated vulnerabilities, passing audit, final critic result or security clearance is claimed. Target application execution remains blocked by the unverified OS sandbox controls.

## Exact next action

Use [the Phase 4.1 guide](PHASE_4_MISSION_PILOT.md) to update/restart only development, run focused checks and complete the Scholarship Email pilot acceptance checklist. No migration or content publication is required for this build. Verify CI and independent beginner/device completion evidence before broadening the mission redesign. Keep beta open; Phase 3.2 and wider educational/operational/final audit gaps remain as recorded.

The owner instructed on 26 October 2026 that the formal security-audit-skill stage be deferred until the end of all development. This supersedes the earlier audit-first next action. Continue security by design, secure coding/review and normal tests throughout. Resume the formal audit against the then-current source, revalidating changes and unresolved earlier leads; no security clearance is implied.

## Implemented source changes and checks

- Configurable server-side API/health proxy with validation; existing beta default and reset-password security headers preserved.
- Home game-library and logout requests now default to same-origin browser requests. Server-rendered pathway requests use the configured frontend origin.
- Guarded development launcher explicitly selects the development database and local services, removes inherited beta application/mail settings, refuses occupied ports and never runs migrations automatically.
- Development-only non-secret process identity endpoint; ordinary beta mode does not register it. The verification command requires direct and frontend-proxied identities to match.
- Added development requirements and a local startup/verification runbook. Existing local Compose setup remains pending review/commit.
- Focused verification in the assistant workspace: 6 Python unittest guard cases and 4 Node proxy/configuration cases passed. Python syntax compilation passed. These checks used no live beta database or mail service.
- Subsequent owner-supplied Windows output verifies successful development service startup and the runtime isolation check, plus continued beta HTTP health. This supports successful application startup but is not a full regression or browser result.
- The owner subsequently reported both the baseline manual learner checklist and local checks of the updated build passed. Latest-build assistant checks and their limits are listed above; full regression and independent browser automation remain pending.

## Outstanding work

- [x] Development frontend routing configuration implemented and runtime identity matching verified by the owner.
- [x] Startup configuration loading and inherited-environment guards implemented and unit tested.
- [x] Development API/frontend running; owner verified runtime isolation and database/schema readiness.
- [x] Owner reported all six baseline synthetic learner checks passed (registration/login, learning persistence, assessment, mission, feedback and logout). This is a manual report, not a full automated regression result.
- [ ] Dependency baseline comparison and controlled reproducibility plan. Broad requirements ranges were used during setup; do not assume development and beta installed identical versions.
- [ ] Real-backend browser and regression checks.
- [ ] Versioned release/recovery procedures and application-version feedback metadata.
- [x] Cloudflare skill read and pinned; unchanged reference tooling, provenance hashes, scope and capability gates prepared.
- [ ] Full Cloudflare audit workflow, independent verification, validated ledger/findings and final reports.
- [ ] OS-enforced audit execution sandbox and parent-side evidence promotion verified.
- [x] Assessment-length and activity-navigation additions implemented; owner reported successful local checks and no errors after the update.
- [ ] Other feedback-driven learning and mission improvements.
- [ ] Later phases of the approved roadmap.

The Cloudflare audit started but remains incomplete; the full regression suite has not run. The owner reported successful local acceptance after the latest changes. Latest assistant assessment HTTP tests and frontend unit/build checks passed as listed above; independently executed real-browser automation and full PostgreSQL regression remain outstanding.

## Working tree and source-control notes

The last beta status included a generated frontend declaration-file modification, which was preserved. Inspect it before deciding whether any action is needed; do not reset or stage it automatically.

The development setup created a non-secret Compose definition, an ignored credential file and a local Python environment. Only the appropriate reviewed source/configuration belongs in Git. Local exclusions do not replace a reviewed repository-wide ignore policy.

## Continuation and maintenance rules

The owner wants complete corrected PowerShell blocks whenever commands need changing, rather than replacement fragments.

After each verified milestone, update this file with:
- date and evidence source;
- relevant source changes and commit references;
- checks actually run and their results;
- unresolved issues;
- one concrete next action.

Refresh actual Git/runtime state at the beginning of a new session. Keep beta testing open, develop against separate data and do not mark proposed commands as completed work. Do not commit private operational metadata or raw tester data.




## Phase 3.1 — Python foundations pilot

Implemented on 26 October 2026, addressing FB-01, FB-06, FB-07 and FB-08. Three expanded Python lessons provide nine objectives, worked examples/output and six guided checks. Twenty reviewed assessment questions align with taught objectives; Quick/Standard/Extended/Custom lengths remain supported. Practice feedback is server-checked and does not save grades or completion. The explicit development-only publisher preserves course/lesson IDs, completed progress, historic question rows and attempt scores; startup performs no publication or migration. Customized/conflicting content is refused.

Verification: 45 focused backend tests and 11 subtests passed with synthetic SQLite/auth overrides; 15 frontend unit tests, TypeScript and production build passed. Pre-existing CSS warnings remain. Two browser cases were added; Chromium cannot start here because required socket creation is denied, so browser interaction assertions remain unexecuted. Full backend collection was attempted but blocked by missing Alembic in the workspace test environment; no full regression or PostgreSQL result is claimed. Browser/backend CI selects this branch, and the backend fixture port now matches the existing password-recovery guard; CI execution is pending.

See [implementation, complete PowerShell commands and acceptance](PYTHON_FOUNDATIONS.md). No owner database or beta services were accessed. The remaining Phase 3 course reviews are outstanding. The formal audit remains deferred by owner direction until the end of development.


## Phase 3.1 owner acceptance — 26 October 2026

After receiving build `6d70ba9` and its publication/acceptance guide, the owner reported: “All works well.” Record this as successful owner-reported local acceptance of the Python pilot. No detailed test log or separate mobile, accessibility, full PostgreSQL regression or automated-browser evidence was supplied; those earlier verification limits remain. No application code was changed by this acceptance record.

Next action: implement the remaining Phase 3 learning/assessment improvements for Cyber Safety Foundations and Digital Citizenship. The formal security-audit-skill stage remains deferred until the end of development by owner direction.

## Phase 3.2 — Cyber Safety and Digital Citizenship

Implemented on 27 October 2026 for FB-01, FB-06 and FB-07. The two courses now have six expanded lessons, 18 objectives, worked scenarios, 12 guided checks and 40 distinct assessment questions (20 per course). Digital Citizenship no longer selects the Cyber Safety question bank after explicit publication. Practice remains server-checked, ungraded and separate from lesson completion. The shared publisher preflights both courses before changing either, refuses customized/ambiguous/conflicting content and retains old question IDs, saved scores, completion and other learner records. Existing Python commands remain Python-only and the accepted Python release is preserved.

Local verification: full backend collection completed with 179 passed, 20 database-dependent tests skipped and 11 subtests passed using synthetic SQLite for feature HTTP tests; frontend 15 unit tests, TypeScript and production build passed. Existing CSS compatibility warnings remain. A fresh isolated dependency environment passed pip check and pip-audit after two pinned dependency patches. CI checks for this source revision are pending at this documentation checkpoint. Local Chromium remains blocked by UNIX socket restrictions; added browser cases are not counted as executed locally.

Routine CI maintenance fixes an exact-label sign-in locator and practice focus loss caused by disabling the active control; pending checks now prevent duplicate submissions without removing keyboard focus. The browser harness is installed outside app dependencies to preserve the application lockfile. Certifi and filelock minimum/pinned versions address reports from the existing dependency gate. This is ordinary build maintenance, not a resumed formal security-audit-skill stage. No beta data, provider or owner database was accessed.

See [complete PowerShell update/publication/test/restart blocks and acceptance](FOUNDATIONS_COURSES.md). Source implementation is complete for this bounded build; owner publication/acceptance, beginner testing and final assurance remain outstanding.


## Phase 3.2 owner acceptance — 27 October 2026

After receiving the update, explicit publication, focused test, restart and acceptance instructions for source `a33769b`, the owner reported: “All tests pass.” Record this as successful owner-reported local checks/acceptance. No detailed logs or separately identified beginner walkthrough, mobile/reduced-motion, full PostgreSQL regression or automated-browser results were supplied. Do not infer these additional outcomes. No owner database or beta service was operated by the assistant.

Next: the bounded Phase 4 mission pilot. The formal Cloudflare audit remains deferred until the end of development; normal security-by-design checks continue.


## Phase 4.1 — Scholarship Email mission pilot

Implemented 27 October 2026 from acceptance checkpoint `31cc21a` for FB-02, FB-04 and FB-05. Added role/goals, exact actions and completion conditions, stage tasks and optional hints, stage-specific fictional records shared by 2D/3D, after-decision finding reasoning, five server-checked optional review questions and completed-result reopening. Review is ungraded/nonpersistent and requires ownership of a completed pilot run. Existing mission step order, scoring and saved history are preserved; no migration/publication. Added a synchronous decision guard and 3D error boundary with 2D recovery. See [scope, complete commands and acceptance](PHASE_4_MISSION_PILOT.md).

Assistant verification: 191 backend tests and 11 subtests passed, with 20 database-dependent skips; 15 frontend unit tests, TypeScript and production build passed. Existing CSS compatibility and TestClient deprecation warnings remain. Locked environment pip check passed. New HTTP tests use synthetic SQLite/overridden identity, including legacy runs, all missions finishing and review validation/ownership; they do not establish full authentication/PostgreSQL locking. Four new browser cases were attempted but Chromium could not launch because a required UNIX socket is denied. Browser assertions remain unexecuted locally; CI is pending at this checkpoint. No owner database/computer, beta service or mail provider was accessed.

Next: verify CI and owner development acceptance plus independent beginner/device walkthroughs of this pilot, then choose the next mission. Phase 4 is not complete. Formal audit remains deferred by owner instruction until the end of development.
