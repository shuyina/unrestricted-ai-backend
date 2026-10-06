from fastapi import APIRouter

from src.api.v1.endpoints.health import router as health_router
from src.api.v1.endpoints.image_generation import router as image_router
from src.api.v1.endpoints.video_generation import router as video_router
from src.api.v1.endpoints.face_swap import router as face_swap_router
from src.api.v1.endpoints.llm import router as llm_router
from src.api.v1.endpoints.nerf import router as nerf_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(image_router, prefix="/generate/image", tags=["image"])
api_router.include_router(video_router, prefix="/generate/video", tags=["video"])
api_router.include_router(face_swap_router, prefix="/faceswap", tags=["faceswap"])
api_router.include_router(llm_router, prefix="/llm", tags=["llm"])
api_router.include_router(nerf_router, prefix="/nerf", tags=["nerf"])
