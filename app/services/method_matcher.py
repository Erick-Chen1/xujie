from typing import List, Dict, Any
from core.kimi import KimiAPI
from core.knowledge_base import KnowledgeBase
from schemas.learning_path import LearningPathCreate

class MethodMatcher:
    def __init__(self, knowledge_base: KnowledgeBase):
        """Initialize method matcher with knowledge base and Kimi API"""
        self.knowledge_base = knowledge_base
        self.kimi_api = KimiAPI()

    async def match_methods(self, user_profile: LearningPathCreate) -> List[Dict[str, Any]]:
        """Match study methods to user profile using Kimi API and knowledge base"""
        # Get AI recommendations
        recommendations = await self.kimi_api.generate_method_match(user_profile.dict())
        
        # Map recommendations to actual methods in knowledge base
        matched_methods = []
        for rec in recommendations:
            # Search knowledge base for methods matching the recommendation
            query = f"{rec['method_type']} {rec.get('reasoning', '')}"
            similar_methods = self.knowledge_base.search_methods(query, k=2)
            
            if similar_methods:
                method_data = similar_methods[0]['method']
                matched_methods.append({
                    "method": method_data,
                    "reasoning": rec.get('reasoning', ''),
                    "priority": rec.get('priority', 3),
                    "time_allocation": rec.get('time_allocation', '30分钟')
                })
        
        return matched_methods
