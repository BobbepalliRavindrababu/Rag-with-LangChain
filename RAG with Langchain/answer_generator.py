"""
Answer Generator - Constructs answers from retrieved chunks (No LLM)
Uses extractive methods to generate answers without generative AI
"""
from typing import List, Dict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class AnswerGenerator:
    """Generates answers using extractive methods (no LLM)"""
    
    def __init__(self):
        """Initialize the answer generator"""
        self.max_answer_length = 500  # Maximum characters in answer
    
    def generate_answer(self, query: str, retrieved_chunks: List[dict]) -> dict:
        """
        Generate an answer from retrieved chunks using extractive methods
        
        Args:
            query: User's question
            retrieved_chunks: List of relevant chunks from retrieval
            
        Returns:
            Dictionary with answer, confidence, sources, and method
        """
        if not retrieved_chunks:
            return {
                'answer': "I couldn't find relevant information in the documents to answer this question.",
                'confidence': 0.0,
                'sources': [],
                'method': 'none'
            }
        
        # Choose generation strategy based on query type
        query_lower = query.lower()
        
        if self._is_definition_query(query_lower):
            return self._generate_definition_answer(query, retrieved_chunks)
        elif self._is_factual_query(query_lower):
            return self._generate_factual_answer(query, retrieved_chunks)
        else:
            return self._generate_general_answer(query, retrieved_chunks)
    
    def _is_definition_query(self, query: str) -> bool:
        """Check if query is asking for a definition"""
        definition_patterns = [
            r'\bwhat is\b', r'\bwhat are\b', r'\bdefine\b', 
            r'\bdefinition of\b', r'\bmeaning of\b'
        ]
        return any(re.search(pattern, query) for pattern in definition_patterns)
    
    def _is_factual_query(self, query: str) -> bool:
        """Check if query is asking for specific facts"""
        factual_patterns = [
            r'\bwhen\b', r'\bwhere\b', r'\bwho\b', r'\bhow many\b',
            r'\bhow much\b', r'\bwhich\b',
            r'\bphone\b', r'\bmobile\b', r'\bnumber\b', r'\bcontact\b',
            r'\bemail\b', r'\baddress\b', r'\blocat\b', r'\bname\b',
            r'\bobjective\b', r'\bgoal\b', r'\bskill\b', r'\bexperience\b'
        ]
        return any(re.search(pattern, query) for pattern in factual_patterns)
    
    def _generate_definition_answer(self, query: str, chunks: List[dict]) -> dict:
        """
        Generate answer for definition-type questions
        Extract the most relevant sentence that defines the concept
        """
        # Use the highest-scoring chunk
        best_chunk = chunks[0]
        text = best_chunk['text']
        
        # Extract key terms from query
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        stopwords = {'what', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'but'}
        query_words = query_words - stopwords
        
        print(f"[ANSWER DEBUG] Definition query: '{query}'")
        print(f"[ANSWER DEBUG] Keywords: {query_words}")
        
        # Find sentences containing key terms
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) >= 20]
        
        if not sentences:
            return self._generate_general_answer(query, chunks)
        
        print(f"[ANSWER DEBUG] Found {len(sentences)} sentences")
        
        # Use TF-IDF to find best matching sentence
        try:
            vectorizer = TfidfVectorizer()
            corpus = sentences + [query]
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            query_vec = tfidf_matrix[-1]
            sentence_vecs = tfidf_matrix[:-1]
            
            similarities = (sentence_vecs * query_vec.T).toarray().flatten()
            best_idx = np.argmax(similarities)
            
            print(f"[ANSWER DEBUG] Best similarity: {similarities[best_idx]:.3f}")
            print(f"[ANSWER DEBUG] Answer: {sentences[best_idx][:100]}")
            
            answer = sentences[best_idx]
        except Exception as e:
            print(f"[ANSWER DEBUG] TF-IDF failed: {e}, using keyword matching")
            # Fallback to keyword matching
            scored_sentences = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                score = sum(1 for word in query_words if word in sentence_lower)
                if score > 0:
                    scored_sentences.append((score, sentence.strip()))
            
            if scored_sentences:
                scored_sentences.sort(reverse=True, key=lambda x: x[0])
                answer = scored_sentences[0][1]
            else:
                # Fallback to first few sentences
                answer = '. '.join(sentences[:2]).strip()
        
        return {
            'answer': answer,
            'confidence': best_chunk['score'],
            'sources': [{'source': best_chunk['source'], 'chunk_id': best_chunk['chunk_id']}],
            'method': 'definition_extraction'
        }
    
    def _generate_factual_answer(self, query: str, chunks: List[dict]) -> dict:
        """
        Generate answer for factual questions
        Extract the most relevant fact-containing sentence or information
        """
        # Combine top chunks
        top_chunks = chunks[:3]  # Use top 3 chunks
        combined_text = ' '.join([c['text'] for c in top_chunks])
        
        # Extract query keywords - be more selective
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        # Remove common words
        stopwords = {'what', 'is', 'the', 'my', 'your', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        query_words = query_words - stopwords
        
        print(f"[ANSWER DEBUG] Query: '{query}'")
        print(f"[ANSWER DEBUG] Keywords: {query_words}")
        
        # Find the most relevant sentence
        sentences = [s.strip() for s in re.split(r'[.!?]+', combined_text) if len(s.strip()) > 10]
        
        if not sentences:
            return self._generate_general_answer(query, chunks)
        
        print(f"[ANSWER DEBUG] Found {len(sentences)} sentences")
        
        # Use TF-IDF for better matching
        try:
            vectorizer = TfidfVectorizer()
            corpus = sentences + [query]
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            # Calculate similarity between query and each sentence
            query_vec = tfidf_matrix[-1]
            sentence_vecs = tfidf_matrix[:-1]
            
            similarities = (sentence_vecs * query_vec.T).toarray().flatten()
            
            # Get top 3 sentences
            top_indices = np.argsort(similarities)[::-1][:3]
            
            print(f"[ANSWER DEBUG] Top 3 similarities: {similarities[top_indices]}")
            for idx in top_indices[:3]:
                print(f"  - [{similarities[idx]:.3f}] {sentences[idx][:100]}")
            
            # Use the best matching sentence
            best_idx = top_indices[0]
            answer = sentences[best_idx]
            
            # If similarity is very low, return multiple sentences for context
            if similarities[best_idx] < 0.1:
                print(f"[ANSWER DEBUG] Low similarity, returning multiple sentences")
                top_sentences = [sentences[i] for i in top_indices if similarities[i] > 0.05][:2]
                if len(top_sentences) > 1:
                    answer = '. '.join(top_sentences) + '.'
                    
        except Exception as e:
            print(f"[ANSWER DEBUG] TF-IDF failed: {e}, using first sentence")
            # Fallback to first sentence of best chunk
            answer = sentences[0]
        
        avg_confidence = np.mean([c['score'] for c in top_chunks])
        
        return {
            'answer': answer,
            'confidence': float(avg_confidence),
            'sources': [{'source': c['source'], 'chunk_id': c['chunk_id']} for c in top_chunks],
            'method': 'factual_extraction'
        }
    
    def _generate_general_answer(self, query: str, chunks: List[dict]) -> dict:
        """
        Generate answer for general questions
        Combine and summarize multiple chunks
        """
        # Take top chunks up to max length
        selected_chunks = []
        total_length = 0
        
        for chunk in chunks:
            chunk_text = chunk['text']
            if total_length + len(chunk_text) <= self.max_answer_length:
                selected_chunks.append(chunk)
                total_length += len(chunk_text)
            else:
                break
        
        if not selected_chunks:
            selected_chunks = [chunks[0]]
        
        # Combine chunks with ellipsis
        answer_parts = []
        for chunk in selected_chunks:
            text = chunk['text'].strip()
            # Truncate if needed
            if len(text) > 200:
                # Try to end at sentence boundary
                sentences = re.split(r'[.!?]+', text)
                truncated = '. '.join(sentences[:2]) + '.'
                answer_parts.append(truncated)
            else:
                answer_parts.append(text)
        
        answer = '\n\n'.join(answer_parts)
        
        # Calculate average confidence
        avg_confidence = np.mean([c['score'] for c in selected_chunks])
        
        return {
            'answer': answer,
            'confidence': float(avg_confidence),
            'sources': [{'source': c['source'], 'chunk_id': c['chunk_id']} for c in selected_chunks],
            'method': 'multi_chunk_extraction'
        }
    
    def format_answer(self, answer_dict: dict, show_sources: bool = True) -> str:
        """
        Format the answer for display
        
        Args:
            answer_dict: Answer dictionary from generate_answer
            show_sources: Whether to show source information
            
        Returns:
            Formatted answer string
        """
        lines = []
        lines.append("📝 Answer:")
        lines.append("-" * 60)
        lines.append(answer_dict['answer'])
        lines.append("-" * 60)
        
        if show_sources and answer_dict['sources']:
            lines.append(f"\n📊 Confidence: {answer_dict['confidence']:.2%}")
            lines.append(f"🔍 Method: {answer_dict['method']}")
            
            sources = answer_dict['sources']
            source_names = list(set(s['source'] for s in sources))
            chunk_ids = [s['chunk_id'] for s in sources]
            
            lines.append(f"📚 Sources: {', '.join(source_names)}")
            lines.append(f"📄 Chunks: {', '.join(map(str, chunk_ids))}")
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test the answer generator
    generator = AnswerGenerator()
    
    # Sample retrieved chunks
    test_chunks = [
        {
            'text': 'Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming.',
            'score': 0.85,
            'source': 'ai_basics.txt',
            'chunk_id': 5
        },
        {
            'text': 'Neural networks are computational models inspired by biological neurons in the brain.',
            'score': 0.72,
            'source': 'ai_basics.txt',
            'chunk_id': 12
        }
    ]
    
    # Test with a definition query
    query = "What is machine learning?"
    answer = generator.generate_answer(query, test_chunks)
    print(generator.format_answer(answer))
