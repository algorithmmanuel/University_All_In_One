# Development handover

**Last updated:** 26 October 2026 (Africa/Lagos).  
**Checkpoint:** separate development database migrated and seeded; development API/frontend not yet started.  
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

**Finish development service isolation before starting the development API or frontend.**

1. Fetch the development branch and fast-forward the development worktree to the documentation commit. Preserve local setup files and the beta worktree.
2. Inspect `web/next.config.mjs`. The existing API and health rewrites hardcode the beta backend destination. A development frontend started unchanged could reach the beta API.
3. Make the server-side proxy target configurable, retaining existing beta behaviour. Explicitly configure development to its separate backend. Preserve reset-password security headers and inspect other API URL construction.
4. Add a supported development startup method that explicitly loads local development configuration, verifies the intended development database and prevents inherited beta database/email settings from overriding it. Keep development services bound to loopback.
5. Review and commit the non-secret development Compose definition and startup/configuration documentation. Keep credentials, private exports, database archives and virtual environments excluded.
6. Install frontend dependencies from the repository lockfile if present. Start development API/frontend separately, preserving the beta services and tunnel.
7. Verify direct API readiness and frontend-proxied requests. Prove the frontend reaches development, rather than assuming that HTTP success establishes isolation. Confirm beta remains healthy.
8. Create synthetic development learners through supported flows and verify a representative browser journey.
9. Run meaningful checks against isolated test data. Inspect `api/run-isolated-tests.ps1` and its call to `scripts/sync-before-test.ps1` before use; repository synchronisation must not unexpectedly alter the beta worktree.
10. Record verified results here before marking runtime isolation complete and proceeding with the baseline security audit.

## Outstanding work

- [ ] Development frontend proxy isolation.
- [ ] Startup configuration loading and inherited-environment safeguards.
- [ ] Development API/frontend running and validated.
- [ ] Dependency baseline comparison and controlled reproducibility plan. Broad requirements ranges were used during setup; do not assume development and beta installed identical versions.
- [ ] Real-backend browser and regression checks.
- [ ] Versioned release/recovery procedures and application-version feedback metadata.
- [ ] Cloudflare security-audit skill read at a pinned upstream revision, installed and executed under its required sandbox controls.
- [ ] Feedback-driven learning and mission improvements.
- [ ] Later phases of the approved roadmap.

The Cloudflare audit has not been run. No full regression suite or new feature acceptance tests have run during this setup checkpoint. Successful migration/seeding is not a replacement for those checks.

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
