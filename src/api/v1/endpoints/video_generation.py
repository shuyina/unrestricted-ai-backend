from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from src.api.schemas import GenerationResponse, JobStatusResponse, VideoGenerationRequest
from src.services.video_service import VideoService

router = APIRouter()
service = VideoService()


@router.post("/")
async def generate_video(payload: VideoGenerationRequest):
    try:
        job_id = str(uuid4())
        return await service.generate(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/image-to-video")
async def image_to_video(payload: VideoGenerationRequest):
    try:
        job_id = str(uuid4())
        return await service.image_to_video(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/job/{job_id}")
async def get_video_job(job_id: str):
    try:
        return await service.get_status(job_id)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=404, detail=str(exc)) from exc
