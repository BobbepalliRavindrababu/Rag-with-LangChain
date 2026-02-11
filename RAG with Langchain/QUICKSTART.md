# Quick Start Guide

## RAG Document Q&A System (No LLM)

### Overview
This system performs **Retrieval-Augmented Generation** without using generative AI:
- **Retrieval**: Vector similarity search using sentence transformers
- **Generation**: Extractive answer construction from retrieved chunks

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download NLTK data (automatic on first run):**
The system will automatically download required NLTK data when needed.

### Usage

#### Option 1: Interactive Mode
```bash
python main.py
```

Then choose:
- `sample` - Use built-in sample documents
- Enter paths to your own PDF/TXT files
- Type `done` when finished

#### Option 2: Command Line with Files
```bash
python main.py document1.pdf document2.txt
```

#### Option 3: Programmatic Use
```python
from main import RAGSystem

# Initialize system
rag = RAGSystem()

# Load documents
rag.load_documents(['document.pdf', 'notes.txt'])

# Ask questions
answer = rag.ask("What is machine learning?")

# Interactive mode
rag.interactive_mode()
```

### Interactive Commands

Once documents are loaded:
- Type any question to get an answer
- `stats` - Show system statistics
- `help` - Show available commands
- `quit` or `exit` - Exit the program

### Example Session

```
💬 Your question: What is machine learning?

🔍 Searching for relevant information...
✓ Found 3 relevant chunk(s)

💡 Generating answer...

📝 Answer:
------------------------------------------------------------
Machine Learning is a subset of AI that enables computers to 
learn from data without being explicitly programmed. ML algorithms 
build mathematical models based on sample data, known as training 
data, to make predictions or decisions.
------------------------------------------------------------

📊 Confidence: 87%
🔍 Method: definition_extraction
📚 Sources: ai_overview.txt
📄 Chunks: 5, 12, 18
```

### How It Works

1. **Document Processing**: PDF/TXT files are parsed and text is extracted
2. **Chunking**: Documents are split into overlapping chunks (~500 chars)
3. **Embedding**: Each chunk is converted to a 384-dimensional vector using sentence transformers
4. **Indexing**: Vectors are stored in a FAISS index for fast similarity search
5. **Retrieval**: When you ask a question, it finds the most similar chunks
6. **Answer Generation**: Uses extractive methods to construct an answer:
   - Definition queries → Extract relevant defining sentence
   - Factual queries → Extract fact-containing sentence using TF-IDF
   - General queries → Combine multiple relevant chunks

### Supported File Formats
- PDF (`.pdf`)
- Plain Text (`.txt`)

### Configuration

You can customize the system by modifying initialization parameters:

```python
# Adjust chunk size and overlap
chunker = TextChunker(chunk_size=500, overlap=100)

# Use different embedding model
vector_store = VectorStore(model_name='all-MiniLM-L6-v2')

# Change retrieval parameters
results = retriever.retrieve(query, top_k=5, min_score=0.3)
```

### Saving and Loading Index

```python
# Save index for reuse
rag.save_index('my_index')

# Load previously saved index
rag.load_index('my_index')
```

### Testing

Run the test suite:
```bash
python test_rag_system.py
```

### Advantages of This Approach

✅ **No Hallucinations**: Answers come directly from your documents
✅ **Transparent**: Shows sources and confidence scores
✅ **Fast**: Local processing, no API calls
✅ **Privacy**: All processing happens on your machine
✅ **Cost-Free**: No LLM API costs
✅ **Verifiable**: Can trace back to source documents

### Limitations

⚠️ **No Synthesis**: Cannot combine information creatively
⚠️ **Limited Reasoning**: Cannot infer or deduce
⚠️ **Dependent on Content**: Can only answer from available text
⚠️ **Extractive Only**: Cannot rephrase or simplify

### Troubleshooting

**Issue**: Model download fails
- **Solution**: Check internet connection, the model downloads automatically on first run

**Issue**: Out of memory
- **Solution**: Reduce chunk size or process fewer documents at once

**Issue**: Poor answer quality
- **Solution**: Try adjusting chunk_size, overlap, or top_k parameters

### Next Steps

- Add more documents to improve coverage
- Experiment with different embedding models
- Adjust chunk sizes for your specific documents
- Integrate with a UI (Streamlit, Gradio, etc.)
