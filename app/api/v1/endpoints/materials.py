from fastapi import APIRouter, HTTPException
from typing import List
from schemas.materials import Material

router = APIRouter()

@router.get("/materials/{stage_id}", response_model=List[Material])
async def get_materials(stage_id: str):
    """
    Retrieve learning materials for a specific learning stage
    """
    pass  # Implementation will be added later
