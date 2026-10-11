"""Request telemetry must never expose user-controlled URLs or secrets."""
import asyncio
import logging
import re

from starlette.requests import Request
from starlette.responses import JSONResponse
from request_telemetry import RequestTelemetryMiddleware


def test_request_id_and_redacted_logging(caplog):
    async def app(scope, receive, send):
        response = JSONResponse({"ok": True})
        await response(scope, receive, send)

    middleware = RequestTelemetryMiddleware(app)

    async def run():
        scope = {"type": "http", "method": "GET", "path": "/secret",
                 "raw_path": b"/secret", "query_string": b"token=private-token",
                 "headers": [(b"authorization", b"Bearer private-token")],
                 "scheme": "http", "server": ("localhost", 80), "client": ("127.0.0.1", 1234),
                 "http_version": "1.1", "root_path": ""}
        messages = []
        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}
        async def send(message):
            messages.append(message)
        await middleware(scope, receive, send)
        return messages

    with caplog.at_level(logging.INFO, logger="educyber.requests"):
        messages = asyncio.run(run())
    response = next(m for m in messages if m["type"] == "http.response.start")
    headers = dict(response["headers"])
    request_id = headers[b"x-request-id"].decode()
    assert re.fullmatch(r"[a-f0-9]{32}", request_id)
    assert response["status"] == 200
    assert "status=200" in caplog.text
    assert "private-token" not in caplog.text
    assert "/secret" not in caplog.text
