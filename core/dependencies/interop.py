from fastapi import Depends

from core.database import get_db
from core.dependencies.alias import get_alias_event_repository, get_hash_chain_service
from domain.repositories import (
    IAliasEventRepository,
    IGlobalAliasRepository,
    IInteropAuditRepository,
)
from domain.services import BankRoutingService, HashChainService, InteropService
from infrastructure.database.repositories import (
    GlobalAliasRepository,
    InteropAuditRepository,
)


def get_global_alias_repository(db=Depends(get_db)) -> IGlobalAliasRepository:
    return GlobalAliasRepository(db)


def get_interop_audit_repository(db=Depends(get_db)) -> IInteropAuditRepository:
    return InteropAuditRepository(db)


def get_bank_routing_service() -> BankRoutingService:
    return BankRoutingService()


def get_interop_service(
    global_alias_repo: IGlobalAliasRepository = Depends(get_global_alias_repository),
    audit_repo: IInteropAuditRepository = Depends(get_interop_audit_repository),
    bank_routing: BankRoutingService = Depends(get_bank_routing_service),
    alias_event_repo: IAliasEventRepository = Depends(get_alias_event_repository),
    hash_chain_service: HashChainService = Depends(get_hash_chain_service),
) -> InteropService:
    return InteropService(
        global_alias_repo,
        audit_repo,
        bank_routing,
        alias_event_repo,
        hash_chain_service,
    )
