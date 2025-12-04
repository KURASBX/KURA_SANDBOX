from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from infrastructure.database.models.base import BaseModel
from utils import EEventType


class AliasEventModel(BaseModel):
    __tablename__ = "alias_events"

    alias_normalized = Column(Text, nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    event_type = Column(
        SQLEnum(EEventType),
        name="event_type",
        nullable=False,
        default=EEventType.RESOLVE,
    )
    correlation_id = Column(UUID(as_uuid=True), nullable=False)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    deleted_at = None
