import hashlib
import os
from datetime import date, datetime
from typing import Optional

from application.dtos import WormEvidenceItem, WormEvidenceResponse
from core.config import settings
from core.logger import get_logger, log_execution_time
from domain.entities import AliasEventEntity
from domain.repositories import IAliasEventRepository
from domain.services import DigitalSignatureService

logger = get_logger("use_cases.worm")


class GenerateWormEvidenceUseCase:
    def __init__(
        self,
        alias_event_repository: IAliasEventRepository,
        signature_service: DigitalSignatureService,
    ):
        self.repo = alias_event_repository
        self.signer = signature_service

    def execute(
        self, target_date: date, tenant_id: Optional[str] = None
    ) -> WormEvidenceResponse:
        # ejemplo de uso de logger de tiempo de ejecución

        # Medir solo la parte de base de datos + procesamiento
        with log_execution_time(logger, "WORM data processing"):
            daily_events = self.repo.get_events_by_date(target_date, tenant_id)
            worm_events = self._build_worm_events(daily_events)
            root_hash = self._calculate_period_root(worm_events)

        # Medir solo la firma digital (operación criptográfica)
        with log_execution_time(logger, "Digital signature"):
            signature_payload = f"{target_date.isoformat()}:{root_hash}"
            digital_signature = self.signer.sign(signature_payload)

        logger.info(
            "WORM evidence generated successfully",
            events_count=len(worm_events),
            root_hash=root_hash,
        )

        return WormEvidenceResponse(
            version=settings.WORM_VERSION,
            issuer=settings.WORM_ISSUER,
            issued_at=datetime.now().isoformat() + "Z",
            period=target_date.isoformat(),
            root_hash=root_hash,
            hash_chain=worm_events,
            digital_signature=digital_signature,
            public_key=self.signer.get_public_key_pem(),
        )

    def _build_worm_events(
        self, events: list[AliasEventEntity]
    ) -> list[WormEvidenceItem]:
        """Convierte eventos en formato WORM sin PII"""
        worm_events = []

        for event in events:
            tenant_id_hash = hashlib.sha256(
                f"{event.tenant_id}_{os.getenv('CUB_PEPPER')}".encode()
            ).hexdigest()

            worm_events.append(
                WormEvidenceItem(
                    timestamp=event.timestamp.isoformat() + "Z",
                    event_type=event.event_type,
                    tenant_id_hash=tenant_id_hash[:16],
                    payload_hash=event.current_hash,
                    previous_hash=event.previous_hash,
                    current_hash=event.current_hash,
                )
            )

        return worm_events

    def _calculate_period_root(self, worm_events: list[WormEvidenceItem]) -> str:
        """Calcula hash raíz concatenando todos los current_hash finales"""
        if not worm_events:
            return hashlib.sha256(b"empty_day").hexdigest()

        hash_material = "".join(event.current_hash for event in worm_events)
        return hashlib.sha256(hash_material.encode()).hexdigest()
