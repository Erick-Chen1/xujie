from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_HOST: str
    API_PORT: int
    
    # Database
    DATABASE_URL: str
    
    # CORS
    FRONTEND_URL: str
    
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
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
