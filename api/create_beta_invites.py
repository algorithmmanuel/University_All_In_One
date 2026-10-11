"""Create six single-use signup codes. Accounts remain reusable after redemption.

Run locally only after migration 0008; requires DATABASE_URL and explicit confirmation.
Codes are printed once. Do not commit or log them.
"""
import argparse
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from models import BetaInvite

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    if not args.confirm or not (1 <= args.count <= 6) or not (1 <= args.days <= 90):
        parser.error("Require --confirm, --count 1..6 and --days 1..90")
    url = os.getenv("DATABASE_URL", "")
    if not url.startswith("postgresql+psycopg://") or "/educyber" not in url.split("?")[0]:
        parser.error("Expected explicit EduCyber PostgreSQL DATABASE_URL")
    engine = create_engine(url)
    codes = []
    with Session(engine) as db:
        now = datetime.now(timezone.utc)
        existing = db.scalar(select(func.count()).select_from(BetaInvite)) or 0
        if existing + args.count > 6:
            parser.error("Cohort limit is six total invitations. No codes created.")
        for _ in range(args.count):
            code = secrets.token_urlsafe(32)
            db.add(BetaInvite(code_hash=hashlib.sha256(code.encode()).hexdigest(),
                              expires_at=now + timedelta(days=args.days)))
            codes.append(code)
        db.commit()
    print("Share each invitation code privately with exactly one tester:")
    for i, code in enumerate(codes, 1):
        print(f"Tester {existing+i}: {code}")
    print("Codes are for registration only. Testers can sign in repeatedly after signup.")
    engine.dispose()

if __name__ == "__main__":
    main()
