"""Ultra-minimal FastAPI application with aggressive memory optimization."""
import gc
import os
import logging
from typing import Dict, Any

# Configure minimal logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_memory() -> Dict[str, Any]:
    """Get current memory usage."""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory = process.memory_info()
        stats = {
            "rss": f"{memory.rss / 1024 / 1024:.1f}MB",
            "vms": f"{memory.vms / 1024 / 1024:.1f}MB"
        }
        logger.info(f"Memory Usage - RSS: {stats['rss']}, VMS: {stats['vms']}")
        return stats
    except ImportError:
        return {"error": "psutil not available"}

def create_minimal_app():
    """Create bare minimum FastAPI app."""
    # Force garbage collection
    gc.collect()
    
    # Import only what's needed for basic functionality
    from fastapi import FastAPI, Response
    from fastapi.middleware.cors import CORSMiddleware
    
    # Create minimal app without docs
    app = FastAPI(
        title="AI Learning Path API",
        description="API for personalized learning path generation",
        version="1.0.0",
        docs_url=None,  # Disable docs
        redoc_url=None,  # Disable redoc
        openapi_url=None  # Disable OpenAPI schema
    )
    
    # Minimal CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    @app.get("/health")
    async def health_check():
        """Minimal health check."""
        gc.collect()
        return Response(
            content='{"status":"healthy"}',
            media_type="application/json"
        )
    
    @app.on_event("startup")
    async def startup_event():
        """Lazy load API router."""
        try:
            # Import router only when needed
            from app.api.v1.api import router
            app.include_router(router, prefix="/api/v1")
        except Exception as e:
            logger.error(f"Router load failed: {e}")
        finally:
            gc.collect()
    
    return app

# Create minimal app instance
app = create_minimal_app()
