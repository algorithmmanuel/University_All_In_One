"""Read-only synthetic Brevo diagnostics tests; no network calls."""
from mail_diagnostics import diagnose, URLS

SETTINGS = {
    "BREVO_API_KEY": "example-placeholder",
    "EDUCYBER_EMAIL_SENDER": "noreply@example.org",
    "EDUCYBER_PUBLIC_WEB_URL": "https://beta.example.org",
}


def test_account_and_active_sender():
    called = []
    def fetch(url, key):
        called.append(url)
        if url == URLS["account"]:
            return {"ok": True}
        return {"senders": [{"email": "noreply@example.org", "active": True}]}
    data = diagnose(SETTINGS, fetch=fetch)
    assert called == [URLS["account"], URLS["senders"]]
    assert data["configured"] is True
    assert data["api_key_valid"] is True
    assert data["sender_registered"] is True
    assert data["sender_active"] is True


def test_missing_sender_and_config():
    data = diagnose(SETTINGS, fetch=lambda url, key:
                    {} if url == URLS["account"] else {"senders": []})
    assert data["sender_registered"] is False
    data = diagnose({**SETTINGS, "BREVO_API_KEY": ""},
                    fetch=lambda url, key: (_ for _ in ()).throw(AssertionError()))
    assert data["configured"] is False


def test_provider_status_and_network_are_sanitized():
    from urllib.error import HTTPError, URLError
    def unauthorized(url, key):
        raise HTTPError(url, 401, "rejected", {}, None)
    result = diagnose(SETTINGS, fetch=unauthorized)
    assert result["api_key_valid"] is False
    assert result["provider_status"] == 401
    def unreachable(url, key):
        raise URLError("unreachable")
    result = diagnose(SETTINGS, fetch=unreachable)
    assert result["transport_or_response_error"] is True
