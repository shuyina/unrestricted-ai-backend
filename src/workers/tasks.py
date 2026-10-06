import logging

from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.health_check")
def health_check():
    return {"status": "ok"}


@celery_app.task(name="tasks.generate_image")
def generate_image_task(prompt: str, **kwargs):
    logger.info("Simulated image generation task: %s", prompt)
    return {"status": "completed", "prompt": prompt, "output": "placeholder.png"}
