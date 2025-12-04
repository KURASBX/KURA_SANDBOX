from .health_router import health_router
from .v1.endpoints import routers as v1_routers

routers = [(health_router, "/health")]

for router, prefix in v1_routers:
    routers.append((router, f"/v1{prefix}"))
