# Phase 10.6 - Age-aware registration and safeguarding baseline

## Registration policy (initial conservative product rule)
- Date of birth is mandatory for **new** registrations and validated on the API.
- Under 13: registration rejected **before any user account is stored**. Guardian registration is not implemented.
- Ages 13–17: an inactive account is created, with no login or gameplay access until a verified guardian-consent/age-assurance process is built and reviewed. No self-service approval endpoint exists.
- Adults 18+: student account activated; teacher account still requires teacher approval.
- Age is calculated from DOB on the server. Self-declared DOB is **not proof of age**.
- The API's public user response excludes DOB and guardian consent state.

## Migration and existing accounts
Migration `0007_age_safeguards` adds nullable `users.date_of_birth`, `age_band` defaulting to `unverified`, and `guardian_consent_verified` defaulting to false. This **preserves existing accounts and data**. Existing users have not been age-verified; a separate re-verification and transition plan is required before public launch. Do not assume old accounts are adults.

## Before public release
- Confirm age-of-consent, guardian-consent and data protection obligations with qualified Nigerian counsel and for every launch jurisdiction; 13/18 are preliminary product boundaries, not legal conclusions.
- Implement verified guardian consent, consent withdrawal, age assurance proportionate to risk, retention/deletion schedules, data-subject requests and age transitions.
- Restrict database access to DOB and protect backups; do not collect identity documents by default.
- Complete safeguarding threat model and review potential social, messaging, profile and leaderboard features before enabling them for minors.
- Never mark guardian consent verified merely because a checkbox was ticked.

## Test
`./api/run-isolated-tests.ps1 -FullSuite` synchronizes the branch and runs tests against the isolated `educyber_test` PostgreSQL instance. Migration is applied **only** to the dedicated test database. The existing development database on port 5433 must be backed up and migration state inspected before any migration is applied there.

## Controlled development migration (Windows PowerShell)

From the repository root, while the existing `postgres` development service is running:

```powershell
.\scripts\prepare-age-migration.ps1
```

This is a **read-only preflight**: safely syncs GitHub, requires a clean working tree, checks Docker Compose's `postgres` service and the expected `educyber` database, and inspects the current Alembic revision. It does **not** modify the database.

Only after the preflight succeeds and you are ready to migrate, run:

```powershell
.\scripts\prepare-age-migration.ps1 -Apply
```

The `-Apply` command first creates a PostgreSQL custom-format backup, verifies the archive can be listed, and copies it into the ignored `local-backups/` directory **outside the container**. Only then does it apply migration `0007_age_safeguards` (if not already applied), followed by read-only schema verification. The backup is deliberately retained; never commit it, upload it publicly, or treat it as encrypted. Secure it and delete it under an approved retention plan. Do not use this command on production.

The script refuses unexpected branches, uncommitted files, database names, Docker service identities and schema revisions. If any check fails, **stop and inspect**; do not force a reset or run a blind migration. This operation cannot be executed on the user's laptop through GitHub Actions.
