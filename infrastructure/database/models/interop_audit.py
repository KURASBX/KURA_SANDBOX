from sqlalchemy import UUID, Column, DateTime, Index, Text
from sqlalchemy import Enum as SQLEnum

from infrastructure.database.models.base import BaseModel
from utils import EQueryType


class InteropAuditModel(BaseModel):
    __tablename__ = "interop_audits"

    requesting_tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    alias_normalized = Column(Text, primary_key=True)
    target_tenant_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    query_type = Column(
        SQLEnum(EQueryType),
        nullable=False,
        index=True,
        default=EQueryType.GLOBAL_VALIDATION,
    )
    timestamp = Column(DateTime, nullable=False, index=True)
    correlation_id = Column(UUID(as_uuid=True), nullable=True, index=True)

    __table_args__ = (
        Index("idx_interop_alias_tenant", "alias_normalized", "requesting_tenant_id"),
        Index("idx_interop_timestamp", "timestamp"),
    )
