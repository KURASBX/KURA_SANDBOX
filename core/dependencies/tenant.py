from typing import Optional

from fastapi import Depends, Request

from application.use_cases import (
    GetTenantUseCase,
    UpdateTenantUseCase,
)
from application.use_cases.tenant.activate_tenant import ActivateTenantUseCase
from application.use_cases.tenant.authenticate_tenant import AuthenticateTenantUseCase
from application.use_cases.tenant.create_tenant import CreateTenantUseCase
from application.use_cases.tenant.generate_api_key import GenerateAPIKeyUseCase
from application.use_cases.tenant.get_tenant_list import GetTenantListUseCase
from core.config import settings
from core.database import get_db
from domain.repositories import ITenantRepository
from domain.services import JWTValidationService
from infrastructure.database.repositories import (
    TenantRepository,
)
from utils.value_objects.enums import TenantRole


def get_jwt_service() -> JWTValidationService:
    """Servicio JWT unificado para toda la aplicación"""
    return JWTValidationService(
        secret=settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
    )


def get_tenant_repository(db=Depends(get_db)):
    return TenantRepository(db)


def get_activate_tenant_use_case(
    tenant_repo: ITenantRepository = Depends(get_tenant_repository),
) -> ActivateTenantUseCase:
    return ActivateTenantUseCase(tenant_repo)


def get_generate_api_key_use_case(
    tenant_repo: ITenantRepository = Depends(get_tenant_repository),
) -> GenerateAPIKeyUseCase:
    return GenerateAPIKeyUseCase(tenant_repo)


def get_create_tenant_use_case(
    tenant_repo: ITenantRepository = Depends(get_tenant_repository),
) -> CreateTenantUseCase:
    return CreateTenantUseCase(tenant_repo)


def get_authenticate_tenant_use_case(
    tenant_repo: ITenantRepository = Depends(get_tenant_repository),
    jwt_service: JWTValidationService = Depends(get_jwt_service),
) -> AuthenticateTenantUseCase:
    return AuthenticateTenantUseCase(tenant_repo, jwt_service)


def get_update_tenant_use_case(
    tenant_repo=Depends(get_tenant_repository),
) -> UpdateTenantUseCase:
    return UpdateTenantUseCase(tenant_repo)


def get_tenant_use_case(
    tenant_repo=Depends(get_tenant_repository),
) -> GetTenantUseCase:
    return GetTenantUseCase(tenant_repo)


def get_current_tenant_data(
    jwt_service: JWTValidationService = Depends(get_jwt_service),
    request: Request = None,
) -> dict:
    """Obtiene los datos del tenant actual desde el token JWT"""
    auth: Optional[str] = None
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"]
    if not auth:
        return {}

    scheme, _, token = auth.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return {}

    payload = jwt_service.validate_token(token)
    return payload.get("tenant", {})


def get_current_roles(
    jwt_service: JWTValidationService = Depends(get_jwt_service),
    request: Request = None,
) -> list[TenantRole]:
    """Extrae roles directamente del token JWT - VERSIÓN MEJORADA"""
    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Bearer "):
        return [TenantRole.OPERATOR]

    token = auth[7:]
    try:
        payload = jwt_service.validate_token(token)
        roles = payload.get("roles", [TenantRole.OPERATOR.value])

        tenant_roles = []
        for role in roles:
            if isinstance(role, str):
                try:
                    for tenant_role in TenantRole:
                        if tenant_role.value == role.lower():
                            tenant_roles.append(tenant_role)
                            break
                    else:
                        tenant_roles.append(TenantRole[role.upper()])
                except (ValueError, KeyError):
                    continue
            elif isinstance(role, TenantRole):
                tenant_roles.append(role)

        return tenant_roles if tenant_roles else [TenantRole.OPERATOR]

    except Exception:
        return [TenantRole.OPERATOR]


def get_tenant_list(
    tenant_repo=Depends(get_tenant_repository),
) -> GetTenantListUseCase:
    return GetTenantListUseCase(tenant_repo)
