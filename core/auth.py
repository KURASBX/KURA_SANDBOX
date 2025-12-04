from typing import Optional
from uuid import UUID

from fastapi import Header, HTTPException, Request, status
from fastapi.security import HTTPBearer

from infrastructure.security.jwt_config import get_jwt_validation_service
from utils import MESSAGES

security = HTTPBearer()


async def get_current_tenant(
    request: Request,
    authorization: Optional[str] = Header(None),
) -> UUID:
    """
    Dependencia principal para extraer tenant_id del JWT
    """

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MESSAGES.ERROR.AUTH.TOKEN_REQUIRED.CODE,
        )

    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=MESSAGES.ERROR.AUTH.INVALID_AUTH_FORMAT.CODE,
            )

        token = authorization.replace("Bearer ", "").strip()

        validation_service = get_jwt_validation_service()
        payload = validation_service.validate_token(token)

        if validation_service.is_token_expired(payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=MESSAGES.ERROR.AUTH.TOKEN_EXPIRED.CODE,
            )

        tenant_id = validation_service.extract_tenant_id(payload)

        request.state.jwt_payload = payload
        request.state.tenant_id = tenant_id

        return tenant_id

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MESSAGES.ERROR.AUTH.ERROR_GENERATING_TOKEN.CODE,
        ) from e


async def get_current_user_payload(
    request: Request,
    authorization: Optional[str] = Header(None),
) -> dict:
    """
    Dependencia para obtener el payload completo del JWT
    Útil para extraer roles u otra información
    """
    await get_current_tenant(request, authorization)
    return request.state.jwt_payload


async def require_role(
    required_role: str, request: Request, authorization: Optional[str] = Header(None)
):
    """
    Dependencia para verificar roles específicos
    """
    payload = await get_current_user_payload(request, authorization)

    user_roles = payload.get("roles", [])
    if required_role not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Se requiere rol: {required_role}",
        )

    return payload
