from sqlalchemy.orm import Session

from domain.entities import BannerEntity
from domain.repositories import IBannerRepository
from infrastructure.database.models import BannerModel

from .base_sql_repository import BaseSQLRepository


class BannerRepository(BaseSQLRepository[BannerModel, BannerEntity], IBannerRepository):
    """ADAPTER - Implementación concreta para PostgreSQL"""

    def __init__(self, db: Session):
        super().__init__(db, BannerModel)

    def get_all_active(self) -> list[BannerEntity]:
        db_banners = (
            self.db.query(self.model)
            .filter(self.model.is_active)
            .filter(self.model.deleted_at.is_(None))
            .order_by(self.model.display_order)
            .all()
        )
        return [self._to_entity(banner) for banner in db_banners]

    def _to_entity(self, db_banner: BannerModel) -> BannerEntity:
        """Convertir modelo SQLAlchemy a entidad"""
        entity_data = {
            "id": db_banner.id,
            "title": db_banner.title,
            "description": db_banner.description,
            "image_url": db_banner.image_url,
            "is_active": db_banner.is_active,
            "display_order": db_banner.display_order,
            "created_at": db_banner.created_at.isoformat()
            if db_banner.created_at
            else None,
            "updated_at": db_banner.updated_at.isoformat()
            if db_banner.updated_at
            else None,
        }
        return BannerEntity(**entity_data)
