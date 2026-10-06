from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "unrestricted-ai-backend"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "postgresql://aiuser:aipass@localhost:5432/aidb"
    DATABASE_ECHO: bool = False

    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str = "./storage"
    UPLOAD_MAX_SIZE: int = 5_000_000_000

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = ""
    AWS_REGION: str = "us-east-1"

    MINIO_URL: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "ai-outputs"

    USE_GPU: bool = True
    GPU_DEVICE: int = 0
    GPU_MEMORY_FRACTION: float = 0.95

    DIFFUSION_MODEL: str = "stabilityai/stable-diffusion-xl-base-1.0"
    REALVIS_MODEL: str = "SG161222/RealVisXL_V4.0"
    IMG2IMG_STRENGTH: float = 0.75
    INPAINT_PADDING: int = 32
    UPSCALE_FACTOR: int = 4

    VIDEO_MODEL: str = "animatediff"
    VIDEO_FPS: int = 24
    VIDEO_DURATION_MAX: int = 60
    MOCHI_MODEL: str = "genmo/mochi-1"
    GROK_API_KEY: str = ""

    FACE_SWAP_METHOD: str = "roop"
    DEEPFACE_LIVE_ENABLED: bool = True
    FACE_DETECTION_MODEL: str = "retinaface"
    FACE_RECOGNITION_MODEL: str = "insightface"
    BLEND_RATIO: float = 0.5

    NERF_BACKEND: str = "nerfstudio"
    NERF_RESOLUTION: int = 512
    NERF_TRAIN_STEPS: int = 10000

    LLM_PROVIDER: str = "local"
    LLM_MODEL: str = "llama3"
    LLM_MAX_TOKENS: int = 2048
    LLM_TEMPERATURE: float = 0.7
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    HF_TOKEN: str = ""
    HF_CACHE_DIR: str = "./models/huggingface"

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    JOB_TIMEOUT: int = 3600
    JOB_RETRY_COUNT: int = 3
    MAX_QUEUE_SIZE: int = 1000

    API_TITLE: str = "Unrestricted AI Platform"
    API_VERSION: str = "1.0.0"
    CORS_ORIGINS: str = "*"

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
