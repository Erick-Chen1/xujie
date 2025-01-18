from pydantic import BaseModel
from typing import List, Optional
from core.knowledge_base import StudyMethod

class Material(BaseModel):
    id: str
    title: str
    description: str
    type: str
    content: str
    category: str
    difficulty_level: str
    estimated_time: str
    prerequisites: List[str]
    related_methods: List[str]
    learning_outcomes: List[str]

class MaterialResponse(Material):
    similarity_score: float
    stage_id: str
    related_methods: List[StudyMethod]
