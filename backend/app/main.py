"""Bare minimum FastAPI health check."""
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
    """Health check endpoint."""
    return Response(
        content='{"status":"healthy"}',
        media_type="application/json"
    )
