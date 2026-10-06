import logging
from datetime import datetime

from src.api.schemas import GenerationResponse, NerfTrainRequest
from src.services.orchestrator import GenerationOrchestrator
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


class NerfService:
    async def train(self, job_id: str, payload: NerfTrainRequest):
        celery_app.send_task(
            "tasks.nerf_train",
            args=(job_id, payload.image_urls, payload.resolution, payload.num_steps),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="nerf_train",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=1800,
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "output_url": None,
            "error": None,
        }
