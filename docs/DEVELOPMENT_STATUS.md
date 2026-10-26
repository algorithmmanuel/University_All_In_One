# Development handover

**Last updated:** 26 October 2026 (Africa/Lagos).  
**Checkpoint:** owner reported the complete baseline learner checklist passed. Assessment-length choices and activity focus/scroll are implemented and tested; updated-build Windows/browser acceptance is pending.  
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

## Exact next action

**Update only the development checkout, restart only its services and accept the two new features locally.**

1. Stop the development API/frontend foreground processes while leaving beta services and its tunnel running.
2. Fetch and fast-forward the development branch, preserve local setup files and install the updated development Python requirements.
3. Run the focused assessment HTTP tests, frontend typecheck/unit tests and restart the guarded development API/frontend launchers.
4. Run the existing runtime isolation check and confirm beta remains healthy separately.
5. Test Quick, Extended and Custom lengths against the real development database; inspect saved totals/history. Test invalid custom sizes.
6. Open/reopen courses, start/resume missions and start assessments; verify automatic viewport movement and keyboard focus. Check mobile and reduced motion. Completing lessons or choosing answers must not jump back.
7. Record actual pass/fail evidence in this handover. Full PostgreSQL regression and real-browser automation are still outstanding.
8. Continue with the Cloudflare baseline audit prerequisites, local Compose review, dependency reproducibility and lint configuration work in the approved plan.

## Implemented source changes and checks

- Configurable server-side API/health proxy with validation; existing beta default and reset-password security headers preserved.
- Home game-library and logout requests now default to same-origin browser requests. Server-rendered pathway requests use the configured frontend origin.
- Guarded development launcher explicitly selects the development database and local services, removes inherited beta application/mail settings, refuses occupied ports and never runs migrations automatically.
- Development-only non-secret process identity endpoint; ordinary beta mode does not register it. The verification command requires direct and frontend-proxied identities to match.
- Added development requirements and a local startup/verification runbook. Existing local Compose setup remains pending review/commit.
- Focused verification in the assistant workspace: 6 Python unittest guard cases and 4 Node proxy/configuration cases passed. Python syntax compilation passed. These checks used no live beta database or mail service.
- Subsequent owner-supplied Windows output verifies successful development service startup and the runtime isolation check, plus continued beta HTTP health. This supports successful application startup but is not a full regression or browser result.
- The owner subsequently reported the baseline manual learner checklist passed. Latest-build assistant checks are listed above; updated-build Windows/browser acceptance and full regression remain pending.

## Outstanding work

- [x] Development frontend routing configuration implemented and runtime identity matching verified by the owner.
- [x] Startup configuration loading and inherited-environment guards implemented and unit tested.
- [x] Development API/frontend running; owner verified runtime isolation and database/schema readiness.
- [x] Owner reported all six baseline synthetic learner checks passed (registration/login, learning persistence, assessment, mission, feedback and logout). This is a manual report, not a full automated regression result.
- [ ] Dependency baseline comparison and controlled reproducibility plan. Broad requirements ranges were used during setup; do not assume development and beta installed identical versions.
- [ ] Real-backend browser and regression checks.
- [ ] Versioned release/recovery procedures and application-version feedback metadata.
- [ ] Cloudflare security-audit skill read at a pinned upstream revision, installed and executed under its required sandbox controls.
- [x] Assessment-length and activity-navigation feature code added; updated-build local acceptance pending.
- [ ] Other feedback-driven learning and mission improvements.
- [ ] Later phases of the approved roadmap.

The Cloudflare audit and full regression suite have not run. The owner reported the baseline manual learner checklist passed before the latest changes. Latest assessment feature HTTP tests and frontend unit/build checks passed as listed above; updated-build real-browser and Windows acceptance remain pending.

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


