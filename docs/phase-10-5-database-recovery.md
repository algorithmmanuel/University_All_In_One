# Phase 10.5 - PostgreSQL backup-and-restore rehearsal

GitHub Actions runs the **Isolated PostgreSQL recovery rehearsal** on two disposable PostgreSQL 17 service containers. This is deliberately **not** an operation against the developer's existing `educyber` database, Docker volumes or a production database.

## Recovery acceptance criteria

1. Create and migrate a disposable source database `educyber_test` on CI port 55431.
2. Insert a synthetic learner and a partially completed professional mission.
3. Create a PostgreSQL custom-format archive with `pg_dump`.
4. Restore it into a separate, initially empty `educyber_restore_test` database on port 55432 using `pg_restore`.
5. Verify the restored learner, mission step, score, choices and Alembic migration revision.
6. Remove the temporary archive; CI service containers are ephemeral.

The script **refuses all other database URLs**, preventing accidental invocation against development or production. Its CI-only credentials are hard-coded solely as a safety constraint for disposable test databases; they must never be used for real services.

## Production boundaries

A successful CI rehearsal proves logical backup/restore behavior for the tested schema and sample data. It does **not** prove production recovery time objectives, backup encryption, off-site retention, key management, point-in-time recovery, or a full-scale disaster recovery plan. Do not set `EDUCYBER_BACKUP_VERIFIED=yes` in production solely because this CI rehearsal passes. A separate, documented production recovery drill remains necessary.
