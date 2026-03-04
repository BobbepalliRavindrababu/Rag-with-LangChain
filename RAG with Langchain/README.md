# RAG-based Document Question Answering System (No LLM)

A Retrieval-Augmented Generation system that answers questions from uploaded documents using **vector similarity search** and **extractive answer construction** - no generative AI involved.

## Features

- 📄 **Multi-format support**: PDF, DOCX, TXT, CSV, JSON, Excel (XLSX/XLS), PowerPoint (PPTX), HTML, Markdown
- 🔍 Vector-based semantic search using sentence transformers
- 📝 Extractive answer generation (no LLM hallucinations)
- ⚡ Fast retrieval with FAISS indexing
- 🎯 Relevant chunk highlighting with similarity scores

## Supported Document Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Word | `.docx` | Microsoft Word documents |
| Text | `.txt` | Plain text files |
| CSV | `.csv` | Comma-separated values |
| JSON | `.json` | JSON data files |
| Excel | `.xlsx`, `.xls` | Microsoft Excel spreadsheets |
| PowerPoint | `.pptx` | Microsoft PowerPoint presentations |
| HTML | `.html`, `.htm` | Web pages |
| Markdown | `.md` | Markdown documents |

## How It Works

1. **Document Upload**: User uploads PDF or TXT files
2. **Chunking**: Documents are split into semantically meaningful chunks
3. **Embedding**: Chunks are converted to vector embeddings using sentence transformers
4. **Indexing**: Vectors are stored in FAISS for fast similarity search
5. **Question**: User asks a question
6. **Retrieval**: System finds most similar chunks via cosine similarity
7. **Answer Construction**: Extractive methods combine retrieved chunks into an answer

## System Flow Diagram

```mermaid
flowchart TD
    A([👤 User]) -->|Upload documents| B[DocumentProcessor]
    B --> C{File type?}
    C -->|.pdf| D[PyPDF2 extractor]
    C -->|.docx| E[python-docx extractor]
    C -->|.txt| F[Plain text reader]
    C -->|.csv / .json / .xlsx| G[Pandas / json parser]
    C -->|.html / .md / .pptx| H[BeautifulSoup / pptx parser]
    D & E & F & G & H --> I[Raw text content]

    I --> J[TextChunker\nchunk_size=500, overlap=100]
    J --> K[Overlapping text chunks]

    K --> L[VectorStore\nall-MiniLM-L6-v2]
    L --> M[Sentence embeddings\n384 dimensions]
    M --> N[(FAISS Index\ncosine similarity)]

    A -->|Ask a question| O[Query text]
    O --> P[Encode query embedding]
    P --> Q[Search FAISS Index\ntop-k nearest neighbours]
    N --> Q
    Q --> R[Retrieved chunks\nwith similarity scores]

    R --> S[AnswerGenerator]
    S --> T{Query type?}
    T -->|what is / define| U[Definition extraction\nTF-IDF sentence ranking]
    T -->|when / who / where| V[Factual extraction\nTF-IDF sentence ranking]
    T -->|general| W[Multi-chunk extraction\ncombine top chunks]
    U & V & W --> X[Answer + Confidence + Sources]

    X --> Y([💬 Display to User])
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Then:
1. Upload your documents (PDF, DOCX, TXT, CSV, JSON, Excel, PowerPoint, HTML, Markdown, etc.)
2. Ask questions
3. Get extractive answers from your documents

## Architecture

- `document_processor.py`: Multi-format document parsing (PDF, DOCX, CSV, JSON, Excel, PowerPoint, HTML, Markdown, TXT)
- `chunker.py`: Text chunking strategies
- `vector_store.py`: Embedding and FAISS indexing
- `retriever.py`: Similarity search
- `answer_generator.py`: Extractive answer construction
- `main.py`: CLI interface

## Example

```
> Upload document: research_paper.pdf
✓ Processed 45 chunks

> Question: What is the main conclusion?
📍 Answer (based on 3 relevant chunks):
The study concludes that... [extracted from document]

Confidence: 0.87
Sources: chunks 12, 23, 34
```
