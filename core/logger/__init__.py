import logging
import sys
import time
from contextlib import contextmanager
from typing import Any

from core.config import settings


class StructuredLogger:
    """Logger estructurado para aplicación enterprise"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        """Configurar el logger individual"""
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)

            if settings.LOG_FORMAT == "json":
                formatter = logging.Formatter(
                    '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s"}',
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            else:
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))
            self.logger.propagate = False

    def debug(self, message: str, **extra: Any):
        self.logger.debug(message, extra=extra)

    def info(self, message: str, **extra: Any):
        self.logger.info(message, extra=extra)

    def warning(self, message: str, **extra: Any):
        self.logger.warning(message, extra=extra)

    def error(self, message: str, **extra: Any):
        self.logger.error(message, extra=extra)

    def critical(self, message: str, **extra: Any):
        self.logger.critical(message, extra=extra)

    def api_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        tenant: str = None,
    ):
        """Log especializado para requests HTTP"""
        message = f"{method} {path} - {status_code} - {duration_ms}ms"
        extra = {
            "type": "api_request",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "tenant": tenant,
        }
        self.info(message, **extra)

    def database_query(
        self, operation: str, table: str, duration_ms: float, rows_affected: int = None
    ):
        """Log especializado para queries de base de datos"""
        message = f"DB {operation} on {table} - {duration_ms}ms"
        extra = {
            "type": "database_query",
            "operation": operation,
            "table": table,
            "duration_ms": duration_ms,
            "rows_affected": rows_affected,
        }
        self.debug(message, **extra)


def get_logger(name: str) -> StructuredLogger:
    """Factory function para obtener loggers estructurados"""
    return StructuredLogger(name)


@contextmanager
def log_execution_time(logger: StructuredLogger, operation: str):
    """Context manager para medir tiempo de ejecución"""
    start_time = time.time()
    try:
        yield
    finally:
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"{operation} completed in {duration_ms:.2f}ms",
            operation=operation,
            duration_ms=duration_ms,
        )
