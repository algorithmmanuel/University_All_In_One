#!/usr/bin/env sh
# Generate Python 3.13 Linux lockfile in a clean environment.
set -eu
cd "$(dirname "$0")"
python -m pip install 'pip-tools>=7.4,<8'
python -m piptools compile --resolver=backtracking --output-file=requirements-ci.lock requirements-ci.in
python -m pip install --dry-run -r requirements-ci.lock
echo "Lockfile generated. Review changes and commit requirements-ci.lock."
