from fastapi import APIRouter, HTTPException

from src.api.schemas import LLMChatRequest
from src.services.llm_service import LLMService

router = APIRouter()
service = LLMService()


@router.post("/chat")
async def llm_chat(payload: LLMChatRequest):
    try:
        return await service.chat(payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/complete")
async def llm_complete(prompt: str, max_tokens: int = 256):
    try:
        return await service.complete(prompt, max_tokens)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
