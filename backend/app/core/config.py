from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,  # Don't require .env file
        case_sensitive=False,
        extra="allow"
    )

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///:memory:"
    
    # CORS
    FRONTEND_URL: str = "https://ai-learning-planner-app-xjgsc107.devinapps.com"
    
    # AI Model Settings
    EMBEDDING_MODEL: str = "paraphrase-MiniLM-L3-v2"  # Smallest available model
    MAX_SEQUENCE_LENGTH: int = 32  # Minimal sequence length
    
    # Memory Management
    MODEL_DEVICE: str = "cpu"
    TORCH_THREADS: int = 1
    BATCH_SIZE: int = 4  # Minimal batch size
    ENABLE_CUDA: bool = False  # Force CPU-only mode
    GC_COLLECT_INTERVAL: int = 10  # Very frequent garbage collection
    LAZY_LOAD_THRESHOLD: int = 100 * 1024 * 1024  # 100MB threshold for lazy loading
    
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
