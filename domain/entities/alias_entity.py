from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from utils import MESSAGES, AliasStatus, EAccountType


class AliasRegistryEntity(BaseModel):
    """Entidad de dominio para Alias - Pura lógica de negocio"""

    id: Optional[UUID] = None
    tenant_id: UUID
    alias_raw: str
    alias_normalized: str
    bank: str
    account_type: EAccountType
    last_4: str
    status: AliasStatus = AliasStatus.ACTIVE
    acc_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @field_validator("alias_raw")
    def validate_alias_format(cls, v):
        if len(v) < 4 or len(v) > 30:
            raise ValueError(
                MESSAGES.ERROR.VALIDATION.ALIAS_MUST_HAVE_4_TO_30_CHARACTERS.CODE
            )
        return v

    @field_validator("last_4")
    def validate_last_4(cls, v):
        if not v.isdigit() or len(v) != 4:
            raise ValueError(
                MESSAGES.ERROR.VALIDATION.ALIAS_LAST_4_MUST_BE_4_DIGITS.CODE
            )
        return v

    def activate(self):
        self.status = AliasStatus.ACTIVE

    def deactivate(self):
        self.status = AliasStatus.INACTIVE

    def normalize_alias(self) -> str:
        return self.alias_raw.strip().lower()

    class Config:
        from_attributes = True
