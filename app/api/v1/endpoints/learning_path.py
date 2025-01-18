from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
from schemas.learning_path import LearningPathCreate, LearningPath
from services.path_generator import PathGenerator
from core.knowledge_base import KnowledgeBase
from core.materials_base import MaterialsBase

router = APIRouter()

def get_knowledge_base():
    """Dependency to get KnowledgeBase instance"""
    kb = KnowledgeBase()
    kb.load_methods("data/study_methods/methods.json")
    return kb

def get_materials_base():
    """Dependency to get MaterialsBase instance"""
    mb = MaterialsBase()
    mb.load_materials("data/study_materials/materials.json")
    return mb

def get_path_generator(
    kb: KnowledgeBase = Depends(get_knowledge_base),
    mb: MaterialsBase = Depends(get_materials_base)
):
    """Dependency to get PathGenerator instance"""
    return PathGenerator(kb, mb)

@router.post("/learning-path", response_model=LearningPath)
async def create_learning_path(
    path: LearningPathCreate,
    generator: PathGenerator = Depends(get_path_generator)
):
    """
    Create a new learning path based on user preferences and goals
    
    Request format:
    {
        "subject": "高中数学",
        "difficulty_level": "中等",
        "learning_goals": "提高数学解题能力",
        "available_time": "每天2小时",
        "learning_style": "实践与理论结合"
    }
    """
    try:
        # Generate learning path with stages and materials
        learning_stages = await generator.generate_path(path)
        
        # Create learning path response
        learning_path = LearningPath(
            id=str(uuid.uuid4()),
            subject=path.subject,
            difficulty_level=path.difficulty_level,
            learning_goals=path.learning_goals,
            available_time=path.available_time,
            learning_style=path.learning_style,
            created_at=datetime.utcnow(),
            tasks=learning_stages
        )
        
        return learning_path
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create learning path: {str(e)}"
        )
