# Phase 8.4 — Operational security and deployment readiness

**Status: preparation only. No production deployment has been performed.**

## Before public deployment

1. Use a dedicated production PostgreSQL database and a least-privilege application role. Store credentials in the hosting platform's secret manager, not Git or client-side `NEXT_PUBLIC_*` variables. Rotate credentials after any exposure.
2. Set `EDUCYBER_ENV=production`, `DATABASE_URL`, `EDUCYBER_CORS_ORIGINS` to exact HTTPS frontend origin(s), and `EDUCYBER_PUBLIC_HOST` to the intended API hostname. Run `python -m deployment_checks` from `api/` as a deployment preflight. This is an **offline configuration check**, not a substitute for network, TLS, identity or database verification.
3. Terminate TLS at a trusted reverse proxy, apply request-size and IP/bot rate limits at the edge, and restrict `/health/db` to internal monitoring. Disable or restrict publicly accessible API docs according to deployment policy.
4. Use separate development, staging and production databases. Apply Alembic migrations with a backup and rollback plan; never run tests against production. Limit outbound database access and inbound administrative access.
5. Schedule `purge_expired_auth_records` with a separate operations job, and record aggregate success/failure metrics. Never log access tokens, passwords, email addresses or full request payloads.
6. Configure daily encrypted PostgreSQL backups, restricted access, offsite retention, and periodic **restoration tests**. Agree RPO/RTO before launch; do not claim backup readiness until restoration is demonstrated.
7. Route structured authentication event counts to monitoring with alert thresholds, secure retention and access control. Add application availability/error metrics and an incident escalation process.
8. For child users, complete age-appropriate consent, safeguarding, privacy notice, account deletion, data minimization, retention and access-rights review under applicable Nigerian law. Treat this as a public-launch gate.
9. Review production dependency vulnerabilities, Android client security, browser accessibility, load tests and independent application security testing before inviting broad public traffic.

## Local configuration check (example, not a deployment)

Run only after populating real environment values in your hosting platform or a temporary local process environment:

```powershell
Set-Location api
python -m pytest test_deployment_checks.py -q
# For actual production configuration only:
# python -m deployment_checks
Set-Location ..
```

The configuration validator deliberately never prints database credentials. It rejects a local/test database and insecure CORS values, but it does not prove that the credentials work or the service is reachable.

## Operational acceptance evidence to collect

- Production architecture, inventory, domains, TLS and secret ownership.
- Signed-off restore drill with measured RPO/RTO.
- Logs and alerts tested without personal data leakage.
- Threat model, access review, vulnerability and penetration test results.
- Privacy and child safeguarding approval before public release.

**Decision:** keep the Phase 8 pull request open until the new CI and local tests pass. Public launch requires the separate operational evidence above.
