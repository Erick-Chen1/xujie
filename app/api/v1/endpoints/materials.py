from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from schemas.materials import Material, MaterialResponse
from core.materials_base import MaterialsBase
from core.knowledge_base import KnowledgeBase

router = APIRouter()

def get_materials_base():
    """Dependency to get MaterialsBase instance"""
    mb = MaterialsBase()
    mb.load_materials("data/study_materials/materials.json")
    return mb

def get_knowledge_base():
    """Dependency to get KnowledgeBase instance"""
    kb = KnowledgeBase()
    kb.load_methods("data/study_methods/methods.json")
    return kb

@router.get("/materials/{stage_id}", response_model=List[MaterialResponse])
async def get_materials(
    stage_id: str,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    materials_base: MaterialsBase = Depends(get_materials_base),
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
):
    """
    Retrieve learning materials for a specific learning stage
    
    Parameters:
    - stage_id: Learning stage identifier
    - category: Optional filter by category (e.g., 基本概念, 性质与关系)
    - difficulty: Optional filter by difficulty level
    
    Returns:
    List of materials with their associated study methods
    """
    try:
        # Map stage_id to appropriate categories
        stage_categories = {
            "knowledge_acquisition": ["基本概念", "性质与关系", "基本运算", "应用"],
            "practice_reinforcement": ["基本运算", "应用"],
            "pattern_identification": ["性质与关系", "应用"],
            "special_learning": ["阅读与思考", "信息技术应用", "探究与发现", "数学建模"]
        }
        
        if stage_id not in stage_categories:
            raise HTTPException(
                status_code=404,
                detail=f"Invalid stage_id: {stage_id}"
            )
            
        # Build search query based on filters
        search_categories = [category] if category else stage_categories[stage_id]
        query_parts = []
        
        for cat in search_categories:
            query = cat
            if difficulty:
                query += f" {difficulty}"
            query_parts.append(query)
            
        # Search materials for each category
        all_materials = []
        for query in query_parts:
            materials = materials_base.search_materials(query)
            for material in materials:
                # Get related study methods
                related_methods = []
                for method_id in material["material"]["related_methods"]:
                    try:
                        method = knowledge_base.get_method_by_id(method_id)
                        related_methods.append(method)
                    except ValueError:
                        continue
                        
                # Create response object
                response = MaterialResponse(
                    **material["material"],
                    similarity_score=material["similarity_score"],
                    stage_id=stage_id,
                    related_methods=related_methods
                )
                all_materials.append(response)
        
        # Sort by similarity score and remove duplicates
        seen_ids = set()
        unique_materials = []
        for material in sorted(all_materials, key=lambda x: x.similarity_score, reverse=True):
            if material.id not in seen_ids:
                seen_ids.add(material.id)
                unique_materials.append(material)
        
        return unique_materials
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve materials: {str(e)}"
        )
