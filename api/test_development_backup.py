"""Safety tests for Development archive preflight; no real database or pg_dump."""
import importlib.util
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


IDENTITY = {"database": "educyber_dev", "port": 5435,
            "user": "educyber_dev", "revision": "0013_journey_workshops"}


def load(monkeypatch):
    scripts = Path(__file__).resolve().parents[1] / "scripts"
    monkeypatch.syspath_prepend(str(scripts))
    spec = importlib.util.spec_from_file_location("dev_backup", scripts / "backup_development.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verified_archive_requires_fresh_matching_revision_and_digest(tmp_path, monkeypatch):
    module = load(monkeypatch)
    monkeypatch.setattr(module, "BACKUP_DIR", tmp_path)
    stamp = "educyber-dev-20261105T140000Z-abcd1234"
    archive = tmp_path / (stamp + ".dump")
    archive.write_bytes(b"A" * 2048)
    receipt = {
        **IDENTITY, "archive": archive.name, "created_epoch": 1000.0,
        "size": archive.stat().st_size, "sha256": hashlib.sha256(b"A" * 2048).hexdigest(),
    }
    (tmp_path / (stamp + ".json")).write_text(json.dumps(receipt), encoding="utf-8")
    with patch.object(module, "target", return_value=(IDENTITY, "synthetic-secret")):
        assert module.latest_verified_backup({}, now=1001) == archive
        for change in ("revision", "database", "port", "user", "sha256", "size"):
            mismatch = dict(receipt)
            mismatch[change] = "wrong" if change not in ("port", "size") else -1
            (tmp_path / (stamp + ".json")).write_text(json.dumps(mismatch), encoding="utf-8")
            try:
                module.latest_verified_backup({}, now=1001)
                assert False, "Corrupted or misdirected backup must be rejected"
            except ValueError:
                pass
        (tmp_path / (stamp + ".json")).write_text(json.dumps(receipt), encoding="utf-8")
        try:
            module.latest_verified_backup({}, now=1000 + module.MAX_BACKUP_AGE_SECONDS + 1)
            assert False, "Stale archive cannot authorize migration"
        except ValueError:
            pass
        archive.write_bytes(b"B" * 2048)
        try:
            module.latest_verified_backup({}, now=1001)
            assert False, "Tampered archive cannot authorize migration"
        except ValueError:
            pass


def test_backup_failure_never_leaves_trusted_manifest(tmp_path, monkeypatch):
    module = load(monkeypatch)
    monkeypatch.setattr(module, "BACKUP_DIR", tmp_path)
    monkeypatch.setattr(module.shutil, "which", lambda name: name)
    env = {"DATABASE_URL": "synthetic"}
    with patch.object(module, "target", return_value=(IDENTITY, "synthetic-secret")):
        with patch.object(module.subprocess, "run", return_value=SimpleNamespace(returncode=1)):
            try:
                module.create_backup(env)
                assert False, "Failed pg_dump must stop"
            except ValueError:
                pass
    assert not list(tmp_path.glob("*.json"))
    assert not list(tmp_path.glob("*.dump"))


def test_backup_fails_closed_without_postgres_tools(tmp_path, monkeypatch):
    module = load(monkeypatch)
    monkeypatch.setattr(module, "BACKUP_DIR", tmp_path)
    monkeypatch.setattr(module.shutil, "which", lambda _: None)
    with patch.object(module, "target", return_value=(IDENTITY, "synthetic-secret")):
        try:
            module.create_backup({"DATABASE_URL": "synthetic"})
            assert False, "Missing tools cannot authorize migration"
        except ValueError:
            pass
    assert not list(tmp_path.iterdir())


def test_database_identity_accepts_host_mapped_docker_port(monkeypatch):
    from unittest.mock import MagicMock
    module = load(monkeypatch)
    database_url = (
        "postgresql+psycopg://educyber_dev:synthetic-pass@"
        "127.0.0.1:5435/educyber_dev?connect_timeout=5"
    )
    session = MagicMock()
    session.__enter__.return_value = session
    session.execute.return_value.fetchone.side_effect = [
        ("educyber_dev", "educyber_dev"),
        ("0013_journey_workshops",),
    ]
    with patch("psycopg.connect", return_value=session) as connect:
        identity, password = module.target({"DATABASE_URL": database_url})
    assert identity == IDENTITY
    assert password == "synthetic-pass"
    assert connect.call_args.kwargs["port"] == 5435
    sql = [call.args[0] for call in session.execute.call_args_list]
    assert sql == ["SET TRANSACTION READ ONLY",
                   "SELECT current_database(), current_user",
                   "SELECT version_num FROM alembic_version"]
