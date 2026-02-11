from retriever import Retriever
from vector_store import VectorStore
from document_processor import DocumentProcessor
from chunker import TextChunker

# Load document
doc_proc = DocumentProcessor()
text = doc_proc.load_document('sample_documents/ticket_system_guide.txt')

# Chunk it
chunker = TextChunker(chunk_size=500, overlap=100)
chunks = chunker.chunk_text(text, 'ticket_system_guide.txt')

# Create vector store
store = VectorStore()
store.add_chunks(chunks)

# Test retrieval
retriever = Retriever(store)
query = "what is this document about?"
results = retriever.retrieve(query, top_k=5)

print(f"\nTotal chunks: {len(chunks)}")
print(f"Query: '{query}'")
print(f"Retrieved chunks: {len(results)}")
print(f"Min similarity threshold: {retriever.min_similarity}")

if results:
    print("\nScores:")
    for r in results:
        print(f"  Score: {r['score']:.4f} - {r['text'][:80]}...")
else:
    print("\nNo results passed the filter!")
    
# Now test with raw search (no filtering)
raw_results = store.search(query, top_k=5)
print(f"\nRaw search results (before filtering): {len(raw_results)}")
for chunk, score in raw_results:
    print(f"  Score: {score:.4f} - {chunk['text'][:80]}...")
