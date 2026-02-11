"""
RAG Question Answering System - Main Application
No LLM - Uses extractive methods for answer generation
"""
import os
import sys
from document_processor import DocumentProcessor
from chunker import TextChunker
from vector_store import VectorStore
from retriever import Retriever
from answer_generator import AnswerGenerator


class RAGSystem:
    """Main RAG system orchestrating all components"""
    
    def __init__(self):
        """Initialize the RAG system"""
        print("🚀 Initializing RAG System (No LLM)...")
        print("=" * 60)
        
        self.doc_processor = DocumentProcessor()
        print(f"📄 Supported formats: {', '.join(self.doc_processor.supported_formats)}")
        
        self.chunker = TextChunker(chunk_size=500, overlap=100)
        self.vector_store = VectorStore()
        self.retriever = None
        self.answer_generator = AnswerGenerator()
        
        self.is_ready = False
        
        print("✓ System initialized")
        print("=" * 60)
    
    def load_documents(self, file_paths: list):
        """
        Load and process documents
        
        Args:
            file_paths: List of document file paths
        """
        print("\n📚 Loading documents...")
        
        # Load documents
        documents = self.doc_processor.load_multiple_documents(file_paths)
        
        if not documents:
            print("❌ No documents loaded")
            return False
        
        # Chunk documents
        print("\n✂️  Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        print(f"✓ Created {len(chunks)} total chunks")
        
        # Add to vector store
        print("\n🔢 Creating embeddings and building index...")
        self.vector_store.add_chunks(chunks)
        
        # Initialize retriever
        self.retriever = Retriever(self.vector_store)
        
        # Display stats
        stats = self.vector_store.get_stats()
        print(f"\n📊 Index Statistics:")
        print(f"   • Total chunks: {stats['total_chunks']}")
        print(f"   • Documents: {stats['source_count']}")
        print(f"   • Embedding dimension: {stats['dimension']}")
        
        self.is_ready = True
        print("\n✅ System ready for questions!")
        return True
    
    def ask(self, question: str, top_k: int = 5, show_chunks: bool = False):
        """
        Ask a question and get an answer
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve
            show_chunks: Whether to display retrieved chunks
        """
        if not self.is_ready:
            print("❌ Please load documents first!")
            return None
        
        print("\n" + "=" * 60)
        print(f"❓ Question: {question}")
        print("=" * 60)
        
        # Retrieve relevant chunks
        print("\n🔍 Searching for relevant information...")
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)
        
        if not retrieved_chunks:
            print("❌ No relevant information found.")
            return None
        
        print(f"✓ Found {len(retrieved_chunks)} relevant chunk(s)")
        
        # Show retrieved chunks if requested
        if show_chunks:
            print("\n📄 Retrieved Chunks:")
            for i, chunk_info in enumerate(retrieved_chunks, 1):
                print(f"\n{i}. [{chunk_info['source']}] (similarity: {chunk_info['score']:.3f})")
                print(f"   {chunk_info['text'][:200]}...")
        
        # Generate answer
        print("\n💡 Generating answer...")
        answer_dict = self.answer_generator.generate_answer(question, retrieved_chunks)
        
        # Display answer
        print("\n" + self.answer_generator.format_answer(answer_dict))
        print("=" * 60)
        
        return answer_dict
    
    def save_index(self, path: str = 'rag_index'):
        """Save the vector store index"""
        if not self.is_ready:
            print("Nothing to save")
            return
        
        self.vector_store.save(f"{path}.pkl")
        print(f"✓ Index saved to {path}.pkl")
    
    def load_index(self, path: str = 'rag_index'):
        """Load a previously saved vector store index"""
        success = self.vector_store.load(f"{path}.pkl")
        if success:
            self.retriever = Retriever(self.vector_store)
            self.is_ready = True
            print("✅ System ready for questions!")
        return success
    
    def interactive_mode(self):
        """Run in interactive Q&A mode"""
        if not self.is_ready:
            print("❌ Please load documents first!")
            return
        
        print("\n" + "=" * 60)
        print("🎯 Interactive Q&A Mode")
        print("=" * 60)
        print("Type your questions (or 'quit' to exit, 'help' for commands)")
        print()
        
        while True:
            try:
                question = input("\n💬 Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if question.lower() == 'help':
                    self._show_help()
                    continue
                
                if question.lower() == 'stats':
                    self._show_stats()
                    continue
                
                # Ask the question
                self.ask(question, top_k=5, show_chunks=False)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def _show_help(self):
        """Show help information"""
        print("\n📖 Available Commands:")
        print("  • Type any question to get an answer")
        print("  • 'stats' - Show system statistics")
        print("  • 'help' - Show this help message")
        print("  • 'quit' / 'exit' - Exit the program")
    
    def _show_stats(self):
        """Show system statistics"""
        stats = self.vector_store.get_stats()
        print("\n📊 System Statistics:")
        print(f"  • Total chunks: {stats['total_chunks']}")
        print(f"  • Documents: {stats['source_count']}")
        for source in stats['sources']:
            print(f"    - {source}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("🤖 RAG Document Q&A System (No LLM)")
    print("    Retrieval-Augmented Generation with Extractive Answers")
    print("=" * 60)
    
    # Initialize system
    rag = RAGSystem()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]
        print(f"\n📁 Loading documents from command line: {file_paths}")
        rag.load_documents(file_paths)
        rag.interactive_mode()
    else:
        # Interactive file selection
        print("\n📁 Document Upload")
        print("-" * 60)
        print("Enter document paths (PDF or TXT files)")
        print("Separate multiple files with commas, or type one per line")
        print("Type 'done' when finished, or 'sample' to use example docs")
        print()
        
        file_paths = []
        while True:
            user_input = input("Document path: ").strip()
            
            if user_input.lower() == 'done':
                break
            
            if user_input.lower() == 'sample':
                print("Creating sample documents...")
                create_sample_documents()
                file_paths = get_sample_document_paths()
                break
            
            if not user_input:
                continue
            
            # Handle comma-separated paths
            if ',' in user_input:
                paths = [p.strip() for p in user_input.split(',')]
                file_paths.extend(paths)
            else:
                file_paths.append(user_input)
        
        if file_paths:
            rag.load_documents(file_paths)
            
            # Ask if user wants to save index
            save = input("\n💾 Save index for future use? (y/n): ").strip().lower()
            if save == 'y':
                rag.save_index()
            
            # Start interactive mode
            rag.interactive_mode()
        else:
            print("No documents loaded. Exiting.")


def create_sample_documents():
    """Create sample documents for testing"""
    samples_dir = "sample_documents"
    os.makedirs(samples_dir, exist_ok=True)
    
    # Sample 1: AI Overview
    with open(f"{samples_dir}/ai_overview.txt", 'w') as f:
        f.write("""
Artificial Intelligence Overview

Artificial intelligence (AI) is the simulation of human intelligence by machines. AI systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.

Machine Learning is a subset of AI that enables computers to learn from data without being explicitly programmed. ML algorithms build mathematical models based on sample data, known as training data, to make predictions or decisions.

Deep Learning is a subset of machine learning that uses neural networks with multiple layers. These deep neural networks can automatically learn hierarchical representations of data, making them particularly effective for tasks like image and speech recognition.

Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language. NLP combines computational linguistics with machine learning and deep learning models.

Computer Vision enables machines to interpret and understand visual information from the world. It involves methods for acquiring, processing, analyzing, and understanding digital images.

Applications of AI include autonomous vehicles, medical diagnosis, virtual assistants, recommendation systems, and fraud detection.
        """)
    
    # Sample 2: Python Programming
    with open(f"{samples_dir}/python_basics.txt", 'w') as f:
        f.write("""
Python Programming Basics

Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.

Key Features:
- Easy to learn syntax
- Dynamically typed
- Extensive standard library
- Cross-platform compatibility
- Strong community support

Data Types:
Python supports various data types including integers, floats, strings, lists, tuples, dictionaries, and sets. Lists are mutable sequences, while tuples are immutable.

Functions in Python are defined using the 'def' keyword. They can accept parameters and return values. Python also supports lambda functions for simple operations.

Object-Oriented Programming:
Python supports OOP concepts including classes, objects, inheritance, encapsulation, and polymorphism. Classes are defined using the 'class' keyword.

Popular Libraries:
- NumPy: Numerical computing
- Pandas: Data analysis
- Matplotlib: Data visualization
- Scikit-learn: Machine learning
- TensorFlow: Deep learning

Python is widely used in web development, data science, artificial intelligence, scientific computing, and automation.
        """)
    
    print(f"✓ Sample documents created in '{samples_dir}' directory")


def get_sample_document_paths():
    """Get paths to sample documents"""
    samples_dir = "sample_documents"
    return [
        f"{samples_dir}/ai_overview.txt",
        f"{samples_dir}/python_basics.txt"
    ]


if __name__ == "__main__":
    main()
