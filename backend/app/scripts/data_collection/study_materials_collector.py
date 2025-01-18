"""
Script to collect and process study materials from various sources.
"""
import json
import uuid
from datetime import datetime
from typing import List, Dict
from pathlib import Path

class StudyMaterialCollector:
    def __init__(self, output_dir: str = "data/study_materials"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_sample_materials(self) -> List[Dict]:
        """
        Collect sample study materials for initial testing.
        In production, this would be replaced with actual data collection from various sources.
        """
        sample_materials = [
            # Math Materials - Entry Level
            {
                "id": str(uuid.uuid4()),
                "title": "数学基础概念复习",
                "description": "复习基本数学概念，包括代数运算、几何基础等。通过实例和练习加深理解。",
                "type": "video",
                "subject": "数学",
                "topic": ["代数", "几何", "基础数学"],
                "difficulty_level": "入门",
                "estimated_time": "30分钟",
                "url": "https://example.com/math-basics",
                "prerequisites": ["初中数学基础"],
                "related_methods": ["费曼学习法", "思维导图法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "video_length": "28:30",
                    "has_exercises": True,
                    "key_concepts": ["基本运算", "几何概念", "数学思维"]
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "线性代数基础概念",
                "description": "介绍线性代数中的基本概念，包括向量、矩阵、线性变换等。通过可视化和实际应用来理解抽象概念。",
                "type": "video",
                "subject": "数学",
                "topic": ["线性代数", "向量", "矩阵"],
                "difficulty_level": "入门",
                "estimated_time": "45分钟",
                "url": "https://example.com/linear-algebra-basics",
                "prerequisites": ["高中数学基础"],
                "related_methods": ["费曼学习法", "思维导图法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "video_length": "42:30",
                    "has_exercises": True,
                    "key_concepts": ["向量空间", "线性变换", "矩阵运算"]
                }
            },
            # Math Materials - Intermediate Level
            {
                "id": str(uuid.uuid4()),
                "title": "数学解题技巧与方法",
                "description": "介绍各类数学题型的解题思路和方法，包括代数、几何等领域的典型问题。",
                "type": "interactive",
                "subject": "数学",
                "topic": ["解题技巧", "思维方法", "数学应用"],
                "difficulty_level": "中等",
                "estimated_time": "60分钟",
                "url": "https://example.com/math-problem-solving",
                "prerequisites": ["基础数学概念"],
                "related_methods": ["主动回顾法", "实践练习法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "practice_problems": 20,
                    "interactive_elements": ["在线练习", "即时反馈"],
                    "recommended_review_schedule": "每周3次"
                }
            },
            # English Materials - Entry Level
            {
                "id": str(uuid.uuid4()),
                "title": "英语基础口语练习",
                "description": "通过日常对话场景学习基础英语口语，包括发音规则和常用表达。",
                "type": "video",
                "subject": "英语",
                "topic": ["口语", "发音", "日常英语"],
                "difficulty_level": "入门",
                "estimated_time": "30分钟",
                "url": "https://example.com/basic-english-speaking",
                "prerequisites": ["基础英语词汇"],
                "related_methods": ["听说结合法", "情境学习法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "video_length": "25:00",
                    "has_exercises": True,
                    "practice_dialogues": 10
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "英语写作基础：句子结构",
                "description": "学习英语句子的基本结构和常见句型，通过例句和练习掌握基础写作技巧。",
                "type": "article",
                "subject": "英语",
                "topic": ["写作", "语法", "句型"],
                "difficulty_level": "入门",
                "estimated_time": "45分钟",
                "url": "https://example.com/basic-english-writing",
                "prerequisites": ["基础英语语法"],
                "related_methods": ["模仿写作法", "渐进学习法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "example_count": 15,
                    "writing_exercises": True,
                    "key_concepts": ["主谓宾", "时态", "从句"]
                }
            },
            # English Materials - Intermediate Level
            {
                "id": str(uuid.uuid4()),
                "title": "英语写作进阶：段落组织",
                "description": "学习如何组织和连接段落，使文章结构清晰，逻辑连贯。",
                "type": "article",
                "subject": "英语",
                "topic": ["写作", "段落", "文章结构"],
                "difficulty_level": "中等",
                "estimated_time": "60分钟",
                "url": "https://example.com/intermediate-writing",
                "prerequisites": ["基础写作能力"],
                "related_methods": ["结构分析法", "写作练习法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "word_count": 2000,
                    "example_count": 8,
                    "writing_exercises": True
                }
            },
            # Advanced Materials
            {
                "id": str(uuid.uuid4()),
                "title": "英语写作技巧：论文结构",
                "description": "详细讲解学术论文的基本结构，包括引言、主体、结论的写作方法和技巧。提供多个范文分析。",
                "type": "article",
                "subject": "英语",
                "topic": ["写作", "学术论文", "写作技巧"],
                "difficulty_level": "高级",
                "estimated_time": "60分钟",
                "url": "https://example.com/academic-writing-structure",
                "prerequisites": ["英语B2水平", "基础写作能力"],
                "related_methods": ["SQ3R阅读法", "康奈尔笔记法"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "word_count": 3000,
                    "example_count": 5,
                    "writing_exercises": True,
                    "peer_review_suggested": True
                }
            }
        ]
        return sample_materials
    
    def save_materials(self, materials: List[Dict], filename: str = "sample_materials.json"):
        """Save collected materials to JSON file"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(materials)} materials to {output_path}")
    
    def validate_material(self, material: Dict) -> bool:
        """Validate study material data structure"""
        required_fields = [
            "id", "title", "description", "type", "subject",
            "topic", "difficulty_level", "estimated_time",
            "prerequisites", "related_methods", "created_at", "updated_at"
        ]
        return all(field in material for field in required_fields)
    
    def collect_and_save(self):
        """Main method to collect and save study materials"""
        materials = self.collect_sample_materials()
        valid_materials = [m for m in materials if self.validate_material(m)]
        self.save_materials(valid_materials)
        return valid_materials

if __name__ == "__main__":
    collector = StudyMaterialCollector()
    collector.collect_and_save()
