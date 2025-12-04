from abc import abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities import AliasRegistryEntity
from domain.repositories.base_repository import IBaseRepository


class IAliasRepository(IBaseRepository[AliasRegistryEntity]):
    @abstractmethod
    def find_by_normalized_alias(
        self, tenant_id: str, alias_normalized: str
    ) -> Optional[AliasRegistryEntity]:
        pass

    @abstractmethod
    def find_active_by_normalized_alias(
        self, tenant_id: str, alias_normalized: str
    ) -> Optional[AliasRegistryEntity]:
        pass

    @abstractmethod
    def update_status(self, alias_id: UUID, status: str) -> AliasRegistryEntity:
        pass
