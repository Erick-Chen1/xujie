"""
Task generator for creating structured learning tasks from paths and materials.
"""
from typing import List, Dict
from datetime import datetime, timedelta
import uuid

class TaskGenerator:
    def __init__(self):
        """Initialize the task generator."""
        pass
    
    def _validate_path_structure(self, path: Dict) -> None:
        """
        Validate learning path structure.
        
        Args:
            path: Learning path dictionary
            
        Raises:
            ValueError: If path structure is invalid
            TypeError: If path has wrong type
        """
        if not isinstance(path, dict):
            raise TypeError("path must be a dictionary")
            
        required_fields = {
            'id', 'title', 'stages', 'difficulty_level', 
            'estimated_duration', 'study_methods'
        }
        missing_fields = required_fields - set(path.keys())
        if missing_fields:
            raise ValueError(f"Path missing required fields: {', '.join(missing_fields)}")
            
        if not isinstance(path['stages'], list) or not path['stages']:
            raise ValueError("Path must contain at least one stage")
            
        # Validate stage structure
        required_stage_fields = {'id', 'title', 'duration', 'activities'}
        for stage in path['stages']:
            if not isinstance(stage, dict):
                raise TypeError("Each stage must be a dictionary")
            missing_fields = required_stage_fields - set(stage.keys())
            if missing_fields:
                raise ValueError(f"Stage missing required fields: {', '.join(missing_fields)}")
                
            if not isinstance(stage['activities'], list) or not stage['activities']:
                raise ValueError(f"Stage '{stage['title']}' must contain at least one activity")

    def _validate_materials(self, materials_by_stage: Dict[str, List[Dict]]) -> None:
        """
        Validate materials structure.
        
        Args:
            materials_by_stage: Dictionary mapping stage IDs to materials
            
        Raises:
            ValueError: If materials structure is invalid
            TypeError: If materials have wrong type
        """
        if not isinstance(materials_by_stage, dict):
            raise TypeError("materials_by_stage must be a dictionary")
            
        required_material_fields = {'id', 'title', 'type', 'estimated_time'}
        for stage_id, materials in materials_by_stage.items():
            if not isinstance(materials, list):
                raise TypeError(f"Materials for stage {stage_id} must be a list")
                
            for material in materials:
                if not isinstance(material, dict):
                    raise TypeError("Each material must be a dictionary")
                missing_fields = required_material_fields - set(material.keys())
                if missing_fields:
                    raise ValueError(f"Material missing required fields: {', '.join(missing_fields)}")
                    
                # Validate time format
                time_str = material['estimated_time']
                if not any(unit in time_str for unit in ['小时', '分钟']):
                    raise ValueError(f"Invalid time format in material '{material['title']}'. Must include '小时' or '分钟'")

    def generate_tasks(self, path: Dict, materials_by_stage: Dict[str, List[Dict]]) -> Dict:
        """
        Generate monthly, weekly, and daily tasks from a learning path and its materials.
        
        Args:
            path: Learning path dictionary
            materials_by_stage: Dictionary mapping stage IDs to lists of materials
            
        Returns:
            Dictionary containing monthly, weekly, and daily tasks
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs have wrong types
        """
        try:
            # Validate inputs
            self._validate_path_structure(path)
            self._validate_materials(materials_by_stage)
            
            # Generate tasks
            tasks = {
                "monthly": self._generate_monthly_tasks(path, materials_by_stage),
                "weekly": self._generate_weekly_tasks(path, materials_by_stage),
                "daily": self._generate_daily_tasks(path, materials_by_stage)
            }
            return tasks
        except Exception as e:
            raise RuntimeError(f"Failed to generate tasks: {str(e)}")
    
    def _generate_monthly_tasks(self, path: Dict, materials_by_stage: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate monthly tasks focusing on overall progress and major milestones."""
        monthly_tasks = []
        
        # Calculate total duration in weeks
        total_weeks = sum(
            int(stage["duration"].split("-")[1].replace("周", ""))
            for stage in path["stages"]
        )
        
        # Create monthly overview tasks
        current_week = 1
        for stage in path["stages"]:
            stage_weeks = int(stage["duration"].split("-")[1].replace("周", ""))
            
            # Create monthly task for stage
            monthly_tasks.append({
                "id": str(uuid.uuid4()),
                "title": f"完成{stage['title']}",
                "description": stage["description"],
                "start_week": current_week,
                "end_week": current_week + stage_weeks - 1,
                "stage_id": stage["id"],
                "materials": [
                    {
                        "id": material["id"],
                        "title": material["title"],
                        "type": material["type"],
                        "estimated_time": material["estimated_time"]
                    }
                    for material in materials_by_stage.get(stage["id"], [])
                ],
                "learning_goals": [
                    f"掌握{stage['title']}的核心内容",
                    f"完成{len(materials_by_stage.get(stage['id'], []))}个学习材料",
                    f"应用{', '.join(stage['methods'])}等学习方法"
                ],
                "evaluation_criteria": [
                    "是否完成所有学习材料",
                    "是否掌握核心概念",
                    "是否能够应用所学知识"
                ]
            })
            
            current_week += stage_weeks
        
        return monthly_tasks
    
    def _generate_weekly_tasks(self, path: Dict, materials_by_stage: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate weekly tasks breaking down monthly goals into manageable chunks."""
        weekly_tasks = []
        
        current_week = 1
        for stage in path["stages"]:
            stage_weeks = int(stage["duration"].split("-")[1].replace("周", ""))
            stage_materials = materials_by_stage.get(stage["id"], [])
            
            # Distribute materials across weeks
            materials_per_week = len(stage_materials) // stage_weeks
            if materials_per_week == 0:
                materials_per_week = 1
            
            for week in range(stage_weeks):
                week_materials = stage_materials[week * materials_per_week:(week + 1) * materials_per_week]
                
                # Create weekly tasks
                activities = []
                for activity in stage["activities"]:
                    activities.append({
                        "id": str(uuid.uuid4()),
                        "type": activity["type"],
                        "description": activity["description"],
                        "duration": activity["duration"],
                        "method": activity["method"]
                    })
                
                weekly_tasks.append({
                    "id": str(uuid.uuid4()),
                    "week_number": current_week,
                    "stage_id": stage["id"],
                    "title": f"{stage['title']} 第{week + 1}周",
                    "description": f"完成本周{stage['title']}的学习任务",
                    "materials": [
                        {
                            "id": material["id"],
                            "title": material["title"],
                            "type": material["type"],
                            "estimated_time": material["estimated_time"],
                            "recommended_activity": material["recommended_activity"]
                        }
                        for material in week_materials
                    ],
                    "activities": activities,
                    "total_time": sum(
                        int(material["estimated_time"].replace("分钟", ""))
                        for material in week_materials
                        if "分钟" in material["estimated_time"]
                    ),
                    "learning_goals": [
                        f"完成{len(week_materials)}个学习材料",
                        f"每日练习{stage['activities'][0]['duration']}",
                        "复习本周学习内容"
                    ]
                })
                
                current_week += 1
        
        return weekly_tasks
    
    def _generate_daily_tasks(self, path: Dict, materials_by_stage: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate daily tasks for detailed activity planning."""
        daily_tasks = []
        
        # Calculate days needed based on weekly tasks
        weekly_tasks = self._generate_weekly_tasks(path, materials_by_stage)
        total_days = len(weekly_tasks) * 7
        
        current_day = 1
        for weekly_task in weekly_tasks:
            # Distribute weekly materials across days
            materials = weekly_task["materials"]
            activities = weekly_task["activities"]
            
            # Create tasks for each day of the week
            for day in range(7):
                # Assign materials to specific days
                day_materials = materials[day::7]
                
                daily_tasks.append({
                    "id": str(uuid.uuid4()),
                    "day_number": current_day,
                    "week_id": weekly_task["id"],
                    "title": f"第{current_day}天学习任务",
                    "description": "完成今日学习任务和练习",
                    "materials": [
                        {
                            "id": material["id"],
                            "title": material["title"],
                            "type": material["type"],
                            "estimated_time": material["estimated_time"],
                            "activity": material["recommended_activity"]
                        }
                        for material in day_materials
                    ],
                    "activities": [
                        {
                            "id": activity["id"],
                            "type": activity["type"],
                            "description": activity["description"],
                            "duration": activity["duration"],
                            "method": activity["method"],
                            "status": "pending"
                        }
                        for activity in activities
                    ],
                    "total_time": sum(
                        int(material["estimated_time"].replace("分钟", ""))
                        for material in day_materials
                        if "分钟" in material["estimated_time"]
                    ),
                    "checklist": [
                        "完成今日学习材料",
                        "进行课后练习",
                        "复习昨日内容",
                        "记录学习笔记",
                        "完成自测题"
                    ]
                })
                
                current_day += 1
        
        return daily_tasks
