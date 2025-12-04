from application.dtos import TenantResponse
from domain.repositories import ITenantRepository


class GetTenantListUseCase:
    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def execute(self, skip: int, limit: int) -> list[TenantResponse]:
        tenants = self.tenant_repository.get_all(skip=skip, limit=limit)

        return [
            TenantResponse(
                id=tenant.id,
                name=tenant.name,
                code=tenant.code,
                type=tenant.type,
                contact_email=tenant.contact_email,
                status=tenant.status,
                roles=tenant.roles,
                created_at=tenant.created_at,
                updated_at=tenant.updated_at,
            )
            for tenant in tenants
        ]
