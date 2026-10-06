import logging
from datetime import datetime
from uuid import uuid4

from src.api.schemas import GenerationResponse, ImageGenerationRequest
from src.services.orchestrator import GenerationOrchestrator
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


class ImageService:
    async def generate(self, job_id: str, payload: ImageGenerationRequest):
        # Queue async task
        celery_app.send_task(
            "tasks.generate_image",
            args=(job_id, payload.model, payload.prompt, payload.negative_prompt, payload.width, payload.height, payload.steps, payload.guidance_scale, payload.seed),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="text_to_image",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=60,
        )

    async def img2img(self, job_id: str, payload: ImageGenerationRequest):
        celery_app.send_task(
            "tasks.generate_img2img",
            args=(job_id,),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="image_to_image",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=45,
        )

    async def inpaint(self, job_id: str, payload: ImageGenerationRequest):
        celery_app.send_task(
            "tasks.generate_inpaint",
            args=(job_id,),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="inpaint",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=45,
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "processing",
            "progress": 50.0,
            "output_url": None,
            "error": None,
        }
