from datetime import datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from domain.repositories import IBaseRepository
from infrastructure.database.models.base import BaseModel
from utils import MESSAGES

ModelType = TypeVar("ModelType", bound=BaseModel)
EntityType = TypeVar("EntityType")


class BaseSQLRepository(IBaseRepository[EntityType], Generic[ModelType, EntityType]):
    """Adaptador concreto para SQLAlchemy con soporte para UUID"""

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, id: UUID) -> Optional[EntityType]:
        db_entity = (
            self.db.query(self.model)
            .filter(self.model.id == id, self.model.deleted_at.is_(None))
            .first()
        )
        return self._to_entity(db_entity) if db_entity else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[EntityType]:
        db_entities = (
            self.db.query(self.model)
            .filter(self.model.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(entity) for entity in db_entities]

    def create(self, entity: EntityType) -> EntityType:
        entity_data = self._entity_to_dict(entity)
        db_entity = self.model(**entity_data)
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return self._to_entity(db_entity)

    def update(self, id: UUID, update_data: dict) -> Optional[EntityType]:
        db_entity = self.db.query(self.model).filter(self.model.id == id).first()
        if not db_entity:
            return None

        for field, value in update_data:
            if hasattr(db_entity, field) and field != "id":
                setattr(db_entity, field, value)

        self.db.commit()
        self.db.refresh(db_entity)
        return self._to_entity(db_entity)

    def delete(self, id: UUID) -> bool:
        db_entity = self.db.query(self.model).filter(self.model.id == id).first()
        if not db_entity:
            return False

        db_entity.deleted_at = datetime.now()
        self.db.commit()
        return True

    def _entity_to_dict(self, entity: EntityType) -> dict:
        """Convertir entidad a dict para operaciones de BD"""
        # Para Pydantic v2
        if hasattr(entity, "model_dump") and callable(entity.model_dump):
            return entity.model_dump()

        # Para Pydantic v1
        if hasattr(entity, "dict") and callable(entity.dict):
            return entity.dict()

        # Para dataclasses
        if hasattr(entity, "__dataclass_fields__"):
            from dataclasses import asdict

            return asdict(entity)

        # Para objetos con __dict__
        if hasattr(entity, "__dict__"):
            return entity.__dict__

        if hasattr(entity, "__table__"):
            return {
                column.name: getattr(entity, column.name)
                for column in entity.__table__.columns
            }

        raise TypeError(
            MESSAGES.ERROR.VALIDATION.IMPOSIBLE_TO_CONVERT_ENTITY_TO_DICT.CODE
        )

    def _to_entity(self, db_entity: ModelType) -> EntityType:
        raise NotImplementedError(MESSAGES.ERROR.VALIDATION.METHOD_NOT_IMPLEMENTED.CODE)
