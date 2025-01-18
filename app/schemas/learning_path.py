from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import re

class LearningPathCreate(BaseModel):
    subject: str = Field(..., description="学科名称")
    difficulty_level: str = Field(..., description="难度级别")
    learning_goals: str = Field(..., description="学习目标")
    available_time: str = Field(..., description="可用学习时间")
    learning_style: str = Field(..., description="学习风格")

    @validator('subject')
    def validate_subject(cls, v):
        valid_subjects = {"高中数学"}
        if v not in valid_subjects:
            raise ValueError(f"Subject must be one of: {valid_subjects}")
        return v

    @validator('difficulty_level')
    def validate_difficulty_level(cls, v):
        valid_levels = {"基础", "中等", "提高", "挑战"}
        if v not in valid_levels:
            raise ValueError(f"Difficulty level must be one of: {valid_levels}")
        return v

    @validator('available_time')
    def validate_available_time(cls, v):
        # Match patterns like "每天X小时" or "每周X小时"
        pattern = r'^每(天|周)\d+小时$'
        if not re.match(pattern, v):
            raise ValueError("Available time must be in format: 每天X小时 or 每周X小时")
        return v

    @validator('learning_goals')
    def validate_learning_goals(cls, v):
        if len(v) < 5 or len(v) > 100:
            raise ValueError("Learning goals must be between 5 and 100 characters")
        return v

    @validator('learning_style')
    def validate_learning_style(cls, v):
        valid_styles = {
            "实践与理论结合",
            "以练习为主",
            "以理论为主",
            "探究式学习",
            "传统讲解"
        }
        if v not in valid_styles:
            raise ValueError(f"Learning style must be one of: {valid_styles}")
        return v

class Task(BaseModel):
    id: str = Field(..., description="Task unique identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    completed: bool = Field(default=False, description="Task completion status")
    duration: str = Field(..., description="Expected duration")
    type: str = Field(..., description="Task type (daily, weekly, monthly)")
    stage_id: str = Field(..., description="Learning stage identifier")
    stage_name: str = Field(..., description="Learning stage name")
    due_date: Optional[str] = Field(None, description="Task due date")
    dependencies: List[str] = Field(default=[], description="Dependent task IDs")

    @validator('type')
    def validate_type(cls, v):
        valid_types = {"daily", "weekly", "monthly"}
        if v not in valid_types:
            raise ValueError(f"Task type must be one of: {valid_types}")
        return v

    @validator('stage_id')
    def validate_stage_id(cls, v):
        valid_stages = {
            "knowledge_acquisition",
            "practice_reinforcement",
            "pattern_identification",
            "special_learning"
        }
        if v not in valid_stages:
            raise ValueError(f"Stage ID must be one of: {valid_stages}")
        return v

class LearningPath(BaseModel):
    id: str = Field(..., description="Learning path unique identifier")
    subject: str = Field(..., description="Subject name")
    difficulty_level: str = Field(..., description="Difficulty level")
    learning_goals: str = Field(..., description="Learning objectives")
    available_time: str = Field(..., description="Available study time")
    learning_style: str = Field(..., description="Learning style preference")
    created_at: datetime = Field(..., description="Creation timestamp")
    tasks: List[Task] = Field(..., description="Learning tasks")
