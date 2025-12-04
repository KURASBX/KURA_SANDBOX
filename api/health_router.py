from datetime import datetime

from fastapi import APIRouter

from core.config import settings

health_router = APIRouter(tags=["Health"])

app_start_time = datetime.now()


@health_router.get("/")
async def health_basic():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }
