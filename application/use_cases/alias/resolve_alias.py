from datetime import datetime, timezone
from uuid import UUID

from application.dtos import ResolveAliasQuery, ResolveAliasResponse
from domain.entities import AliasEventEntity
from domain.repositories import IAliasEventRepository, IAliasRepository
from domain.services import HashChainService
from utils import EEventType


class ResolveAliasUseCase:
    def __init__(
        self,
        alias_repository: IAliasRepository,
        alias_event_repository: IAliasEventRepository,
        hash_chain_service: HashChainService,
    ):
        self.alias_repository = alias_repository
        self.alias_event_repository = alias_event_repository
        self.hash_chain_service = hash_chain_service

    def execute(
        self, query: ResolveAliasQuery, correlation_id: UUID
    ) -> ResolveAliasResponse:
        alias_normalized = query.alias.strip().lower()

        alias_entity = self.alias_repository.find_active_by_normalized_alias(
            tenant_id=query.tenant_id, alias_normalized=alias_normalized
        )

        if not alias_entity:
            return ResolveAliasResponse.not_found()

        if alias_entity.tenant_id != query.tenant_id:
            return ResolveAliasResponse.not_found()

        last_event = self.alias_event_repository.get_last_event_for_alias(
            alias_normalized, alias_entity.tenant_id
        )

        previous_hash = last_event.current_hash if last_event else "0" * 64
        timestamp = datetime.now(timezone.utc)
        current_hash = self.hash_chain_service.calculate_event_hash(
            tenant_id=query.tenant_id,
            alias=alias_normalized,
            event_type=EEventType.RESOLVE,
            timestamp=timestamp,
            previous_hash=previous_hash,
        )

        event_entity = AliasEventEntity(
            alias_normalized=alias_normalized,
            tenant_id=query.tenant_id,
            event_type=EEventType.RESOLVE,
            correlation_id=correlation_id,
            previous_hash=previous_hash,
            current_hash=current_hash,
            timestamp=timestamp,
        )
        self.alias_event_repository.create(event_entity)

        return ResolveAliasResponse.found(alias_entity)
