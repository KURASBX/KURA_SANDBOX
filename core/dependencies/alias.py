from fastapi import Depends

from application.use_cases import (
    DeactivateAliasUseCase,
    RegisterAliasUseCase,
    ResolveAliasUseCase,
)
from core.database import get_db
from core.dependencies.alias_event import (
    get_alias_event_repository,
    get_hash_chain_service,
)
from core.dependencies.interop import (
    get_bank_routing_service,
    get_global_alias_repository,
)
from domain.repositories import (
    IAliasEventRepository,
    IAliasRepository,
    IGlobalAliasRepository,
)
from domain.services import BankRoutingService, HashChainService
from infrastructure.database.repositories import AliasRepository


def get_alias_repository(db=Depends(get_db)):
    return AliasRepository(db)


def get_register_alias_use_case(
    alias_repo: IAliasRepository = Depends(get_alias_repository),
    alias_event_repo: IAliasEventRepository = Depends(get_alias_event_repository),
    hash_chain_service: HashChainService = Depends(get_hash_chain_service),
    global_alias_repo: IGlobalAliasRepository = Depends(get_global_alias_repository),
    bank_routing_service: BankRoutingService = Depends(get_bank_routing_service),
) -> RegisterAliasUseCase:
    return RegisterAliasUseCase(
        alias_repository=alias_repo,
        alias_event_repository=alias_event_repo,
        hash_chain_service=hash_chain_service,
        global_alias_repository=global_alias_repo,
        bank_routing_service=bank_routing_service,
    )


def get_resolve_alias_use_case(
    alias_repo=Depends(get_alias_repository),
    alias_event_repo=Depends(get_alias_event_repository),
    hash_chain_service=Depends(get_hash_chain_service),
) -> ResolveAliasUseCase:
    return ResolveAliasUseCase(alias_repo, alias_event_repo, hash_chain_service)


def get_deactivate_alias_use_case(
    alias_repo=Depends(get_alias_repository),
    alias_event_repo=Depends(get_alias_event_repository),
    hash_chain_service=Depends(get_hash_chain_service),
) -> DeactivateAliasUseCase:
    return DeactivateAliasUseCase(alias_repo, alias_event_repo, hash_chain_service)
