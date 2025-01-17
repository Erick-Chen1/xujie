from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import router as api_router

# Create minimal FastAPI application
app = FastAPI(
    title="AI Learning Path API",
    description="API for personalized learning path generation",
    version="1.0.0"
)

# CORS configuration - Do not remove this for full-stack development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Include API router
app.include_router(api_router, prefix="/api/v1")
