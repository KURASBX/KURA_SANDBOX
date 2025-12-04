from pydantic import BaseModel

from core.config import settings


class WormEvidenceItem(BaseModel):
    timestamp: str
    event_type: str
    tenant_id_hash: str
    payload_hash: str
    previous_hash: str
    current_hash: str


class WormEvidenceResponse(BaseModel):
    version: str = settings.WORM_VERSION
    issuer: str = settings.WORM_ISSUER
    issued_at: str
    period: str
    root_hash: str
    hash_chain: list[WormEvidenceItem]
    digital_signature: str
    public_key: str
