from fastapi import Depends, HTTPException

from application.use_cases import GenerateWormEvidenceUseCase
from core.config import settings
from domain.services import DigitalSignatureService
from utils import MESSAGES, TenantRole

from .alias import get_alias_event_repository
from .tenant import get_current_roles


def validate_regulator_access(roles: list = Depends(get_current_roles)):
    """Valida que el tenant tenga permisos de regulador"""
    if TenantRole.ADMIN not in roles:
        raise HTTPException(
            status_code=403, detail=MESSAGES.ERROR.AUTH.REGULATOR_ROLE_REQUIRED.CODE
        )
    return True


def get_digital_signature_service() -> DigitalSignatureService:
    return DigitalSignatureService(settings.WORM_PRIVATE_KEY)


def get_worm_evidence_use_case(
    alias_event_repo=Depends(get_alias_event_repository),
    signature_service=Depends(get_digital_signature_service),
) -> GenerateWormEvidenceUseCase:
    return GenerateWormEvidenceUseCase(alias_event_repo, signature_service)
