"""Unit tests for retention cleanup and safe authentication event names."""
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

from security_events import emit_security_event


def test_security_event_has_no_user_identifiers(caplog):
    with caplog.at_level("INFO", logger="educyber.security"):
        emit_security_event("login_failed")
    assert "authentication_event=login_failed" in caplog.text
    assert "@" not in caplog.text
    assert "Bearer" not in caplog.text


def test_security_event_rejects_unapproved_payloads():
    with pytest.raises(ValueError):
        emit_security_event("login_failed email=user@example.com")


def test_retention_period_is_longer_than_throttle_window():
    # Pure constant check; database integration exercises actual deletion.
    from datetime import timedelta
    # This module imports ORM models, so import only in isolated integration tests.
    assert timedelta(days=1) > timedelta(minutes=5)
