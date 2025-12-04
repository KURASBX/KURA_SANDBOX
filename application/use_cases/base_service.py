from typing import Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

from domain.repositories import IBaseRepository

EntityType = TypeVar("EntityType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[EntityType, CreateSchemaType, UpdateSchemaType]):
    """Caso de uso base que orquesta la lógica"""

    def __init__(self, repository: IBaseRepository[EntityType]):
        self.repository = repository

    def get_by_id(self, id: UUID) -> Optional[EntityType]:
        return self.repository.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[EntityType]:
        return self.repository.get_all(skip=skip, limit=limit)

    def create(self, create_schema: CreateSchemaType) -> EntityType:
        return self.repository.create(create_schema)

    def update(self, id: UUID, update_schema: UpdateSchemaType) -> Optional[EntityType]:
        existing = self.get_by_id(id)
        if not existing:
            return None
        return self.repository.update(id, update_schema)

    def delete(self, id: UUID) -> bool:
        return self.repository.delete(id)
