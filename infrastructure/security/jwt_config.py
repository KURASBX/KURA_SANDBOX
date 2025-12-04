from core import settings
from domain.services import JWTValidationService
from utils import MESSAGES


def get_jwt_validation_service() -> JWTValidationService:
    """Factory para el servicio de validación JWT"""
    secret = settings.JWT_SECRET
    if not secret:
        raise ValueError(MESSAGES.ERROR.VALIDATION.JWT_NOT_CONFIGURED_IN_ENV.CODE)

    return JWTValidationService(
        secret=secret,
        algorithm=settings.JWT_ALG,
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
    )
