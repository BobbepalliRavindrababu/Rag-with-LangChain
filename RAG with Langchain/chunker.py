"""
Text Chunker - Splits documents into meaningful chunks
"""
import re
from typing import List, Tuple
import nltk


class TextChunker:
    """Splits text into chunks with overlap for better context"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target size of each chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Download nltk data if needed
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            print("Downloading NLTK punkt_tab tokenizer...")
            nltk.download('punkt_tab', quiet=True)
        
        # Fallback for older punkt
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    
    def chunk_text(self, text: str, source_name: str = "document") -> List[dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            source_name: Name of the source document
            
        Returns:
            List of chunk dictionaries with metadata
        """
        # Clean the text
        text = self._clean_text(text)
        
        # Split into sentences for better boundaries
        sentences = nltk.sent_tokenize(text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_id = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'source': source_name,
                    'char_count': len(chunk_text)
                })
                
                # Start new chunk with overlap
                overlap_text = chunk_text[-self.overlap:] if len(chunk_text) > self.overlap else chunk_text
                current_chunk = [overlap_text, sentence]
                current_length = len(overlap_text) + sentence_length
                chunk_id += 1
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'source': source_name,
                'char_count': len(chunk_text)
            })
        
        return chunks
    
    def chunk_documents(self, documents: dict) -> List[dict]:
        """
        Chunk multiple documents
        
        Args:
            documents: Dictionary mapping document names to their content
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        global_chunk_id = 0
        
        for doc_name, content in documents.items():
            doc_chunks = self.chunk_text(content, doc_name)
            
            # Update chunk IDs to be globally unique
            for chunk in doc_chunks:
                chunk['id'] = global_chunk_id
                global_chunk_id += 1
            
            all_chunks.extend(doc_chunks)
            print(f"  → {doc_name}: {len(doc_chunks)} chunks")
        
        return all_chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', '', text)
        return text.strip()
    
    def get_chunk_context(self, chunks: List[dict], chunk_id: int, context_window: int = 1) -> str:
        """
        Get a chunk with surrounding context
        
        Args:
            chunks: List of all chunks
            chunk_id: ID of the target chunk
            context_window: Number of chunks before and after to include
            
        Returns:
            Chunk text with context
        """
        chunk_dict = {c['id']: c for c in chunks}
        
        if chunk_id not in chunk_dict:
            return ""
        
        context_chunks = []
        for i in range(max(0, chunk_id - context_window), 
                      min(len(chunks), chunk_id + context_window + 1)):
            if i in chunk_dict:
                context_chunks.append(chunk_dict[i]['text'])
        
        return ' '.join(context_chunks)


if __name__ == "__main__":
    # Test the chunker
    chunker = TextChunker(chunk_size=200, overlap=50)
    
    sample_text = """
    Artificial intelligence is transforming the world. Machine learning algorithms 
    can now recognize patterns in data. Natural language processing enables computers 
    to understand human language. Deep learning has achieved remarkable results in 
    image recognition and speech synthesis.
    """
    
    chunks = chunker.chunk_text(sample_text, "test_doc")
    print(f"Created {len(chunks)} chunks")
    for chunk in chunks:
        print(f"Chunk {chunk['id']}: {chunk['text'][:100]}...")
