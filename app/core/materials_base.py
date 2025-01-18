from typing import List, Dict, Any, Optional
import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field, validator

class StudyMaterial(BaseModel):
    id: str = Field(..., description="Unique identifier for the study material")
    category: str = Field(..., description="Category of the study material (e.g., 基本概念, 性质与关系)")
    title: str = Field(..., description="Title of the study material")
    description: str = Field(..., description="Detailed description of the material")
    content: str = Field(..., description="Main content of the study material")
    type: str = Field(..., description="Type of material (e.g., 教材, 练习题, 探究活动)")
    difficulty_level: str = Field(..., description="Difficulty level (基础, 提高, 挑战)")
    estimated_time: str = Field(..., description="Estimated time to complete")
    prerequisites: List[str] = Field(default=[], description="Required prior knowledge")
    related_methods: List[str] = Field(..., description="IDs of related study methods")
    learning_outcomes: List[str] = Field(..., description="Expected learning outcomes")

    @validator('category')
    def validate_category(cls, v):
        valid_categories = {
            "基本概念", "性质与关系", "基本运算", "应用", "阅读与思考",
            "信息技术应用", "探究与发现", "数学建模", "文献阅读与数学写作"
        }
        if v not in valid_categories:
            raise ValueError(f"Category must be one of: {valid_categories}")
        return v

    @validator('type')
    def validate_type(cls, v):
        valid_types = {"教材", "练习题", "探究活动", "阅读材料", "技术应用", "建模案例"}
        if v not in valid_types:
            raise ValueError(f"Type must be one of: {valid_types}")
        return v

    @validator('difficulty_level')
    def validate_difficulty_level(cls, v):
        valid_levels = {"基础", "提高", "挑战"}
        if v not in valid_levels:
            raise ValueError(f"Difficulty level must be one of: {valid_levels}")
        return v

class MaterialsBase:
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize materials base with sentence transformer model"""
        self.model = SentenceTransformer(embedding_model)
        self.dimension: int = 384  # Default dimension for MiniLM-L6-v2
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(self.dimension)
        self.materials: List[StudyMaterial] = []
        self.material_embeddings: np.ndarray | None = None

    def load_materials(self, file_path: str) -> None:
        """Load study materials from a JSON file and initialize FAISS index"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Study materials file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.materials = [StudyMaterial(**material) for material in data.get("study_materials", [])]
            
        # Create embeddings for all materials
        texts = [
            f"{m.title} {m.description} {m.content}"
            for m in self.materials
        ]
        
        if texts:
            # Create embeddings and normalize for cosine similarity
            self.material_embeddings = self.model.encode(texts).astype(np.float32)
            vectors = self.material_embeddings.copy()
            faiss.normalize_L2(vectors)
            self.index.add(vectors)

    def save_materials(self, file_path: str) -> None:
        """Save study materials to a JSON file"""
        data = {"study_materials": [material.dict() for material in self.materials]}
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def search_materials(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant study materials using FAISS with cosine similarity"""
        if not self.materials:
            return []
            
        # Encode and normalize query
        query_embedding = self.model.encode([query]).astype(np.float32)
        faiss.normalize_L2(query_embedding)
        
        # Search using inner product (cosine similarity since vectors are normalized)
        similarities, indices = self.index.search(query_embedding, min(k, len(self.materials)))
        
        results = []
        for similarity, idx in zip(similarities[0], indices[0]):
            if idx < len(self.materials) and idx >= 0:
                material = self.materials[idx]
                results.append({
                    "material": material.dict(),
                    "similarity_score": float(similarity)
                })
        
        return sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    def add_material(self, material: StudyMaterial) -> None:
        """Add a new study material to the knowledge base"""
        self.materials.append(material)
        text = f"{material.title} {material.description} {material.content}"
        embedding = self.model.encode([text]).astype(np.float32)
        
        if self.material_embeddings is None:
            self.material_embeddings = embedding
        else:
            self.material_embeddings = np.vstack([self.material_embeddings, embedding])
            
        # Reset index and add all vectors
        # Reset index and add normalized vectors
        self.index.reset()
        vectors = self.material_embeddings.copy()
        faiss.normalize_L2(vectors)
        self.index.add(vectors)

    def get_material_by_id(self, material_id: str) -> StudyMaterial:
        """Retrieve a study material by its ID"""
        for material in self.materials:
            if material.id == material_id:
                return material
        raise ValueError(f"Study material not found with ID: {material_id}")

    def get_materials_by_method(self, method_id: str) -> List[StudyMaterial]:
        """Get all materials related to a specific study method"""
        return [
            material for material in self.materials
            if method_id in material.related_methods
        ]
