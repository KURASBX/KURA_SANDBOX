from uuid import UUID

from pydantic import BaseModel

from application.dtos.alias import AliasCreate


class ResolveAliasQuery(BaseModel):
    """DTO para consultas de resolución de alias"""

    tenant_id: UUID
    alias: str


class DeactivateAliasCommand(BaseModel):
    """DTO para comandos de desactivación de alias"""

    tenant_id: UUID
    alias: str
    correlation_id: str


class RegisterAliasCommand(BaseModel):
    """DTO para comandos de registro de alias"""

    tenant_id: UUID
    create_dto: AliasCreate
    correlation_id: UUID


class VerifyHashChainQuery(BaseModel):
    tenant_id: UUID
    alias: str
    correlation_id: UUID
