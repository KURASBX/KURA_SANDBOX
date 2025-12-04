from application.dtos import TenantResponse, TenantUpdate
from domain.repositories import ITenantRepository
from utils import MESSAGES


class UpdateTenantUseCase:
    def __init__(self, tenant_repository: ITenantRepository):
        self.tenant_repository = tenant_repository

    def execute(self, tenant_code: str, update_dto: TenantUpdate) -> TenantResponse:
        tenant_entity = self.tenant_repository.find_by_code(tenant_code)
        if not tenant_entity:
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_NOT_FOUND.CODE)

        if update_dto.name is not None:
            tenant_entity.name = update_dto.name
        if update_dto.contact_email is not None:
            existing_email = self.tenant_repository.find_by_email(
                update_dto.contact_email
            )
            if existing_email and existing_email.id != tenant_entity.id:
                raise ValueError(
                    MESSAGES.ERROR.VALIDATION.TENANT_EMAIL_ALREADY_EXISTS.CODE
                )
            tenant_entity.contact_email = update_dto.contact_email
        if update_dto.roles is not None:
            tenant_entity.roles = update_dto.roles

        updated_tenant = self.tenant_repository.update(tenant_entity)

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
