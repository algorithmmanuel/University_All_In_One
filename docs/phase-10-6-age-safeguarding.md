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
