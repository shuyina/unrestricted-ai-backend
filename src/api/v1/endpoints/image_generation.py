from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from src.api.schemas import GenerationResponse, ImageGenerationRequest, JobStatusResponse
from src.services.image_service import ImageService

router = APIRouter()
service = ImageService()


@router.post("/")
async def generate_image(payload: ImageGenerationRequest):
    try:
        job_id = str(uuid4())
        return await service.generate(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/img2img")
async def generate_img2img(payload: ImageGenerationRequest):
    try:
        job_id = str(uuid4())
        return await service.img2img(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/inpaint")
async def generate_inpaint(payload: ImageGenerationRequest):
    try:
        job_id = str(uuid4())
        return await service.inpaint(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/job/{job_id}")
async def get_image_job(job_id: str):
    try:
        return await service.get_status(job_id)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=404, detail=str(exc)) from exc
