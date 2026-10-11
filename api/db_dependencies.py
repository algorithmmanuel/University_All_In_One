"""Shared request-scoped SQLAlchemy session dependency.

All route modules import this callable. FastAPI dependency overrides continue
to work because the same function object is used throughout the application.
Sessions are closed on response completion; commits remain explicit in routes.
"""
from database import SessionLocal


def get_db():
    """Yield a request-scoped session without implicitly committing changes."""
    with SessionLocal() as session:
        yield session
