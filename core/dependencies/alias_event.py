from fastapi import Depends

from application.use_cases import (
    GetAliasEventHistoryUseCase,
    VerifyHashChainUseCase,
)
from core.database import get_db
from domain.repositories import IAliasEventRepository
from domain.services import HashChainService
from infrastructure.database.repositories import AliasEventRepository


def get_alias_event_repository(db=Depends(get_db)):
    return AliasEventRepository(db)


def get_alias_event_history_use_case(
    alias_event_repo: IAliasEventRepository = Depends(get_alias_event_repository),
) -> GetAliasEventHistoryUseCase:
    return GetAliasEventHistoryUseCase(alias_event_repo)


def get_hash_chain_service():
    return HashChainService()


def get_verify_hash_chain_use_case(
    alias_event_repo: IAliasEventRepository = Depends(get_alias_event_repository),
    hash_chain_service: HashChainService = Depends(get_hash_chain_service),
) -> VerifyHashChainUseCase:
    return VerifyHashChainUseCase(alias_event_repo, hash_chain_service)
