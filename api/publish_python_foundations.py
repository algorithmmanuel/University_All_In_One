"""Backwards-compatible Python-only entry point for the accepted Phase 3.1 guide.

Shared preflight/publication logic lives in publish_foundations. Existing
content-preview/content-apply commands continue to affect only Python.
"""
from publish_foundations import publish_releases, safe_cli


def publish(db, *, apply=False):
    return publish_releases(db, ('python',), apply=apply)['results'][0]


if __name__ == '__main__':
    raise SystemExit(safe_cli(('python',), __doc__))
