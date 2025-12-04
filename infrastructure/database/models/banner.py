from sqlalchemy import Boolean, Column, Integer, String, Text

from infrastructure.database.models import BaseModel


class BannerModel(BaseModel):
    __tablename__ = "banners"

    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    display_order = Column(Integer, default=0)
