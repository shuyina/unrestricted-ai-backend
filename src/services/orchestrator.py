import logging
import httpx
from datetime import datetime
from uuid import uuid4
from pathlib import Path

from src.core.config import settings
from src.models.diffusion import DiffusionModelManager
from src.models.video import VideoGenerator
from src.models.face_detection import FaceDetector
from src.models.providers import LLMProvider
from src.utils.file_io import ensure_dir, save_bytes
from src.api.schemas import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    FaceSwapRequest,
    LLMChatRequest,
    NerfTrainRequest,
)

logger = logging.getLogger(__name__)


class GenerationOrchestrator:
    def __init__(self):
        self.diffusion_manager = DiffusionModelManager()
        self.video_generator = VideoGenerator()
        self.face_detector = FaceDetector()
        self.llm_provider = LLMProvider(
            provider=settings.LLM_PROVIDER,
            model=settings.LLM_MODEL,
        )
        ensure_dir(settings.STORAGE_LOCAL_PATH)

    async def generate_image(
        self,
        job_id: str,
        payload: ImageGenerationRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: Generating image - {payload.prompt}")

            image = await self.diffusion_manager.generate_text2img(
                prompt=payload.prompt,
                negative_prompt=payload.negative_prompt,
                width=payload.width,
                height=payload.height,
                num_inference_steps=payload.steps,
                guidance_scale=payload.guidance_scale,
                seed=payload.seed,
                model_id=self._get_model_id(payload.model),
            )

            output_path = self._save_image(job_id, image, "image")

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "text_to_image",
                "output_url": f"/outputs/{Path(output_path).name}",
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: Image generation failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def generate_img2img(
        self,
        job_id: str,
        payload: ImageGenerationRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: Generating img2img")

            # Download source image
            source_image = await self._download_image(payload.prompt)

            result_image = await self.diffusion_manager.generate_img2img(
                image=source_image,
                prompt=payload.prompt,
                negative_prompt=payload.negative_prompt,
                strength=settings.IMG2IMG_STRENGTH,
                num_inference_steps=payload.steps,
                guidance_scale=payload.guidance_scale,
                seed=payload.seed,
                model_id=self._get_model_id(payload.model),
            )

            output_path = self._save_image(job_id, result_image, "img2img")

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "image_to_image",
                "output_url": f"/outputs/{Path(output_path).name}",
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: Img2img generation failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def generate_inpaint(
        self,
        job_id: str,
        payload: ImageGenerationRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: Generating inpaint")

            source_image = await self._download_image(payload.prompt)
            # Create dummy mask for demo
            mask_image = source_image.convert("L")

            result_image = await self.diffusion_manager.generate_inpaint(
                image=source_image,
                mask_image=mask_image,
                prompt=payload.prompt,
                negative_prompt=payload.negative_prompt,
                num_inference_steps=payload.steps,
                guidance_scale=payload.guidance_scale,
                seed=payload.seed,
                model_id=self._get_model_id(payload.model),
            )

            output_path = self._save_image(job_id, result_image, "inpaint")

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "inpaint",
                "output_url": f"/outputs/{Path(output_path).name}",
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: Inpaint generation failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def generate_video(
        self,
        job_id: str,
        payload: VideoGenerationRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: Generating video - {payload.prompt}")

            frames = await self.video_generator.generate_text_to_video(
                prompt=payload.prompt,
                negative_prompt=payload.negative_prompt,
                num_frames=int(payload.duration_seconds * payload.fps),
                height=int(payload.resolution.split("x")[1]),
                width=int(payload.resolution.split("x")[0]),
            )

            output_path = self._save_video(job_id, frames, payload.fps, "video")

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "text_to_video",
                "output_url": f"/outputs/{Path(output_path).name}",
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: Video generation failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def faceswap(
        self,
        job_id: str,
        payload: FaceSwapRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: Face swap {payload.method}")

            source_image = await self._download_image(payload.source_image_url)
            target_image = await self._download_image(payload.target_image_url)

            # Detect faces
            source_faces = self.face_detector.detect_faces(source_image)
            target_faces = self.face_detector.detect_faces(target_image)

            if not source_faces or not target_faces:
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "error": "No faces detected in source or target image",
                    "created_at": datetime.utcnow().isoformat(),
                }

            # Placeholder for actual face swap (Roop/DeepFaceLive)
            output_path = self._save_image(job_id, target_image, "faceswap")

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "face_swap",
                "method": payload.method,
                "output_url": f"/outputs/{Path(output_path).name}",
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: Face swap failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def llm_chat(
        self,
        job_id: str,
        payload: LLMChatRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: LLM chat with {payload.model}")

            messages = [{"role": m.role, "content": m.content} for m in payload.messages]

            response = await self.llm_provider.chat(
                messages=messages,
                max_tokens=payload.max_tokens,
                temperature=payload.temperature,
                system_prompt=payload.system_prompt,
            )

            return {
                "job_id": job_id,
                "status": "completed",
                "mode": "llm_chat",
                "model": payload.model,
                "response": response,
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: LLM chat failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    async def train_nerf(
        self,
        job_id: str,
        payload: NerfTrainRequest,
    ) -> dict:
        try:
            logger.info(f"Job {job_id}: NeRF training with {len(payload.image_urls)} images")
            # Placeholder for NeRF training
            return {
                "job_id": job_id,
                "status": "queued",
                "mode": "nerf_train",
                "images_count": len(payload.image_urls),
                "estimated_duration_seconds": 600,
                "created_at": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Job {job_id}: NeRF training failed - {e}")
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(e),
                "created_at": datetime.utcnow().isoformat(),
            }

    def _get_model_id(self, model_name: str) -> str:
        models = {
            "sdxl": settings.DIFFUSION_MODEL,
            "realvis": settings.REALVIS_MODEL,
        }
        return models.get(model_name, settings.DIFFUSION_MODEL)

    def _save_image(self, job_id: str, image, suffix: str) -> str:
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "images"
        ensure_dir(str(output_dir))
        output_path = output_dir / f"{job_id}_{suffix}.png"
        image.save(str(output_path))
        logger.info(f"Image saved: {output_path}")
        return str(output_path)

    def _save_video(self, job_id: str, frames, fps: int, suffix: str) -> str:
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "videos"
        ensure_dir(str(output_dir))
        output_path = output_dir / f"{job_id}_{suffix}.mp4"
        self.video_generator.frames_to_video(frames, str(output_path), fps)
        logger.info(f"Video saved: {output_path}")
        return str(output_path)

    async def _download_image(self, url: str):
        from PIL import Image
        import io

        try:
            if url.startswith(("http://", "https://")):
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=30.0)
                    response.raise_for_status()
                    image = Image.open(io.BytesIO(response.content))
            else:
                image = Image.open(url)
            return image
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            # Return placeholder image
            return Image.new("RGB", (512, 512), color=(0, 0, 0))
