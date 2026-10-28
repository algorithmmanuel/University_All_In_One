# Development handover

**Last updated:** 28 October 2026 (Africa/Lagos).
**Checkpoint:** Combined Phase 5 has owner-reported local acceptance following the passing automated gates (594 backend tests + 11 subtests, 147 intercepted-API and 3 real-API browser cases). All planned Phase 5 implementation was delivered in one release. Phase 6 source inspection is complete. Owner redirected the next work toward consequential browser gameplay, richer cybersecurity courses and extensive practice; see [the current proposed plan](PHASE_6_GAMEPLAY_PLAN.md). English only; AI later. Next: settle the complete first playable build scope. Independent learner/device, operational and final security assurance gates remain open.
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

Plan the complete first playable strategy-game slice using [the current gameplay and learning plan](PHASE_6_GAMEPLAY_PLAN.md). Owner direction now prioritises a browser video-game experience inspired by ThreatGEN, richer cybersecurity lessons with public further reading, and extensive topic practice. Defer all Nigerian-language additions and the separate study helper; AI is a longer-term option. The recommended first build is one animated top-down/isometric Blue Team scenario with consequential actions, save/resume/debrief, supporting modules and 100 reviewed practice questions. Those build parameters remain proposals for discussion. The previous six-investigation/tutor recommendation is superseded; do not implement it as the next build.

Keep beta open and preserve operational and final security assurance gates. Formal security-audit-skill execution remains deferred until the end of development; ordinary secure coding/review/tests continue.

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


## Phase 4.4 CI evidence — 28 October 2026

Implementation `ad8f244` passed [backend run 40661421407](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40661421407): 361 tests and 11 subtests passed with 20 database-dependent skips in the unit job; 381 tests and 11 subtests passed against isolated PostgreSQL; dependency consistency/audit passed. The existing TestClient deprecation warning remains.

[Browser run 40661421374](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40661421374) passed all 72 browser cases, including 60 guided-mission journeys across all 15 guides × desktop/mobile × 2D/3D, plus existing course/navigation cases. The job also passed 15 frontend unit tests, TypeScript and production build. Browser responses are synthetic intercepted replies using actual static stage content and catalogue pathways; actual API/PostgreSQL checks separately verify grading and persistence. No complete real-backend browser, independent learner effectiveness, actual-device performance or final security clearance is claimed.

Next: use [the complete Phase 4.4 guide](PHASE_4_RECOVERY_AND_ACADEMY.md) to update/restart development and accept MFA Guardian, Backup Buddy, Operation Firewall, Network Watch, Web Defense and Cloud Perimeter. No migration or publication command is needed. Fifteen of 30 games have guidance implemented: all ten Explorers and five Academy games. Continue the remaining 15 games in approved batches after owner acceptance, keeping beta separate.


## Phase 4.4 owner acceptance — 28 October 2026

After handover `f4a2c67` and its six-game update/test/restart/acceptance guide, the owner reported “all tests pass, go on.” Record successful owner-reported local acceptance and authorisation for the next approved-size batch. No detailed log or separately identified independent learner, actual-device performance, accessibility or complete real-backend browser evidence was supplied. These wider gates remain open. No new beta incident or change was requested.

## Phase 4.5 — Academy and branch-response batch

Implemented 28 October 2026 from `f4a2c67`, addressing FB-02/FB-04/FB-05. Added distinct goals, tasks/records, six hints, post-decision finding reasoning and five explained optional review questions to each of Forensics Desk, Malware Clues, Identity Lab, Secure Code Review, Threat Hunter and Branch Resilience (mission ID incident-response; workspace title Ransomware at the Branch). All ten Explorer and all ten Academy games now have guides, plus one professional game, for 21 of 30. Previous guide data, mission definitions, keys, scoring, history and schema are unchanged. No migration/publication, dependency pin or beta change.

[Complete commands, scope and acceptance](PHASE_4_ACADEMY_AND_RESPONSE.md). Backend cases cover all 21 guides; unsupported-review checks choose a still-unregistered mission from source so the newly guided incident-response mission does not invalidate them. Browser coverage expands automatically to 84 guided desktop/mobile × 2D/3D journeys with catalogue pathways, including Cyber Command; replies remain synthetic. Local Chromium's known UNIX-socket blocker remains. Local checks passed: 433 backend tests and 11 subtests with 20 database-dependent skips; 15 frontend unit tests, TypeScript, production build and pip check passed. Existing TestClient deprecation/CSS compatibility warnings remain as applicable. HTTP tests use synthetic SQLite/overridden identity, not full authentication or PostgreSQL lock proof. CI is pending at this checkpoint. No owner computer/database, beta service or mail provider was accessed.

Next: verify CI and owner acceptance of the six games, then continue the nine remaining professional games. Phase 4 and the independent educational/device/final-audit gates are not complete.


## Phase 4.5 CI evidence — 28 October 2026

Implementation `08fd752` passed [backend run 40677079039](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40677079039): 433 tests and 11 subtests with 20 database-dependent skips in the unit job; 453 tests and 11 subtests against isolated PostgreSQL; dependency consistency/audit passed. The existing TestClient deprecation warning remains.

[Browser run 40677079256](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40677079256) passed all 96 browser cases, including 84 guided journeys across all 21 guides × desktop/mobile × 2D/3D and existing course/navigation cases. The job also passed 15 frontend unit tests, TypeScript and production build. Browser replies are synthetic with actual static content and catalogue pathways; separate API/PostgreSQL tests provide grading/persistence evidence. This is not a complete real-backend browser, actual-device performance, independent learning-effectiveness or final security result.

Next: use [the full Phase 4.5 guide](PHASE_4_ACADEMY_AND_RESPONSE.md) to update/restart development and accept Forensics Desk, Malware Clues, Identity Lab, Secure Code Review, Threat Hunter and Branch Resilience (workspace title Ransomware at the Branch). No migration or publication is needed. All ten Explorer and all ten Academy games plus one professional game have guided content: 21 of 30, with nine Cyber Command games remaining. Keep beta separate and continue approved batches after owner acceptance.


## Continuation authorisation after Phase 4.5 — 28 October 2026

After handover `683cbc8`, the owner instructed “go on.” This authorises the next development batch but supplies no separate Phase 4.5 local test result. Phase 4.5 owner acceptance and wider independent learner/device/operational/final assurance evidence remain pending. No new beta incident or change was requested. Continue the next six-game batch while preserving those acceptance records accurately.

## Phase 4.6 — Cyber Command batch

Implemented 28 October 2026 from `683cbc8` for FB-02/FB-04/FB-05. Added distinct goals, tasks/records, six hints, post-decision finding reasoning and five explained optional review questions to Risk Command, Zero Trust Briefing, Cloud Incident, Supply Chain Watch, Ransomware Recovery and Identity Crisis. The shared registry/API/UI now serves 27 guides: ten Explorers, ten Academy and seven Command games. Previous guide data, mission definitions, keys, scoring, saved history and schema are unchanged. No migration/publication, dependency pin or beta change.

[Complete commands, scope and acceptance](PHASE_4_COMMAND_BATCH.md). Backend cases cover all 27 guides; browser coverage automatically includes 108 guided desktop/mobile × 2D/3D journeys with actual static content/catalogue pathways and synthetic API replies. Local Chromium's known UNIX-socket limitation remains. Local checks passed: 505 backend tests and 11 subtests, with 20 database-dependent skips; 15 frontend unit tests, TypeScript, production build and pip check passed. Existing TestClient deprecation/CSS compatibility warnings remain as applicable. Local HTTP cases use SQLite/overridden identity, not full authentication or PostgreSQL lock proof. CI is pending at this checkpoint. No owner computer/database, beta service or mail provider was accessed.

Next: verify CI and local acceptance for this batch, record Phase 4.5 results when supplied, then finish Boardroom Breach, AI Governance and Audit Trail. Phase 4 and wider assurance gates remain open.


## Phase 4.6 CI evidence — 28 October 2026

Implementation `57f395b` passed [backend run 40679518968](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40679518968): 505 tests and 11 subtests with 20 database-dependent skips in the unit job; 525 tests and 11 subtests against isolated PostgreSQL; dependency consistency/audit passed. The existing TestClient deprecation warning remains.

[Browser run 40679519091](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40679519091) passed all 120 browser cases, including 108 guided desktop/mobile × 2D/3D journeys across all 27 guides and existing course/navigation cases. The job also passed 15 frontend unit tests, TypeScript and production build. Browser replies are synthetic with actual static content and catalogue pathways; separate API/PostgreSQL cases verify grading/persistence. No complete real-backend browser, actual-device performance, independent educational effectiveness or final security assurance result is claimed.

Next: use [the full Phase 4.6 guide](PHASE_4_COMMAND_BATCH.md) to update/restart development and accept the six Command games, and report the still-outstanding Phase 4.5 local checks. No migration or publication is needed. Twenty-seven of 30 guides are implemented; Boardroom Breach, AI Governance and Audit Trail remain. The owner authorised continuing development but did not assert Phase 4.5 acceptance. Keep beta separate and preserve all wider gates.


## Phase 4.6 owner acceptance — 28 October 2026

After handover `1193d5f`, the owner reported: “all tests passed.” Record successful owner-reported local acceptance of the latest six-game Command batch. No detailed local logs or separate Phase 4.5 acceptance, actual-device observations, independent learner results or security assurance evidence were supplied. Existing CI evidence and its scope remain as recorded above. This acceptance record changes documentation only; no beta service or database was accessed.

Next: complete the guidance upgrades for Boardroom Breach, AI Governance and Audit Trail, bringing implemented coverage to all 30 existing games once verified. Keep the outstanding wider roadmap gates open.


## Phase 4.7 — Final three Command guidance upgrades

Implemented 28 October 2026 from `94f3010` after owner-reported Phase 4.6 acceptance and authorisation to continue. Boardroom Breach, AI Governance and Audit Trail add nine tasks, 18 hints, 27 detailed records, post-decision explanations and 15 optional explained review questions for FB-02/FB-04/FB-05. All 30 existing games now have guidance (ten per pathway), with 150 optional review questions. Source coverage does not establish independent educational success or actual-device performance.

The shared registry and parameterised backend/browser suites include all three. Underlying definitions, keys, scoring, existing history/schema and earlier guidance are preserved. No migration/publication, dependencies or beta service changes. [Complete PowerShell blocks and acceptance](PHASE_4_FINAL_COMMAND_GAMES.md). Local verification passed: 541 backend tests and 11 subtests with 20 database-dependent skips; 15 frontend unit tests, TypeScript, production build and pip check passed. The TestClient deprecation warning remains. Local HTTP tests use SQLite/overridden identity; local Chromium remains blocked by its known UNIX-socket limitation. CI is pending at this checkpoint; no owner computer/database or mail provider was accessed. Phase 4.7 local acceptance and wider gates remain open.


## Phase 4.7 verification follow-up — 28 October 2026

Implementation `576fe7d` passed [backend run 40682317930](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40682317930): 561 tests and 11 subtests against isolated PostgreSQL; the unit and dependency jobs passed. The existing TestClient deprecation warning remains. [Browser run 40682317923](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40682317923) passed all 132 cases: 120 guided journeys across all 30 games × desktop/mobile × 2D/3D, plus existing course/navigation cases. The job also passed 15 frontend unit tests, TypeScript and production build. Browser replies use synthetic API responses with actual static content/catalogue pathways; separate HTTP/PostgreSQL tests verify grading and persistence. This is not a complete real-backend browser, actual-device performance, independent educational or final security result. Phase 4.7 owner acceptance remains pending.

A preliminary source check for the next phase found that `quiz_routes.py` and `web/app/assessments/page.tsx` provide saved score/count history and per-answer explanations, but no topic-level results or tailored recommendations. `QuizQuestion` has no objective/topic field, and `QuizAttempt` saves answers and aggregate scores without a versioned topic-analysis snapshot. Phase 5 should define objective mapping, evidence limits and historical compatibility before claiming persistent topic strengths/weaknesses. No Phase 5 behaviour or schema is changed by this batch.


## Phase 4.7 owner acceptance — 28 October 2026

After handover `5da4e8b`, the owner reported: “All tests pass.” Record successful owner-reported local acceptance of Boardroom Breach, AI Governance and Audit Trail. No detailed local logs, separate Phase 4.5 acceptance, independent learner/device observations or final security evidence were supplied. This documentation-only update does not change application source, beta services or databases.

Next: begin Phase 5 progression/results/usability improvements using the source observations above. All 30 guidance implementations are delivered; the wider educational/device gate remains open.


## Phase 5.1 — Assessment results and next steps (FB-03)

Implemented 28 October 2026 from `5567e76`. New server-authored attempt snapshots preserve reviewed objective counts, sample limits, original answer explanations and lesson recommendations across catalogue changes. Each of the three published foundations courses has nine stable objectives; unmatched/customized/unpublished items receive no guessed topic credit. Duplicate prompts count once as topic evidence. Historical attempt answers/scores/timestamps are retained with no inferred or regraded topic history. Owned result reopening and lesson deep links are implemented; no aggregate mastery/learning-gain claim is made.

Migration `0010_attempt_results` adds one nullable JSON column without backfill. An explicit development-only migrator reuses branch/interpreter/dedicated-database/environment guards and refuses occupied development ports. Beta was not accessed. See [scope, evidence contract, complete PowerShell blocks, recovery limits and acceptance](PHASE_5_RESULTS.md).

Assistant verification: 560 backend tests and 11 subtests passed with 20 database-dependent skips; the subsequent focused results/migration/launcher run passed all 22 cases, including three new launcher guard tests. All 15 frontend unit tests, TypeScript, production build and pip check passed. Migration preservation was exercised on synthetic populated SQLite, and HTTP feature tests override authentication. PostgreSQL/real-session assertions and CI are pending at this checkpoint. Three new browser tests could not launch Chromium because the workspace denied its required UNIX socket; no local browser assertion is credited. Existing CSS/TestClient warnings remain.

This is a bounded Phase 5 source milestone, not completion of the full phase. Dashboard previews, wider progression and outstanding usability/device/learner evidence remain open. Phase 4.5 acceptance, independent Phase 4 evidence, operational assurance and final formal security audit remain outstanding. Next: verify CI and development migration/acceptance using the linked guide.

Phase 5.1 subsequent CI: implementation `32549cd` passed [backend run 40686917851](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40686917851). Migration and the complete suite passed with isolated PostgreSQL available: 583 tests and 11 subtests, including real-session result ownership checks. The many synthetic content fixtures remain SQLite/auth-overridden by design. Database-independent and dependency audit jobs passed as well. The first browser run passed all 132 existing journeys plus two new cases (134/135); the new mobile test failed because it enumerated the question fields before asynchronous loading completed. The test now waits for all five fields, with no product-source change. Corrected browser verification is pending.

Corrected browser checkpoint: source `d64bf41`, [run 40688326456](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40688326456), passed the dedicated three new assessment-evidence browser cases, all 15 frontend unit tests, TypeScript and production build. The second 132-case baseline run remains in progress; the initial run already passed those cases against identical application source. The first workflow was not green (134/135); its mobile synchronization failure is now verified fixed in the dedicated step. Check final rerun status before calling the full workflow green. Development migration/owner acceptance are still pending.


### Phase 5.1 final CI outcome — 28 October 2026

Resumed after a workspace-credit interruption and verified [browser run 40688326456](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40688326456) completed successfully at source `d64bf41`. Logs show 3/3 new assessment-evidence cases and 132/132 existing browser journeys passed, plus all 15 frontend unit tests, TypeScript and production build. This supersedes the earlier in-progress browser checkpoint. API replies in browser tests are synthetic; real-backend browser and independent learner/device gates remain open. Backend/PostgreSQL run 40686917851 passed 583 tests and 11 subtests as recorded above.

The credit interruption prevented the preceding draft handover from reaching the branch; this update reconciles the final observed outcome. Next: stop only development services, follow the complete Phase 5.1 update/migration/test/restart blocks, and perform local acceptance. No owner migration or acceptance has been reported. Beta remains unchanged; defer wider Phase 5 work until this bounded build is accepted.


## Phase 5.1 owner acceptance — 28 October 2026

After receiving handover `e272f34`, the complete development migration/update/test/restart guide and acceptance checklist, the owner reported: "All tests pass". Record this as successful owner-reported local checks/acceptance. No detailed logs or separately identified mobile, independent learner, real-backend browser or operational evidence was supplied; do not infer those outcomes.

## Phase 5.2 — Saved dashboard progress and usability

Implemented after the Phase 5.1 acceptance above. Source inspection confirmed missing saved-progress dashboard previews and an unbounded dashboard logout request. Added a read-only student overview of owned, enrolled published course progress, first incomplete lessons and chronological recent attempts; previews are limited to three courses/attempts. Added lesson/result navigation, loading/empty/error-retry behavior, and bounded dashboard logout/local token removal. No data migration, content publication or dependency change. Existing history is preserved. See [scope, complete commands, acceptance and limits](PHASE_5_DASHBOARD.md).

Assistant checks: 570 backend tests and 11 subtests passed with 20 database-dependent skips; all 15 frontend unit tests, TypeScript, production build, pip check and whitespace checks passed. New HTTP fixtures use synthetic SQLite/overridden identity; real-session overview assertions are included in PostgreSQL CI. Five new browser cases join the early progression step; no local browser assertions are credited. CI and owner development acceptance remain pending at this source checkpoint. Formal audit remains deferred; no beta source/data/service or owner database was accessed.

Next: verify Phase 5.2 CI, then update/restart development and run local acceptance using the linked guide. Keep independent learner/device, full real-backend browser and operational/final security gates open.

Phase 5.2 subsequent CI: [backend run 40698410040](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40698410040) passed 590 tests and 11 subtests with isolated PostgreSQL available, including real-session overview access checks; unit/dependency jobs passed. A browser test assertion was scoped to the saved-progress panel so Next.js's separate route-announcement alert is not counted as a progress error; no application source changed for that fix. Source `9edc7e4`, [browser run 40698843615](https://github.com/algorithmmanuel/University_All_In_One/actions/runs/40698843615), passed all eight progression cases plus frontend unit/type/build checks. The corrected browser run completed successfully: 132/132 existing journeys passed in addition to the eight progression cases, for 140/140 browser cases. This supersedes the initial failed test-assertion checkpoint; browser API replies remain synthetic. Owner acceptance of Phase 5.2 remains pending.


### Phase 5.2 final source handover

Source implementation `003fed0` passed backend/PostgreSQL run 40698410040 (590 tests and 11 subtests). Test-assertion correction `9edc7e4` passed browser run 40698843615 (140 cases), frontend unit/type/build checks included. No application code changed for the test correction. The handover records the owner's Phase 5.1 acceptance but does not infer Phase 5.2 acceptance. Next: update/restart development and complete the Phase 5.2 checklist; no new migration/content publication. Beta remains unchanged, and the formal audit stays deferred.


## Combined Phase 5 release — owner batching direction, 28 October 2026

The owner clarified that Phase 5.2 had not been installed and requested all remaining Phase 5 work at once. This supersedes the previous next-action requirement to accept 5.2 separately. No 5.2 owner acceptance is recorded. Scope now includes the uninstalled 5.2 dashboard changes plus owned mission progress/reopening and original saved decision recaps, older assessment/mission history access, onboarding feedback focus, dark/mobile readability/layout fixes, shared bounded home/dashboard logout and failed-load recovery. No further planned incremental Phase 5 feature releases are required before the combined acceptance; fix defects as needed. See [the unified scope/evidence matrix and complete guide](PHASE_5_RELEASE.md).

Local checks: 574 backend tests and 11 subtests passed with 20 database-dependent skips; 15 frontend unit tests, TypeScript, clean production build and pip check passed. Seven mock-browser cases and two real-API/PostgreSQL browser journeys were added; combined CI remains pending at this checkpoint. Tests and fixtures use synthetic data only. No beta source/services, owner database or mail provider was accessed. New source introduces no migration beyond the accepted Phase 5.1 schema.

Next: verify all combined CI gates and hand over one release for development update/acceptance. Keep independent learner/device/operational evidence and the final formal security audit open.

Combined Phase 5 subsequent checks: application source `c0d5e75` passed backend/PostgreSQL run 40728223888 with 594 tests and 11 subtests, unit/dependency checks included. Real API browser run 40728223984 passed all three cases, including both new desktop/mobile registration→lesson/assessment persistence→dashboard/result→server-verified logout journeys. The intercepted-API job exposed an older fixture's missing mission-progress response and broad two-panel alert locator; fixtures were corrected at `def9fae` without application-source changes. Corrected progression checks passed; full intercepted-API and automatic real-API reruns are pending at this drafting checkpoint.


## Combined Phase 5 final handover — 28 October 2026

All planned Phase 5 implementation is bundled; no further planned 5.3/5.4 feature releases or intermediate 5.2 installation are required. Application source `c0d5e75` passed backend/PostgreSQL run 40728223888 (594 tests and 11 subtests, unit/dependency jobs included). Test-fixture correction `def9fae` passed intercepted-API browser run 40728703388 (147 cases: 15 progression + 132 existing), frontend unit/type/build checks, and real-API browser rerun 40728703380 (3 cases including desktop/mobile registration through saved learning/assessment results and server-verified logout). No application source changed for the fixture correction. These outcomes supersede the earlier in-progress checks.

The owner explicitly has not installed Phase 5.2; no acceptance of it or the combined release is inferred. Next: use [the one combined release guide](PHASE_5_RELEASE.md) to update/schema-check/test/restart development, then complete one combined local acceptance pass. Keep beta open and unchanged. Independent learner/device, wider real-backend/operational and final formal security-audit gates remain open; defects can still require fixes.


## Combined Phase 5 owner acceptance — 28 October 2026

After receiving combined release handover `f081cb8` and its single update/schema-check/test/restart and acceptance guide, the owner reported: "all test passed". Record this as successful owner-reported local checks/acceptance of the combined Phase 5 build, including the previously uninstalled Phase 5.2 changes. No separate incremental 5.2 acceptance is required.

No detailed logs or separately identified independent learner/physical-device, accessibility, operational-recovery or formal security evidence was supplied. Do not infer those outcomes or promotion to beta. Earlier CI evidence remains as recorded; this acceptance update changes documentation only and does not rerun application tests.

Next: inspect the actual Phase 6 catalogue/tutor gaps and define a cohesive build from evidence; retain the existing 30-game inventory and outstanding assurance gates.


## Phase 6 source inspection — 28 October 2026

Inspected clean development source `9950eed`; [inventory, gaps, prerequisites and next-build acceptance contract](PHASE_6_SCOPE.md) now recorded. All 30 games already have guides (ten per pathway), 90 stages, 260 detailed artifacts and 150 optional review questions. The active guided UI selects shared artifact cards; older themed investigation components are fallbacks, and correlation/hypothesis work remains a local ungraded scratchpad. Source inspection found no web/API tutor or Yoruba/Igbo content. Do not count the AI Governance mission as tutor support.

Executed static-source inventory checks confirm catalogue/mission/guide alignment and matching artifact/evidence counts across every stage. Seven dependency-free frontend assertions passed; the full Node unit invocation could not load two test files because TypeScript is absent, and pytest is unavailable in this fresh checkout. No new full regression/build/browser/PostgreSQL result is claimed. No application source, dependencies, schema, owner runtime/database or beta was changed, and no formal audit ran. Previous Phase 5 CI and owner-reported acceptance remain unchanged; Phase 4.5 separate local acceptance and wider assurance gates remain open.

Next: implement one development build with six deeper Academy investigation practices plus the deterministic source-linked study-helper foundation specified in the contract. Yoruba/Igbo publication needs fluent review; a future generative provider needs separate data/cost/safety decisions and evaluation. This documentation checkpoint requires no local installation or restart.


## Owner vision correction and planning — 28 October 2026

The owner requested planning for an interactive cybersecurity browser game inspired by ThreatGEN, deeper cybersecurity courses with public reading links and a practice bank potentially around 500 questions across topics; AI can follow longer term. Explicitly defer Yoruba, Igbo and all other Nigerian-language additions. The previous six-investigation and tutor-foundation next-build recommendation is superseded.

[The proposed gameplay and learning plan](PHASE_6_GAMEPLAY_PLAN.md) records public reference research, the current source gap, an original strategy-game pilot, course/source quality rules, proposed ten-topic/500-question allocation, practice-session changes and staged acceptance targets. The inspected curated source has three course banks of 20 questions each; this does not count installed database rows or the separate 150 mission reviews. Current explicit-length selection repeats the same sample, so varied practice requires server-pinned sessions rather than only increasing the bank.

Documentation/planning only: no application code, dependencies, migrations, published content, beta or owner runtime changed; no new application test pass is claimed. Public ThreatGEN descriptions were reviewed, not a signed-in gameplay session. Owner requirements are distinguished from proposed gameplay/release details and numeric targets.

Next: discuss the proposed Build A style/scope, then implement one complete consequential-game foundation with aligned teaching/practice. Preserve historic scores/progress and all outstanding learner/device/operational/final-audit evidence gates.
