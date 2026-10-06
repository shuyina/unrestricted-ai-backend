from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    negative_prompt: str = ""
    width: int = 1024
    height: int = 1024
    steps: int = Field(30, ge=1, le=150)
    guidance_scale: float = Field(7.5, ge=0.0, le=20.0)
    seed: Optional[int] = None
    model: str = "sdxl"


class ImageToImageRequest(BaseModel):
    image_url: str
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    strength: float = Field(0.75, ge=0.0, le=1.0)
    steps: int = Field(30, ge=1, le=150)
    guidance_scale: float = Field(7.5, ge=0.0, le=20.0)
    seed: Optional[int] = None


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    negative_prompt: str = ""
    duration_seconds: int = Field(5, ge=1, le=60)
    fps: int = Field(24, ge=1, le=60)
    resolution: str = "1024x1024"
    model: str = "animatediff"


class FaceSwapRequest(BaseModel):
    source_image_url: str
    target_image_url: str
    method: str = "roop"
    blend_ratio: float = Field(0.5, ge=0.0, le=1.0)


class ChatMessage(BaseModel):
    role: str
    content: str


class LLMChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "llama3"
    max_tokens: int = Field(1024, ge=1, le=4096)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    system_prompt: Optional[str] = None


class NerfTrainRequest(BaseModel):
    image_urls: List[str]
    resolution: int = 512
    num_steps: int = 10000


class GenerationResponse(BaseModel):
    job_id: str
    status: str
    mode: str
    created_at: str
    estimated_time_seconds: int


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    output_url: Optional[str] = None
    error: Optional[str] = None
