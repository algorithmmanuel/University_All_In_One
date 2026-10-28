# Development handover

**Last updated:** 28 October 2026 (Africa/Lagos).
**Checkpoint:** Phase 4.3 owner-reported acceptance recorded. Phase 4.4 six-game recovery/Academy batch implemented; CI and owner acceptance pending. Fifteen of 30 guides are implemented, including all ten Explorers. Formal audit remains deferred.
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

Verify CI and follow [the Phase 4.4 guide](PHASE_4_RECOVERY_AND_ACADEMY.md) to update/restart only development, run focused checks and accept MFA Guardian, Backup Buddy, Operation Firewall, Network Watch, Web Defense and Cloud Perimeter. No migration or content publication is required. Keep beta open. Continue the remaining games in approved five-to-six-game batches after acceptance; independent educational/device, operational and final security assurance gates remain open.

The owner-directed deferral of the formal security-audit-skill workflow until the end of development remains in effect. Security by design, review and ordinary testing continue throughout; no security clearance is implied.

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


## Phase 4.1 CI evidence — 27 October 2026

Implementation commit: `277164e`; browser assertion maintenance: `bfacb11`. [Backend run 40468541737](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40468541737) passed all jobs: database-independent collection 191 passed, 20 skipped and 11 subtests; isolated PostgreSQL collection 211 passed and 11 subtests; dependency consistency/audit passed. The TestClient deprecation warning remains. This is CI evidence on synthetic/test data, not owner deployment or production assurance.

[Browser run 40468828728](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40468828728) passed all 16 browser cases, plus 15 frontend unit tests, TypeScript and production build. The four new pilot cases cover desktop/mobile 2D/3D controls, hints, three decisions, review focus/duplicate guarding and error/retry, result reopening and partial resume, using synthetic API interception. Earlier run 40468541739 passed all four new pilot cases but failed a stale existing dashboard greeting locator; `bfacb11` now checks the current greeting and actual dashboard heading. No application behavior was changed to satisfy that assertion.

Local Chromium remains blocked by its required UNIX socket; the successful real-browser execution above occurred in GitHub CI. These mock-API browser cases and separate PostgreSQL API tests do not establish a complete real-backend browser journey, independent learner understanding, device performance or final security assurance.

Next action: follow [the pilot guide](PHASE_4_MISSION_PILOT.md) for development update/restart and owner acceptance; gather independent beginner and supported-device walkthrough evidence before extending the redesign. No migration or curriculum publication is required. Beta remains on its separate branch.


## Phase 4.1 owner acceptance and beta access — 27 October 2026

After handover `2ef17ef` and its development test/restart/acceptance guide, the owner reported: “All phase 4.1 tests pass and beta testers can access the link, lets proceed. I will let you know if further issues arise.” Record this as successful owner-reported Phase 4.1 local acceptance and restored tester access. The preceding 404 was on an unimplemented frontend /app path; the owner subsequently confirmed access after receiving the implemented entry routes. No beta service, tunnel, port, credentials or source branch was changed by the assistant. Do not infer detailed independent beginner, device performance, accessibility or deployed end-to-end evidence from this report.

The owner explicitly authorised proceeding. Next bounded build: extend the accepted guidance/review pattern to Password Fortress and Midnight Login Alerts while keeping beta separate.

## Phase 4.2 — Account safety and SOC triage

Implemented 27 October 2026 from `2ef17ef`, for FB-02/FB-04/FB-05. Added mission-specific goals, tasks, detailed stage records, six hints and five explained review questions to each of Password Fortress and Midnight Login Alerts. A static registry shares the existing route/UI across three guides; accepted Scholarship Email data is moved unchanged into a content module. Reviews are selected from the owned completed run, remain ungraded/nonpersistent and reject cross-mission question IDs. Existing engine steps, answer/finding keys, scoring and saved run history are unchanged; no migration/publication. See [complete commands, scope and acceptance](PHASE_4_ACCOUNT_AND_SOC.md).

Local verification: 217 backend tests and 11 subtests passed; 20 database-dependent skips. All 15 frontend unit tests, TypeScript and production build passed; pip check passed. Source-generated browser fixtures cover all three guided missions in a 12-case desktop/mobile and 2D/3D matrix. Known local Chromium UNIX-socket restrictions remain; CI is pending at this checkpoint. HTTP tests use synthetic SQLite/overridden identity; no full-authentication, PostgreSQL concurrency, owner runtime or complete real-backend browser claim is made from these local checks. Existing warnings remain. No beta/owner database, beta services or mail provider was accessed.

Next: verify CI and owner development acceptance plus beginner/device walkthroughs of these two missions. Three of 30 existing missions now have the guided pattern; this does not complete Phase 4. Formal Cloudflare audit remains deferred by owner instruction until the end of development.


## Phase 4.2 CI evidence — 27 October 2026

Source `a6a04a8` passed [backend run 40472624805](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40472624805): 217 passed, 20 skipped and 11 subtests in the database-independent job; 237 passed and 11 subtests against isolated PostgreSQL; dependency audit/consistency passed. The existing TestClient deprecation warning remains.

[Browser run 40472624786](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40472624786) passed all 24 browser cases, including the 12 guided-mission desktop/mobile × 2D/3D cases using actual static stage content and intercepted API responses. Frontend 15 unit tests, TypeScript and production build also passed. The accepted scholarship source data was additionally verified byte-for-byte against the earlier content block before its module move.

These successful CI results do not establish a complete real-backend browser journey, production operation, independent educational effectiveness, actual-device performance or final security assurance. Owner development acceptance for Phase 4.2 is still pending. Next: use [the complete update/test/restart and acceptance guide](PHASE_4_ACCOUNT_AND_SOC.md), check Password Fortress and Midnight Login Alerts, then choose the next bounded improvement. No migration or publication command is needed. Beta remains separate; formal audit stays deferred.


## Phase 4.2 owner acceptance and larger batches — 28 October 2026

After handover `f4c9976`, the owner reported “This phase passes” and requested more than two games per build to accelerate improving all 30. The assistant proposed five-to-six-game batches and a next six-game batch; the owner instructed “do so.” Record successful owner-reported Phase 4.2 acceptance and authorisation for the batch-size change. No detailed logs or separately identified independent beginner, actual-device performance, accessibility or real-backend browser evidence was supplied. These wider gates remain outstanding. The beta-access restoration from the prior report remains recorded; no new beta incident or change was requested.

## Phase 4.3 — Six Cyber Explorers games

Implemented 28 October 2026 from `f4c9976`, addressing FB-02/FB-04/FB-05. Privacy Patrol, Scam Spotter, Safe Social, Device Defender, Wi-Fi Wise and Digital Footprints each gain three objectives/tasks, six hints, stage-specific fictional records, finding reasoning and five explained optional review questions. The shared allowlisted registry/API/UI serves all nine guided missions. Accepted guide data, mission definitions, score/finding keys, historic runs and schema are unchanged. Review remains server-checked, owned-run scoped, ungraded and nonpersistent. No migration/publication, dependency changes or beta changes.

[Scope, complete commands and per-game acceptance](PHASE_4_EXPLORERS_BATCH.md). Tests now cover all nine guides and the browser matrix automatically covers every guide (36 desktop/mobile × 2D/3D journeys). Browser contexts remain isolated while the process is reused for faster batches; API-only content changes trigger browser CI. Local checks: 289 backend tests and 11 subtests passed, with 20 database-dependent skips; all 15 frontend unit tests, TypeScript and production build passed. Locked-environment pip check passed. HTTP checks use synthetic SQLite/overridden identity, not full authentication or PostgreSQL lock proof. Existing TestClient deprecation/CSS compatibility warnings remain as applicable. CI results are pending at this checkpoint, not inferred from added cases. Local Chromium's known UNIX-socket blocker remains. No owner database/computer, beta service or mail provider was accessed.

Next: verify CI, run owner development acceptance for all six games, then select the next five-to-six-game batch. Nine of 30 games have the guided pattern in source; Phase 4 and the wider educational/device/final-audit gates are not complete.


## Phase 4.3 CI evidence — 28 October 2026

Implementation `4e5df28` passed [backend run 40654992864](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40654992864): 289 tests and 11 subtests passed with 20 database-dependent skips in the unit job; 309 tests and 11 subtests passed against isolated PostgreSQL; dependency consistency/audit passed. The existing TestClient deprecation warning remains.

[Browser run 40654992839](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40654992839) passed all 48 browser cases, including 36 guided-mission journeys across all nine guides × desktop/mobile × 2D/3D. The job also passed 15 frontend unit tests, TypeScript and production build. Browser responses are intercepted synthetic API replies with actual static stage content; the separate API/PostgreSQL suite supplies grading and persistence evidence. No complete real-backend browser, production performance, independent learner understanding or final security clearance is claimed.

Next: follow [the complete Phase 4.3 guide](PHASE_4_EXPLORERS_BATCH.md) to update/restart development and accept Privacy Patrol, Scam Spotter, Safe Social, Device Defender, Wi-Fi Wise and Digital Footprints. No migration or publication command is needed. Nine of 30 guides are implemented; 21 remain. Keep beta separate and continue in approved five-to-six-game batches after acceptance.


## Phase 4.3 owner acceptance — 28 October 2026

After handover `954c086` and its six-game update/test/restart/acceptance guide, the owner reported “all test pass, lets go to next phase.” Record this as successful owner-reported local acceptance and authorisation for the next approved-size batch. No detailed logs, separately identified independent learner walkthroughs, actual-device performance, accessibility or full real-backend browser evidence were supplied. Do not infer these wider outcomes. No new beta incident or configuration change was requested.

## Phase 4.4 — Recovery and Cyber Academy batch

Implemented 28 October 2026 from `954c086` for FB-02/FB-04/FB-05. Added distinct goals, stage tasks/records, six hints, post-decision finding reasoning and five explained optional review questions to each of MFA Guardian, Backup Buddy, Operation Firewall, Network Watch, Web Defense and Cloud Perimeter. The accepted registry/API/UI now serves 15 guides: all ten Explorers plus five Academy games. Existing mission definitions, keys, scoring, saved history, schema and earlier guide content are unchanged. No migration/publication, dependency pin change or beta change.

[Complete commands, scope and acceptance](PHASE_4_RECOVERY_AND_ACADEMY.md). Backend cases expand to all 15 guides; the browser matrix contains 60 guided desktop/mobile × 2D/3D journeys with actual static content and catalogue-derived pathways. Browser responses are synthetic and not a full real-backend journey. Local Chromium's known UNIX-socket blocker remains. Local checks passed: 361 backend tests and 11 subtests, with 20 database-dependent skips; 15 frontend unit tests, TypeScript, production build and pip check passed. Existing TestClient deprecation/CSS compatibility warnings remain as applicable. These local HTTP checks use SQLite/overridden identity, not full authentication or PostgreSQL lock proof. CI is pending at this checkpoint. No owner computer/database, beta services or mail provider was accessed.

Next: verify CI and owner acceptance for the six games, then choose the next approved-size batch. Fifteen games remain. Phase 4, independent beginner/device assurance and final audit gates are not complete.
