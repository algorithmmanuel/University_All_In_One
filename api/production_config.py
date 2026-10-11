"""Fail-closed production configuration checks without accessing credentials."""
import os
from urllib.parse import urlsplit


def production_issues(env: dict[str, str] | None = None) -> list[str]:
    config = os.environ if env is None else env
    if config.get("EDUCYBER_ENV", "development").lower() != "production":
        return []
    issues = []
    origins = [v.strip() for v in config.get("EDUCYBER_CORS_ORIGINS", "").split(",") if v.strip()]
    if not origins:
        issues.append("EDUCYBER_CORS_ORIGINS must specify the deployed HTTPS frontend")
    for origin in origins:
        parsed = urlsplit(origin)
        if (parsed.scheme != "https" or not parsed.hostname or
                parsed.username or parsed.password or parsed.path or
                parsed.query or parsed.fragment or "*" in origin or
                parsed.hostname in ("localhost", "127.0.0.1")):
            issues.append("CORS origins must be explicit production HTTPS origins")
            break
    database = config.get("DATABASE_URL", "")
    if not database.startswith("postgresql+psycopg://"):
        issues.append("Production DATABASE_URL must use PostgreSQL and psycopg")
    if "sslmode=require" not in database and "sslmode=verify-full" not in database:
        issues.append("Production DATABASE_URL must explicitly require TLS")
    if config.get("EDUCYBER_EDGE_RATE_LIMITING") != "enabled":
        issues.append("Production edge rate limiting must be confirmed")
    if config.get("EDUCYBER_BACKUP_VERIFIED") != "yes":
        issues.append("A tested database backup and recovery procedure must be confirmed")
    return issues


def require_safe_production_configuration() -> None:
    issues = production_issues()
    if issues:
        raise RuntimeError("Unsafe EduCyber production configuration: " + "; ".join(issues))
