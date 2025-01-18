from typing import List, Dict, Any, Optional, Union
import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field, validator

class StudyMethod(BaseModel):
    id: str = Field(..., description="Unique identifier for the study method")
    category: str = Field(..., description="Category of the study method (e.g., 基本概念, 性质与关系)")
    title: str = Field(..., description="Title of the study method")
    description: str = Field(..., description="Detailed description of the study method")
    steps: List[str] = Field(..., description="Step-by-step instructions for applying the method")
    suitable_topics: List[str] = Field(..., description="Topics where this method is most effective")
    difficulty_level: str = Field(..., description="Difficulty level (基础, 提高, 挑战)")
    time_required: str = Field(..., description="Estimated time required to apply this method")
    prerequisites: List[str] = Field(default=[], description="Required prior knowledge")
    learning_outcomes: List[str] = Field(..., description="Expected learning outcomes")

    @validator('category')
    def validate_category(cls, v):
        valid_categories = {
            "基本概念", "性质与关系", "基本运算", "应用", "阅读与思考",
            "信息技术应用", "探究与发现", "数学建模", "文献阅读与数学写作",
            "考试技巧"
        }
        if v not in valid_categories:
            raise ValueError(f"Category must be one of: {valid_categories}")
        return v

    @validator('difficulty_level')
    def validate_difficulty_level(cls, v):
        valid_levels = {"基础", "提高", "挑战"}
        if v not in valid_levels:
            raise ValueError(f"Difficulty level must be one of: {valid_levels}")
        return v

class KnowledgeBase:
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize knowledge base with sentence transformer model"""
        self.model = SentenceTransformer(embedding_model)
        self.dimension: int = 384  # Default dimension for MiniLM-L6-v2
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(self.dimension)
        self.methods: List[StudyMethod] = []
        self.method_embeddings: np.ndarray | None = None
        
    def load_methods(self, file_path: str) -> None:
        """Load study methods from a JSON file and initialize FAISS index"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Study methods file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.methods = [StudyMethod(**method) for method in data]
            
        # Create embeddings for all methods
        texts = [
            f"{m.title} {m.description} {' '.join(m.steps)} {' '.join(m.suitable_topics)}"
            for m in self.methods
        ]
        self.method_embeddings = self.model.encode(texts)
        
        # Initialize FAISS index for cosine similarity
        self.dimension = self.method_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        vectors = self.method_embeddings.astype(np.float32)
        faiss.normalize_L2(vectors)  # Normalize vectors for cosine similarity
        self.index.add(vectors)
        
    def save_methods(self, file_path: str) -> None:
        """Save study methods to a JSON file"""
        data = [method.dict() for method in self.methods]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def search_methods(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant study methods using FAISS with cosine similarity"""
        if self.index is None or not self.methods:
            return []
            
        # Encode and normalize query
        query_embedding = self.model.encode([query]).astype(np.float32)
        faiss.normalize_L2(query_embedding)
        
        # Search using inner product (cosine similarity since vectors are normalized)
        D, I = self.index.search(query_embedding, k)
        
        results = []
        for similarity, idx in zip(D[0], I[0]):
            if idx < len(self.methods) and idx >= 0:
                method = self.methods[idx]
                results.append({
                    "method": method.dict(),
                    "similarity_score": float(similarity)  # Already normalized
                })
        
        return sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    
    def add_method(self, method: StudyMethod) -> None:
        """Add a new study method to the knowledge base"""
        self.methods.append(method)
        text = f"{method.title} {method.description} {' '.join(method.steps)} {' '.join(method.suitable_topics)}"
        embedding = self.model.encode([text]).astype(np.float32)
        
        if self.method_embeddings is None:
            self.method_embeddings = embedding
        else:
            self.method_embeddings = np.vstack([self.method_embeddings, embedding])
            
        # Reset index and add all vectors
        self.index.reset()
        vectors = self.method_embeddings.reshape(-1, self.dimension)
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        
    def get_method_by_id(self, method_id: str) -> StudyMethod:
        """Retrieve a study method by its ID"""
        for method in self.methods:
            if method.id == method_id:
                return method
        raise ValueError(f"Study method not found with ID: {method_id}")
