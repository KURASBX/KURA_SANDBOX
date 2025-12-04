from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from domain.entities import GlobalAliasEntity
from domain.repositories import IGlobalAliasRepository
from infrastructure.database.models import GlobalAliasModel
from infrastructure.database.repositories.base_sql_repository import BaseSQLRepository


class GlobalAliasRepository(
    BaseSQLRepository[GlobalAliasEntity, GlobalAliasModel], IGlobalAliasRepository
):
    def __init__(self, db: Session):
        super().__init__(db, GlobalAliasModel)

    def find_active_alias(self, alias_normalized: str) -> Optional[GlobalAliasEntity]:
        db_entity = (
            self.db.query(GlobalAliasModel)
            .filter(
                GlobalAliasModel.alias_normalized == alias_normalized,
                GlobalAliasModel.is_active,
            )
            .first()
        )
        return self._to_entity(db_entity) if db_entity else None

    def deactivate_alias(self, alias_normalized: str) -> bool:
        """Implementación concreta del método"""
        db_entity = (
            self.db.query(self.model)
            .filter(self.model.alias_normalized == alias_normalized)
            .first()
        )

        if not db_entity:
            return False

        db_entity.is_active = False
        db_entity.updated_at = datetime.now()
        self.db.commit()
        return True

    def _to_entity(self, db: GlobalAliasModel) -> GlobalAliasEntity:
        return GlobalAliasEntity(
            id=db.id,
            alias_normalized=db.alias_normalized,
            owning_tenant_id=db.owning_tenant_id,
            routing_code=db.routing_code,
            is_active=db.is_active,
            created_at=db.created_at,
            updated_at=db.updated_at,
            deleted_at=db.deleted_at,
        )
