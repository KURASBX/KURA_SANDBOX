import secrets
from uuid import uuid4

from application.dtos import TenantCreate, TenantResponse
from domain.entities import TenantEntity
from domain.repositories import ITenantRepository
from utils import MESSAGES, TenantStatus


class CreateTenantUseCase:
    def __init__(
        self,
        tenant_repository: ITenantRepository,
    ):
        self.tenant_repository = tenant_repository

    def execute(self, create_dto: TenantCreate) -> TenantResponse:
        if self.tenant_repository.find_by_code(create_dto.code):
            raise ValueError(MESSAGES.ERROR.VALIDATION.TENANT_CODE_EXISTS.CODE)

        if self.tenant_repository.find_by_email(create_dto.contact_email):
            raise ValueError(MESSAGES.ERROR.VALIDATION.TENANT_EMAIL_ALREADY_EXISTS.CODE)

        if create_dto.tax_id and self.tenant_repository.find_by_tax_id(
            create_dto.tax_id
        ):
            raise ValueError(MESSAGES.ERROR.VALIDATION.TENANT_TAX_ID_EXISTS.CODE)

        tenant_entity = TenantEntity(
            id=uuid4(),
            name=create_dto.name,
            code=create_dto.code,
            type=create_dto.type,
            contact_email=create_dto.contact_email,
            contact_phone=create_dto.contact_phone,
            website=create_dto.website,
            legal_name=create_dto.legal_name,
            tax_id=create_dto.tax_id,
            status=TenantStatus.PENDING,
            tenant_metadata=create_dto.tenant_metadata,
            roles=create_dto.roles,
        )

        saved_tenant = self.tenant_repository.create(tenant_entity)

        api_key = f"tk_{saved_tenant.code}_{secrets.token_urlsafe(24)}"

        return TenantResponse(
            id=saved_tenant.id,
            name=saved_tenant.name,
            code=saved_tenant.code,
            type=saved_tenant.type,
            contact_email=saved_tenant.contact_email,
            status=saved_tenant.status,
            roles=saved_tenant.roles,
            api_key=api_key,
            created_at=saved_tenant.created_at,
        )
