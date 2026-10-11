# Phase 8 authentication operations

## Implemented
- Login: per-normalized-email atomic PostgreSQL bucket, 10 requests per five-minute window.
- Registration: separate per-email bucket, five requests per five-minute window.
- Auth events: allowlisted event names only; never include passwords, bearer tokens, email addresses, or request bodies.
- Retention: `security_maintenance.purge_expired_auth_records(db)` removes expired sessions and login/registration buckets older than one day. Schedule externally; do not run per HTTP request.

## Required before public deployment
1. Apply Alembic migration `0006_login_limits` to the target environment before enabling the throttled endpoints. The test database migration alone does not migrate development or production.
2. Schedule a single authenticated maintenance job with restricted DB permissions; monitor errors and cleanup counts.
3. Add gateway/WAF rate limits by verified client IP, request size limits, bot detection, and registration quotas. Per-email buckets alone do not stop attackers rotating addresses.
4. Assess denial-of-service implications of account-only throttling; consider separate IP+account signals, progressive delays, and safe recovery.
5. Route structured event logs to a protected sink with access control and retention. Do not infer IP from untrusted forwarding headers.
6. Verify GitHub Actions test and dependency-audit jobs; add secret scanning and PostgreSQL integration CI as separate quality gates.
7. Evaluate registration account enumeration, email verification, abuse handling, and child privacy before launch.

## Security verification
Run `python -m pytest -q` with `TEST_DATABASE_URL` pointing to local `educyber_test`. Keep `DATABASE_URL` absent or identical during test runs. Review test failures before any merge.
