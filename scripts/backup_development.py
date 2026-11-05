"""Verified, explicit backup of the isolated *Development* PostgreSQL DB.

Run with this checkout's api/.venv Python, after stopping Dev API/web/worker.
Never reads Beta settings, prints passwords, overwrites archives or migrates.
pg_dump and pg_restore must be installed and available on PATH.
"""
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit

from development import ROOT, configuration, require_free_port

BACKUP_DIR = ROOT / ".local-development-backups"
EXPECTED = ("127.0.0.1", 5435, "educyber_dev", "educyber_dev")
MAX_BACKUP_AGE_SECONDS = 24 * 60 * 60


def target(environment):
    """Fail closed using the existing strict launcher guard and DB identity."""
    from development_runtime import validate_development_database
    from psycopg import connect
    from psycopg.rows import tuple_row

    address = environment["DATABASE_URL"]
    validate_development_database(address)
    parsed = urlsplit(address)
    host, port, dbname, user = EXPECTED
    if (parsed.hostname, parsed.port, parsed.path[1:], unquote(parsed.username or "")) != EXPECTED:
        raise ValueError("Unapproved Development database identity")
    password = unquote(parsed.password or "")
    if not password:
        raise ValueError("Development database password missing")
    with connect(host=host, port=port, dbname=dbname, user=user,
                 password=password, connect_timeout=5, row_factory=tuple_row) as connection:
        connection.execute("SET TRANSACTION READ ONLY")
        # The host's mapped port is checked by the URL and connection.
        # PostgreSQL may report an internal container port such as 5432.
        actual = connection.execute(
            "SELECT current_database(), current_user"
        ).fetchone()
        if actual != (dbname, user):
            raise ValueError("Connected database is not dedicated Development database")
        revision = connection.execute(
            "SELECT version_num FROM alembic_version"
        ).fetchone()
        if not revision or not isinstance(revision[0], str):
            raise ValueError("Development migration revision missing")
    return {"database": dbname, "port": port, "user": user, "revision": revision[0]}, password


def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_verified_backup(environment, *, now=None):
    """Verify a fresh manifest AND complete archive; never trust filename alone."""
    import time

    identity, _ = target(environment)
    now = time.time() if now is None else now
    if not BACKUP_DIR.is_dir():
        raise ValueError("No Development backup directory")
    candidates = sorted(BACKUP_DIR.glob("educyber-dev-*.json"), reverse=True)
    for manifest_path in candidates:
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            if set(data) != {"archive", "created_epoch", "database", "port",
                             "user", "revision", "sha256", "size"}:
                continue
            if any(data[k] != identity[k] for k in identity):
                continue
            if type(data["created_epoch"]) not in (int, float):
                continue
            if not 0 <= now - data["created_epoch"] <= MAX_BACKUP_AGE_SECONDS:
                continue
            name = data["archive"]
            if not isinstance(name, str) or name != manifest_path.stem + ".dump":
                continue
            archive = BACKUP_DIR / name
            if (not archive.is_file() or archive.is_symlink()
                    or archive.stat().st_size != data["size"]
                    or data["size"] < 1024):
                continue
            if hash_file(archive) != data["sha256"]:
                continue
            return archive
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
            continue
    raise ValueError("No fresh verified backup for the current Development schema")


def create_backup(environment):
    """One private archive plus integrity manifest; leaves failures untrusted."""
    identity, password = target(environment)
    pg_dump = shutil.which("pg_dump")
    pg_restore = shutil.which("pg_restore")
    if not pg_dump or not pg_restore:
        raise ValueError("pg_dump and pg_restore must be installed on PATH")
    BACKUP_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = "educyber-dev-" + stamp + "-" + secrets.token_hex(4)
    archive = BACKUP_DIR / (stem + ".dump")
    manifest = BACKUP_DIR / (stem + ".json")
    environment = dict(environment)
    environment["PGPASSWORD"] = password
    try:
        dump = subprocess.run(
            [pg_dump, "--host=127.0.0.1", "--port=5435", "--username=educyber_dev",
             "--format=custom", "--no-password", "--file=" + str(archive),
             "educyber_dev"], env=environment, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=False,
        )
        if dump.returncode != 0 or not archive.is_file() or archive.stat().st_size < 1024:
            raise ValueError("Development pg_dump did not produce a valid archive")
        check = subprocess.run(
            [pg_restore, "--list", str(archive)], env=environment,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
        if check.returncode != 0:
            raise ValueError("Development pg_restore could not read the archive")
        import time

        data = {
            **identity, "archive": archive.name, "created_epoch": time.time(),
            "size": archive.stat().st_size, "sha256": hash_file(archive),
        }
        with manifest.open("x", encoding="utf-8") as stream:
            json.dump(data, stream, sort_keys=True)
        manifest.chmod(0o600)
        archive.chmod(0o600)
        return archive
    except Exception:
        # Clean only files created by this invocation, never existing backups.
        manifest.unlink(missing_ok=True)
        archive.unlink(missing_ok=True)
        raise


def main():
    try:
        env = configuration()
        require_free_port(8010)
        require_free_port(3010)
        archive = create_backup(env)
        verified = latest_verified_backup(env)
        if verified != archive:
            raise ValueError("New Development backup did not verify")
        print("DEVELOPMENT BACKUP VERIFIED: " + archive.name)
        print("Archive stored privately under .local-development-backups; no Beta access.")
        return 0
    except Exception as exc:
        print("Development backup stopped (" + type(exc).__name__ +
              "). Check dedicated DB on port 5435, stopped Dev services and pg_dump/pg_restore availability.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
