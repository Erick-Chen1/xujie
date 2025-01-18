from typing import Dict, Any, List
import httpx
import json
from config import get_settings

class KimiAPI:
    def __init__(self):
        """Initialize Kimi API client with configuration"""
        settings = get_settings()
        self.api_key = settings.KIMI_API_KEY
        self.base_url = "https://api.kimi.moonshot.cn/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_method_match(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate method matches based on user profile using Kimi API"""
        prompt = self._create_method_match_prompt(user_profile)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "messages": [
                        {"role": "system", "content": "You are an AI tutor specializing in Chinese high school mathematics education."},
                        {"role": "user", "content": prompt}
                    ],
                    "model": "moonshot-v1-8k",
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Kimi API error: {response.text}")
                
            result = response.json()
            return self._parse_method_match_response(result)

    def _create_method_match_prompt(self, user_profile: Dict[str, Any]) -> str:
        """Create prompt for method matching based on user profile"""
        return f"""Based on the following student profile, suggest appropriate study methods:

Subject: {user_profile.get('subject', '高中数学')}
Difficulty Level: {user_profile.get('difficulty_level', '中等')}
Learning Goals: {user_profile.get('learning_goals', '')}
Available Time: {user_profile.get('available_time', '')}
Learning Style: {user_profile.get('learning_style', '')}

Please analyze this profile and provide study method recommendations in the following JSON format:
{{
    "recommended_methods": [
        {{
            "method_type": "string",
            "reasoning": "string",
            "priority": "number (1-5)",
            "time_allocation": "string"
        }}
    ],
    "learning_style_analysis": "string",
    "time_management_suggestions": "string"
}}"""

    def _parse_method_match_response(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse and validate Kimi API response"""
        try:
            content = response['choices'][0]['message']['content']
            if isinstance(content, str):
                content = json.loads(content)
            
            # Extract and validate recommended methods
            methods = content.get('recommended_methods', [])
            if not isinstance(methods, list):
                raise ValueError("Invalid response format: recommended_methods must be a list")
                
            return methods
            
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to parse Kimi API response: {str(e)}")
