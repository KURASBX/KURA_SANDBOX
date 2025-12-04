from abc import abstractmethod
from datetime import date
from typing import Optional

from domain.entities import AliasEventEntity
from domain.repositories import IBaseRepository


class IAliasEventRepository(IBaseRepository[AliasEventEntity]):
    @abstractmethod
    def get_events_for_alias(
        self, alias_normalized: str, tenant_id: str
    ) -> list[AliasEventEntity]:
        pass

    @abstractmethod
    def get_last_event_for_alias(
        self, alias_normalized: str, tenant_id: str
    ) -> Optional[AliasEventEntity]:
        pass

    @abstractmethod
    def get_events_by_date(
        self, target_date: date, tenant_id: Optional[str] = None
    ) -> list[AliasEventEntity]:
        """Obtiene todos los eventos de una fecha para WORM"""
        pass
