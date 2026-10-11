# Phase 10.3 - Production safeguards and GitHub/local synchronization

## Safe developer workflow
The active branch is `feature/phase-9-platform-expansion`. GitHub Actions validate remote commits; they cannot directly change code on a Windows laptop.

- `./scripts/sync-before-test.ps1` fetches GitHub and fast-forwards only when safe. It refuses divergent branches and refuses to overwrite uncommitted changes. It does not push.
- `./api/run-isolated-tests.ps1 -FullSuite` invokes the synchronization check before running isolated PostgreSQL backend tests.
- `./web/run-local-checks.ps1` invokes the same check before frontend typechecking and tests. Add `-Build` only after stopping the Next.js development server.
- Optional periodic revision checks: `./scripts/install-periodic-sync.ps1` registers a Windows Task Scheduler job running every four hours while the computer is available. It only performs `git fetch` and writes status to `.git/educyber-sync/latest.txt`; it never merges, resets, or pushes. Remove it with `./scripts/install-periodic-sync.ps1 -Remove`.

If local modifications are present, the safe behavior is to stop before a GitHub fast-forward. Review `git status`, commit or stash deliberately, then rerun. No automated operation discards local changes.

## Production configuration
When `EDUCYBER_ENV=production`, API startup now rejects missing explicit HTTPS CORS origins, non-PostgreSQL database URLs, database URLs without explicit TLS requirements, unconfirmed edge rate limiting, and unconfirmed backup/recovery verification. Development behavior is unchanged.

`EDUCYBER_EDGE_RATE_LIMITING=enabled` and `EDUCYBER_BACKUP_VERIFIED=yes` are operator attestations, **not implementations**. Do not set them unless the corresponding external infrastructure and recovery drills are genuinely completed. These checks are not a substitute for production TLS certificate verification, WAF protections, monitoring, secret management, child privacy safeguards, and disaster recovery tests.

## Test boundaries
Chromium browser tests currently use a mocked API. Backend tests use real HTTP and isolated PostgreSQL. A complete browser-to-real-API integration suite and recovery rehearsal are still outstanding launch gates.
