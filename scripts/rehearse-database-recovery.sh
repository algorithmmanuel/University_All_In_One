#!/usr/bin/env bash
set -euo pipefail

# This script intentionally refuses arbitrary hosts, names or destinations.
# Only the ephemeral CI database pair is permitted.
: "${SOURCE_DATABASE_URL:?SOURCE_DATABASE_URL required}"
: "${RESTORE_DATABASE_URL:?RESTORE_DATABASE_URL required}"
: "${PGPASSWORD:?PGPASSWORD required}"
source_expected="postgresql://educyber_ci:ci_only_password@127.0.0.1:55431/educyber_test"
restore_expected="postgresql://educyber_ci:ci_only_password@127.0.0.1:55432/educyber_restore_test"
if [[ "$SOURCE_DATABASE_URL" != "$source_expected" || "$RESTORE_DATABASE_URL" != "$restore_expected" ]]; then
  echo "REFUSED: only the two dedicated CI PostgreSQL databases are permitted" >&2
  exit 2
fi
if [[ "$SOURCE_DATABASE_URL" == "$RESTORE_DATABASE_URL" ]]; then
  echo "REFUSED: source and destination must differ" >&2
  exit 2
fi

for command in pg_dump pg_restore psql; do
  command -v "$command" >/dev/null || { echo "Missing $command" >&2; exit 2; }
done

archive="$(mktemp /tmp/educyber-recovery-XXXXXX.dump)"
trap 'rm -f "$archive"' EXIT

# Seed representative mission progress and session data without touching real users.
psql "$SOURCE_DATABASE_URL" -v ON_ERROR_STOP=1 <<'SQL'
INSERT INTO users (full_name, email, password_hash, role, is_active, is_approved)
VALUES ('Recovery Test Learner', 'recovery@example.invalid', 'disabled-test-hash',
        'student', true, true);
INSERT INTO mission_runs (user_id, mission_id, step_index, score, choices)
SELECT id, 'risk-command', 2, 25, '[{"step":0,"points":10},{"step":1,"points":15}]'::json
FROM users WHERE email='recovery@example.invalid';
SQL

pg_dump --format=custom --no-owner --no-acl --file="$archive" "$SOURCE_DATABASE_URL"
test -s "$archive"
pg_restore --exit-on-error --no-owner --no-acl --dbname="$RESTORE_DATABASE_URL" "$archive"

# Validate both schema revision and exact representative learner state.
psql "$RESTORE_DATABASE_URL" -v ON_ERROR_STOP=1 -At <<'SQL' | grep -Fx '1|2|25|2'
SELECT COUNT(*)::text || '|' || MAX(m.step_index)::text || '|' ||
       MAX(m.score)::text || '|' || MAX(json_array_length(m.choices))::text
FROM users u JOIN mission_runs m ON m.user_id=u.id
WHERE u.email='recovery@example.invalid' AND m.mission_id='risk-command';
SQL

source_revision="$(psql "$SOURCE_DATABASE_URL" -At -c 'SELECT version_num FROM alembic_version')"
restore_revision="$(psql "$RESTORE_DATABASE_URL" -At -c 'SELECT version_num FROM alembic_version')"
if [[ -z "$source_revision" || "$source_revision" != "$restore_revision" ]]; then
  echo "FAIL: schema migration revision mismatch" >&2
  exit 1
fi

echo "RECOVERY VERIFIED: isolated schema and representative mission progress restored."
