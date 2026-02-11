"""
Retriever - Handles semantic search and chunk retrieval
"""
from typing import List, Tuple
from vector_store import VectorStore


class Retriever:
    """Retrieves relevant chunks for a given query"""
    
    def __init__(self, vector_store: VectorStore):
        """
        Initialize retriever with a vector store
        
        Args:
            vector_store: VectorStore instance with indexed chunks
        """
        self.vector_store = vector_store
        self.min_similarity = -1.0  # Accept all scores (cosine similarity ranges from -1 to 1)
    
    def retrieve(self, query: str, top_k: int = 5, min_score: float = None) -> List[dict]:
        """
        Retrieve most relevant chunks for a query
        
        Args:
            query: User's question
            top_k: Maximum number of chunks to retrieve
            min_score: Minimum similarity score (0-1). If None, uses self.min_similarity
            
        Returns:
            List of retrieved chunks with metadata
        """
        min_score = min_score if min_score is not None else self.min_similarity
        
        # Search vector store
        results = self.vector_store.search(query, top_k=top_k)
        
        # Debug logging
        print(f"\n[RETRIEVER DEBUG]")
        print(f"Query: '{query}'")
        print(f"Min score threshold: {min_score}")
        print(f"Raw results from vector store: {len(results)}")
        for i, (chunk, score) in enumerate(results, 1):
            print(f"  Result {i}: score={score:.4f}, source={chunk['source']}")
        
        # Filter by minimum similarity
        filtered_results = []
        for chunk, score in results:
            if score >= min_score:
                filtered_results.append({
                    'chunk': chunk,
                    'score': score,
                    'text': chunk['text'],
                    'source': chunk['source'],
                    'chunk_id': chunk['id']
                })
        
        print(f"Filtered results: {len(filtered_results)}")
        
        return filtered_results
    
    def retrieve_with_context(self, query: str, top_k: int = 3, 
                            context_window: int = 0) -> List[dict]:
        """
        Retrieve chunks with surrounding context
        
        Args:
            query: User's question
            top_k: Maximum number of chunks to retrieve
            context_window: Number of adjacent chunks to include (0 = no context)
            
        Returns:
            List of retrieved chunks with expanded context
        """
        results = self.retrieve(query, top_k=top_k)
        
        if context_window == 0:
            return results
        
        # Expand each result with context
        for result in results:
            chunk_id = result['chunk_id']
            
            # Get adjacent chunks
            context_chunks = []
            for delta in range(-context_window, context_window + 1):
                target_id = chunk_id + delta
                for chunk in self.vector_store.chunks:
                    if chunk['id'] == target_id and chunk['source'] == result['source']:
                        context_chunks.append(chunk['text'])
                        break
            
            result['text_with_context'] = ' '.join(context_chunks)
        
        return results
    
    def print_results(self, results: List[dict], show_scores: bool = True):
        """
        Pretty print retrieval results
        
        Args:
            results: List of retrieval results
            show_scores: Whether to show similarity scores
        """
        if not results:
            print("No relevant chunks found.")
            return
        
        print(f"\n📍 Found {len(results)} relevant chunk(s):\n")
        
        for i, result in enumerate(results, 1):
            score_str = f" (similarity: {result['score']:.3f})" if show_scores else ""
            print(f"{i}. [{result['source']}]{score_str}")
            print(f"   {result['text'][:200]}...")
            print()
    
    def get_best_match(self, query: str) -> dict:
        """
        Get the single best matching chunk
        
        Args:
            query: User's question
            
        Returns:
            Best matching chunk or None
        """
        results = self.retrieve(query, top_k=1)
        return results[0] if results else None


if __name__ == "__main__":
    # Test the retriever
    from vector_store import VectorStore
    
    # Create and populate vector store
    store = VectorStore()
    test_chunks = [
        {'id': 0, 'text': 'Python is a high-level programming language.', 'source': 'test.txt'},
        {'id': 1, 'text': 'Machine learning models learn from data.', 'source': 'test.txt'},
        {'id': 2, 'text': 'Neural networks are inspired by the human brain.', 'source': 'test.txt'},
    ]
    store.add_chunks(test_chunks)
    
    # Create retriever
    retriever = Retriever(store)
    
    # Test retrieval
    results = retriever.retrieve("How do ML models work?", top_k=2)
    retriever.print_results(results)
