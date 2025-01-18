from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudyMaterial(BaseModel):
    id: str
    title: str
    description: str
    type: str  # e.g., video, article, book, exercise
    subject: str
    topic: List[str]
    difficulty_level: str
    estimated_time: str
    url: Optional[str] = None
    content: Optional[str] = None
    prerequisites: List[str]
    related_methods: List[str]  # references to study methods
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None
