"""Request telemetry must not expose user-controlled URLs or secrets."""
import logging
import re

from fastapi import FastAPI
from fastapi.testclient import TestClient
from request_telemetry import RequestTelemetryMiddleware


def test_request_id_and_redacted_logging(caplog):
    app = FastAPI()
    app.add_middleware(RequestTelemetryMiddleware)

    @app.get("/secret")
    def endpoint():
        return {"ok": True}

    with caplog.at_level(logging.INFO, logger="educyber.requests"):
        with TestClient(app) as client:
            response = client.get("/secret?token=private-token",
                                  headers={"Authorization": "Bearer private-token"})
    assert response.status_code == 200
    assert re.fullmatch(r"[a-f0-9]{32}", response.headers["x-request-id"])
    assert "status=200" in caplog.text
    assert "private-token" not in caplog.text
    assert "/secret" not in caplog.text
