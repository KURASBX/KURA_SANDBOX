from sqlalchemy.orm import Session

from domain.entities.error_log import ErrorLogEntity
from domain.repositories.error_log_repository import IErrorLogRepository
from infrastructure.database.models.error_log import ErrorLogModel


class ErrorLogRepository(IErrorLogRepository):
    """Adaptador para el repositorio de logs de errores con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db
        self.model = ErrorLogModel

    def create(self, error_log: ErrorLogEntity) -> ErrorLogEntity:
        db_error_log = self.model(**error_log.model_dump(exclude={"id"}))
        self.db.add(db_error_log)
        self.db.commit()
        self.db.refresh(db_error_log)
        return ErrorLogEntity.model_validate(db_error_log)
