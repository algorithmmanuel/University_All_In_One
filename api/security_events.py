"""Minimal structured authentication event logging.

Never log credentials, email addresses, bearer tokens or request payloads.
Attach request correlation IDs at the gateway when deployed.
"""
import logging

logger = logging.getLogger("educyber.security")

ALLOWED_EVENTS = frozenset({
    "login_failed", "login_succeeded", "login_throttled",
    "registration_throttled", "registration_succeeded", "logout_succeeded",
})


def emit_security_event(event: str) -> None:
    """Emit a low-cardinality event name without personal data."""
    if event not in ALLOWED_EVENTS:
        raise ValueError("Unrecognized security event")
    logger.info("authentication_event=%s", event)
