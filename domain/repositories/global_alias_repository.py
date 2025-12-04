from abc import abstractmethod
from typing import Optional

from domain.entities import GlobalAliasEntity
from domain.repositories.base_repository import IBaseRepository


class IGlobalAliasRepository(IBaseRepository[GlobalAliasEntity]):
    @abstractmethod
    def find_active_alias(self, alias_normalized: str) -> Optional[GlobalAliasEntity]:
        pass

    @abstractmethod
    def create(self, entity: GlobalAliasEntity) -> GlobalAliasEntity:
        pass

    @abstractmethod
    def deactivate_alias(self, alias_normalized: str) -> bool:
        pass
