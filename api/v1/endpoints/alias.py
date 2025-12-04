from datetime import date
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi.security import HTTPBearer

from application.dtos import (
    AliasCreate,
    AliasEventHistoryResponse,
    AliasResponse,
    DeactivateAliasCommand,
    GetAliasEventHistoryQuery,
    HashChainVerificationResponse,
    RegisterAliasCommand,
    ResolveAliasQuery,
    ResolveAliasResponse,
    VerifyHashChainQuery,
    WormEvidenceResponse,
)
from application.use_cases import (
    DeactivateAliasUseCase,
    GenerateWormEvidenceUseCase,
    GetAliasEventHistoryUseCase,
    RegisterAliasUseCase,
    ResolveAliasUseCase,
    VerifyHashChainUseCase,
)
from core.auth import get_current_tenant
from core.dependencies.alias import (
    get_deactivate_alias_use_case,
    get_register_alias_use_case,
    get_resolve_alias_use_case,
)
from core.dependencies.alias_event import (
    get_alias_event_history_use_case,
    get_verify_hash_chain_use_case,
)
from core.dependencies.interop import get_interop_service
from core.dependencies.tenant import get_current_roles
from core.dependencies.worm import get_worm_evidence_use_case, validate_regulator_access
from domain.services.interop_service import InteropService
from utils import MESSAGES

tenant_security = HTTPBearer(auto_error=False)

alias_router = APIRouter(tags=["aliases"], dependencies=[Depends(tenant_security)])


@alias_router.post("/", response_model=AliasResponse)
async def register_alias(
    request: Request,
    create_dto: AliasCreate,
    tenant_id: str = Depends(get_current_tenant),
    use_case: RegisterAliasUseCase = Depends(get_register_alias_use_case),
):
    correlation_id = getattr(request.state, "correlation_id", uuid4())
    command = RegisterAliasCommand(
        tenant_id=tenant_id,
        create_dto=create_dto,
        correlation_id=str(correlation_id),
    )
    try:
        return use_case.execute(command)
    except ValueError as e:
        if "already exists" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail=MESSAGES.ERROR.VALIDATION.ALIAS_ALREADY_EXISTS.CODE,
            ) from e
        if "invalid" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=MESSAGES.ERROR.VALIDATION.ALIAS_MUST_HAVE_4_TO_30_CHARACTERS.CODE,
            ) from e

        raise HTTPException(status_code=400, detail=str(e)) from e


@alias_router.get("/{alias}", response_model=ResolveAliasResponse)
async def resolve_alias(
    request: Request,
    alias: str = Path(..., min_length=4, max_length=30),
    tenant_id: str = Depends(get_current_tenant),
    use_case: ResolveAliasUseCase = Depends(get_resolve_alias_use_case),
):
    correlation_id = getattr(request.state, "correlation_id", uuid4())

    query = ResolveAliasQuery(tenant_id=tenant_id, alias=alias)
    try:
        return use_case.execute(query, correlation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@alias_router.get("/{alias}/history", response_model=AliasEventHistoryResponse)
async def get_alias_history(
    alias: str = Path(..., min_length=4, max_length=30),
    tenant_id: str = Depends(get_current_tenant),
    use_case: GetAliasEventHistoryUseCase = Depends(get_alias_event_history_use_case),
):
    """
    Obtener el historial completo de eventos de un alias
    """
    query = GetAliasEventHistoryQuery(
        tenant_id=tenant_id, alias=alias, correlation_id=uuid4()
    )
    try:
        return use_case.execute(query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@alias_router.get("/{alias}/verify-chain", response_model=HashChainVerificationResponse)
async def verify_hash_chain(
    alias: str = Path(..., min_length=4, max_length=30),
    tenant_id: str = Depends(get_current_tenant),
    use_case: VerifyHashChainUseCase = Depends(get_verify_hash_chain_use_case),
):
    """
    Verifica la integridad de la cadena de hashes para un alias
    - Valida que cada hash se calcule correctamente del anterior
    - Detecta manipulación o corrupción de datos
    - Proporciona reporte detallado de integridad
    """
    query = VerifyHashChainQuery(
        tenant_id=tenant_id, alias=alias, correlation_id=uuid4()
    )
    try:
        return use_case.execute(query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@alias_router.delete("/{alias}")
async def deactivate_alias(
    request: Request,
    alias: str = Path(..., min_length=4, max_length=30),
    tenant_id: str = Depends(get_current_tenant),
    use_case: DeactivateAliasUseCase = Depends(get_deactivate_alias_use_case),
):
    correlation_id = getattr(request.state, "correlation_id", uuid4())

    command = DeactivateAliasCommand(
        tenant_id=tenant_id,
        alias=alias,
        correlation_id=str(correlation_id),
    )
    success = use_case.execute(command)

    if not success:
        error_detail = MESSAGES.ERROR.VALIDATION.ALIAS_NOT_FOUND.CODE
        raise HTTPException(status_code=404, detail=error_detail)

    return {"ok": True, "alias": alias, "status": "INACTIVE"}


@alias_router.get(
    "/regulatory/worm-evidence/{evidence_date}", response_model=WormEvidenceResponse
)
async def get_worm_evidence(
    evidence_date: date,
    tenant_filter: Optional[str] = Query(
        None, description="Filtrar por tenant específico"
    ),
    regulator_access: bool = Depends(validate_regulator_access),
    use_case: GenerateWormEvidenceUseCase = Depends(get_worm_evidence_use_case),
    roles: list = Depends(get_current_roles),
):
    """
    Endpoint WORM para reguladores
    - RBAC: Solo tenants con rol ADMIN
    - DLP: No expone PII, solo hashes anonimizados
    - Audit: Debes implementar logging de acceso
    """

    return use_case.execute(evidence_date, tenant_filter)


@alias_router.get("/{alias}/validate", response_model=dict)
async def validate_global_alias(
    alias: str,
    tenant_id: str = Depends(get_current_tenant),
    interop_service: InteropService = Depends(get_interop_service),
):
    """
    Validación segura de alias - solo expone información anonimizada
    """
    return interop_service.validate_alias_global(alias, tenant_id)
