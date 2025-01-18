from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudyMethod(BaseModel):
    id: str
    title: str
    description: str
    source: str
    tags: List[str]
    effectiveness_rating: float
    difficulty_level: str
    time_commitment: str
    prerequisites: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None
