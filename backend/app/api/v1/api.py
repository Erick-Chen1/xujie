"""API router with deferred endpoint loading."""
import gc
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    gc.collect()  # Force garbage collection
    return {"status": "healthy"}

# Defer endpoint imports to reduce memory usage
def load_endpoints():
    """Load endpoint modules on demand."""
    try:
        from app.api.v1.endpoints import study_methods, learning_paths
        
        # Include study methods endpoints
        router.include_router(
            study_methods.router,
            prefix="/study-methods",
            tags=["study-methods"]
        )
        
        # Include learning paths endpoints
        router.include_router(
            learning_paths.router,
            prefix="/learning-paths",
            tags=["learning-paths"]
        )
        
        # Force garbage collection after loading
        gc.collect()
    except Exception as e:
        print(f"Warning: Failed to load endpoints: {e}")
        gc.collect()  # Clean up on failure

# Load endpoints after router creation
load_endpoints()
