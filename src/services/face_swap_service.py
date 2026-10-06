from datetime import datetime

from src.api.schemas import GenerationResponse


class FaceSwapService:
    async def swap(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="face_swap",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=120,
        )

    async def batch_swap(self, job_id: str, requests):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="face_swap_batch",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=max(60, len(requests) * 60),
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "processing",
            "progress": 20.0,
            "output_url": None,
            "error": None,
        }
