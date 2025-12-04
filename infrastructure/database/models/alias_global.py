from sqlalchemy import (
    Boolean,
    Column,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.database.models import BaseModel


class GlobalAliasModel(BaseModel):
    __tablename__ = "global_aliases"

    alias_normalized = Column(Text, primary_key=True)
    owning_tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    routing_code = Column(String(11), nullable=False)  # Código SWIFT/BIC
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        Index("idx_global_alias_active", "alias_normalized", "is_active"),
        ForeignKeyConstraint(["owning_tenant_id"], ["tenants.id"]),
    )
