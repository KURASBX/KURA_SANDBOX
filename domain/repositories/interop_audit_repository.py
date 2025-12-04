from abc import abstractmethod

from domain.entities import InteropAuditEntity
from domain.repositories.base_repository import IBaseRepository


class IInteropAuditRepository(IBaseRepository[InteropAuditEntity]):
    @abstractmethod
    def log_validation_query(self, audit_entity: InteropAuditEntity) -> None:
        pass

    @abstractmethod
    def get_cross_tenant_queries(
        self, tenant_id: str, days: int = 30
    ) -> list[InteropAuditEntity]:
        pass
