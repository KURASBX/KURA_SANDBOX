from application.dtos import BannerCreate, BannerUpdate
from domain.entities import BannerEntity
from domain.repositories import IBannerRepository

from .base_service import BaseService


class BannerService(BaseService[BannerEntity, BannerCreate, BannerUpdate]):
    """Caso de uso específico para Banners que extiende BaseService"""

    def __init__(self, banner_repository: IBannerRepository):
        super().__init__(banner_repository)
        self.banner_repo = banner_repository

    def get_active_banners(self) -> list[BannerEntity]:
        """Método específico de Banner que no está en el BaseService"""
        return self.banner_repo.get_all_active()
