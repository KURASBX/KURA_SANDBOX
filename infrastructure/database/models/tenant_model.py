from sqlalchemy import JSON, Column, Index, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY

from infrastructure.database.models.base import BaseModel
from utils import TenantRole, TenantStatus, TenantType


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    name = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False, unique=True, index=True)
    type = Column(SQLEnum(TenantType), nullable=False, default=TenantType.BANK)
    contact_email = Column(String(255), nullable=False, unique=True)
    contact_phone = Column(String(20), nullable=True)
    website = Column(Text, nullable=True)
    legal_name = Column(String(255), nullable=True)
    tax_id = Column(String(20), nullable=True, unique=True)
    status = Column(SQLEnum(TenantStatus), nullable=False, default=TenantStatus.PENDING)
    tenant_metadata = Column(JSON, nullable=False, default=dict)
    roles = Column(
        ARRAY(SQLEnum(TenantRole)), nullable=False, default=[TenantRole.OPERATOR]
    )

    __table_args__ = (
        Index("idx_tenant_status_type", "status", "type"),
        Index("idx_tenant_active_banks", "status", "type"),
    )
