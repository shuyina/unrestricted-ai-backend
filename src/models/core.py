import logging
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ImagePromptInput(BaseModel):
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    width: int = 1024
    height: int = 1024
    steps: int = 30
    guidance_scale: float = 7.5
    seed: int | None = None
    model: str = "sdxl"


class Img2ImgPromptInput(BaseModel):
    image_url: str
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    strength: float = 0.75
    steps: int = 30
    guidance_scale: float = 7.5
    seed: int | None = None
    model: str = "sdxl"


class VideoPromptInput(BaseModel):
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    duration_seconds: int = 5
    fps: int = 24
    resolution: str = "1024x1024"
    model: str = "animatediff"


class FaceSwapInput(BaseModel):
    source_image_url: str
    target_image_url: str
    method: str = "roop"
    blend_ratio: float = 0.5


class ChatMessage(BaseModel):
    role: str
    content: str


class LLMChatInput(BaseModel):
    messages: list[ChatMessage]
    model: str = "llama3"
    max_tokens: int = 1024
    temperature: float = 0.7
    system_prompt: str | None = None


class NerfTrainInput(BaseModel):
    image_urls: list[str]
    resolution: int = 512
    num_steps: int = 10000


class GenerationJob(BaseModel):
    job_id: str
    status: str
    mode: str
    created_at: str
    estimated_time_seconds: int


class GenerationJobStatus(BaseModel):
    job_id: str
    status: str
    progress: float = 0.0
    output_url: str | None = None
    error: str | None = None
