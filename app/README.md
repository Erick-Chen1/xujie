# AI Learning Path Generator Backend

FastAPI backend for AI-powered learning path generation for Chinese high school mathematics.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Activate virtual environment:
```bash
poetry shell
```

3. Run development server:
```bash
uvicorn main:app --reload
```

## Project Structure

- `main.py`: FastAPI application entry point
- `config.py`: Configuration and environment variables
- `api/`: API endpoints and routing
- `core/`: Core functionality and utilities
- `models/`: Database models
- `schemas/`: Pydantic models for request/response
- `services/`: Business logic and services
- `utils/`: Utility functions and helpers
