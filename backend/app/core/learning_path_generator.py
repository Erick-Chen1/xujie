"""
AI model for generating learning paths based on personalized study methods.
"""
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL, BATCH_SIZE
from app.core.materials_knowledge_base import StudyMaterialKnowledgeBase

class LearningPathGenerator:
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the learning path generator."""
        self.model_name = model_name or EMBEDDING_MODEL
        self.model = None  # Lazy load the model
        self.materials_kb = None  # Lazy load the knowledge base
        
    def _ensure_initialized(self):
        """Ensure model and knowledge base are initialized."""
        import psutil
        import gc
        
        def log_memory():
            mem = psutil.Process().memory_info()
            return f"Memory usage: RSS={mem.rss/1024/1024:.1f}MB, VMS={mem.vms/1024/1024:.1f}MB"
            
        print(f"Before initialization: {log_memory()}")
        gc.collect()  # Force garbage collection before loading
        
        if self.model is None:
            print(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"After loading model: {log_memory()}")
            
        if self.materials_kb is None:
            print("Initializing materials knowledge base...")
            self.materials_kb = StudyMaterialKnowledgeBase()
            self.materials_kb.build_index()
            print(f"After initializing KB: {log_memory()}")
            
        gc.collect()  # Clean up any temporary objects
        print(f"Final memory state: {log_memory()}")
    
    def _validate_path_inputs(self, personalized_methods: List[Dict], user_info: Dict) -> None:
        """
        Validate inputs for path generation.
        
        Args:
            personalized_methods: List of personalized study methods
            user_info: User profile information
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs have wrong types
        """
        if not isinstance(personalized_methods, list):
            raise TypeError("personalized_methods must be a list")
        if not isinstance(user_info, dict):
            raise TypeError("user_info must be a dictionary")
            
        if not personalized_methods:
            raise ValueError("personalized_methods cannot be empty")
            
        required_method_fields = {'title', 'description', 'time_commitment'}
        for method in personalized_methods:
            missing_fields = required_method_fields - set(method.keys())
            if missing_fields:
                raise ValueError(f"Study method missing required fields: {', '.join(missing_fields)}")
                
        required_user_fields = {'subjects', 'difficulty_level', 'learning_goals', 
                              'learning_style', 'available_time'}
        missing_fields = required_user_fields - set(user_info.keys())
        if missing_fields:
            raise ValueError(f"User profile missing required fields: {', '.join(missing_fields)}")

    def generate_path(self, personalized_methods: List[Dict], user_info: Dict) -> Dict:
        """
        Generate a learning path based on personalized study methods.
        
        Args:
            personalized_methods: List of personalized study methods
            user_info: User profile information
            
        Returns:
            Dict containing the generated learning path
            
        Raises:
            ValueError: If inputs are invalid
            RuntimeError: If path generation fails
        """
        import gc
        try:
            # Validate inputs
            self._validate_path_inputs(personalized_methods, user_info)
            
            # Initialize components
            self._ensure_initialized()
            
            # Create path structure
            path = {
                "id": str(uuid.uuid4()),
                "title": self._generate_path_title(user_info),
                "description": self._generate_path_description(user_info, personalized_methods),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "subject": user_info["subjects"],  # Now validated, can use direct access
                "difficulty_level": user_info["difficulty_level"],
                "estimated_duration": self._calculate_total_duration(personalized_methods),
                "stages": self._generate_stages(personalized_methods, user_info),
                "prerequisites": self._gather_prerequisites(personalized_methods),
                "learning_goals": user_info["learning_goals"],
                "study_methods": [method["title"] for method in personalized_methods],
                "metadata": {
                    "user_learning_style": user_info["learning_style"],
                    "available_time": user_info["available_time"],
                    "preferences": user_info.get("preferences", "")  # Optional field
                }
            }
            return path
        except Exception as e:
            raise RuntimeError(f"Failed to generate learning path: {str(e)}")
        finally:
            # Clean up resources after path generation
            if hasattr(self, 'model'):
                del self.model
                self.model = None
            if hasattr(self, 'materials_kb'):
                del self.materials_kb
                self.materials_kb = None
            gc.collect()
    
    def _generate_path_title(self, user_info: Dict) -> str:
        """Generate a descriptive title for the learning path."""
        subject = user_info.get("subjects", "")
        level = user_info.get("difficulty_level", "")
        return f"{subject}{level}级学习路径"
    
    def _generate_path_description(self, user_info: Dict, methods: List[Dict]) -> str:
        """Generate a detailed description of the learning path."""
        goals = user_info.get("learning_goals", "")
        method_names = ", ".join(method["title"] for method in methods)
        return (
            f"这是一个为实现\"{goals}\"而定制的学习路径。"
            f"路径采用了{method_names}等学习方法，"
            f"针对{user_info.get('learning_style', '')}的学习风格进行了优化。"
        )
    
    def _calculate_total_duration(self, methods: List[Dict]) -> str:
        """Calculate the estimated total duration for the learning path."""
        # This is a simplified calculation, could be more sophisticated
        return "4-6周"
    
    def _generate_stages(self, methods: List[Dict], user_info: Dict) -> List[Dict]:
        """Generate learning stages based on study methods."""
        stages = []
        
        # Stage 1: Foundation
        stages.append({
            "id": str(uuid.uuid4()),
            "title": "基础阶段",
            "description": "掌握核心概念和基础知识",
            "duration": "1-2周",
            "methods": [methods[0]["title"]],  # Primary method for basics
            "activities": [
                {
                    "type": "学习",
                    "description": "理解和掌握基本概念",
                    "method": methods[0]["title"],
                    "duration": "每天1-2小时"
                },
                {
                    "type": "练习",
                    "description": "完成基础练习和测试",
                    "method": methods[0]["title"],
                    "duration": "每天30-60分钟"
                }
            ]
        })
        
        # Stage 2: Practice
        stages.append({
            "id": str(uuid.uuid4()),
            "title": "实践阶段",
            "description": "应用学习方法，深化理解",
            "duration": "2-3周",
            "methods": [method["title"] for method in methods],  # All methods
            "activities": [
                {
                    "type": "应用",
                    "description": "实践应用学习方法",
                    "method": methods[1]["title"] if len(methods) > 1 else methods[0]["title"],
                    "duration": "每天2-3小时"
                },
                {
                    "type": "复习",
                    "description": "定期复习和巩固",
                    "method": methods[-1]["title"],
                    "duration": "每天1小时"
                }
            ]
        })
        
        # Stage 3: Advanced
        stages.append({
            "id": str(uuid.uuid4()),
            "title": "提高阶段",
            "description": "深入学习和能力提升",
            "duration": "1-2周",
            "methods": [method["title"] for method in methods],  # All methods
            "activities": [
                {
                    "type": "深入学习",
                    "description": "探索高级主题和应用",
                    "method": methods[0]["title"],
                    "duration": "每天2-3小时"
                },
                {
                    "type": "总结",
                    "description": "知识整理和方法总结",
                    "method": methods[-1]["title"],
                    "duration": "每天1小时"
                }
            ]
        })
        
        return stages
    
    def _gather_prerequisites(self, methods: List[Dict]) -> List[str]:
        """Gather prerequisites from all study methods."""
        prerequisites = set()
        for method in methods:
            prerequisites.update(method.get("prerequisites", []))
        return list(prerequisites)
    
    def get_stage_materials(self, path: Dict) -> Dict[str, List[Dict]]:
        """
        Get study materials organized by stage for the learning path.
        Materials are selected based on stage requirements and learning progression.
        
        Returns:
            Dict mapping stage IDs to lists of recommended materials
        """
        materials = []
        seen_materials = set()  # Track seen material IDs
        difficulty_levels = {'入门': 0, '中等': 1, '高级': 2}
        base_level = difficulty_levels.get(path["difficulty_level"], 1)
        
        # Search materials for each stage with progressive difficulty
        for i, stage in enumerate(path["stages"]):
            # Adjust difficulty based on stage and base level
            if base_level == 0:  # Entry level
                stage_level = list(difficulty_levels.keys())[0]  # Stay at entry level
            elif base_level == 1:  # Intermediate
                if i == 0:  # First stage
                    stage_level = list(difficulty_levels.keys())[0]  # Start with entry
                else:  # Later stages
                    stage_level = list(difficulty_levels.keys())[1]  # Move to intermediate
            else:  # Advanced
                if i == 0:  # First stage
                    stage_level = list(difficulty_levels.keys())[1]  # Start with intermediate
                else:  # Later stages
                    stage_level = list(difficulty_levels.keys())[2]  # Move to advanced
            
            # Create stage-specific query with activity context
            activities = [f"{act['type']}: {act['description']}" for act in stage["activities"]]
            stage_query = (
                f"{stage['title']} {stage['description']} "
                f"{path['subject']} {' '.join(path['study_methods'])} "
                f"{' '.join(activities)}"
            )
            
            # Add stage-specific filters
            filters = {
                "subject": path["subject"],
                "difficulty_level": stage_level
            }
            
            # Add time filter using the longest activity duration
            max_minutes = 0
            for activity in stage["activities"]:
                if "每天" in activity["duration"]:
                    time_str = activity["duration"].replace("每天", "")
                    # Handle time ranges (e.g., "1-2小时")
                    if "-" in time_str:
                        max_time = time_str.split("-")[1]
                    else:
                        max_time = time_str
                        
                    if "小时" in max_time:
                        # Remove any non-numeric characters except decimal point
                        hours = float(''.join(c for c in max_time.replace("小时", "") if c.isdigit() or c == '.'))
                        minutes = int(hours * 60)
                    elif "分钟" in max_time:
                        # Remove any non-numeric characters
                        minutes = int(''.join(c for c in max_time.replace("分钟", "") if c.isdigit()))
                    max_minutes = max(max_minutes, minutes)
            
            if max_minutes > 0:
                filters["max_time"] = max_minutes
            
            # Search for materials with relaxed filters first
            print(f"\nSearching materials for stage: {stage['title']}")
            self._ensure_initialized()
            if self.materials_kb is None:
                print("Warning: Materials knowledge base is not initialized!")
                return {}
            
            print(f"Searching with query: {stage_query[:100]}...")
            stage_materials = self.materials_kb.search(
                query=stage_query,
                filters={"subject": path["subject"]},  # Start with just subject filter
                k=10  # Get more candidates
            )
            print(f"Found {len(stage_materials)} initial materials")
            
            # Apply difficulty and time filters manually for better control
            filtered_materials = []
            for material in stage_materials:
                if self.materials_kb._matches_filters(material, filters):
                    filtered_materials.append(material)
                    
            stage_materials = filtered_materials[:5]  # Keep top 5 after filtering
            
            # Add unique materials with stage context
            added_for_stage = 0
            for material in stage_materials:
                if material["id"] not in seen_materials and added_for_stage < 2:
                    material["stage"] = stage["title"]
                    material["stage_description"] = stage["description"]
                    material["recommended_activity"] = next(
                        (act["type"] for act in stage["activities"] 
                         if act["type"].lower() in material["description"].lower()),
                        stage["activities"][0]["type"]
                    )
                    materials.append(material)
                    seen_materials.add(material["id"])
                    added_for_stage += 1
        
        # Organize materials by stage ID
        materials_by_stage = {}
        for stage in path["stages"]:
            stage_materials = []
            for material in materials:
                if material.get("stage") == stage["title"]:
                    # Add stage-specific metadata
                    material["stage_id"] = stage["id"]
                    material["stage_duration"] = stage["duration"]
                    material["learning_activities"] = stage["activities"]
                    stage_materials.append(material)
            materials_by_stage[stage["id"]] = stage_materials
        
        return materials_by_stage
