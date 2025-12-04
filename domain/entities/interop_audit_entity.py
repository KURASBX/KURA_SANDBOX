from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from utils import EQueryType


class InteropAuditEntity(BaseModel):
    """Entidad para auditoría de consultas de interoperabilidad"""

    id: Optional[UUID] = None
    requesting_tenant_id: UUID
    alias_normalized: str
    target_tenant_id: Optional[UUID] = None
    query_type: EQueryType
    timestamp: datetime
    correlation_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def create_validation_query(
        cls,
        requesting_tenant_id: UUID,
        alias_normalized: str,
        target_tenant_id: Optional[UUID] = None,
    ):
        return cls(
            requesting_tenant_id=requesting_tenant_id,
            alias_normalized=alias_normalized,
            target_tenant_id=target_tenant_id,
            query_type=EQueryType.GLOBAL_VALIDATION,
            timestamp=datetime.now(),
            correlation_id=uuid4(),
        )

    class Config:
        from_attributes = True
