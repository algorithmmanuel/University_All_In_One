"""Reassign an existing beta slot, retaining historic feedback."""
import argparse
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
from models import BetaInvite, AuthSession, User

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slot", type=int, required=True)
    p.add_argument("--expected-email", required=True)
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()
    if not args.confirm or args.slot < 1:
        p.error("Explicit --confirm and a positive slot number are required")
    url = os.getenv("DATABASE_URL", "")
    if not url.startswith("postgresql+psycopg://") or url.split("?")[0].rsplit("/", 1)[-1] != "educyber":
        p.error("Set the development EduCyber PostgreSQL DATABASE_URL")
    engine = create_engine(url)
    try:
        with Session(engine) as db:
            invite = db.scalar(select(BetaInvite).where(BetaInvite.id == args.slot).with_for_update())
            if invite is None:
                p.error("Slot not found")
            user = db.get(User, invite.redeemed_by) if invite.redeemed_by else None
            current = user.email if user else "unused"
            if current.lower() != args.expected_email.strip().lower():
                p.error("Slot owner mismatch; nothing changed")
            new_code = secrets.token_urlsafe(32)
            if user:
                user.is_active = False
                db.execute(delete(AuthSession).where(AuthSession.user_id == user.id))
            invite.redeemed_by = None
            invite.code_hash = hashlib.sha256(new_code.encode()).hexdigest()
            invite.expires_at = datetime.now(timezone.utc) + timedelta(days=30)
            db.commit()
        print("Slot reassigned; prior sessions revoked and account disabled.")
        print("Replacement code (copy privately; shown once):", new_code)
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()
