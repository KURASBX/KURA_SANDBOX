from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from utils import EAccountType


class AliasCreate(BaseModel):
    alias: str = Field(..., pattern=r"^[A-Za-z0-9._-]{4,30}$")
    bank: str = Field(..., min_length=2, max_length=64)
    account_type: EAccountType = Field(..., min_length=2, max_length=32)
    last_4: str = Field(..., pattern=r"^\d{4}$")


class AliasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    alias_raw: str
    bank: str
    account_type: str
    last_4: str
    status: str


class AccountHint(BaseModel):
    """DTO para la información limitada de la cuenta"""

    bank: str
    type: str
    last_4: str


class ResolveAliasResponse(BaseModel):
    exists: bool
    status: Optional[str] = None
    account_hint: Optional[AccountHint] = None

    @classmethod
    def not_found(cls):
        return cls(exists=False)

    @classmethod
    def found(cls, alias_entity):
        return cls(
            exists=True,
            status=alias_entity.status,
            account_hint=AccountHint(
                bank=alias_entity.bank,
                type=alias_entity.account_type,
                last_4=alias_entity.last_4,
            ),
        )


class HashChainVerificationResponse(BaseModel):
    alias: str
    is_valid: bool
    total_events: int
    valid_events: int
    corrupted_events: list[int]
    chain_break_at: Optional[int] = None
    expected_hash: str
    actual_hash: str
    details: str
