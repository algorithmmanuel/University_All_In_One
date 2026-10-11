# Phase 10.1: Migration-aware readiness and gameplay integration

EduCyber already has six Alembic revisions. The new read-only schema readiness check requires the current migration revision and the expected tables and columns. It never changes database data.

IMPORTANT: The development authentication rate-limit table was previously created manually. Before attempting any Alembic upgrade or revision stamp, inspect the database migration history and take a backup. A missing revision marker does not mean tables are absent. Never drop existing tables or stamp a revision without reconciling the actual schema.

The new test_full_gameplay_http.py executes three HTTP decision stages in all 30 games and verifies persisted scores and replay rejection. It uses only an isolated localhost PostgreSQL database named educyber_test and cleans up its own test records. Existing concurrency and access-control integration tests remain active.

Local checks from the api folder:
- python -m alembic current
- python -m alembic heads
- python -m pytest test_schema_readiness.py test_full_gameplay_http.py -q

The HTTP integration test does not automate clicking through 2D/3D browser controls. Browser end-to-end tests, production migration rehearsals, backup validation, monitoring, child privacy, and performance testing remain separate launch gates.
