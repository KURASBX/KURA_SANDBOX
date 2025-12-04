from datetime import date
from typing import Optional

from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

from domain.entities.alias_event_entity import AliasEventEntity
from domain.repositories.alias_event_repository import IAliasEventRepository
from infrastructure.database.models import AliasEventModel
from infrastructure.database.repositories.base_sql_repository import BaseSQLRepository


class AliasEventRepository(
    BaseSQLRepository[AliasEventEntity, AliasEventModel], IAliasEventRepository
):
    def __init__(self, db: Session):
        super().__init__(db, AliasEventModel)

    def get_events_for_alias(
        self, alias_normalized: str, tenant_id: str
    ) -> list[AliasEventEntity]:
        db_events = (
            self.db.query(self.model)
            .filter(
                self.model.alias_normalized == alias_normalized,
                self.model.tenant_id == tenant_id,
            )
            .order_by(self.model.timestamp)
            .all()
        )
        return [self._to_entity(event) for event in db_events]

    def get_last_event_for_alias(
        self, alias_normalized: str, tenant_id: str
    ) -> Optional[AliasEventEntity]:
        db_event = (
            self.db.query(self.model)
            .filter(
                self.model.alias_normalized == alias_normalized,
                self.model.tenant_id == tenant_id,
            )
            .order_by(self.model.timestamp.desc())
            .first()
        )
        return self._to_entity(db_event) if db_event else None

    def _to_entity(self, db_event: AliasEventModel) -> AliasEventEntity:
        return AliasEventEntity(
            id=db_event.id,
            alias_normalized=db_event.alias_normalized,
            tenant_id=db_event.tenant_id,
            event_type=db_event.event_type,
            correlation_id=db_event.correlation_id,
            previous_hash=db_event.previous_hash,
            current_hash=db_event.current_hash,
            timestamp=db_event.timestamp,
        )

    def get_events_by_date(
        self, target_date: date, tenant_id: Optional[str] = None
    ) -> list[AliasEventEntity]:
        """
        Obtiene todos los eventos de una fecha específica para WORM
        """
        query = self.db.query(self.model).filter(
            cast(self.model.timestamp, Date) == target_date
        )

        if tenant_id:
            query = query.filter(self.model.tenant_id == tenant_id)

        db_events = query.order_by(self.model.timestamp).all()

        return [self._to_entity(event) for event in db_events]
