import logging
import asyncio

from src.workers.celery_app import celery_app
from src.services.orchestrator import GenerationOrchestrator
from src.api.schemas import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    FaceSwapRequest,
    LLMChatRequest,
    NerfTrainRequest,
    ChatMessage,
)

logger = logging.getLogger(__name__)
orchestrator = GenerationOrchestrator()


@celery_app.task(bind=True, name="tasks.generate_image")
def generate_image_task(
    self,
    job_id: str,
    model: str,
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    steps: int,
    guidance_scale: float,
    seed: int,
):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Generating image")

        payload = ImageGenerationRequest(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            guidance_scale=guidance_scale,
            seed=seed,
            model=model,
        )

        result = asyncio.run(orchestrator.generate_image(job_id, payload))
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return result
    except Exception as e:
        logger.error(f"Task {job_id}: Image generation failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.generate_img2img")
def generate_img2img_task(self, job_id: str):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Generating img2img")
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return {"status": "completed", "job_id": job_id}
    except Exception as e:
        logger.error(f"Task {job_id}: Img2img failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.generate_inpaint")
def generate_inpaint_task(self, job_id: str):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Generating inpaint")
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return {"status": "completed", "job_id": job_id}
    except Exception as e:
        logger.error(f"Task {job_id}: Inpaint failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.generate_video")
def generate_video_task(
    self,
    job_id: str,
    prompt: str,
    negative_prompt: str,
    duration_seconds: int,
    fps: int,
):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Generating video")

        payload = VideoGenerationRequest(
            prompt=prompt,
            negative_prompt=negative_prompt,
            duration_seconds=duration_seconds,
            fps=fps,
        )

        result = asyncio.run(orchestrator.generate_video(job_id, payload))
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return result
    except Exception as e:
        logger.error(f"Task {job_id}: Video generation failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.generate_image_to_video")
def generate_image_to_video_task(self, job_id: str):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Generating image-to-video")
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return {"status": "completed", "job_id": job_id}
    except Exception as e:
        logger.error(f"Task {job_id}: Image-to-video failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.faceswap")
def faceswap_task(
    self,
    job_id: str,
    source_image_url: str,
    target_image_url: str,
    method: str,
    blend_ratio: float,
):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: Face swap")

        payload = FaceSwapRequest(
            source_image_url=source_image_url,
            target_image_url=target_image_url,
            method=method,
            blend_ratio=blend_ratio,
        )

        result = asyncio.run(orchestrator.faceswap(job_id, payload))
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return result
    except Exception as e:
        logger.error(f"Task {job_id}: Face swap failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task(bind=True, name="tasks.nerf_train")
def nerf_train_task(
    self,
    job_id: str,
    image_urls: list,
    resolution: int,
    num_steps: int,
):
    try:
        self.update_state(state="PROGRESS", meta={"progress": 10})
        logger.info(f"Task {job_id}: NeRF training")

        payload = NerfTrainRequest(
            image_urls=image_urls,
            resolution=resolution,
            num_steps=num_steps,
        )

        result = asyncio.run(orchestrator.train_nerf(job_id, payload))
        self.update_state(state="PROGRESS", meta={"progress": 100})
        return result
    except Exception as e:
        logger.error(f"Task {job_id}: NeRF training failed - {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
