"""Two-service FastAPI application with health check separation."""
import gc
import os
import logging
import multiprocessing
import signal
import sys
from typing import Dict, Any

# Configure minimal logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_health_app():
    """Create minimal health check service."""
    from fastapi import FastAPI, Response
    
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        default_response_class=Response
    )
    
    @app.get("/")
    @app.get("/health")
    async def health_check():
        """Minimal health check."""
        return Response(
            content='{"status":"healthy"}',
            media_type="application/json"
        )
    
    return app

def create_api_app():
    """Create main API service (loaded on demand)."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title="AI Learning Path API",
        description="API for personalized learning path generation",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    try:
        from app.api.v1.api import router
        app.include_router(router, prefix="/api/v1")
    except Exception as e:
        logger.error(f"Failed to load API router: {e}")
    
    return app

def run_health_service():
    """Run minimal health check service."""
    import uvicorn
    app = create_health_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=80,
        workers=1,
        limit_concurrency=1,
        timeout_keep_alive=2,
        access_log=False,
        limit_max_requests=100
    )

def run_api_service():
    """Run main API service."""
    import uvicorn
    app = create_api_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        workers=1,
        limit_concurrency=1,
        access_log=False
    )

if __name__ == "__main__":
    # Start health check service in main process
    health_process = multiprocessing.Process(target=run_health_service)
    health_process.start()
    
    # Start API service in separate process
    api_process = multiprocessing.Process(target=run_api_service)
    api_process.start()
    
    def cleanup(signum, frame):
        """Clean up processes on shutdown."""
        health_process.terminate()
        api_process.terminate()
        sys.exit(0)
    
    # Handle termination signals
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)
    
    # Wait for processes
    health_process.join()
    api_process.join()
