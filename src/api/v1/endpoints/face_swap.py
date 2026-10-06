from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from src.api.schemas import FaceSwapRequest, GenerationResponse
from src.services.face_swap_service import FaceSwapService

router = APIRouter()
service = FaceSwapService()


@router.post("/")
async def faceswap(payload: FaceSwapRequest):
    try:
        job_id = str(uuid4())
        return await service.swap(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/batch")
async def faceswap_batch(requests: list[FaceSwapRequest]):
    try:
        job_id = str(uuid4())
        return await service.batch_swap(job_id, requests)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/job/{job_id}")
async def get_faceswap_job(job_id: str):
    try:
        return await service.get_status(job_id)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=404, detail=str(exc)) from exc
