from uuid import uuid4

from fastapi import APIRouter, HTTPException

from src.api.schemas import NerfTrainRequest
from src.services.nerf_service import NerfService

router = APIRouter()
service = NerfService()


@router.post("/train")
async def train_nerf(payload: NerfTrainRequest):
    try:
        job_id = str(uuid4())
        return await service.train(job_id, payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/job/{job_id}")
async def get_nerf_job(job_id: str):
    try:
        return await service.get_status(job_id)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=404, detail=str(exc)) from exc
