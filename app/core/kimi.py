from typing import Dict, Any, List, Optional
import httpx
import json
import base64
import asyncio
from datetime import datetime, timedelta
from config import get_settings
from fastapi import HTTPException

class KimiAPIError(Exception):
    """Base exception for Kimi API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class KimiAuthenticationError(KimiAPIError):
    """Raised when there are authentication issues"""
    def __init__(self, message: str):
        super().__init__(message, status_code=401)

class KimiRateLimitError(KimiAPIError):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after

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
        self.rate_limit = {
            "requests": 0,
            "window_start": datetime.now(),
            "max_requests": 100,  # Requests per minute
            "window_size": 60     # Window size in seconds
        }
        
        # Validate API key format
        self._validate_api_key()

    def _validate_api_key(self):
        """Validate API key format (Base64)"""
        try:
            # Check if key is valid base64
            if not self.api_key:
                raise ValueError("API key is required")
            decoded = base64.b64decode(self.api_key)
            if len(decoded) < 32:  # Minimum key length
                raise ValueError("API key is too short")
        except Exception as e:
            raise KimiAuthenticationError(f"Invalid API key format: {str(e)}")

    async def _check_rate_limit(self):
        """Check and update rate limit"""
        now = datetime.now()
        window_size = timedelta(seconds=self.rate_limit["window_size"])
        
        # Reset window if needed
        if now - self.rate_limit["window_start"] > window_size:
            self.rate_limit["requests"] = 0
            self.rate_limit["window_start"] = now
            
        # Check limit
        if self.rate_limit["requests"] >= self.rate_limit["max_requests"]:
            retry_after = int((self.rate_limit["window_start"] + window_size - now).total_seconds())
            raise KimiRateLimitError(
                "Rate limit exceeded",
                retry_after=retry_after
            )
            
        self.rate_limit["requests"] += 1

    async def generate_method_match(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate method matches based on user profile using Kimi API"""
        try:
            await self._check_rate_limit()
            prompt = self._create_method_match_prompt(user_profile)
            
            async with httpx.AsyncClient() as client:
                try:
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
                        },
                        timeout=30.0  # 30 second timeout
                    )
                    
                    if response.status_code == 401:
                        raise KimiAuthenticationError("Invalid API key or authentication failed")
                    elif response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        raise KimiRateLimitError("Rate limit exceeded", retry_after=retry_after)
                    elif response.status_code != 200:
                        raise KimiAPIError(f"Kimi API error: {response.text}", status_code=response.status_code)
                        
                    result = response.json()
                    return self._parse_method_match_response(result)
                    
                except httpx.TimeoutError:
                    raise KimiAPIError("Request timed out", status_code=504)
                except httpx.RequestError as e:
                    raise KimiAPIError(f"Request failed: {str(e)}", status_code=502)
                    
        except KimiAPIError as e:
            # Convert to FastAPI HTTPException
            raise HTTPException(
                status_code=e.status_code,
                detail={"message": e.message, "retry_after": getattr(e, "retry_after", None)}
            )

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
