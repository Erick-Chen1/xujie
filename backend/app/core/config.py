import os

class Settings:
    def __init__(self):
        # API Settings
        self.API_HOST = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT = int(os.getenv("API_PORT", "8000"))
        
        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        
        # CORS
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
        
        # AI Model Settings
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")
        self.MAX_SEQUENCE_LENGTH = int(os.getenv("MAX_SEQUENCE_LENGTH", "32"))
        
        # Memory Management
        self.MODEL_DEVICE = os.getenv("MODEL_DEVICE", "cpu")
        self.TORCH_THREADS = int(os.getenv("TORCH_THREADS", "1"))
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "4"))
        self.ENABLE_CUDA = os.getenv("ENABLE_CUDA", "false").lower() == "true"
        self.GC_COLLECT_INTERVAL = int(os.getenv("GC_COLLECT_INTERVAL", "10"))
        self.LAZY_LOAD_THRESHOLD = int(os.getenv("LAZY_LOAD_THRESHOLD", str(100 * 1024 * 1024)))

settings = Settings()
