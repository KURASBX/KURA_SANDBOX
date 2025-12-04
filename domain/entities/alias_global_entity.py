import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GlobalAliasEntity(BaseModel):
    """Entidad para aliases globales en interoperabilidad"""

    alias_normalized: str  # Primary Key
    owning_tenant_id: uuid.UUID
    routing_code: str  # Código SWIFT/BIC
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def create(
        cls, alias_normalized: str, owning_tenant_id: uuid.UUID, routing_code: str
    ):
        return cls(
            alias_normalized=alias_normalized,
            owning_tenant_id=owning_tenant_id,
            routing_code=routing_code,
            is_active=True,
            created_at=datetime.now(),
        )

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()
