"""
Knowledge base implementation for study materials using vector embeddings for semantic search.
"""
from typing import List, Dict, Optional
import json
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import faiss
from app.core.config import EMBEDDING_MODEL, BATCH_SIZE

class StudyMaterialKnowledgeBase:
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the knowledge base with a sentence transformer model."""
        self.model_name = model_name or EMBEDDING_MODEL
        self.model = None  # Lazy load
        self.index = None
        self.materials = []
        self.material_map = {}
        
    def _ensure_initialized(self):
        """Ensure model is initialized."""
        import psutil
        import gc
        
        def log_memory():
            mem = psutil.Process().memory_info()
            return f"Memory usage: RSS={mem.rss/1024/1024:.1f}MB, VMS={mem.vms/1024/1024:.1f}MB"
            
        print(f"Before model initialization: {log_memory()}")
        gc.collect()  # Force garbage collection before loading
        
        if self.model is None:
            print(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"After model loading: {log_memory()}")
            
        gc.collect()  # Clean up any temporary objects
        print(f"Final memory state: {log_memory()}")
        
    def _create_material_text(self, material: Dict) -> str:
        """Create a searchable text representation of a study material."""
        text_parts = [
            material['title'],
            material['description'],
            material['subject'],
            material['difficulty_level'],
            material['type'],
            ' '.join(material.get('tags', []))
        ]
        
        # Add metadata if available
        if material.get('metadata'):
            if 'key_concepts' in material['metadata']:
                text_parts.append(' '.join(material['metadata']['key_concepts']))
            if 'recommended_practice' in material['metadata']:
                text_parts.append(material['metadata']['recommended_practice'])
        
        return ' '.join(filter(None, text_parts))
    
    def build_index(self, materials_file: str = "data/study_materials/sample_materials.json"):
        """Build the FAISS index from study materials."""
        self._ensure_initialized()
        print("Building materials knowledge base index...")
        # Load study materials
        with open(materials_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.materials = data['materials']  # Access the materials array
        
        # Create text representations
        texts = [self._create_material_text(material) for material in self.materials]
        
        # Generate embeddings in batches
        batch_size = BATCH_SIZE
        embeddings_list = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            with torch.no_grad():
                self._ensure_initialized()  # Ensure model is initialized before each batch
                embeddings = self.model.encode(
                    batch,
                    convert_to_tensor=True,
                    show_progress_bar=False
                )
                embeddings_list.append(embeddings.cpu().numpy())
        
        embeddings_np = np.vstack(embeddings_list)
        
        # Build FAISS index
        dimension = embeddings_np.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_np)
        
        # Create material mapping
        self.material_map = {i: material for i, material in enumerate(self.materials)}
        
        return len(self.materials)
    
    def search(self, query: str, filters: Optional[Dict] = None, k: int = 3) -> List[Dict]:
        """
        Search for study materials using semantic similarity and optional filters.
        
        Args:
            query: Search query (can be learning path description, topic, etc.)
            filters: Optional filters (subject, difficulty_level, etc.)
            k: Number of results to return
            
        Returns:
            List of matching study materials
        """
        self._ensure_initialized()
        if not self.index:
            raise ValueError("Knowledge base index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        # Search index
        distances, indices = self.index.search(query_embedding, k * 3)  # Get more results for filtering
        
        # Apply filters and return matched materials
        results = []
        for i, idx in enumerate(indices[0]):
            # Skip invalid indices
            if idx < 0:
                continue
                
            material = self.material_map[idx].copy()
            
            # Apply filters if provided
            if filters:
                if not self._matches_filters(material, filters):
                    continue
            
            material['similarity_score'] = float(1 / (1 + distances[0][i]))
            results.append(material)
            
            if len(results) >= k:
                break
        
        # If no results found after filtering, try without filters
        if not results and filters:
            print(f"\nNo results found with filters {filters}. Showing unfiltered results:")
            return self.search(query, filters=None, k=k)
        
        return results[:k]
    
    def _matches_filters(self, material: Dict, filters: Dict) -> bool:
        """Check if material matches the given filters with flexible matching."""
        difficulty_levels = {'入门': 0, '中等': 1, '高级': 2}
        
        for key, value in filters.items():
            if key == 'subject':
                # Allow partial subject matches
                material_subject = material.get('subject', '').lower()
                filter_subject = value.lower()
                if not (material_subject in filter_subject or filter_subject in material_subject):
                    return False
                    
            elif key == 'difficulty_level':
                material_level = material.get('difficulty_level', '中等')
                filter_level = value
                
                material_value = difficulty_levels.get(material_level, 1)
                filter_value = difficulty_levels.get(filter_level, 1)
                
                # For entry level, only allow entry level materials
                if filter_value == 0 and material_value > 0:
                    return False
                # For intermediate level, allow entry and intermediate
                elif filter_value == 1 and material_value > 1:
                    return False
                # For advanced level, allow all levels but prefer matching
                
            elif key == 'type':
                # Type is a soft filter
                pass
                
            elif key == 'max_time':
                material_time = self._parse_time_to_minutes(material.get('estimated_time', '0分钟'))
                # Allow slightly longer materials (up to 50% more)
                if material_time > value * 1.5:
                    return False
                    
        return True
    
    def _parse_time_to_minutes(self, time_str: str) -> int:
        """Convert time string to minutes, handling ranges by taking the maximum."""
        # Handle ranges (e.g., "1-2小时")
        if '-' in time_str:
            time_str = time_str.split('-')[1]  # Take the maximum time
            
        if '小时' in time_str:
            # Extract numeric value, handling decimals
            hours = float(''.join(c for c in time_str.replace('小时', '') if c.isdigit() or c == '.'))
            return int(hours * 60)
        elif '分钟' in time_str:
            # Extract numeric value
            return int(''.join(c for c in time_str.replace('分钟', '') if c.isdigit()))
        return 0
    
    def add_material(self, material: Dict) -> bool:
        """Add a new study material to the knowledge base."""
        self._ensure_initialized()
        if not self.index:
            raise ValueError("Knowledge base index not built. Call build_index() first.")
        
        # Generate embedding for new material
        text = self._create_material_text(material)
        embedding = self.model.encode([text])
        
        # Add to index
        self.index.add(embedding)
        
        # Update material map
        next_idx = len(self.materials)
        self.material_map[next_idx] = material
        self.materials.append(material)
        
        return True
    
    def save(self, directory: str = "data/knowledge_base"):
        """Save the knowledge base to disk."""
        save_dir = Path(directory)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save materials
        with open(save_dir / "materials.json", 'w', encoding='utf-8') as f:
            json.dump(self.materials, f, ensure_ascii=False, indent=2)
        
        # Save FAISS index
        faiss.write_index(self.index, str(save_dir / "materials.index"))
    
    @classmethod
    def load(cls, directory: str = "data/knowledge_base") -> 'StudyMaterialKnowledgeBase':
        """Load a knowledge base from disk."""
        load_dir = Path(directory)
        kb = cls()
        
        # Load materials
        with open(load_dir / "materials.json", 'r', encoding='utf-8') as f:
            kb.materials = json.load(f)
        kb.material_map = {i: material for i, material in enumerate(kb.materials)}
        
        # Load FAISS index
        kb.index = faiss.read_index(str(load_dir / "materials.index"))
        
        return kb
