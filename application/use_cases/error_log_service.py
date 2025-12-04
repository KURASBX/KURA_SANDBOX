from domain.entities.error_log import ErrorLogEntity
from domain.repositories.error_log_repository import IErrorLogRepository


class ErrorLogService:
    """Caso de uso para el log de errores"""

    def __init__(self, error_log_repository: IErrorLogRepository):
        self.error_log_repo = error_log_repository

    def log_error(self, error_log: ErrorLogEntity) -> ErrorLogEntity:
        return self.error_log_repo.create(error_log)
