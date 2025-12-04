from application.dtos import AliasResponse, RegisterAliasCommand
from domain.entities import AliasEventEntity, AliasRegistryEntity, GlobalAliasEntity
from domain.repositories import (
    IAliasEventRepository,
    IAliasRepository,
    IGlobalAliasRepository,
)
from domain.services import BankRoutingService, HashChainService
from utils import MESSAGES, AliasStatus, EEventType


class RegisterAliasUseCase:
    def __init__(
        self,
        alias_repository: IAliasRepository,
        alias_event_repository: IAliasEventRepository,
        hash_chain_service: HashChainService,
        global_alias_repository: IGlobalAliasRepository,
        bank_routing_service: BankRoutingService,
    ):
        self.alias_repository = alias_repository
        self.alias_event_repository = alias_event_repository
        self.hash_chain_service = hash_chain_service
        self.global_alias_repository = global_alias_repository
        self.bank_routing_service = bank_routing_service

    def execute(self, command: RegisterAliasCommand) -> AliasResponse:
        alias_normalized = command.create_dto.alias.strip().lower()

        existing_alias = self.alias_repository.find_active_by_normalized_alias(
            command.tenant_id, alias_normalized
        )
        existing_global_alias = self.global_alias_repository.find_active_alias(
            alias_normalized
        )
        if existing_alias or existing_global_alias:
            raise ValueError(MESSAGES.ERROR.VALIDATION.ALIAS_ALREADY_EXISTS.CODE)

        alias_entity = AliasRegistryEntity(
            tenant_id=command.tenant_id,
            alias_raw=command.create_dto.alias,
            alias_normalized=alias_normalized,
            bank=command.create_dto.bank,
            account_type=command.create_dto.account_type,
            last_4=command.create_dto.last_4,
            status=AliasStatus.ACTIVE,
        )

        alias_entity.acc_hash = self.hash_chain_service.calculate_cub_hash(
            tenant_id=command.tenant_id,
            bank=command.create_dto.bank,
            account_type=command.create_dto.account_type,
            last_4=command.create_dto.last_4,
            alias_normalized=alias_normalized,
        )

        saved_alias = self.alias_repository.create(alias_entity)

        routing_code = self.bank_routing_service.get_routing_code(
            command.create_dto.bank
        )

        global_alias_entity = GlobalAliasEntity.create(
            alias_normalized=alias_normalized,
            owning_tenant_id=command.tenant_id,
            routing_code=routing_code,
        )

        self.global_alias_repository.create(global_alias_entity)

        last_event = self.alias_event_repository.get_last_event_for_alias(
            alias_normalized, command.tenant_id
        )
        previous_hash = last_event.current_hash if last_event else "0" * 64
        current_hash = self.hash_chain_service.calculate_event_hash(
            tenant_id=command.tenant_id,
            alias=alias_normalized,
            event_type=EEventType.REGISTER,
            timestamp=saved_alias.created_at,
            previous_hash=previous_hash,
        )

        event_entity = AliasEventEntity(
            alias_normalized=alias_normalized,
            tenant_id=command.tenant_id,
            event_type=EEventType.REGISTER,
            correlation_id=command.correlation_id,
            previous_hash=previous_hash,
            current_hash=current_hash,
            timestamp=saved_alias.created_at,
        )
        self.alias_event_repository.create(event_entity)

        return AliasResponse(
            id=saved_alias.id,
            alias_raw=saved_alias.alias_raw,
            bank=saved_alias.bank,
            account_type=saved_alias.account_type,
            last_4=saved_alias.last_4,
            status=saved_alias.status,
        )
