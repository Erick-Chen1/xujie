from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import router as api_router

# Create minimal FastAPI application
app = FastAPI(
    title="AI Learning Path API",
    description="API for personalized learning path generation",
    version="1.0.0"
)

# CORS configuration - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

# Include API router
app.include_router(api_router, prefix="/api/v1")
