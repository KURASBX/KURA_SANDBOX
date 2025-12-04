from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from utils import MESSAGES


class BannerEntity(BaseModel):
    """ENTIDAD de dominio - pura lógica de negocio"""

    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True
    display_order: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @field_validator("display_order")
    def validate_order(cls, v):
        if v < 0:
            raise ValueError(MESSAGES.ERROR.VALIDATION.DISPLAY_ORDER_INVALID.CODE)
        return v

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    class Config:
        from_attributes = True
