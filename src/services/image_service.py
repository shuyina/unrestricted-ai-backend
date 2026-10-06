from datetime import datetime

from src.api.schemas import GenerationResponse


class BaseService:
    async def get_status(self, job_id: str):
        return {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "output_url": None,
            "error": None,
        }


class ImageService(BaseService):
    async def generate(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="text_to_image",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=60,
        )

    async def img2img(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="image_to_image",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=45,
        )

    async def inpaint(self, job_id: str, payload):
        return GenerationResponse(
            job_id=job_id,
            status="queued",
            mode="inpaint",
            created_at=datetime.utcnow().isoformat(),
            estimated_time_seconds=45,
        )
