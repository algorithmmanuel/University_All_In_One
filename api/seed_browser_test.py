"""Create an ephemeral student session for browser-to-real-API tests.

Only an isolated localhost PostgreSQL database named educyber_test is allowed.
Outputs JSON with a bearer token; never print this in CI logs.
"""
import json
import os
import uuid
from sqlalchemy.engine import make_url


def main():
    """Seed only when explicitly executed, never during pytest collection."""
    _seed()


def _seed():
    url = os.environ.get("DATABASE_URL", "")
    test_url = os.environ.get("TEST_DATABASE_URL", "")
    if not url or url != test_url:
        raise SystemExit("Refusing to seed without identical DATABASE_URL and TEST_DATABASE_URL")
    parsed = make_url(url)
    if (not parsed.drivername.startswith("postgresql") or
            parsed.database != "educyber_test" or
            parsed.host not in ("127.0.0.1", "localhost")):
        raise SystemExit("Refusing to seed outside isolated localhost educyber_test")
    
    from database import engine
    from sqlalchemy.orm import Session
    from models import User
    from auth import issue_session
    
    with Session(engine) as db:
        user = User(full_name="Browser Test Learner",
                    email=f"browser-e2e-{uuid.uuid4().hex}@example.invalid",
                    password_hash="e2e-disabled-password",
                    role="student", is_active=True, is_approved=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = issue_session(db, user)
        print(json.dumps({"token": token, "user_id": user.id}))
    

if __name__ == '__main__':
    main()
