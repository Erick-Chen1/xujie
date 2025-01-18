from typing import List, Dict, Any
from datetime import datetime, timedelta
from core.kimi import KimiAPI
from core.knowledge_base import KnowledgeBase
from core.materials_base import MaterialsBase
from schemas.learning_path import LearningPathCreate

class PathGenerator:
    def __init__(self, knowledge_base: KnowledgeBase, materials_base: MaterialsBase):
        """Initialize path generator with knowledge and materials bases"""
        self.knowledge_base = knowledge_base
        self.materials_base = materials_base
        self.kimi_api = KimiAPI()
        
        # Define learning flow stages
        self.learning_stages = [
            {
                "name": "knowledge_acquisition",
                "categories": ["基本概念", "性质与关系", "基本运算", "应用"],
                "description": "初始知识获取阶段"
            },
            {
                "name": "practice_reinforcement",
                "categories": ["基本运算", "应用"],
                "description": "练习强化阶段"
            },
            {
                "name": "pattern_identification",
                "categories": ["性质与关系", "应用"],
                "description": "题型规律识别阶段"
            },
            {
                "name": "special_learning",
                "categories": ["阅读与思考", "信息技术应用", "探究与发现", "数学建模"],
                "description": "特色学习环节"
            }
        ]

    async def generate_path(self, user_profile: LearningPathCreate) -> List[Dict[str, Any]]:
        """Generate complete learning path following the required sequence"""
        # Get AI recommendations for path structure
        path_structure = await self.kimi_api.generate_method_match({
            **user_profile.dict(),
            "learning_stages": self.learning_stages
        })
        
        learning_path = []
        current_date = datetime.now()
        
        # Process each learning stage
        for stage in self.learning_stages:
            stage_materials = []
            
            # Get materials for each category in the stage
            for category in stage["categories"]:
                # Search for relevant materials
                materials = self.materials_base.search_materials(
                    f"{category} {user_profile.difficulty_level} {user_profile.learning_goals}",
                    k=3
                )
                
                # Add materials to stage with scheduling
                for material in materials:
                    stage_materials.append({
                        "material": material["material"],
                        "scheduled_date": current_date.strftime("%Y-%m-%d"),
                        "stage": stage["name"],
                        "category": category,
                        "estimated_time": material["material"]["estimated_time"]
                    })
                    current_date += timedelta(days=1)
            
            # Get methods appropriate for this stage
            stage_methods = self.knowledge_base.search_methods(
                f"{stage['description']} {user_profile.learning_style}",
                k=2
            )
            
            # Create stage entry
            learning_path.append({
                "stage": stage["name"],
                "description": stage["description"],
                "materials": stage_materials,
                "methods": [method["method"] for method in stage_methods],
                "duration": f"{len(stage_materials)}天",
                "learning_focus": self._generate_learning_focus(stage["name"], user_profile)
            })
        
        return learning_path
        
    def _generate_learning_focus(self, stage: str, profile: LearningPathCreate) -> str:
        """Generate learning focus based on stage and user profile"""
        focus_map = {
            "knowledge_acquisition": "掌握核心概念和基本原理",
            "practice_reinforcement": "通过练习加深理解和熟练度",
            "pattern_identification": "识别题型特征和解题模式",
            "special_learning": "拓展思维和应用能力"
        }
        return focus_map.get(stage, "全面提升数学能力")
