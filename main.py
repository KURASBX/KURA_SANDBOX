from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api import routers
from core import http_error_handler_middleware, settings
from core.middleware.logging import LoggingMiddleware
from core.setup_logger import setup_logging

setup_logging()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.middleware("http")(http_error_handler_middleware)

for router, prefix in routers:
    app.include_router(router, prefix=f"/api{prefix}")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
