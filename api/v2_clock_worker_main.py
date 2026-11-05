"""Foreground development-only deadline worker for isolated timed matches.

Start via scripts/development.py clock-worker, NEVER with a copied Beta .env.
A separate process handles deadlines even if all browsers are closed. Once
serverless hosting is selected, replace this loop with a supervised scheduler
calling the same transactionally locked process_due_once.
"""
import os
import time

from cyber_warfare.v2_timeout_worker import process_due_once
from database import SessionLocal
from development_runtime import validate_development_database


def main():
    if os.environ.get("EDUCYBER_ENV") != "development":
        raise ValueError("V2 clock worker requires isolated development mode")
    validate_development_database(os.environ.get("DATABASE_URL", ""))
    print("Isolated V2 Development clock worker started; no Beta data accessed.", flush=True)
    try:
        while True:
            try:
                with SessionLocal() as db:
                    process_due_once(db)
            except Exception as exc:
                # Database exceptions can contain private configuration. Log
                # only the exception class; retain fail-closed state.
                print("V2 clock check failed (" + type(exc).__name__ +
                      "); inspect isolated development storage.", flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Development clock worker stopped.", flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
