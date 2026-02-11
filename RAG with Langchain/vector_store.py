"""
Vector Store - Handles embedding generation and FAISS indexing
"""
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pickle
import os


class VectorStore:
    """Manages document embeddings and vector similarity search"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize vector store with sentence transformer model
        
        Args:
            model_name: Name of the sentence transformer model
                       'all-MiniLM-L6-v2' is fast and efficient (384 dimensions)
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = []
        print(f"✓ Model loaded (dimension: {self.dimension})")
    
    def add_chunks(self, chunks: List[dict]):
        """
        Add chunks to the vector store
        
        Args:
            chunks: List of chunk dictionaries with 'text' and metadata
        """
        if not chunks:
            print("No chunks to add")
            return
        
        print(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Store chunks
        self.chunks = chunks
        
        # Extract text and generate embeddings
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index using Inner Product (for normalized vectors, this is cosine similarity)
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        print(f"  → Created IndexFlatIP for cosine similarity")
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"✓ Added {len(chunks)} chunks to vector store")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """
        Search for most similar chunks to a query
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of tuples (chunk, similarity_score)
        """
        if self.index is None or len(self.chunks) == 0:
            print("Vector store is empty. Please add chunks first.")
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        top_k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # For IndexFlatIP with normalized vectors, scores are cosine similarities (range -1 to 1)
        # No conversion needed - higher scores mean more similar
        
        # Prepare results
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], float(score)))
        
        return results
    
    def save(self, path: str = 'vector_store.pkl'):
        """Save the vector store to disk"""
        if self.index is None:
            print("Nothing to save - vector store is empty")
            return
        
        data = {
            'chunks': self.chunks,
            'dimension': self.dimension
        }
        
        # Save metadata
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        # Save FAISS index
        faiss.write_index(self.index, path.replace('.pkl', '.index'))
        
        print(f"✓ Vector store saved to {path}")
    
    def load(self, path: str = 'vector_store.pkl'):
        """Load the vector store from disk"""
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return False
        
        # Load metadata
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.chunks = data['chunks']
        self.dimension = data['dimension']
        
        # Load FAISS index
        index_path = path.replace('.pkl', '.index')
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            print(f"✓ Vector store loaded from {path}")
            print(f"  → {len(self.chunks)} chunks indexed")
            return True
        else:
            print(f"Index file not found: {index_path}")
            return False
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store"""
        if self.index is None:
            return {'chunks': 0, 'dimension': self.dimension}
        
        sources = set(chunk['source'] for chunk in self.chunks)
        
        return {
            'total_chunks': len(self.chunks),
            'dimension': self.dimension,
            'sources': list(sources),
            'source_count': len(sources)
        }


if __name__ == "__main__":
    # Test the vector store
    store = VectorStore()
    
    # Sample chunks
    test_chunks = [
        {'id': 0, 'text': 'Machine learning is a subset of artificial intelligence.', 'source': 'test.txt'},
        {'id': 1, 'text': 'Deep learning uses neural networks with multiple layers.', 'source': 'test.txt'},
        {'id': 2, 'text': 'Natural language processing helps computers understand text.', 'source': 'test.txt'},
    ]
    
    store.add_chunks(test_chunks)
    
    # Test search
    results = store.search("What is neural networks?", top_k=2)
    print("\nSearch results:")
    for chunk, score in results:
        print(f"  Score: {score:.3f} - {chunk['text'][:60]}...")
