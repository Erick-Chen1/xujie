"""Minimal FastAPI application with aggressive memory optimization."""
import gc
import os
import psutil

def create_app():
    """Create FastAPI app with minimal imports."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    # Force garbage collection before creating app
    gc.collect()
    
    app = FastAPI(
        title="AI Learning Path API",
        description="API for personalized learning path generation",
        version="1.0.0"
    )
    
    # CORS configuration - minimal middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        # Force garbage collection
        gc.collect()
        
        # Get memory usage
        process = psutil.Process(os.getpid())
        memory = process.memory_info()
        
        return {
            "status": "healthy",
            "message": "API is running",
            "memory": {
                "rss": f"{memory.rss / 1024 / 1024:.1f}MB",
                "vms": f"{memory.vms / 1024 / 1024:.1f}MB"
            }
        }
    
    @app.on_event("startup")
    async def startup_event():
        """Import heavy modules only after startup."""
        try:
            # Force garbage collection before imports
            gc.collect()
            
            # Import router lazily
            from app.api.v1.api import router as api_router
            app.include_router(api_router, prefix="/api/v1")
            
            # Clean up after router initialization
            gc.collect()
        except Exception as e:
            print(f"Warning: Failed to load API router: {e}")
            gc.collect()
    
    return app

# Create app instance with minimal memory usage
app = create_app()
