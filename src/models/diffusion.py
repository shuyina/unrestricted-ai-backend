import logging
import torch
from typing import Optional
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, StableDiffusionXLInpaintPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image
from src.core.config import settings
from src.core.exceptions import ModelError

logger = logging.getLogger(__name__)


class DiffusionModelManager:
    def __init__(self):
        self.device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if settings.USE_GPU else torch.float32
        self.text2img_pipeline = None
        self.img2img_pipeline = None
        self.inpaint_pipeline = None
        self.loaded_model = None

    def load_text2img_pipeline(self, model_id: str = None):
        try:
            model_id = model_id or settings.DIFFUSION_MODEL
            if self.text2img_pipeline and self.loaded_model == model_id:
                return self.text2img_pipeline

            logger.info(f"Loading text-to-image pipeline: {model_id}")
            self.text2img_pipeline = StableDiffusionXLPipeline.from_pretrained(
                model_id,
                torch_dtype=self.dtype,
                use_safetensors=True,
                variant="fp16" if self.dtype == torch.float16 else None,
            )
            self.text2img_pipeline = self.text2img_pipeline.to(self.device)
            self.text2img_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.text2img_pipeline.scheduler.config
            )
            self.loaded_model = model_id
            logger.info(f"Text-to-image pipeline loaded on {self.device}")
            return self.text2img_pipeline
        except Exception as e:
            raise ModelError(model_id, str(e))

    def load_img2img_pipeline(self, model_id: str = None):
        try:
            model_id = model_id or settings.DIFFUSION_MODEL
            if self.img2img_pipeline and self.loaded_model == model_id:
                return self.img2img_pipeline

            logger.info(f"Loading img2img pipeline: {model_id}")
            self.img2img_pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                model_id,
                torch_dtype=self.dtype,
                use_safetensors=True,
                variant="fp16" if self.dtype == torch.float16 else None,
            )
            self.img2img_pipeline = self.img2img_pipeline.to(self.device)
            self.img2img_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.img2img_pipeline.scheduler.config
            )
            self.loaded_model = model_id
            logger.info(f"Img2img pipeline loaded on {self.device}")
            return self.img2img_pipeline
        except Exception as e:
            raise ModelError(model_id, str(e))

    def load_inpaint_pipeline(self, model_id: str = None):
        try:
            model_id = model_id or settings.DIFFUSION_MODEL
            if self.inpaint_pipeline and self.loaded_model == model_id:
                return self.inpaint_pipeline

            logger.info(f"Loading inpaint pipeline: {model_id}")
            self.inpaint_pipeline = StableDiffusionXLInpaintPipeline.from_pretrained(
                model_id,
                torch_dtype=self.dtype,
                use_safetensors=True,
                variant="fp16" if self.dtype == torch.float16 else None,
            )
            self.inpaint_pipeline = self.inpaint_pipeline.to(self.device)
            self.inpaint_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.inpaint_pipeline.scheduler.config
            )
            self.loaded_model = model_id
            logger.info(f"Inpaint pipeline loaded on {self.device}")
            return self.inpaint_pipeline
        except Exception as e:
            raise ModelError(model_id, str(e))

    async def generate_text2img(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        model_id: str = None,
    ) -> Image.Image:
        try:
            pipeline = self.load_text2img_pipeline(model_id)
            generator = torch.Generator(self.device).manual_seed(seed) if seed else None

            image = pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator,
            ).images[0]

            logger.info(f"Generated image: {width}x{height}")
            return image
        except Exception as e:
            logger.error(f"Text-to-image generation failed: {e}")
            raise ModelError("text2img", str(e))

    async def generate_img2img(
        self,
        image: Image.Image,
        prompt: str,
        negative_prompt: str = "",
        strength: float = 0.75,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        model_id: str = None,
    ) -> Image.Image:
        try:
            pipeline = self.load_img2img_pipeline(model_id)
            generator = torch.Generator(self.device).manual_seed(seed) if seed else None

            output_image = pipeline(
                prompt=prompt,
                image=image,
                negative_prompt=negative_prompt,
                strength=strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator,
            ).images[0]

            logger.info(f"Generated img2img with strength {strength}")
            return output_image
        except Exception as e:
            logger.error(f"Img2img generation failed: {e}")
            raise ModelError("img2img", str(e))

    async def generate_inpaint(
        self,
        image: Image.Image,
        mask_image: Image.Image,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        model_id: str = None,
    ) -> Image.Image:
        try:
            pipeline = self.load_inpaint_pipeline(model_id)
            generator = torch.Generator(self.device).manual_seed(seed) if seed else None

            output_image = pipeline(
                prompt=prompt,
                image=image,
                mask_image=mask_image,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator,
            ).images[0]

            logger.info(f"Generated inpaint mask")
            return output_image
        except Exception as e:
            logger.error(f"Inpaint generation failed: {e}")
            raise ModelError("inpaint", str(e))

    def unload_models(self):
        if self.text2img_pipeline:
            del self.text2img_pipeline
        if self.img2img_pipeline:
            del self.img2img_pipeline
        if self.inpaint_pipeline:
            del self.inpaint_pipeline
        torch.cuda.empty_cache()
        logger.info("Models unloaded")
