# Unrestricted AI Backend Platform

Production-grade backend scaffold for:
- Image generation: SDXL, RealVisXL, img2img, inpainting, upscaling
- Face swap: Roop, DeepFaceLive-style pipelines
- Video generation: AnimateDiff and image-to-video
- LLM integration: GPT-style, LLaMA, Mistral compatible providers
- Ultra-realistic rendering: diffusion + NeRF-ready architecture

## Features
- FastAPI API
- Celery/Redis task support
- Pydantic validation
- Docker-ready deployment
- Health checks and job status endpoints
- Local storage helpers for generated media

## Quick start

1. Create env file:

```bash
cp .env.example .env
```

2. Install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run app:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

4. API docs:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Docker

```bash
docker compose up --build
```

## Included API routes

- `GET /health`
- `POST /api/v1/generate/image`
- `POST /api/v1/generate/image/img2img`
- `POST /api/v1/generate/image/inpaint`
- `POST /api/v1/generate/video`
- `POST /api/v1/generate/video/image-to-video`
- `POST /api/v1/faceswap`
- `POST /api/v1/llm/chat`
- `POST /api/v1/nerf/train`

## Notes

This repository is a functional starter scaffold. It runs as a backend and exposes endpoints. The service layer is designed so you can plug in actual SDXL, RealVisXL, AnimateDiff, roop, or LLM backends next.
