from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
import uuid
from schemas.learning_path import LearningPathCreate, LearningPath, Task
from services.path_generator import PathGenerator
from services.task_generator import TaskGenerator
from core.knowledge_base import KnowledgeBase
from core.materials_base import MaterialsBase
from core.kimi import KimiAPIError, KimiAuthenticationError, KimiRateLimitError

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

def get_task_generator():
    """Dependency to get TaskGenerator instance"""
    return TaskGenerator()

@router.post(
    "/learning-path",
    response_model=LearningPath,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Learning path created successfully"},
        400: {"description": "Invalid request parameters"},
        401: {"description": "Authentication failed"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"}
    }
)
async def create_learning_path(
    path: LearningPathCreate,
    generator: PathGenerator = Depends(get_path_generator),
    task_generator: TaskGenerator = Depends(get_task_generator)
):
    """
    Create a new learning path based on user preferences and goals
    
    Parameters:
    - subject: 学科名称 (e.g., 高中数学)
    - difficulty_level: 难度级别 (基础, 中等, 提高, 挑战)
    - learning_goals: 学习目标
    - available_time: 可用学习时间 (每天X小时 or 每周X小时)
    - learning_style: 学习风格 (实践与理论结合, 以练习为主, etc.)
    
    Returns:
    - LearningPath object with generated tasks and schedule
    
    Raises:
    - 400: Invalid request parameters
    - 401: Authentication failed
    - 429: Rate limit exceeded
    - 500: Internal server error
    """
    try:
        # Generate learning path with stages and materials
        learning_stages = await generator.generate_path(path)
        
        # Generate tasks for each stage
        tasks = await task_generator.generate_tasks(path, learning_stages)
        
        # Create learning path response
        learning_path = LearningPath(
            id=str(uuid.uuid4()),
            subject=path.subject,
            difficulty_level=path.difficulty_level,
            learning_goals=path.learning_goals,
            available_time=path.available_time,
            learning_style=path.learning_style,
            created_at=datetime.utcnow(),
            tasks=[Task(**task) for task in tasks]
        )
        
        return learning_path
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except KimiAuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except KimiRateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"message": str(e), "retry_after": e.retry_after}
        )
    except KimiAPIError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create learning path: {str(e)}"
        )
