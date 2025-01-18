"""Minimal configuration optimized for low memory usage."""
import os

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Database - Use in-memory SQLite for minimal footprint
DATABASE_URL = "sqlite:///:memory:"

# AI Model Settings - Use smallest available model
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # 50MB model
MAX_SEQUENCE_LENGTH = 16  # Minimal sequence length

# Memory Management - Ultra aggressive optimization
MODEL_DEVICE = "cpu"  # Force CPU only
TORCH_THREADS = 1  # Single thread
BATCH_SIZE = 1  # Process one at a time
ENABLE_CUDA = False  # No GPU
GC_COLLECT_INTERVAL = 1  # Continuous GC
LAZY_LOAD_THRESHOLD = 32 * 1024 * 1024  # 32MB threshold
MAX_WORKERS = 1  # Single worker
KEEP_ALIVE = 2  # Short keep-alive
BACKLOG = 8  # Minimal connection backlog
