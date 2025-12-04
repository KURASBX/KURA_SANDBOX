import re
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from utils import MESSAGES, TenantRole, TenantStatus, TenantType


class TenantEntity(BaseModel):
    """Entidad de dominio para Tenants"""

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: Optional[uuid.UUID] = None
    name: str
    code: str
    type: TenantType
    contact_email: str
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    status: TenantStatus = TenantStatus.PENDING
    tenant_metadata: dict = {}
    roles: list[TenantRole] = [TenantRole.OPERATOR]
    # api_keys: list[str] = [] # Placeholder "TenantAPIKey"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @field_validator("contact_email")
    @classmethod
    def email_must_be_valid(cls, v):
        if v and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError(MESSAGES.ERROR.VALIDATION.INVALID_EMAIL_FORMAT.CODE)
        return v

    @field_validator("code")
    @classmethod
    def code_must_be_alphanumeric(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", v):
            raise ValueError(MESSAGES.ERROR.VALIDATION.CODE_MUST_BE_ALPHANUMERIC.CODE)
        return v

    @field_validator("tax_id")
    def tax_id_must_be_valid(cls, v):
        if v and not re.match(r"^[a-zA-Z0-9]{10,20}$", v):
            raise ValueError(MESSAGES.ERROR.VALIDATION.INVALID_TAX_ID.CODE)
        return v

    def has_role(self, role: TenantRole) -> bool:
        return role in self.roles

    def can_manage_aliases(self) -> bool:
        return self.type in [TenantType.BANK, TenantType.ADMIN]

    def can_manage_tenants(self) -> bool:
        return TenantRole.ADMIN in self.roles

    def activate(self):
        self.status = TenantStatus.ACTIVE

    def deactivate(self):
        self.status = TenantStatus.INACTIVE

    def suspend(self):
        self.status = TenantStatus.SUSPENDED

    def is_active(self) -> bool:
        return self.status == TenantStatus.ACTIVE

    def add_api_key(self, api_key: str):
        """Agregar una nueva API Key"""
        # TODO: Implementar lógica de hashing y almacenamiento
        pass

    def verify_api_key(self, api_key: str) -> bool:
        """MVP: Verificación simple de API Key"""
        expected_prefix = f"tk_{self.code}_"
        return (
            api_key.startswith(expected_prefix)
            and len(api_key) >= len(expected_prefix) + 32
            and re.match(r"^[a-zA-Z0-9_-]+$", api_key[len(expected_prefix) :])
        )
