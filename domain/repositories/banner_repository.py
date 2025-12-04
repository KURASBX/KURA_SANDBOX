from abc import ABC, abstractmethod

from domain.entities import BannerEntity

from .base_repository import IBaseRepository


class IBannerRepository(IBaseRepository[BannerEntity], ABC):
    """PORT - Extiende la interfaz base con métodos específicos de Banner"""

    @abstractmethod
    def get_all_active(self) -> list[BannerEntity]:
        pass
