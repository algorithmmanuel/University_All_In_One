# Development handover

**Last updated:** 26 October 2026 (Africa/Lagos).  
**Checkpoint:** development routing and guarded startup implemented and tested in isolation; Windows service startup and browser verification still pending.  
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

Recovery evidence establishes successful logical snapshot restoration and the stated checks. It does not establish off-site retention, encryption, point-in-time recovery, service recovery time or a complete application recovery drill.

## Exact next action

**Fetch the development changes, install dependencies and validate the isolated development runtime on Windows.**

1. Fast-forward only the development checkout to the latest development branch. Preserve local setup files and the beta worktree.
2. Follow [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md): install development Python requirements and frontend dependencies from the lockfile.
3. Run `scripts/development.py api` and `scripts/development.py web` with the development checkout's own Python in separate terminals.
4. Run `scripts/development.py check` in a third terminal. It must match API/proxy process identities and pass database/schema readiness and database identity checks. Confirm beta remains healthy separately.
5. Run frontend typecheck/unit tests and a synthetic learner browser journey. Record actual Windows outputs; do not infer success from the focused guard tests below.
6. Review the existing local non-secret Compose definition before committing it; no credential files or beta records belong in Git.
7. Inspect existing test/synchronisation wrappers before database suites: their branch expectations predate the current development branch. Do not switch the beta worktree to satisfy them.
8. Update this status with verified results before proceeding with the baseline security audit.

## Implemented source changes and checks

- Configurable server-side API/health proxy with validation; existing beta default and reset-password security headers preserved.
- Home game-library and logout requests now default to same-origin browser requests. Server-rendered pathway requests use the configured frontend origin.
- Guarded development launcher explicitly selects the development database and local services, removes inherited beta application/mail settings, refuses occupied ports and never runs migrations automatically.
- Development-only non-secret process identity endpoint; ordinary beta mode does not register it. The verification command requires direct and frontend-proxied identities to match.
- Added development requirements and a local startup/verification runbook. Existing local Compose setup remains pending review/commit.
- Focused verification in the assistant workspace: 6 Python unittest guard cases and 4 Node proxy/configuration cases passed. Python syntax compilation passed. These checks used no live beta database or mail service.
- Full application import/startup, Windows process behaviour, frontend typecheck, full regression suite and browser journeys remain unverified at this checkpoint.

## Outstanding work

- [x] Development frontend routing configuration implemented; runtime verification pending.
- [x] Startup configuration loading and inherited-environment guards implemented and unit tested.
- [ ] Development API/frontend running and validated.
- [ ] Dependency baseline comparison and controlled reproducibility plan. Broad requirements ranges were used during setup; do not assume development and beta installed identical versions.
- [ ] Real-backend browser and regression checks.
- [ ] Versioned release/recovery procedures and application-version feedback metadata.
- [ ] Cloudflare security-audit skill read at a pinned upstream revision, installed and executed under its required sandbox controls.
- [ ] Feedback-driven learning and mission improvements.
- [ ] Later phases of the approved roadmap.

The Cloudflare audit has not been run. No full regression suite or new learner-feature acceptance tests have run during this checkpoint. Focused isolation checks and successful migration/seeding are not replacements for those checks.

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

