"""Read-only Brevo configuration probe. Never sends mail or prints secrets.

Run ONLY via the guarded Beta launcher. This script makes two GET requests
to the Brevo API; no account addresses, API keys, contacts or response bodies
are displayed. Provider 'accepted' does not guarantee inbox delivery.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from beta_runtime import validate_mail

URLS = {
    "account": "https://api.brevo.com/v3/account",
    "senders": "https://api.brevo.com/v3/senders",
}


def _get_json(url, api_key):
    req = Request(url, headers={"api-key": api_key, "Accept": "application/json"}, method="GET")
    with urlopen(req, timeout=12) as response:
        if response.status != 200:
            raise ValueError("Unexpected provider response")
        data = response.read(131073)
        if len(data) > 131072:
            raise ValueError("Provider response exceeds diagnostics size limit")
        return json.loads(data)


def diagnose(env, fetch=_get_json):
    """Return non-sensitive booleans/status codes only."""
    output = {"configured": False, "api_key_valid": None,
              "sender_registered": None, "sender_active": None,
              "provider_status": None}
    try:
        validate_mail(env)
    except (ValueError, KeyError, TypeError):
        output["configuration_error"] = True
        return output
    output["configured"] = True
    key = env["BREVO_API_KEY"]
    sender = env["EDUCYBER_EMAIL_SENDER"].strip().casefold()
    try:
        fetch(URLS["account"], key)
        output["api_key_valid"] = True
    except HTTPError as error:
        output["api_key_valid"] = False
        output["provider_status"] = error.code
        return output
    except (URLError, OSError, ValueError, TimeoutError):
        output["transport_or_response_error"] = True
        return output
    try:
        payload = fetch(URLS["senders"], key)
        matching = next((s for s in payload.get("senders", [])
                         if isinstance(s, dict) and
                         str(s.get("email", "")).casefold() == sender), None)
        output["sender_registered"] = matching is not None
        output["sender_active"] = (matching.get("active") is True
                                   if matching is not None else None)
    except HTTPError as error:
        output["provider_status"] = error.code
    except (URLError, OSError, ValueError, TimeoutError, AttributeError, TypeError):
        output["transport_or_response_error"] = True
    return output


def main():
    if os.getenv("EDUCYBER_ENV") != "beta":
        raise ValueError("Read-only mail diagnosis requires the Beta launcher")
    # Existing launcher constructs a sanitized env from .env and api/.env.beta.
    print(json.dumps(diagnose(os.environ), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
