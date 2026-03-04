"""
RAG Document Q&A System - Web UI
Streamlit application with file upload and question answering
"""
import re
import streamlit as st
import os
import tempfile
from document_processor import DocumentProcessor
from chunker import TextChunker
from vector_store import VectorStore
from retriever import Retriever
from answer_generator import AnswerGenerator


# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .answer-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .chunk-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ffa500;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'is_ready' not in st.session_state:
    st.session_state.is_ready = False
if 'uploaded_files_count' not in st.session_state:
    st.session_state.uploaded_files_count = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def initialize_rag_system():
    """Initialize RAG system components"""
    if st.session_state.rag_system is None:
        with st.spinner("🚀 Initializing RAG System..."):
            doc_processor = DocumentProcessor()
            chunker = TextChunker(chunk_size=500, overlap=100)
            vector_store = VectorStore()
            answer_generator = AnswerGenerator()
            
            st.session_state.rag_system = {
                'doc_processor': doc_processor,
                'chunker': chunker,
                'vector_store': vector_store,
                'retriever': None,
                'answer_generator': answer_generator
            }
            st.success("✅ System initialized!")


def process_uploaded_files(uploaded_files):
    """Process uploaded files and build vector store"""
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one document.")
        return False
    
    initialize_rag_system()
    
    # IMPORTANT: Create a fresh vector store for new documents
    rag = st.session_state.rag_system
    rag['vector_store'] = VectorStore()  # Fresh instance to avoid cached index
    
    # Save uploaded files to temporary directory
    temp_dir = tempfile.mkdtemp()
    file_paths = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Save files
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"📄 Processing {uploaded_file.name}...")
        
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
        
        progress_bar.progress((i + 1) / (len(uploaded_files) * 3))
    
    # Load documents
    status_text.text("📚 Loading documents...")
    documents = rag['doc_processor'].load_multiple_documents(file_paths)
    
    if not documents:
        st.error("❌ No documents could be loaded.")
        return False
    
    # Debug: Show document info
    st.info(f"📄 Loaded {len(documents)} document(s)")
    for doc_name, content in documents.items():
        st.write(f"  • **{doc_name}**: {len(content)} characters")
    
    progress_bar.progress(len(uploaded_files) * 2 / (len(uploaded_files) * 3))
    
    # Chunk documents
    status_text.text("✂️ Chunking documents...")
    chunks = rag['chunker'].chunk_documents(documents)
    
    st.info(f"✂️ Created {len(chunks)} total chunks")
    
    # Add to vector store
    status_text.text("🔢 Creating embeddings and building index...")
    rag['vector_store'].add_chunks(chunks)
    
    # Initialize retriever
    rag['retriever'] = Retriever(rag['vector_store'])
    
    progress_bar.progress(1.0)
    status_text.text("✅ Processing complete!")
    
    # Update session state
    st.session_state.is_ready = True
    st.session_state.uploaded_files_count = len(uploaded_files)
    
    # Display stats
    stats = rag['vector_store'].get_stats()
    st.success(f"✅ Successfully processed {len(uploaded_files)} document(s) into {stats['total_chunks']} chunks!")
    
    # Debug: Show sample chunks
    with st.expander("🔍 View Sample Chunks (Debug)", expanded=False):
        for i, chunk in enumerate(rag['vector_store'].chunks[:5], 1):
            st.write(f"**Chunk {i}** ({chunk['source']}):")
            st.text(chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'])
            st.divider()
    
    return True


def ask_question(question, top_k=5):
    """Ask a question and get an answer"""
    if not st.session_state.is_ready:
        st.warning("⚠️ Please upload documents first!")
        return None
    
    rag = st.session_state.rag_system
    
    with st.spinner("🔍 Searching for relevant information..."):
        # Debug: Show system status
        stats = rag['vector_store'].get_stats()
        st.info(f"🔍 Searching in {stats['total_chunks']} chunks from {stats['source_count']} documents...")
        
        # Retrieve relevant chunks
        retrieved_chunks = rag['retriever'].retrieve(question, top_k=top_k)
        
        # Debug: Show retrieval info
        if retrieved_chunks:
            st.success(f"✅ Found {len(retrieved_chunks)} relevant chunks!")
            for i, chunk in enumerate(retrieved_chunks[:3], 1):
                st.write(f"**Chunk {i} Score:** {chunk['score']:.3f}")
        else:
            st.warning(f"❌ No relevant information found. Tried searching {stats['total_chunks']} chunks.")
            st.info("💡 Tip: Try rephrasing your question or check if the document was uploaded correctly.")
            return None
        
        # Generate answer
        answer_dict = rag['answer_generator'].generate_answer(question, retrieved_chunks)
        
        return {
            'answer': answer_dict,
            'chunks': retrieved_chunks
        }


# Header
st.markdown('<div class="main-header">📚 RAG Document Q&A System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload documents and ask questions - No LLM, pure extractive answers</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📁 Document Upload")
    
    # Show supported formats
    with st.expander("📋 Supported Formats", expanded=False):
        st.markdown("""
        - **PDF** (.pdf)
        - **Word** (.docx)
        - **Text** (.txt)
        - **CSV** (.csv)
        - **JSON** (.json)
        - **Excel** (.xlsx, .xls)
        - **PowerPoint** (.pptx)
        - **HTML** (.html, .htm)
        - **Markdown** (.md)
        """)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'txt', 'docx', 'csv', 'json', 'xlsx', 'xls', 'pptx', 'html', 'htm', 'md'],
        accept_multiple_files=True,
        help="Upload one or more documents to analyze"
    )
    
    if uploaded_files:
        st.write(f"📎 {len(uploaded_files)} file(s) selected")
        for file in uploaded_files:
            st.write(f"  • {file.name}")
    
    process_button = st.button("🚀 Process Documents", type="primary", use_container_width=True)
    
    if process_button and uploaded_files:
        process_uploaded_files(uploaded_files)
    
    # System status
    st.divider()
    st.header("📊 System Status")
    
    if st.session_state.is_ready:
        st.success("✅ Ready for questions")
        stats = st.session_state.rag_system['vector_store'].get_stats()
        st.metric("Documents", st.session_state.uploaded_files_count)
        st.metric("Total Chunks", stats['total_chunks'])
        st.metric("Embedding Dimension", stats['dimension'])
    else:
        st.info("ℹ️ Upload documents to begin")
    
    # Settings
    st.divider()
    st.header("⚙️ Settings")
    top_k = st.slider("Number of chunks to retrieve", min_value=1, max_value=10, value=5)
    show_chunks = st.checkbox("Show retrieved chunks", value=True)
    show_scores = st.checkbox("Show similarity scores", value=True)

FLOW_DIAGRAM_HTML = """
<div class="mermaid">
flowchart TD
    A([👤 User]) -->|Upload documents| B[DocumentProcessor]
    B --> C{File type?}
    C -->|.pdf| D[PyPDF2 extractor]
    C -->|.docx| E[python-docx extractor]
    C -->|.txt| F[Plain text reader]
    C -->|.csv / .json / .xlsx| G[Pandas / json parser]
    C -->|.html / .md / .pptx| H[BeautifulSoup / pptx parser]
    D & E & F & G & H --> I[Raw text content]

    I --> J[TextChunker<br/>chunk_size=500, overlap=100]
    J --> K[Overlapping text chunks]

    K --> L[VectorStore<br/>all-MiniLM-L6-v2]
    L --> M[Sentence embeddings<br/>384 dimensions]
    M --> N[(FAISS Index<br/>cosine similarity)]

    A -->|Ask a question| O[Query text]
    O --> P[Encode query embedding]
    P --> Q[Search FAISS Index<br/>top-k nearest neighbours]
    N --> Q
    Q --> R[Retrieved chunks<br/>with similarity scores]

    R --> S[AnswerGenerator]
    S --> T{Query type?}
    T -->|what is / define| U[Definition extraction<br/>TF-IDF sentence ranking]
    T -->|when / who / where| V[Factual extraction<br/>TF-IDF sentence ranking]
    T -->|general| W[Multi-chunk extraction<br/>combine top chunks]
    U & V & W --> X[Answer + Confidence + Sources]

    X --> Y([💬 Display to User])
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default' });
</script>
"""


def _highlight_keywords(text: str, query: str) -> str:
    """Wrap query keywords in <mark> tags for highlighting (single-pass regex)."""
    stopwords = {'what', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'but',
                 'in', 'on', 'at', 'to', 'for', 'of', 'how', 'why', 'when',
                 'where', 'who', 'which', 'do', 'does', 'did', 'can', 'could'}
    words = [re.escape(w) for w in re.findall(r'\b\w+\b', query.lower())
             if w not in stopwords and len(w) > 2]
    if not words:
        return text
    pattern = re.compile(r'(?i)\b(' + '|'.join(words) + r')\b')
    return pattern.sub(r'<mark style="background-color:#fff176;">\1</mark>', text)


# Main content area
if st.session_state.is_ready:
    tab_qa, tab_flow = st.tabs(["💬 Ask Questions", "🗺️ System Flow"])

    with tab_flow:
        st.header("🗺️ RAG System Flow Diagram")
        st.markdown(
            "This diagram shows how your documents are processed and how questions are answered.",
            unsafe_allow_html=False,
        )
        st.components.v1.html(FLOW_DIAGRAM_HTML, height=700, scrolling=True)

    with tab_qa:
        st.header("💬 Ask Questions")

        # Question input
        question = st.text_input(
            "Enter your question:",
            placeholder="What is the main topic of the documents?",
            key="question_input"
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🔍 Ask", type="primary")
        with col2:
            clear_button = st.button("🗑️ Clear History")

        if clear_button:
            st.session_state.chat_history = []
            st.rerun()

        if ask_button and question:
            result = ask_question(question, top_k=top_k)

            if result:
                # Add to chat history
                st.session_state.chat_history.append({
                    'question': question,
                    'result': result
                })

        # Display chat history
        if st.session_state.chat_history:
            st.divider()
            st.header("📝 Q&A History")

            for i, item in enumerate(reversed(st.session_state.chat_history)):
                with st.container():
                    st.subheader(f"❓ {item['question']}")

                    answer_dict = item['result']['answer']

                    # Display answer
                    st.markdown(f"""
                    <div class="answer-box">
                        <strong>💡 Answer:</strong><br>
                        {answer_dict['answer']}
                    </div>
                    """, unsafe_allow_html=True)

                    # Display metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Confidence", f"{answer_dict['confidence']:.2%}")
                    with col2:
                        st.metric("Sources", len(answer_dict['sources']))
                    with col3:
                        st.metric("Method", answer_dict['method'])

                    # Show retrieved chunks if enabled
                    if show_chunks:
                        with st.expander(f"📄 Retrieved Chunks ({len(item['result']['chunks'])})"):
                            for j, chunk in enumerate(item['result']['chunks'], 1):
                                score_text = f" (similarity: {chunk['score']:.3f})" if show_scores else ""
                                chunk_full = chunk['text']
                                if len(chunk_full) > 300:
                                    # Truncate at word boundary before highlighting
                                    cutoff = chunk_full.rfind(' ', 0, 300)
                                    cutoff = cutoff if cutoff > 0 else 300
                                    truncated = chunk_full[:cutoff] + '...'
                                else:
                                    truncated = chunk_full
                                highlighted_preview = _highlight_keywords(truncated, item['question'])
                                st.markdown(f"""
                                <div class="chunk-box">
                                    <strong>Chunk {j}</strong> - <em>{chunk['source']}</em>{score_text}<br>
                                    {highlighted_preview}
                                </div>
                                """, unsafe_allow_html=True)

                    if i < len(st.session_state.chat_history) - 1:
                        st.divider()

else:
    # Welcome screen — show the flow diagram alongside the "how to use" guide
    tab_welcome, tab_flow = st.tabs(["🏠 Welcome", "🗺️ System Flow"])

    with tab_flow:
        st.header("🗺️ RAG System Flow Diagram")
        st.markdown(
            "This diagram shows how your documents are processed and how questions are answered.",
            unsafe_allow_html=False,
        )
        st.components.v1.html(FLOW_DIAGRAM_HTML, height=700, scrolling=True)

    with tab_welcome:
        st.info("👈 Upload documents using the sidebar to get started!")

        st.markdown("""
        ### How to use:

        1. **Upload Documents** - Click the file uploader in the sidebar and select your documents
        2. **Process** - Click the "Process Documents" button to analyze your files
        3. **Ask Questions** - Once processed, enter your questions in the text box
        4. **Get Answers** - Receive extractive answers based on your documents

        ### Features:

        - ✅ **No LLM hallucinations** - Answers are extracted directly from your documents
        - ✅ **Multi-format support** - PDF, Word, Excel, PowerPoint, and more
        - ✅ **Fast semantic search** - Uses vector similarity for accurate retrieval
        - ✅ **Source tracking** - See exactly where answers come from
        - ✅ **Flow diagram** - See the "System Flow" tab for a visual overview of the pipeline
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    RAG Document Q&A System | Retrieval-Augmented Generation with Extractive Answers
</div>
""", unsafe_allow_html=True)
