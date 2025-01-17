"""
Test script for the study methods knowledge base.
"""
from app.core.knowledge_base import StudyMethodKnowledgeBase

def test_knowledge_base():
    # Initialize knowledge base
    kb = StudyMethodKnowledgeBase()
    
    # Build index from collected methods
    num_methods = kb.build_index()
    print(f"Built knowledge base with {num_methods} study methods")
    
    # Test various search scenarios
    test_queries = [
        "需要提高记忆力和长期记忆的方法",
        "适合课堂笔记和知识整理的学习方法",
        "提高阅读理解能力的方法",
        "时间管理和专注力提升的技巧",
        "适合理科学习的方法"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = kb.search(query)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']} (Score: {result['similarity_score']:.3f})")
            print(f"   描述: {result['description']}")
            print(f"   标签: {', '.join(result['tags'])}")
            print(f"   适用于: {', '.join(result['metadata'].get('best_for', []))}")
    
    # Save knowledge base
    kb.save()
    print("\nKnowledge base saved successfully")
    
    # Test loading saved knowledge base
    loaded_kb = StudyMethodKnowledgeBase.load()
    test_query = "需要提高记忆力的方法"
    results = loaded_kb.search(test_query)
    print(f"\nTest loaded knowledge base with query: {test_query}")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']} (Score: {result['similarity_score']:.3f})")

if __name__ == "__main__":
    test_knowledge_base()
