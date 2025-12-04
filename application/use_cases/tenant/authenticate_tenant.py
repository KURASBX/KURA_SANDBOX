from application.dtos import TenantAuthRequest, TenantAuthResponse
from domain.repositories import ITenantRepository
from domain.services import JWTValidationService
from utils import MESSAGES


class AuthenticateTenantUseCase:
    def __init__(
        self,
        tenant_repository: ITenantRepository,
        jwt_service: JWTValidationService,
    ):
        self.tenant_repository = tenant_repository
        self.jwt_service = jwt_service

    def execute(self, auth_request: TenantAuthRequest) -> TenantAuthResponse:
        tenant = self.tenant_repository.find_by_code(auth_request.tenant_code)

        if not tenant:
            raise ValueError(MESSAGES.ERROR.AUTH.INVALID_CREDENTIALS.CODE)

        if not tenant.is_active():
            raise ValueError(MESSAGES.ERROR.AUTH.TENANT_INACTIVE.CODE)

        if not tenant.verify_api_key(auth_request.api_key):
            raise ValueError(MESSAGES.ERROR.AUTH.INVALID_CREDENTIALS.CODE)

        token = self.jwt_service.create_tenant_token(
            tenant_code=tenant.code,
            tenant_id=str(tenant.id),
            tenant_type=tenant.type,
            roles=tenant.roles,
        )

        return TenantAuthResponse(
            access_token=token,
            token_type="bearer",
            expires_in=86400,
            tenant_id=str(tenant.id),
            tenant_code=tenant.code,
            tenant_type=tenant.type,
            roles=tenant.roles,
        )
