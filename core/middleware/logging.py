import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.logger import get_logger

logger = get_logger("api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Excluir endpoints de health check del logging detallado
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Extraer tenant del header si existe
        tenant = request.headers.get("X-Tenant-ID", "unknown")

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000

        # Log del request
        logger.api_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            tenant=tenant,
        )

        return response
