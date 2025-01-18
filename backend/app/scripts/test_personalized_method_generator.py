"""
Test script for the personalized method generator.
"""
from app.core.personalized_method_generator import PersonalizedMethodGenerator

def test_personalized_method_generator():
    # Initialize generator
    generator = PersonalizedMethodGenerator()
    
    # Test various user profiles
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
        },
        {
            "learning_goals": "掌握物理基本原理和实验方法",
            "learning_style": "动手实践",
            "available_time": "周末充足时间",
            "preferences": "喜欢做实验和解题",
            "difficulty_level": "高级",
            "subjects": "物理"
        }
    ]
    
    for i, profile in enumerate(test_profiles, 1):
        print(f"\n测试用户配置 {i}:")
        print(f"学习目标: {profile['learning_goals']}")
        print(f"学习风格: {profile['learning_style']}")
        print(f"可用时间: {profile['available_time']}")
        print(f"难度级别: {profile['difficulty_level']}")
        print(f"学习科目: {profile['subjects']}")
        
        # Generate personalized methods
        methods = generator.generate_personalized_methods(profile)
        
        print("\n推荐的学习方法:")
        for j, method in enumerate(methods, 1):
            print(f"\n{j}. {method['title']} (匹配度: {method['similarity_score']:.3f})")
            print(f"   描述: {method['description']}")
            print(f"   时间投入: {method['time_commitment']}")
            print(f"   建议:")
            for rec in method['recommendations']:
                print(f"   - {rec}")

if __name__ == "__main__":
    test_personalized_method_generator()
