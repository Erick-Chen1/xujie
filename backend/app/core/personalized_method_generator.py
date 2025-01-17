"""
AI model for generating personalized study methods based on user information.
"""
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.knowledge_base import StudyMethodKnowledgeBase
from app.core.config import settings

class PersonalizedMethodGenerator:
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the personalized method generator."""
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None  # Lazy load the model
        self.knowledge_base = None  # Lazy load the knowledge base
        
    def _ensure_initialized(self):
        """
        Ensure model and knowledge base are initialized.
        
        Raises:
            RuntimeError: If initialization of model or knowledge base fails
        """
        try:
            if self.model is None:
                self.model = SentenceTransformer(self.model_name)
            if self.knowledge_base is None:
                self.knowledge_base = StudyMethodKnowledgeBase()
                self.knowledge_base.build_index()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize components: {str(e)}")
    
    def _create_user_profile_embedding(self, user_info: Dict) -> np.ndarray:
        """
        Create a searchable embedding from user information.
        
        Args:
            user_info: Dictionary containing user profile information
            
        Returns:
            np.ndarray: Embedding vector for the user profile
            
        Raises:
            RuntimeError: If model is not initialized or encoding fails
        """
        self._ensure_initialized()
        if self.model is None:
            raise RuntimeError("Model not initialized")
            
        try:
            profile_text = self._format_user_profile(user_info)
            return self.model.encode([profile_text])[0]
        except Exception as e:
            raise RuntimeError(f"Failed to create profile embedding: {str(e)}")
    
    def _format_user_profile(self, user_info: Dict) -> str:
        """Format user information into a searchable text."""
        profile_parts = [
            f"学习目标: {user_info.get('learning_goals', '')}",
            f"学习风格: {user_info.get('learning_style', '')}",
            f"学习时间: {user_info.get('available_time', '')}",
            f"学习偏好: {user_info.get('preferences', '')}",
            f"学习难度: {user_info.get('difficulty_level', '')}",
            f"学科: {user_info.get('subjects', '')}"
        ]
        return " ".join(filter(None, profile_parts))
    
    def _validate_user_profile(self, user_info: Dict) -> None:
        """Validate user profile data."""
        required_fields = ['learning_goals', 'learning_style', 'available_time', 
                         'difficulty_level', 'subjects']
        
        # Check required fields
        missing_fields = [field for field in required_fields if not user_info.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields in user profile: {', '.join(missing_fields)}")
            
        # Validate difficulty level
        valid_levels = {'入门', '中等', '高级'}
        if user_info['difficulty_level'] not in valid_levels:
            raise ValueError(f"Invalid difficulty level. Must be one of: {', '.join(valid_levels)}")
            
        # Validate learning style
        valid_styles = {'视觉学习', '听觉学习', '动手实践'}
        if user_info['learning_style'] not in valid_styles:
            raise ValueError(f"Invalid learning style. Must be one of: {', '.join(valid_styles)}")
            
        # Basic time format validation
        time_str = user_info['available_time']
        valid_time_indicators = ['小时', '分钟', '每天', '充足时间', '有限', '周末']
        if not any(indicator in time_str for indicator in valid_time_indicators):
            raise ValueError("Invalid time format. Must include time indicators like '小时'/'分钟'/'每天'/'充足时间'/'周末'")

    def generate_personalized_methods(self, user_info: Dict, num_methods: int = 3) -> List[Dict]:
        """
        Generate personalized study methods based on user information.
        
        Args:
            user_info: Dictionary containing user information and preferences
            num_methods: Number of methods to generate
            
        Returns:
            List of personalized study methods with explanations
            
        Raises:
            ValueError: If user profile is invalid or missing required fields
            RuntimeError: If initialization fails
        """
        if not isinstance(user_info, dict):
            raise TypeError("user_info must be a dictionary")
        if not isinstance(num_methods, int) or num_methods < 1:
            raise ValueError("num_methods must be a positive integer")
            
        # Validate user profile
        self._validate_user_profile(user_info)
        
        try:
            # Initialize components
            self._ensure_initialized()
            if self.knowledge_base is None:
                raise RuntimeError("Failed to initialize knowledge base")
                
            # Generate profile and search for methods
            profile_text = self._format_user_profile(user_info)
            base_methods = self.knowledge_base.search(
                profile_text,
                k=num_methods * 2
            )
            
            # Handle case when no methods are found
            if not base_methods:
                print(f"No suitable methods found for profile: {profile_text}")
                return []
            
            # Personalize and combine methods
            personalized_methods = []
            for method in base_methods[:num_methods]:
                personalized_method = self._personalize_method(method, user_info)
                personalized_methods.append(personalized_method)
            
            return personalized_methods
        except Exception as e:
            raise RuntimeError(f"Failed to generate personalized methods: {str(e)}")
        
        # Personalize and combine methods
        personalized_methods = []
        for method in base_methods[:num_methods]:
            personalized_method = self._personalize_method(method, user_info)
            personalized_methods.append(personalized_method)
        
        return personalized_methods
    
    def _personalize_method(self, base_method: Dict, user_info: Dict) -> Dict:
        """Customize a study method based on user information."""
        personalized = base_method.copy()
        
        # Adjust time commitment based on user's available time
        available_time = user_info.get('available_time', '')
        if '有限' in available_time or '繁忙' in available_time:
            personalized['time_commitment'] = self._adjust_time_commitment(
                base_method['time_commitment'],
                factor=0.7
            )
        
        # Modify difficulty based on user's level
        user_level = user_info.get('difficulty_level', '')
        if user_level and user_level != base_method['difficulty_level']:
            personalized['description'] = self._adjust_difficulty_description(
                base_method['description'],
                user_level
            )
        
        # Add personalized recommendations
        personalized['recommendations'] = self._generate_recommendations(
            base_method,
            user_info
        )
        
        return personalized
    
    def _adjust_time_commitment(self, time_str: str, factor: float) -> str:
        """Adjust time commitment by a factor."""
        # Extract prefix if exists (e.g., "每个概念", "每次学习后")
        prefix = ""
        if '每个' in time_str:
            parts = time_str.split('每个')
            prefix = f"每个{parts[0]}" if parts[0] else "每个"
            time_str = parts[1]
        elif '每次' in time_str:
            parts = time_str.split('每次')
            prefix = f"每次{parts[0]}" if parts[0] else "每次"
            time_str = parts[1]
            
        # Handle range format (e.g., "30-60分钟")
        if '-' in time_str:
            try:
                start, end = time_str.split('-')
                if '分钟' in end:
                    end_num = int(end.replace('分钟', ''))
                    start_num = int(start)
                    adjusted_start = int(start_num * factor)
                    adjusted_end = int(end_num * factor)
                    return f"{prefix}{adjusted_start}-{adjusted_end}分钟"
                elif '小时' in end:
                    end_num = float(end.replace('小时', ''))
                    start_num = float(start)
                    adjusted_start = start_num * factor
                    adjusted_end = end_num * factor
                    return f"{prefix}{adjusted_start:.1f}-{adjusted_end:.1f}小时"
            except ValueError:
                return time_str
        
        # Handle single value format
        if '分钟' in time_str:
            try:
                minutes = int(time_str.replace('分钟', ''))
                return f"{prefix}{int(minutes * factor)}分钟"
            except ValueError:
                return time_str
        elif '小时' in time_str:
            try:
                hours = float(time_str.replace('小时', ''))
                return f"{prefix}{hours * factor:.1f}小时"
            except ValueError:
                return time_str
        
        return time_str
    
    def _adjust_difficulty_description(self, description: str, target_level: str) -> str:
        """Adjust method description based on target difficulty level."""
        if target_level == '入门':
            return f"{description}\n建议：可以从基础概念开始，循序渐进地掌握。"
        elif target_level == '中等':
            return f"{description}\n建议：在掌握基础后，可以尝试更复杂的应用。"
        elif target_level == '高级':
            return f"{description}\n建议：可以探索更深入的概念，尝试创新性的应用。"
        return description
    
    def _generate_recommendations(self, method: Dict, user_info: Dict) -> List[str]:
        """Generate personalized recommendations for applying the study method."""
        recommendations = []
        
        # Time management recommendations
        available_time = user_info.get('available_time', '')
        if '有限' in available_time:
            recommendations.append("建议将学习内容分成更小的单元，每次专注15-20分钟。")
        
        # Learning style recommendations
        learning_style = user_info.get('learning_style', '')
        if '视觉' in learning_style:
            recommendations.append("可以使用思维导图或图表来可视化学习内容。")
        elif '听觉' in learning_style:
            recommendations.append("可以录音学习内容，通过复述来加深理解。")
        
        # Subject-specific recommendations
        subjects = user_info.get('subjects', '')
        if '数学' in subjects:
            recommendations.append("建议多做练习题，通过实践来巩固概念。")
        elif '语言' in subjects:
            recommendations.append("建议多进行口语练习和写作练习。")
        
        return recommendations
