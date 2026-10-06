import logging
from datetime import datetime

from src.api.schemas import GenerationResponse, FaceSwapRequest
from src.services.orchestrator import GenerationOrchestrator
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


class FaceSwapService:
    async def swap(self, job_id: str, payload: FaceSwapRequest):
        celery_app.send_task(
            "tasks.faceswap",
            args=(job_id, payload.source_image_url, payload.target_image_url, payload.method, payload.blend_ratio),
        )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="face_swap",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=120,
        )

    async def batch_swap(self, job_id: str, requests):
        for idx, req in enumerate(requests):
            celery_app.send_task(
                "tasks.faceswap",
                args=(f"{job_id}_{idx}", req.source_image_url, req.target_image_url, req.method, req.blend_ratio),
            )
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="face_swap_batch",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=len(requests) * 120,
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "processing",
            "progress": 15.0,
            "output_url": None,
            "error": None,
        }
