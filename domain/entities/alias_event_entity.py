from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from utils import EEventType


class AliasEventEntity(BaseModel):
    """Entidad de dominio para Eventos de Alias"""

    id: Optional[UUID] = None
    alias_normalized: str
    tenant_id: UUID
    event_type: EEventType = EEventType.RESOLVE
    correlation_id: UUID
    previous_hash: str
    current_hash: str
    timestamp: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
