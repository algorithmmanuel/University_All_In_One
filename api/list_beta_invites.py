"""Show beta slot occupancy without exposing invite secrets."""
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import BetaInvite, User

def main():
    url = os.getenv("DATABASE_URL", "")
    if not url.startswith("postgresql+psycopg://") or url.split("?")[0].rsplit("/", 1)[-1] != "educyber":
        raise SystemExit("Set EduCyber development DATABASE_URL")
    engine = create_engine(url)
    try:
        with Session(engine) as db:
            for invite in db.scalars(select(BetaInvite).order_by(BetaInvite.id)):
                owner = db.get(User, invite.redeemed_by) if invite.redeemed_by else None
                status = ("occupied" if owner and owner.is_active else "inactive" if owner else "unused")
                print(f"Slot {invite.id}: {status}; owner={owner.email if owner else '-'}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()
