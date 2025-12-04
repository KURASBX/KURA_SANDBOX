from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from utils import TenantRole, TenantStatus, TenantType


class TenantCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{3,20}$")
    type: TenantType
    contact_email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    contact_phone: Optional[str] = Field(None, pattern=r"^\+?[\d\s-]{10,}$")
    website: Optional[str] = Field(None, pattern=r"^https?://[^\s/$.?#].[^\s]*$")
    legal_name: Optional[str] = Field(None, min_length=2, max_length=255)
    tax_id: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9]{10,20}$")
    tenant_metadata: dict = Field(default_factory=dict)
    roles: list[TenantRole] = [TenantRole.OPERATOR]


class TenantAuthRequest(BaseModel):
    tenant_code: str
    api_key: str


class TenantAuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    tenant_id: UUID
    tenant_code: str
    tenant_type: str
    roles: list[TenantRole]


class TenantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    code: str
    type: TenantType
    contact_email: str
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    status: TenantStatus
    roles: list[TenantRole]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Solo en creación
    api_key: Optional[str] = None


class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    contact_email: Optional[str] = Field(
        None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    roles: Optional[list[TenantRole]] = None
    contact_phone: Optional[str] = Field(None, pattern=r"^\+?[\d\s-]{10,}$")
    website: Optional[str] = Field(None, pattern=r"^https?://[^\s/$.?#].[^\s]*$")
    tenant_metadata: Optional[dict] = None
