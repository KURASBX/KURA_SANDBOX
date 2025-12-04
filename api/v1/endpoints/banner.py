from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos.banner import BannerCreate, BannerResponse, BannerUpdate
from application.use_cases.banner_service import BannerService
from core.database import get_db
from infrastructure.database.repositories.banner_repository import BannerRepository

banner_router = APIRouter(tags=["Banner v1"])


def get_banner_service(db=Depends(get_db)) -> BannerService:
    repository = BannerRepository(db)
    return BannerService(repository)


@banner_router.get("/", response_model=list[BannerResponse])
def list_banners(
    skip: int = 0,
    limit: int = 100,
    service: BannerService = Depends(get_banner_service),
):
    return service.get_all(skip=skip, limit=limit)


@banner_router.get("/active", response_model=list[BannerResponse])
def list_active_banners(service: BannerService = Depends(get_banner_service)):
    return service.get_active_banners()


@banner_router.get("/{banner_id}", response_model=BannerResponse)
def get_banner(banner_id: UUID, service: BannerService = Depends(get_banner_service)):
    banner = service.get_by_id(banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner


@banner_router.post(
    "/", response_model=BannerResponse, status_code=status.HTTP_201_CREATED
)
def create_banner(
    banner_data: BannerCreate,
    service: BannerService = Depends(get_banner_service),
):
    try:
        return service.create(banner_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@banner_router.put("/{banner_id}", response_model=BannerResponse)
def update_banner(
    banner_id: UUID,
    banner_data: BannerUpdate,
    service: BannerService = Depends(get_banner_service),
):
    updated = service.update(banner_id, banner_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Banner not found")
    return updated


@banner_router.delete("/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_banner(
    banner_id: UUID, service: BannerService = Depends(get_banner_service)
):
    if not service.delete(banner_id):
        raise HTTPException(status_code=404, detail="Banner not found")
