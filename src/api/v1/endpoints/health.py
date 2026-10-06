from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "healthy", "service": "api"}


@router.get("/status")
async def status():
    return {
        "status": "operational",
        "components": {
            "api": "healthy",
            "gpu": "ready",
            "redis": "configured",
            "storage": "ready",
        },
    }
