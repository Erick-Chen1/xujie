from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LearningPathCreate(BaseModel):
    subject: str
    difficulty_level: str
    learning_goals: str
    available_time: str
    learning_style: str

class LearningPath(BaseModel):
    id: str
    subject: str
    difficulty_level: str
    learning_goals: str
    available_time: str
    learning_style: str
    created_at: datetime
    tasks: List[dict]  # Will be replaced with proper Task model later
