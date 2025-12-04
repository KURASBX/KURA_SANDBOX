from uuid import UUID

from application.dtos import TenantResponse
from domain.repositories import ITenantRepository
from utils import MESSAGES


class GetTenantUseCase:
    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def execute(self, tenant_id: UUID) -> TenantResponse:
        tenant_entity = self.tenant_repository.get_by_id(tenant_id)
        if not tenant_entity:
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_NOT_FOUND.CODE)

        return TenantResponse(
            id=tenant_entity.id,
            name=tenant_entity.name,
            code=tenant_entity.code,
            contact_email=tenant_entity.contact_email,
            status=tenant_entity.status,
            roles=tenant_entity.roles,
            created_at=tenant_entity.created_at,
            updated_at=tenant_entity.updated_at,
        )
