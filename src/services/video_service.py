from datetime import datetime

from src.api.schemas import GenerationResponse


class VideoService:
    async def generate(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="text_to_video",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=180,
        )

    async def image_to_video(self, job_id: str, payload):
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
            "progress": 35.0,
            "output_url": None,
            "error": None,
        }
