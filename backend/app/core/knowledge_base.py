"""
Knowledge base implementation for study methods using vector embeddings for semantic search.
"""
from typing import List, Dict, Optional
import json
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import faiss
from app.core.config import settings

class StudyMethodKnowledgeBase:
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the knowledge base with a sentence transformer model."""
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None  # Lazy load
        self.index = None
        self.methods = []
        self.method_map = {}
        
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
    
    def _create_method_text(self, method: Dict) -> str:
        """Create a searchable text representation of a study method."""
        return f"{method['title']} {method['description']} {' '.join(method['tags'])} {' '.join(method['metadata'].get('best_for', []))}"
    
    def build_index(self, methods_file: str = "data/study_methods/sample_methods.json"):
        """Build the FAISS index from study methods."""
        self._ensure_initialized()
        print("Building knowledge base index...")
        # Load study methods
        with open(methods_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.methods = data['methods']  # Access the methods array
        
        # Create text representations
        texts = [self._create_method_text(method) for method in self.methods]
        
        # Generate embeddings in batches
        batch_size = settings.BATCH_SIZE
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
        
        # Create method mapping
        self.method_map = {i: method for i, method in enumerate(self.methods)}
        
        return len(self.methods)
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search for study methods using semantic similarity.
        
        Args:
            query: Search query (can be user preferences, learning style, etc.)
            k: Number of results to return
            
        Returns:
            List of matching study methods
        """
        self._ensure_initialized()
        if not self.index:
            raise ValueError("Knowledge base index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        # Search index
        distances, indices = self.index.search(query_embedding, k)
        
        # Return matched methods with scores
        results = []
        for i, idx in enumerate(indices[0]):
            # Skip invalid indices (no matches found)
            if idx < 0:
                continue
                
            method = self.method_map[idx].copy()
            method['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity score
            results.append(method)
        
        # If no valid results found, return empty list
        if not results:
            print(f"No matching methods found for query: {query}")
            return []
            
        return results
    
    def add_method(self, method: Dict) -> bool:
        """
        Add a new study method to the knowledge base.
        
        Args:
            method: Study method dictionary following the defined schema
            
        Returns:
            bool: True if successful
        """
        self._ensure_initialized()
        if not self.index:
            raise ValueError("Knowledge base index not built. Call build_index() first.")
        
        # Generate embedding for new method
        text = self._create_method_text(method)
        embedding = self.model.encode([text])
        
        # Add to index
        self.index.add(embedding)
        
        # Update method map
        next_idx = len(self.methods)
        self.method_map[next_idx] = method
        self.methods.append(method)
        
        return True
    
    def save(self, directory: str = "data/knowledge_base"):
        """Save the knowledge base to disk."""
        save_dir = Path(directory)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save methods
        with open(save_dir / "methods.json", 'w', encoding='utf-8') as f:
            json.dump(self.methods, f, ensure_ascii=False, indent=2)
        
        # Save FAISS index
        faiss.write_index(self.index, str(save_dir / "methods.index"))
    
    @classmethod
    def load(cls, directory: str = "data/knowledge_base") -> 'StudyMethodKnowledgeBase':
        """Load a knowledge base from disk."""
        load_dir = Path(directory)
        kb = cls()
        
        # Load methods
        with open(load_dir / "methods.json", 'r', encoding='utf-8') as f:
            kb.methods = json.load(f)
        kb.method_map = {i: method for i, method in enumerate(kb.methods)}
        
        # Load FAISS index
        kb.index = faiss.read_index(str(load_dir / "methods.index"))
        
        return kb
