from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities import AliasRegistryEntity
from domain.repositories.alias_repository import IAliasRepository
from infrastructure.database.models import AliasRegistryModel
from infrastructure.database.repositories.base_sql_repository import BaseSQLRepository


class AliasRepository(
    BaseSQLRepository[AliasRegistryEntity, AliasRegistryModel], IAliasRepository
):
    def __init__(self, db: Session):
        super().__init__(db, AliasRegistryModel)

    def find_by_normalized_alias(
        self, tenant_id: str, alias_normalized: str
    ) -> Optional[AliasRegistryEntity]:
        db_alias = (
            self.db.query(self.model)
            .filter(
                self.model.alias_normalized == alias_normalized,
                self.model.tenant_id == tenant_id,
            )
            .first()
        )
        return self._to_entity(db_alias) if db_alias else None

    def find_active_by_normalized_alias(
        self, tenant_id: str, alias_normalized: str
    ) -> Optional[AliasRegistryEntity]:
        db_alias = (
            self.db.query(self.model)
            .filter(
                self.model.alias_normalized == alias_normalized,
                self.model.tenant_id == tenant_id,
                self.model.status == "ACTIVE",
                self.model.deleted_at.is_(None),
            )
            .first()
        )
        return self._to_entity(db_alias) if db_alias else None

    def update_status(self, alias_id: UUID, status: str) -> bool:
        db_alias = self.db.query(self.model).filter(self.model.id == alias_id).first()
        if not db_alias:
            return False
        db_alias.status = status
        db_alias.updated_at = datetime.now()
        self.db.commit()
        return True

    def create(self, entity: AliasRegistryEntity) -> AliasRegistryEntity:
        """Override para manejar enums correctamente"""
        entity_data = self._entity_to_dict(entity)
        db_entity = self.model(**entity_data)
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)

        return self._to_entity(db_entity)

    def _to_entity(self, db_alias: AliasRegistryModel) -> AliasRegistryEntity:
        return AliasRegistryEntity(
            id=db_alias.id,
            tenant_id=db_alias.tenant_id,
            alias_raw=db_alias.alias_raw,
            alias_normalized=db_alias.alias_normalized,
            bank=db_alias.bank,
            account_type=db_alias.account_type,
            last_4=db_alias.last_4,
            status=db_alias.status,
            acc_hash=db_alias.acc_hash,
            created_at=db_alias.created_at,
            updated_at=db_alias.updated_at,
            deleted_at=db_alias.deleted_at,
        )
