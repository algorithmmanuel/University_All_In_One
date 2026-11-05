"""The explicit migration command stops before invoking Alembic if guards fail."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
from pathlib import Path
import sys


def load_migrator(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / 'scripts'))
    spec = importlib.util.spec_from_file_location('development_migrator', root / 'scripts/migrate_development.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_guard_failure_never_migrates(monkeypatch):
    module = load_migrator(monkeypatch)
    with patch.object(module, 'configuration', side_effect=ValueError('wrong environment')), patch.object(module.subprocess, 'call') as run:
        assert module.main() == 1
        run.assert_not_called()


def test_running_development_service_never_migrates(monkeypatch):
    module = load_migrator(monkeypatch)
    with patch.object(module, 'configuration', return_value={}), patch.object(module, 'require_free_port', side_effect=OSError('occupied')), patch.object(module.subprocess, 'call') as run:
        assert module.main() == 1
        run.assert_not_called()


def test_explicit_action_uses_only_guarded_environment(monkeypatch):
    module = load_migrator(monkeypatch)
    env = {'DATABASE_URL': 'synthetic-guarded-target'}
    with patch.object(module, 'configuration', return_value=env), patch.object(module, 'require_free_port') as port, patch.object(module, 'latest_verified_backup', return_value=Path('educyber-dev-test.dump')) as backup, patch.object(module.subprocess, 'call', return_value=0) as run:
        assert module.main() == 0
        assert [c.args[0] for c in port.call_args_list] == [8010, 3010]
        backup.assert_called_once_with(env)
        run.assert_called_once_with([sys.executable, '-m', 'alembic', 'upgrade', 'head'], cwd=module.ROOT / 'api', env=env)


def test_migration_refuses_missing_verified_backup(monkeypatch):
    module = load_migrator(monkeypatch)
    env = {'DATABASE_URL': 'synthetic-guarded-target'}
    with patch.object(module, 'configuration', return_value=env), patch.object(module, 'require_free_port'), patch.object(module, 'latest_verified_backup', side_effect=ValueError('No fresh verified backup')), patch.object(module.subprocess, 'call') as run:
        assert module.main() == 1
        run.assert_not_called()
