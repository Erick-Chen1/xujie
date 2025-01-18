from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
from core.kimi import KimiAPI
from schemas.learning_path import LearningPathCreate

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        duration: str,
        type: str,
        stage_id: str,
        stage_name: str,
        due_date: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.completed = False
        self.duration = duration
        self.type = type
        self.stage_id = stage_id
        self.stage_name = stage_name
        self.due_date = due_date
        self.dependencies = dependencies or []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "duration": self.duration,
            "type": self.type,
            "stageId": self.stage_id,
            "stageName": self.stage_name,
            "dueDate": self.due_date,
            "dependencies": self.dependencies
        }

class TaskGenerator:
    def __init__(self):
        """Initialize task generator with Kimi API"""
        self.kimi_api = KimiAPI()
        
        # Define learning stages and their characteristics
        self.stages = [
            {
                "id": "knowledge_acquisition",
                "name": "知识获取",
                "categories": ["基本概念", "性质与关系", "基本运算", "应用"],
                "task_types": ["阅读", "笔记", "练习"],
                "duration_range": {"min": "30分钟", "max": "60分钟"}
            },
            {
                "id": "practice_reinforcement",
                "name": "练习强化",
                "categories": ["基本运算", "应用"],
                "task_types": ["练习", "复习", "测试"],
                "duration_range": {"min": "45分钟", "max": "90分钟"}
            },
            {
                "id": "pattern_identification",
                "name": "规律识别",
                "categories": ["性质与关系", "应用"],
                "task_types": ["分析", "总结", "模拟"],
                "duration_range": {"min": "45分钟", "max": "90分钟"}
            },
            {
                "id": "special_learning",
                "name": "特色学习",
                "categories": ["阅读与思考", "信息技术应用", "探究与发现", "数学建模"],
                "task_types": ["探究", "实践", "项目"],
                "duration_range": {"min": "60分钟", "max": "120分钟"}
            }
        ]

    async def generate_tasks(
        self,
        learning_path: LearningPathCreate,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate tasks based on learning path and materials"""
        all_tasks = []
        current_date = datetime.now()
        
        # Get AI suggestions for task breakdown
        task_suggestions = await self.kimi_api.generate_method_match({
            **learning_path.dict(),
            "stages": self.stages,
            "materials": materials
        })
        
        # Process each stage
        for stage in self.stages:
            stage_materials = [m for m in materials if m["stage_id"] == stage["id"]]
            
            # Generate monthly tasks
            monthly_task = Task(
                title=f"{stage['name']}阶段月度计划",
                description=f"完成{stage['name']}阶段的学习目标",
                duration="1个月",
                type="monthly",
                stage_id=stage["id"],
                stage_name=stage["name"],
                due_date=(current_date + timedelta(days=30)).strftime("%Y-%m-%d")
            )
            all_tasks.append(monthly_task)
            
            # Generate weekly tasks
            for week in range(4):
                weekly_task = Task(
                    title=f"{stage['name']}第{week+1}周计划",
                    description=f"完成本周{stage['name']}学习任务",
                    duration="1周",
                    type="weekly",
                    stage_id=stage["id"],
                    stage_name=stage["name"],
                    due_date=(current_date + timedelta(days=(week+1)*7)).strftime("%Y-%m-%d"),
                    dependencies=[monthly_task.id]
                )
                all_tasks.append(weekly_task)
                
                # Generate daily tasks for materials
                for material in stage_materials:
                    daily_task = Task(
                        title=f"学习{material['title']}",
                        description=material["description"],
                        duration=material["estimated_time"],
                        type="daily",
                        stage_id=stage["id"],
                        stage_name=stage["name"],
                        due_date=(current_date + timedelta(days=week*7 + 1)).strftime("%Y-%m-%d"),
                        dependencies=[weekly_task.id]
                    )
                    all_tasks.append(daily_task)
            
            current_date += timedelta(days=30)
        
        return [task.to_dict() for task in all_tasks]

    def _estimate_task_duration(self, material_time: str, task_type: str) -> str:
        """Estimate task duration based on material time and task type"""
        # Convert material time to minutes
        try:
            minutes = int(material_time.replace("分钟", ""))
            if task_type == "daily":
                return f"{minutes}分钟"
            elif task_type == "weekly":
                return "1周"
            else:
                return "1个月"
        except ValueError:
            return material_time  # Return original if parsing fails
