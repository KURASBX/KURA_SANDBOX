import secrets
from uuid import UUID

from domain.repositories.tenant_repository import ITenantRepository
from utils import MESSAGES


class GenerateAPIKeyUseCase:
    def __init__(
        self,
        tenant_repository: ITenantRepository,
    ):
        self.tenant_repository = tenant_repository

    def execute(self, tenant_id: UUID) -> str:
        tenant = self.tenant_repository.get_by_id(tenant_id)

        if not tenant:
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_NOT_FOUND.CODE)

        if not tenant.is_active():
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_INACTIVE.CODE)

        return f"tk_{tenant.code}_{secrets.token_urlsafe(24)}"
