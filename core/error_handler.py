import logging
import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from application.use_cases.error_log_service import ErrorLogService
from core.config import settings
from core.database import get_db
from domain.entities.error_log import ErrorLogEntity
from infrastructure.database.repositories.error_log_repository import ErrorLogRepository

logger = logging.getLogger(__name__)


async def http_error_handler_middleware(request: Request, call_next):
    """Middleware global para manejo de errores"""
    # Skip health checks
    if request.url.path.startswith("/health") or request.url.path.startswith(
        "/api/v1/health"
    ):
        return await call_next(request)

    try:
        response = await call_next(request)

        # Log HTTP errors
        if 500 <= response.status_code < 600:
            await _log_http_error_to_db(request, response)
            logger.error(
                "Error interno del servidor",
                extra={
                    "operation": "server_error",
                    "status_code": response.status_code,
                    "url": str(request.url),
                },
            )
        elif 400 <= response.status_code < 500:
            logger.warning(
                "Error del cliente",
                extra={
                    "operation": "client_error",
                    "status_code": response.status_code,
                    "url": str(request.url),
                },
            )

        return response

    except HTTPException as http_exc:
        # Manejar excepciones HTTP esperadas
        if http_exc.status_code == 429:
            logger.warning(
                "Rate limit excedido",
                extra={
                    "operation": "rate_limit_blocked",
                    "client_ip": request.client.host,
                    "url": str(request.url),
                },
            )
        else:
            logger.warning(
                "Excepción HTTP",
                extra={
                    "operation": "http_exception",
                    "status_code": http_exc.status_code,
                    "detail": http_exc.detail,
                    "url": str(request.url),
                },
            )
        raise http_exc

    except Exception as e:
        # Excepciones NO esperadas - logging + base de datos
        logger.error(
            "Excepción no manejada",
            extra={
                "operation": "unhandled_exception",
                "error_type": type(e).__name__,
                "error_message": str(e),
                "url": str(request.url),
            },
        )

        await _log_unhandled_error_to_db(request, e)

        # Respuesta al cliente
        if settings.ENVIRONMENT == "production":
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )

        return JSONResponse(
            status_code=500,
            content={
                "detail": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
                if settings.ENVIRONMENT == "development"
                else None,
            },
        )


async def _log_http_error_to_db(request: Request, response):
    """Log errores 5xx en base de datos usando el servicio"""
    try:
        error_log = ErrorLogEntity(
            error_type=f"HTTP {response.status_code}",
            message=f"Server error: {response.status_code}",
            traceback="",
            url=str(request.url),
            method=request.method,
            status_code=response.status_code,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        await _save_error_log(error_log)
    except Exception as e:
        logger.error(f"No se pudo guardar error en BD: {e}")


async def _log_unhandled_error_to_db(request: Request, error: Exception):
    """Log excepciones no manejadas en base de datos usando el servicio"""
    try:
        error_log = ErrorLogEntity(
            error_type=type(error).__name__,
            message=str(error),
            traceback=traceback.format_exc(),
            url=str(request.url),
            method=request.method,
            status_code=500,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        await _save_error_log(error_log)
    except Exception as e:
        logger.error(f"No se pudo guardar error no manejado en BD: {e}")


async def _save_error_log(error_log: ErrorLogEntity):
    """Guardar error log usando el servicio de la capa de aplicación"""
    db = next(get_db())
    try:
        error_log_repo = ErrorLogRepository(db)
        error_log_service = ErrorLogService(error_log_repo)
        error_log_service.log_error(error_log)
    except Exception as e:
        logger.error(f"Error al guardar log: {e}")
    finally:
        db.close()
