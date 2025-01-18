"""Ultra-minimal FastAPI app with bare essentials only."""
import gc
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Force garbage collection
gc.collect()

# Create minimal FastAPI application
app = FastAPI()

# Configure CORS with environment variables
origins = os.getenv("CORS_ORIGINS", "").split(",")
if not any(origins):
    raise ValueError("CORS_ORIGINS environment variable must be set")

# Configure middleware with environment variables
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=os.getenv("CORS_CREDENTIALS", "false").lower() == "true",
    allow_methods=os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE").split(","),
    allow_headers=os.getenv("CORS_HEADERS", "").split(",") or ["*"]
)

@app.get("/")
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    gc.collect()  # Force garbage collection
    return {"status": "healthy"}
