"""
Test script for the task generator.
"""
from app.core.task_generator import TaskGenerator
from app.core.learning_path_generator import LearningPathGenerator
from app.core.personalized_method_generator import PersonalizedMethodGenerator

def test_task_generator():
    """Test task generation with different learning paths."""
    try:
        print("\nInitializing test environment...")
        
        # Initialize generators
        print("\nInitializing method generator...")
        method_generator = PersonalizedMethodGenerator()
        print("\nInitializing path generator...")
        path_generator = LearningPathGenerator()
        print("\nInitializing task generator...")
        task_generator = TaskGenerator()
        print("Initialization complete\n")
        
        # Test profiles
        test_profiles = [
            {
                "learning_goals": "提高数学理解能力和解题速度",
                "learning_style": "视觉学习",
                "available_time": "工作日每天2小时",
                "preferences": "喜欢通过实例学习",
                "difficulty_level": "中等",
                "subjects": "数学"
            },
            {
                "learning_goals": "提高英语写作和口语表达",
                "learning_style": "听觉学习",
                "available_time": "时间有限，每天1小时",
                "preferences": "喜欢互动式学习",
                "difficulty_level": "入门",
                "subjects": "英语"
            }
        ]
        
        for i, profile in enumerate(test_profiles, 1):
            try:
                print(f"\n测试用户配置 {i}:")
                print(f"学习目标: {profile['learning_goals']}")
                print(f"学习风格: {profile['learning_style']}")
                print(f"可用时间: {profile['available_time']}")
                print(f"难度级别: {profile['difficulty_level']}")
                print(f"学习科目: {profile['subjects']}")
                
                print("\n生成个性化学习方法...")
                methods = method_generator.generate_personalized_methods(profile)
                print(f"成功生成 {len(methods)} 个学习方法")
                
                print("\n生成学习路径...")
                path = path_generator.generate_path(methods, profile)
                print("学习路径生成成功")
                
                print("\n检索推荐学习材料...")
                materials_by_stage = path_generator.get_stage_materials(path)
                total_materials = sum(len(materials) for materials in materials_by_stage.values())
                print(f"找到 {total_materials} 个相关学习材料")
                
                print("\n生成学习任务...")
                tasks = task_generator.generate_tasks(path, materials_by_stage)
                
                print("\n月度任务:")
                for j, task in enumerate(tasks["monthly"], 1):
                    print(f"\n{j}. {task['title']}")
                    print(f"   描述: {task['description']}")
                    print(f"   时间: 第{task['start_week']}-{task['end_week']}周")
                    print(f"   学习目标:")
                    for goal in task["learning_goals"]:
                        print(f"   - {goal}")
                
                print("\n周任务示例 (第1周):")
                first_week = next(task for task in tasks["weekly"] if task["week_number"] == 1)
                print(f"\n标题: {first_week['title']}")
                print(f"描述: {first_week['description']}")
                print(f"学习材料:")
                for material in first_week["materials"]:
                    print(f"- {material['title']} ({material['estimated_time']})")
                print(f"活动:")
                for activity in first_week["activities"]:
                    print(f"- {activity['type']}: {activity['description']} ({activity['duration']})")
                
                print("\n日任务示例 (第1天):")
                first_day = next(task for task in tasks["daily"] if task["day_number"] == 1)
                print(f"\n标题: {first_day['title']}")
                print(f"描述: {first_day['description']}")
                if first_day["materials"]:
                    print(f"今日学习材料:")
                    for material in first_day["materials"]:
                        print(f"- {material['title']} ({material['estimated_time']})")
                print(f"今日活动:")
                for activity in first_day["activities"]:
                    print(f"- {activity['type']}: {activity['description']} ({activity['duration']})")
                print(f"检查清单:")
                for item in first_day["checklist"]:
                    print(f"- [ ] {item}")
                    
            except Exception as e:
                print(f"\n处理用户配置 {i} 时出错: {str(e)}")
                continue
                
    except Exception as e:
        print(f"\n测试初始化错误: {str(e)}")
        raise

if __name__ == "__main__":
    test_task_generator()
