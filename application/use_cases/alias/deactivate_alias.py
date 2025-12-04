from datetime import datetime

from application.dtos import DeactivateAliasCommand
from domain.entities import AliasEventEntity
from domain.repositories import IAliasEventRepository, IAliasRepository
from domain.services import HashChainService
from utils import EEventType


class DeactivateAliasUseCase:
    def __init__(
        self,
        alias_repository: IAliasRepository,
        alias_event_repository: IAliasEventRepository,
        hash_chain_service: HashChainService,
    ):
        self.alias_repository = alias_repository
        self.alias_event_repository = alias_event_repository
        self.hash_chain_service = hash_chain_service

    def execute(self, command: DeactivateAliasCommand) -> bool:
        alias_normalized = command.alias.strip().lower()

        alias_entity = self.alias_repository.find_by_normalized_alias(
            command.tenant_id, alias_normalized
        )

        if not alias_entity:
            return False

        if alias_entity.status == "INACTIVE":
            return True

        success = self.alias_repository.update_status(alias_entity.id, "INACTIVE")

        if not success:
            return False

        last_event = self.alias_event_repository.get_last_event_for_alias(
            alias_normalized, command.tenant_id
        )
        previous_hash = last_event.current_hash if last_event else "0" * 64

        current_hash = self.hash_chain_service.calculate_event_hash(
            tenant_id=command.tenant_id,
            alias=alias_normalized,
            event_type=EEventType.DEACTIVATE,
            timestamp=datetime.now(),
            previous_hash=previous_hash,
        )

        event_entity = AliasEventEntity(
            alias_normalized=alias_normalized,
            tenant_id=command.tenant_id,
            event_type=EEventType.DEACTIVATE,
            correlation_id=command.correlation_id,
            previous_hash=previous_hash,
            current_hash=current_hash,
            timestamp=datetime.now(),
        )
        self.alias_event_repository.create(event_entity)

        return True
