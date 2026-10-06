import logging

from src.api.schemas import LLMChatRequest
from src.services.orchestrator import GenerationOrchestrator
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


class LLMService:
    async def chat(self, payload: LLMChatRequest):
        messages = [{"role": m.role, "content": m.content} for m in payload.messages]
        result = await orchestrator.llm_chat(str(payload.model), payload)
        return result

    async def complete(self, prompt: str, max_tokens: int = 256):
        messages = [
            {"role": "user", "content": prompt}
        ]
        return {
            "prompt": prompt,
            "completion": "Placeholder completion from LLM service",
            "tokens": max_tokens,
        }
