"""
API endpoints for learning path generation and material integration.
"""
from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.personalized_method_generator import PersonalizedMethodGenerator
from app.core.learning_path_generator import LearningPathGenerator
from app.api.v1.endpoints.study_methods import UserProfile, LearningStageActivity

router = APIRouter()

class LearningStage(BaseModel):
    """Stage in a learning path."""
    id: str
    title: str
    description: str
    duration: str
    methods: List[str]
    activities: List[LearningStageActivity]

class LearningPath(BaseModel):
    """Complete learning path."""
    id: str
    title: str
    description: str
    created_at: str
    updated_at: str
    subject: str
    difficulty_level: str
    estimated_duration: str
    stages: List[LearningStage]
    prerequisites: List[str]
    learning_goals: str
    study_methods: List[str]
    metadata: dict

class StageMaterial(BaseModel):
    """Study material with stage-specific context."""
    id: str
    title: str
    description: str
    type: str
    subject: str
    difficulty_level: str
    estimated_time: str
    stage_id: str
    stage_duration: str
    recommended_activity: str
    learning_activities: List[LearningStageActivity]

class LearningPathResponse(BaseModel):
    """Response containing learning path with stage materials."""
    path: LearningPath
    materials: Dict[str, List[StageMaterial]]
    message: str = "Successfully generated learning path with materials."

@router.post("/generate", response_model=LearningPathResponse)
async def generate_learning_path(profile: UserProfile):
    """
    Generate a complete learning path with recommended materials.
    
    Args:
        profile: User profile containing learning preferences and goals
        
    Returns:
        Learning path with stage-specific materials
    """
    try:
        # Generate personalized methods with minimal memory usage
        method_generator = PersonalizedMethodGenerator()
        methods = []
        try:
            methods = method_generator.generate_personalized_methods(profile.dict(), num_methods=2)
        except Exception as e:
            print(f"Error generating methods: {str(e)}")
            methods = method_generator.generate_personalized_methods(profile.dict(), num_methods=1)
        finally:
            import gc
            gc.collect()
        
        # Generate learning path with materials using lazy loading
        path_generator = LearningPathGenerator()
        path = path_generator.generate_path(methods, profile.dict())
        
        # Get materials in smaller batches with cleanup
        try:
            materials = path_generator.get_stage_materials(path)
        finally:
            gc.collect()
        
        return LearningPathResponse(
            path=path,
            materials=materials
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating learning path: {str(e)}"
        )

@router.get("/example")
async def get_example_path():
    """Get an example learning path for testing."""
    profile = UserProfile(
        learning_goals="提高数学理解能力和解题速度",
        learning_style="视觉学习",
        available_time="工作日每天2小时",
        preferences="喜欢通过实例学习",
        difficulty_level="中等",
        subjects="数学"
    )
    return await generate_learning_path(profile)
