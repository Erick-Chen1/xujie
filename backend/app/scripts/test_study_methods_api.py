"""
Test script for the study methods API endpoints.
"""
import json
import requests
from typing import Dict

def test_study_methods_api(base_url: str = "http://localhost:8000"):
    """Test the study methods API endpoints."""
    api_url = f"{base_url}/api/v1/study-methods"
    
    print("Testing study methods API...")
    
    # Test getting example profile
    print("\nTesting GET /example-profile")
    response = requests.get(f"{api_url}/example-profile")
    if response.status_code == 200:
        print("✓ Successfully retrieved example profile")
        example_profile = response.json()
    else:
        print(f"✗ Failed to get example profile: {response.status_code}")
        return
    
    # Test profiles with different learning styles and subjects
    test_profiles = [
        example_profile,  # Use the example profile
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
    
    print("\nTesting POST /generate with different profiles")
    for i, profile in enumerate(test_profiles, 1):
        print(f"\nTest Profile {i}:")
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        
        # Generate personalized methods
        response = requests.post(
            f"{api_url}/generate",
            json=profile
        )
        
        if response.status_code == 200:
            print("✓ Successfully generated personalized methods")
            result = response.json()
            print("\nGenerated Methods:")
            for j, method in enumerate(result["methods"], 1):
                print(f"\n{j}. {method['title']} (匹配度: {method['similarity_score']:.3f})")
                print(f"   描述: {method['description']}")
                print(f"   时间投入: {method['time_commitment']}")
                print(f"   建议:")
                for rec in method["recommendations"]:
                    print(f"   - {rec}")
        else:
            print(f"✗ Failed to generate methods: {response.status_code}")
            print(response.text)
    
    print("\nAPI testing completed.")

if __name__ == "__main__":
    test_study_methods_api()
