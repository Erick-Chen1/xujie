"""
Script to collect and process study methods from various sources.
"""
import json
import uuid
from datetime import datetime
from typing import List, Dict
import pandas as pd
from pathlib import Path

class StudyMethodCollector:
    def __init__(self, output_dir: str = "data/study_methods"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_sample_methods(self) -> List[Dict]:
        """
        Collect sample study methods for initial testing.
        In production, this would be replaced with actual data collection from various sources.
        """
        sample_methods = [
            {
                "id": str(uuid.uuid4()),
                "title": "费曼学习法",
                "description": "通过向他人解释概念来深入理解。步骤：1.选择概念 2.假装教授他人 3.识别知识漏洞 4.简化并类比 5.复习和完善",
                "source": "理查德·费曼",
                "tags": ["理解", "教学", "复习", "深度学习"],
                "effectiveness_rating": 4.8,
                "difficulty_level": "中等",
                "time_commitment": "每个概念30-60分钟",
                "prerequisites": ["基础知识", "耐心"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["概念理解", "长期记忆"],
                    "recommended_subjects": ["理论性学科", "科学", "数学"]
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "番茄工作法",
                "description": "将学习时间分成25分钟的专注时段，每个时段后短暂休息。完成4个时段后进行较长休息。",
                "source": "Francesco Cirillo",
                "tags": ["时间管理", "专注", "效率", "休息"],
                "effectiveness_rating": 4.5,
                "difficulty_level": "简单",
                "time_commitment": "可灵活调整",
                "prerequisites": ["计时器"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["专注力提升", "避免疲劳"],
                    "recommended_duration": "25分钟工作，5分钟休息"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "康奈尔笔记法",
                "description": "将笔记页面分为三个区域：笔记区、关键词区和总结区。课堂记录要点，课后提炼关键词，24小时内完成总结。",
                "source": "沃尔特·保利克",
                "tags": ["笔记", "组织", "复习", "总结"],
                "effectiveness_rating": 4.6,
                "difficulty_level": "中等",
                "time_commitment": "课堂期间 + 课后30分钟",
                "prerequisites": ["笔记本", "良好的听课能力"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["课堂学习", "知识整理", "考试复习"],
                    "recommended_subjects": ["所有科目"],
                    "note_format": {
                        "笔记区": "页面右侧2/3区域",
                        "关键词区": "页面左侧1/3区域",
                        "总结区": "页面底部"
                    }
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "思维导图法",
                "description": "通过图形化方式组织知识点，建立知识间的联系。从中心主题出发，延伸出主要分支和次要分支。",
                "source": "东尼·博赞",
                "tags": ["可视化", "联系", "组织", "创造性思维"],
                "effectiveness_rating": 4.7,
                "difficulty_level": "简单",
                "time_commitment": "每个主题20-40分钟",
                "prerequisites": ["绘图工具", "色彩笔"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["知识体系构建", "复习", "头脑风暴"],
                    "recommended_subjects": ["文科", "理科", "跨学科主题"],
                    "tools": ["纸笔", "电子思维导图软件"]
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "间隔重复法",
                "description": "根据艾宾浩斯遗忘曲线安排复习时间。首次学习后在1天、2天、4天、7天、15天进行复习。",
                "source": "赫尔曼·艾宾浩斯",
                "tags": ["记忆", "复习", "效率", "科学方法"],
                "effectiveness_rating": 4.9,
                "difficulty_level": "中等",
                "time_commitment": "每次复习15-30分钟",
                "prerequisites": ["学习计划表", "复习材料"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["长期记忆", "考试准备"],
                    "review_schedule": [
                        "第1天：首次学习",
                        "第2天：第一次复习",
                        "第4天：第二次复习",
                        "第7天：第三次复习",
                        "第15天：第四次复习"
                    ]
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "SQ3R阅读法",
                "description": "Survey（浏览）、Question（提问）、Read（阅读）、Recite（复述）、Review（复习）五步骤深入理解文章。",
                "source": "Francis Robinson",
                "tags": ["阅读", "理解", "记忆", "系统方法"],
                "effectiveness_rating": 4.6,
                "difficulty_level": "中等",
                "time_commitment": "每篇文章30-60分钟",
                "prerequisites": ["文章材料", "笔记工具"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["阅读理解", "文章分析", "考试准备"],
                    "steps": {
                        "Survey": "快速浏览获取整体印象",
                        "Question": "提出问题激发好奇心",
                        "Read": "仔细阅读寻找答案",
                        "Recite": "合上书本复述要点",
                        "Review": "总结归纳加深理解"
                    }
                }
            },
            {
                "id": str(uuid.uuid4()),
                "title": "主动回顾法",
                "description": "在学习过程中主动测试自己，通过自问自答、制作闪卡、写总结等方式加深理解和记忆。",
                "source": "认知科学研究",
                "tags": ["记忆", "理解", "测试", "自主学习"],
                "effectiveness_rating": 4.8,
                "difficulty_level": "中等",
                "time_commitment": "每次学习后15-20分钟",
                "prerequisites": ["学习材料", "闪卡或笔记本"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {
                    "best_for": ["深度理解", "长期记忆"],
                    "techniques": [
                        "制作闪卡",
                        "自问自答",
                        "写总结",
                        "教授他人"
                    ],
                    "recommended_frequency": "每次学习新内容后立即进行"
                }
            }
        ]
        return sample_methods
    
    def save_methods(self, methods: List[Dict], filename: str = "sample_methods.json"):
        """Save collected methods to JSON file"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(methods, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(methods)} methods to {output_path}")
    
    def validate_method(self, method: Dict) -> bool:
        """Validate study method data structure"""
        required_fields = [
            "id", "title", "description", "source", "tags",
            "effectiveness_rating", "difficulty_level", "time_commitment",
            "prerequisites", "created_at", "updated_at"
        ]
        return all(field in method for field in required_fields)
    
    def collect_and_save(self):
        """Main method to collect and save study methods"""
        methods = self.collect_sample_methods()
        valid_methods = [m for m in methods if self.validate_method(m)]
        self.save_methods(valid_methods)
        return valid_methods

if __name__ == "__main__":
    collector = StudyMethodCollector()
    collector.collect_and_save()
