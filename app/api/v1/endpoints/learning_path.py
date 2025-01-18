from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
from schemas.learning_path import LearningPathCreate, LearningPath
from services.method_matcher import MethodMatcher
from core.knowledge_base import KnowledgeBase

router = APIRouter()

def get_knowledge_base():
    """Dependency to get KnowledgeBase instance"""
    kb = KnowledgeBase()
    kb.load_methods("data/study_methods/methods.json")
    return kb

def get_method_matcher(kb: KnowledgeBase = Depends(get_knowledge_base)):
    """Dependency to get MethodMatcher instance"""
    return MethodMatcher(kb)

@router.post("/learning-path", response_model=LearningPath)
async def create_learning_path(
    path: LearningPathCreate,
    matcher: MethodMatcher = Depends(get_method_matcher)
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
        # Match study methods to user profile
        matched_methods = await matcher.match_methods(path)
        
        # Create learning path with matched methods
        learning_path = LearningPath(
            id=str(uuid.uuid4()),
            subject=path.subject,
            difficulty_level=path.difficulty_level,
            learning_goals=path.learning_goals,
            available_time=path.available_time,
            learning_style=path.learning_style,
            created_at=datetime.utcnow(),
            tasks=matched_methods
        )
        
        return learning_path
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create learning path: {str(e)}"
        )
