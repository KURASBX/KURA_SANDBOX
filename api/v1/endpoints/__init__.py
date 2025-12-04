from .alias import alias_router
from .banner import banner_router
from .tenant import router as tenant_router

routers = [
    (alias_router, "/aliases"),
    (tenant_router, "/tenants"),
    (banner_router, "/banners"),
]
