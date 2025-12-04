from datetime import datetime, timedelta

import jwt

from utils import MESSAGES, TenantRole


class JWTValidationService:
    """Servicio de dominio para validación JWT - Extendido para roles"""

    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        audience: str = "alias-api",
        issuer: str = "https://idp.local",
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.audience = audience
        self.issuer = issuer

    def create_tenant_token(
        self,
        tenant_code: str,
        tenant_id: str,
        tenant_type: str = None,
        roles: list = None,
    ) -> str:
        """Crea token JWT para tenant autenticado"""
        roles_for_jwt = []
        if roles:
            for role in roles:
                if isinstance(role, TenantRole):
                    roles_for_jwt.append(role.value)
                else:
                    roles_for_jwt.append(role)
        else:
            roles_for_jwt = [TenantRole.OPERATOR.value]

        payload = {
            "sub": f"tenant:{tenant_id}",
            "tenant_id": tenant_id,
            "tenant_code": tenant_code,
            "roles": roles_for_jwt,
            "aud": self.audience,
            "iss": self.issuer,
            "iat": datetime.now(),
            "exp": datetime.now() + timedelta(hours=24),
        }

        if tenant_type:
            payload["tenant_type"] = tenant_type

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def extract_tenant_id(self, payload: dict) -> str:
        """Extrae tenant_id de los claims del JWT"""
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise ValueError(MESSAGES.ERROR.AUTH.TOKEN_NEED_TENANT_ID.CODE)
        return tenant_id

    def extract_roles(self, payload: dict) -> list[str]:
        """Extrae los roles del JWT"""
        return payload.get("roles", ["operator"])

    def is_token_expired(self, payload: dict) -> bool:
        """Verifica si el token ha expirado"""
        exp = payload.get("exp")
        if not exp:
            return True
        return datetime.now().timestamp() > exp

    def validate_token(self, token: str) -> dict:
        """Verifica si el token es valido"""
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )
        except jwt.PyJWTError as e:
            raise ValueError(MESSAGES.ERROR.AUTH.INVALID_TOKEN.CODE) from e
