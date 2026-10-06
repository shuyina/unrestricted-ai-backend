import logging
from datetime import datetime

from src.api.schemas import GenerationResponse, VideoGenerationRequest
from src.services.orchestrator import GenerationOrchestrator
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


class VideoService:
    async def generate(self, job_id: str, payload: VideoGenerationRequest):
        celery_app.send_task(
            "tasks.generate_video",
            args=(job_id, payload.prompt, payload.negative_prompt, payload.duration_seconds, payload.fps),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="text_to_video",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=300,
        )

    async def image_to_video(self, job_id: str, payload: VideoGenerationRequest):
        celery_app.send_task(
            "tasks.generate_image_to_video",
            args=(job_id,),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="image_to_video",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=240,
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "processing",
            "progress": 25.0,
            "output_url": None,
            "error": None,
        }
