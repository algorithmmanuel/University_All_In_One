"""Low-cardinality request telemetry without credentials or personal information."""
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("educyber.requests")


class RequestTelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = uuid.uuid4().hex
        started = time.monotonic()
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("request_failed request_id=%s method=%s", request_id, request.method)
            raise
        duration_ms = round((time.monotonic() - started) * 1000)
        # Deliberately omit URL, query string, request body, email, IP and token.
        logger.info("request_completed request_id=%s method=%s status=%s duration_ms=%s",
                    request_id, request.method, response.status_code, duration_ms)
        response.headers["X-Request-ID"] = request_id
        return response
