from sqlalchemy.orm import Session

from domain.entities import InteropAuditEntity
from domain.repositories import IInteropAuditRepository
from infrastructure.database.models import InteropAuditModel
from infrastructure.database.repositories.base_sql_repository import BaseSQLRepository


class InteropAuditRepository(
    BaseSQLRepository[InteropAuditEntity, InteropAuditModel], IInteropAuditRepository
):
    def __init__(self, db: Session):
        super().__init__(db, InteropAuditModel)

    def log_validation_query(self, audit_entity: InteropAuditEntity) -> None:
        model = InteropAuditModel(
            requesting_tenant_id=audit_entity.requesting_tenant_id,
            alias_normalized=audit_entity.alias_normalized,
            target_tenant_id=audit_entity.target_tenant_id,
            query_type=audit_entity.query_type,
            timestamp=audit_entity.timestamp,
            correlation_id=audit_entity.correlation_id,
        )
        self.db.add(model)
        self.db.commit()

    def get_cross_tenant_queries(
        self, tenant_id: str, days: int = 30
    ) -> list[InteropAuditEntity]:
        query = self.db.query(InteropAuditModel).filter(
            InteropAuditModel.requesting_tenant_id != tenant_id,
        )
        return [self._to_entity(db) for db in query.all()]
