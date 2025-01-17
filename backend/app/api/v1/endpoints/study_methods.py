"""
API endpoints for personalized study methods generation.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.personalized_method_generator import PersonalizedMethodGenerator

router = APIRouter()

class UserProfile(BaseModel):
    """User profile for personalized study method generation."""
    learning_goals: str
    learning_style: str
    available_time: str
    preferences: str = ""
    difficulty_level: str
    subjects: str

class StudyMethodResponse(BaseModel):
    """Response model for personalized study methods."""
    title: str
    description: str
    time_commitment: str
    similarity_score: float
    recommendations: List[str]

class PersonalizedMethodsResponse(BaseModel):
    """Response containing multiple personalized study methods."""
    methods: List[StudyMethodResponse]
    message: str = "Successfully generated personalized study methods."

@router.post("/generate", response_model=PersonalizedMethodsResponse)
async def generate_personalized_methods(profile: UserProfile):
    """
    Generate personalized study methods based on user profile.
    
    Args:
        profile: User profile containing learning preferences and goals
        
    Returns:
        List of personalized study methods with recommendations
    """
    try:
        # Initialize method generator with lazy loading
        generator = PersonalizedMethodGenerator()
        
        # Generate personalized methods in smaller batches
        methods = []
        try:
            methods = generator.generate_personalized_methods(profile.dict(), num_methods=2)
        except Exception as e:
            print(f"Error generating methods: {str(e)}")
            # Fallback to generating just one method if memory is constrained
            methods = generator.generate_personalized_methods(profile.dict(), num_methods=1)
        finally:
            # Force cleanup
            import gc
            gc.collect()
        
        # Convert to response format
        response_methods = []
        for method in methods:
            response_methods.append(StudyMethodResponse(
                title=method["title"],
                description=method["description"],
                time_commitment=method["time_commitment"],
                similarity_score=method["similarity_score"],
                recommendations=method["recommendations"]
            ))
        
        return PersonalizedMethodsResponse(methods=response_methods)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating personalized methods: {str(e)}"
        )

@router.get("/example-profile")
async def get_example_profile():
    """Get an example user profile for testing."""
    return {
        "learning_goals": "提高数学理解能力和解题速度",
        "learning_style": "视觉学习",
        "available_time": "工作日每天2小时",
        "preferences": "喜欢通过实例学习",
        "difficulty_level": "中等",
        "subjects": "数学"
    }
