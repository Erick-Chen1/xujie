from fastapi import APIRouter
from app.api.v1.endpoints import study_methods, learning_paths

router = APIRouter()

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

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
