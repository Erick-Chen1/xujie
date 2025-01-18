"""Simple configuration using environment variables."""
import os

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# AI Model Settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")
MAX_SEQUENCE_LENGTH = int(os.getenv("MAX_SEQUENCE_LENGTH", "32"))

# Memory Management
MODEL_DEVICE = os.getenv("MODEL_DEVICE", "cpu")
TORCH_THREADS = int(os.getenv("TORCH_THREADS", "1"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "4"))
ENABLE_CUDA = os.getenv("ENABLE_CUDA", "false").lower() == "true"
GC_COLLECT_INTERVAL = int(os.getenv("GC_COLLECT_INTERVAL", "10"))
LAZY_LOAD_THRESHOLD = int(os.getenv("LAZY_LOAD_THRESHOLD", str(100 * 1024 * 1024)))
