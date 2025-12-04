import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from utils import MESSAGES


class DigitalSignatureService:
    def __init__(self, private_key_pem: str):
        self.private_key = self._load_private_key(private_key_pem)

    def _load_private_key(self, private_key_pem: str):
        """Carga la clave privada desde string PEM"""
        if not private_key_pem:
            raise ValueError(MESSAGES.ERROR.VALIDATION.WORM_PRIVATE_KEY_INVALID.CODE)

        return serialization.load_pem_private_key(
            private_key_pem.encode(), password=None
        )

    def sign(self, data: str) -> str:
        """Firma datos y retorna signature en base64"""
        signature = self.private_key.sign(
            data.encode("utf-8"), ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode("utf-8")

    def get_public_key_pem(self) -> str:
        """Para que los reguladores puedan verificar"""
        public_key = self.private_key.public_key()
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
