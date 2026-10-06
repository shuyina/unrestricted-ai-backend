import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.app import create_app
from src.core.config import settings
from src.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


app = create_app(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)
