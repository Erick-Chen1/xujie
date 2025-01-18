"""
Test script for the learning path generator.
"""
from app.core.learning_path_generator import LearningPathGenerator
from app.core.personalized_method_generator import PersonalizedMethodGenerator

def test_learning_path_generator():
    """Test the learning path generator with different scenarios."""
    try:
        print("\nInitializing test environment...")
        
        # Initialize generators
        print("\nInitializing method generator...")
        method_generator = PersonalizedMethodGenerator()
        print("\nInitializing path generator...")
        path_generator = LearningPathGenerator()
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
                
                print("\n生成的学习路径:")
                print(f"标题: {path['title']}")
                print(f"描述: {path['description']}")
                print(f"总时长: {path['estimated_duration']}")
                print(f"采用的学习方法: {', '.join(path['study_methods'])}")
                
                print("\n学习阶段:")
                for j, stage in enumerate(path["stages"], 1):
                    print(f"\n{j}. {stage['title']}")
                    print(f"   描述: {stage['description']}")
                    print(f"   时长: {stage['duration']}")
                    print(f"   活动:")
                    for activity in stage["activities"]:
                        print(f"   - {activity['type']}: {activity['description']} ({activity['duration']})")
                
                print("\n检索推荐学习材料...")
                materials_by_stage = path_generator.get_stage_materials(path)
                total_materials = sum(len(materials) for materials in materials_by_stage.values())
                print(f"找到 {total_materials} 个相关学习材料")
                
                print("\n推荐学习材料预览:")
                for stage in path["stages"]:
                    stage_materials = materials_by_stage.get(stage["id"], [])
                    if stage_materials:
                        print(f"\n{stage['title']}:")
                        for j, material in enumerate(stage_materials, 1):
                            print(f"\n  {j}. {material['title']}")
                            print(f"     类型: {material['type']}")
                            print(f"     难度: {material['difficulty_level']}")
                            print(f"     预计时间: {material['estimated_time']}")
                            print(f"     建议活动: {material['recommended_activity']}")
                            print(f"     活动时长: {material['stage_duration']}")
                            print(f"     描述: {material['description'][:100]}...")
                    
            except Exception as e:
                print(f"\n处理用户配置 {i} 时出错: {str(e)}")
                continue
                
    except Exception as e:
        print(f"\n测试初始化错误: {str(e)}")
        raise

if __name__ == "__main__":
    test_learning_path_generator()
