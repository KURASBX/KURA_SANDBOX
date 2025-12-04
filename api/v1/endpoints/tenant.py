from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from application.dtos.tenant import (
    TenantAuthRequest,
    TenantAuthResponse,
    TenantCreate,
    TenantResponse,
)
from application.use_cases import (
    ActivateTenantUseCase,
    GetTenantListUseCase,
    GetTenantUseCase,
)
from application.use_cases.tenant.create_tenant import CreateTenantUseCase
from core.dependencies.tenant import (
    get_activate_tenant_use_case,
    get_create_tenant_use_case,
    get_jwt_service,
    get_tenant_list,
    get_tenant_repository,
    get_tenant_use_case,
)
from domain.services import JWTValidationService
from infrastructure.database.repositories import TenantRepository
from utils import MESSAGES

tenant_security = HTTPBearer()

router = APIRouter(tags=["Tenants"])


@router.post(
    "/",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new tenant",
)
async def create_tenant(
    create_dto: TenantCreate,
    use_case: CreateTenantUseCase = Depends(get_create_tenant_use_case),
):
    """
    Create a new tenant (Bank, Admin, or Partner)
    """
    try:
        return use_case.execute(create_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("/{tenant_id}", response_model=TenantResponse, summary="Get tenant by ID")
async def get_tenant(
    tenant_id: UUID,
    use_case: GetTenantUseCase = Depends(get_tenant_use_case),
):
    """
    Get tenant details by ID
    """
    try:
        return use_case.execute(tenant_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MESSAGES.ERROR.VALIDATION.TENANT_NOT_FOUND.CODE,
        ) from e


@router.get("/", response_model=list[TenantResponse])
async def list_tenants(
    skip: int = 0,
    limit: int = 10,
    use_case: GetTenantListUseCase = Depends(get_tenant_list),
):
    """
    List all tenants
    """
    return use_case.execute(skip=skip, limit=limit)


@router.post("/auth/token", response_model=TenantAuthResponse)
async def authenticate_tenant_mvp(
    auth_request: TenantAuthRequest,
    tenant_repo: TenantRepository = Depends(get_tenant_repository),
    jwt_service: JWTValidationService = Depends(get_jwt_service),
):
    """
    MVP: Auth simplificado - solo verifica que el tenant exista
    """
    tenant = tenant_repo.find_by_code(auth_request.tenant_code)

    if not tenant:
        raise HTTPException(
            status_code=401, detail=MESSAGES.ERROR.AUTH.TENANT_NOT_FOUND.CODE
        )

    if not tenant.is_active():
        raise HTTPException(
            status_code=401, detail=MESSAGES.ERROR.AUTH.TENANT_INACTIVE.CODE
        )

    if not tenant.verify_api_key(auth_request.api_key):
        raise HTTPException(
            status_code=401, detail=MESSAGES.ERROR.AUTH.INVALID_API_KEY.CODE
        )

    token = jwt_service.create_tenant_token(
        tenant.code, str(tenant.id), tenant.type, tenant.roles
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


@router.post(
    "/{tenant_code}/activate",
    response_model=TenantResponse,
    status_code=status.HTTP_200_OK,
    summary="Activate tenant",
)
async def activate_tenant(
    tenant_code: str,
    use_case: ActivateTenantUseCase = Depends(get_activate_tenant_use_case),
):
    """
    Activate a pending tenant
    """
    try:
        return use_case.execute(tenant_code)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
