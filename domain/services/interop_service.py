import hashlib
from datetime import datetime
from typing import Any

from core.logger import get_logger
from domain.entities import InteropAuditEntity
from domain.entities.alias_event_entity import AliasEventEntity
from domain.repositories import (
    IAliasEventRepository,
    IGlobalAliasRepository,
    IInteropAuditRepository,
)
from domain.services import BankRoutingService, HashChainService
from utils import MESSAGES, EEventType

logger = get_logger("domain.services.interop")


class InteropService:
    """Servicio de dominio para operaciones de interoperabilidad"""

    def __init__(
        self,
        global_alias_repo: IGlobalAliasRepository,
        audit_repo: IInteropAuditRepository,
        bank_routing_service: BankRoutingService,
        alias_event_repo: IAliasEventRepository,
        hash_chain_service: HashChainService,
    ):
        self.global_alias_repo = global_alias_repo
        self.audit_repo = audit_repo
        self.bank_routing_service = bank_routing_service
        self.alias_event_repo = alias_event_repo
        self.hash_chain_service = hash_chain_service

    def validate_alias_global(
        self, alias: str, requesting_tenant_id: str
    ) -> dict[str, Any]:
        """
        Valida un alias a nivel global sin exponer información sensible
        Retorna información anonimizada para interoperabilidad
        """
        alias_normalized = alias.strip().lower()
        global_alias = self.global_alias_repo.find_active_alias(alias_normalized)

        audit_entity = InteropAuditEntity.create_validation_query(
            requesting_tenant_id=requesting_tenant_id,
            alias_normalized=alias_normalized,
            target_tenant_id=global_alias.owning_tenant_id if global_alias else None,
        )
        self.audit_repo.log_validation_query(audit_entity)

        if not global_alias:
            return {
                "exists": False,
                "alias_hash": self._hash_alias(alias_normalized),
                "timestamp": datetime.now().isoformat() + "Z",
                "detail": MESSAGES.ERROR.VALIDATION.ALIAS_NOT_FOUND.CODE,
            }

        if global_alias and not self.bank_routing_service.validate_routing_code(
            global_alias.routing_code
        ):
            return {
                "exists": False,
                "alias_hash": self._hash_alias(alias_normalized),
                "timestamp": datetime.now().isoformat() + "Z",
                "detail": MESSAGES.ERROR.VALIDATION.INVALID_ROUTING_CODE.CODE,
            }
        if global_alias:
            last_event = self.alias_event_repo.get_last_event_for_alias(
                alias_normalized, global_alias.owning_tenant_id
            )
            previous_hash = last_event.current_hash if last_event else "0" * 64

            current_hash = self.hash_chain_service.calculate_event_hash(
                tenant_id=global_alias.owning_tenant_id,
                alias=alias_normalized,
                event_type=EEventType.INTEROP_RESOLVE,
                timestamp=datetime.now(),
                previous_hash=previous_hash,
            )

            event_entity = AliasEventEntity(
                alias_normalized=alias_normalized,
                tenant_id=global_alias.owning_tenant_id,
                event_type=EEventType.INTEROP_RESOLVE,
                correlation_id=audit_entity.correlation_id,
                previous_hash=previous_hash,
                current_hash=current_hash,
                timestamp=datetime.now(),
            )
            self.alias_event_repo.create(event_entity)

        return {
            "exists": True,
            "alias_hash": self._hash_alias(alias_normalized),
            "routing_code": global_alias.routing_code,
            "account_type_category": "VALIDATED",  # Genérico por privacidad
            "validation_level": "CROSS_TENANT",
            "timestamp": datetime.now().isoformat() + "Z",
        }

    def _hash_alias(self, alias_normalized: str) -> str:
        """Calcula hash del alias para no exponer el valor real"""
        return hashlib.sha256(alias_normalized.encode()).hexdigest()
