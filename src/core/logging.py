import logging
from pathlib import Path

from src.core.config import settings


def setup_logging() -> None:
    Path("./logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
