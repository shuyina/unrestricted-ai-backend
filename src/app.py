import logging
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import api_router
from src.core.config import settings
from src.middleware.error_handling import error_handler
from src.middleware.request_logging import RequestLoggingMiddleware

logger = logging.getLogger(__name__)


def create_app(lifespan: Callable | None = None) -> FastAPI:
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="Unrestricted AI generation backend",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return await error_handler(request, exc)

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": settings.APP_NAME}

    @app.get("/")
    async def root():
        return {"message": "Unrestricted AI backend is running", "docs": "/docs"}

    return app
