from datetime import datetime

from src.api.schemas import GenerationResponse


class NerfService:
    async def train(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="nerf_train",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=600,
        )

    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "output_url": None,
            "error": None,
        }
