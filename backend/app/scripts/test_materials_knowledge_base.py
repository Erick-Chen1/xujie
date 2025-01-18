"""
Test script for the study materials knowledge base.
"""
from app.core.materials_knowledge_base import StudyMaterialKnowledgeBase

def test_materials_knowledge_base():
    # Initialize knowledge base
    kb = StudyMaterialKnowledgeBase()
    
    # Build index from collected materials
    num_materials = kb.build_index()
    print(f"Built knowledge base with {num_materials} study materials")
    
    # Test various search scenarios
    test_queries = [
        {
            "query": "需要学习数学基础概念的材料",
            "filters": {"subject": "数学", "difficulty_level": "入门"}
        },
        {
            "query": "物理实验和练习",
            "filters": {"type": "interactive"}
        },
        {
            "query": "英语学术写作指导",
            "filters": {"subject": "英语", "difficulty_level": "高级"}
        },
        {
            "query": "短时间内可以完成的学习材料",
            "filters": {"max_time": 60}  # 60 minutes
        }
    ]
    
    for test in test_queries:
        print(f"\nQuery: {test['query']}")
        print(f"Filters: {test['filters']}")
        results = kb.search(test['query'], filters=test['filters'])
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']} (Score: {result['similarity_score']:.3f})")
            print(f"   类型: {result['type']}")
            print(f"   难度: {result['difficulty_level']}")
            print(f"   预计时间: {result['estimated_time']}")
            print(f"   描述: {result['description']}")
    
    # Save knowledge base
    kb.save()
    print("\nKnowledge base saved successfully")
    
    # Test loading saved knowledge base
    loaded_kb = StudyMaterialKnowledgeBase.load()
    test_query = "数学学习材料"
    results = loaded_kb.search(test_query)
    print(f"\nTest loaded knowledge base with query: {test_query}")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']} (Score: {result['similarity_score']:.3f})")

if __name__ == "__main__":
    test_materials_knowledge_base()
