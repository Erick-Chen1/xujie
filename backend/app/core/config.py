from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,  # Don't require .env file
        case_sensitive=False,
        extra="allow",
        validate_default=True
    )

    # API Settings
    API_HOST: str | None = "0.0.0.0"
    API_PORT: int | None = 8000
    
    # Database
    DATABASE_URL: str | None = "sqlite:///:memory:"
    
    # CORS
    FRONTEND_URL: str | None = "*"  # Allow all origins by default
    
    # AI Model Settings
    EMBEDDING_MODEL: str | None = "paraphrase-MiniLM-L3-v2"
    MAX_SEQUENCE_LENGTH: int | None = 32
    
    # Memory Management
    MODEL_DEVICE: str | None = "cpu"
    TORCH_THREADS: int | None = 1
    BATCH_SIZE: int | None = 4
    ENABLE_CUDA: bool | None = False
    GC_COLLECT_INTERVAL: int | None = 10
    LAZY_LOAD_THRESHOLD: int | None = 100 * 1024 * 1024
    
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
