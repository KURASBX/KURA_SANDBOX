from sqlalchemy import UUID, Column, Index, String, Text
from sqlalchemy import Enum as SQLEnum

from infrastructure.database.models.base import BaseModel
from utils import AliasStatus, EAccountType


class AliasRegistryModel(BaseModel):
    __tablename__ = "alias_registries"

    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    alias_raw = Column(Text, nullable=False)
    alias_normalized = Column(Text, nullable=False, index=True)
    bank = Column(String(255), nullable=False)
    account_type = Column(
        SQLEnum(EAccountType, name="account_type"),
        nullable=False,
        default=EAccountType.CTA_VISTA,
    )
    last_4 = Column(String(4), nullable=False)
    status = Column(
        SQLEnum(AliasStatus, name="alias_status"),
        nullable=False,
        default=AliasStatus.ACTIVE,
    )
    acc_hash = Column(String(255), nullable=True)

    __table_args__ = (
        Index(
            "idx_alias_tenant_active",
            "alias_normalized",
            "tenant_id",
            "status",
            unique=True,
            postgresql_where=(status == "ACTIVE"),
        ),
    )
