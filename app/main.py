from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="AI Learning Path API",
    description="AI-powered learning path generator for Chinese high school mathematics",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Import and include API routers
from api.v1.endpoints import learning_path, materials

app.include_router(
    learning_path.router,
    prefix=os.getenv("API_V1_STR", "/api/v1"),
    tags=["learning-path"]
)

app.include_router(
    materials.router,
    prefix=os.getenv("API_V1_STR", "/api/v1"),
    tags=["materials"]
)
