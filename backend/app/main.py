"""Minimal FastAPI application with lazy loading."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create minimal FastAPI application
app = FastAPI(
    title="AI Learning Path API",
    description="API for personalized learning path generation",
    version="1.0.0"
)

# CORS configuration
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
    return {"status": "healthy", "message": "API is running"}

# Load API router lazily
@app.on_event("startup")
async def startup_event():
    """Import heavy modules only after startup."""
    try:
        from app.api.v1.api import router as api_router
        app.include_router(api_router, prefix="/api/v1")
    except Exception as e:
        print(f"Warning: Failed to load API router: {e}")
        # Continue running with just health check endpoint
