from abc import ABC, abstractmethod

from domain.entities.error_log import ErrorLogEntity


class IErrorLogRepository(ABC):
    """Puerto para el repositorio de logs de errores"""

    @abstractmethod
    def create(self, error_log: ErrorLogEntity) -> ErrorLogEntity:
        pass
