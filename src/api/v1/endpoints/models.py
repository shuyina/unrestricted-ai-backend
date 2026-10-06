from fastapi import APIRouter

router = APIRouter()


@router.get("/available")
async def available_models():
    return {
        "image": ["sdxl", "realvisxl", "img2img"],
        "video": ["animatediff", "image-to-video"],
        "faceswap": ["roop", "deepfacelive"],
        "llm": ["llama3", "mistral", "gpt-4"],
    }
