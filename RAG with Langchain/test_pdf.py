from retriever import Retriever
from vector_store import VectorStore
from document_processor import DocumentProcessor
from chunker import TextChunker
import os

# Find a PDF in sample_documents or workspace
pdf_files = []
for root, dirs, files in os.walk('sample_documents'):
    for file in files:
        if file.endswith('.pdf'):
            pdf_files.append(os.path.join(root, file))

if not pdf_files:
    # Check workspace root
    for file in os.listdir('.'):
        if file.endswith('.pdf'):
            pdf_files.append(file)

if pdf_files:
    print(f"Testing with PDF: {pdf_files[0]}\n")
    
    # Load and process PDF
    doc_proc = DocumentProcessor()
    text = doc_proc.load_document(pdf_files[0])
    
    print(f"Extracted text length: {len(text)} characters")
    print(f"First 500 chars:\n{text[:500]}\n")
    
    # Chunk it
    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_text(text, os.path.basename(pdf_files[0]))
    
    print(f"Created {len(chunks)} chunks\n")
    
    # Create vector store
    store = VectorStore()
    store.add_chunks(chunks)
    
    # Test retrieval with various queries
    retriever = Retriever(store)
    
    test_queries = [
        "what is this document about?",
        "tell me about this",
        "summary",
        "experience",
        "skills"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = retriever.retrieve(query, top_k=3)
        print(f"Retrieved: {len(results)} chunks")
        if results:
            print(f"Top score: {results[0]['score']:.4f}")
            print(f"Preview: {results[0]['text'][:100]}...")
        else:
            print("NO RESULTS!")
else:
    print("No PDF files found to test")
