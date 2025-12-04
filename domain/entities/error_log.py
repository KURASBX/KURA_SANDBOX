from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ErrorLogEntity(BaseModel):
    """Entidad de dominio para logs de errores"""

    id: Optional[UUID] = None
    error_type: str
    message: str
    traceback: Optional[str] = None
    url: str
    method: str
    status_code: int
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
