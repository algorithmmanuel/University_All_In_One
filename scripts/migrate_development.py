"""Explicit development-only migration. Stop development services first.

Reuses branch, interpreter, dedicated database and environment isolation guards.
Ordinary service startup still never runs migrations.
"""
import subprocess
import sys
from development import ROOT, configuration, require_free_port


def main():
    try:
        environment = configuration()
        require_free_port(8010)
        require_free_port(3010)
        return subprocess.call([sys.executable, '-m', 'alembic', 'upgrade', 'head'],
                               cwd=ROOT / 'api', env=environment)
    except Exception as error:
        print('Development migration stopped (' + type(error).__name__ +
              '). Check development branch/environment and stop development services.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
