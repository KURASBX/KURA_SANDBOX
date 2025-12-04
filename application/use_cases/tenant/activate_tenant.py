from application.dtos import TenantResponse
from domain.repositories import ITenantRepository
from utils import MESSAGES


class ActivateTenantUseCase:
    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def execute(self, tenant_code: str) -> TenantResponse:
        tenant_entity = self.tenant_repository.find_by_code(tenant_code)
        if not tenant_entity:
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_NOT_FOUND.CODE)

        tenant_entity.activate()
        updated_tenant = self.tenant_repository.update(tenant_entity.id, tenant_entity)

        return TenantResponse(
            id=updated_tenant.id,
            name=updated_tenant.name,
            code=updated_tenant.code,
            type=updated_tenant.type,
            contact_email=updated_tenant.contact_email,
            status=updated_tenant.status,
            roles=updated_tenant.roles,
            created_at=updated_tenant.created_at,
            updated_at=updated_tenant.updated_at,
        )
