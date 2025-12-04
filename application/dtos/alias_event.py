from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AliasEventHistoryItem(BaseModel):
    """Item individual del historial de eventos"""

    model_config = ConfigDict(from_attributes=True)

    event_type: str
    timestamp: datetime
    correlation_id: UUID
    previous_hash: str
    current_hash: str


class AliasEventHistoryResponse(BaseModel):
    """Respuesta completa del historial"""

    alias: str
    total_events: int
    events: list[AliasEventHistoryItem]


class GetAliasEventHistoryQuery(BaseModel):
    tenant_id: UUID
    alias: str
    correlation_id: UUID
