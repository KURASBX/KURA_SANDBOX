from abc import abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.tenant_entity import TenantEntity, TenantStatus
from domain.repositories.base_repository import IBaseRepository


class ITenantRepository(IBaseRepository[TenantEntity]):
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[TenantEntity]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[TenantEntity]:
        pass

    @abstractmethod
    def find_by_tax_id(self, tax_id: str) -> Optional[TenantEntity]:
        pass

    @abstractmethod
    def find_active_tenants(self) -> list[TenantEntity]:
        pass

    @abstractmethod
    def find_tenants_by_type(self, tenant_type: str) -> list[TenantEntity]:
        pass

    @abstractmethod
    def update_status(self, tenant_id: UUID, status: TenantStatus) -> TenantEntity:
        pass
