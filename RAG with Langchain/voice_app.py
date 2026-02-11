"""
RAG Voice Assistant Application
Voice-enabled Q&A system that answers questions from documents using voice
"""
import os
import sys
import time
from document_processor import DocumentProcessor
from chunker import TextChunker
from vector_store import VectorStore
from retriever import Retriever
from answer_generator import AnswerGenerator
from voice_assistant import VoiceAssistant


class RAGVoiceAssistant:
    """Voice-enabled RAG system for document Q&A"""
    
    def __init__(self):
        """Initialize the RAG Voice Assistant"""
        print("=" * 60)
        print("🎤 RAG Voice Assistant")
        print("    Voice-Enabled Document Question Answering")
        print("=" * 60)
        
        # Initialize RAG components
        print("\n🚀 Initializing RAG System...")
        self.doc_processor = DocumentProcessor()
        self.chunker = TextChunker(chunk_size=500, overlap=100)
        self.vector_store = VectorStore()
        self.retriever = None
        self.answer_generator = AnswerGenerator()
        self.is_ready = False
        
        # Initialize voice assistant
        self.voice = VoiceAssistant(rate=150, volume=0.9)
        
        print("\n✓ System initialized")
        print("=" * 60)
    
    def load_documents(self, file_paths: list):
        """
        Load and process documents
        
        Args:
            file_paths: List of document file paths
        """
        print("\n📚 Loading documents...")
        self.voice.speak("Loading documents", async_mode=True)
        
        # Load documents
        documents = self.doc_processor.load_multiple_documents(file_paths)
        
        if not documents:
            print("❌ No documents loaded")
            self.voice.speak("No documents could be loaded")
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
        print("\n✅ System ready for voice questions!")
        self.voice.speak("System ready for questions")
        return True
    
    def ask_voice(self, question: str = None, top_k: int = 5):
        """
        Ask a question via voice or text and get a voice answer
        
        Args:
            question: Optional text question (if None, will listen for voice)
            top_k: Number of chunks to retrieve
        """
        if not self.is_ready:
            print("❌ Please load documents first!")
            self.voice.speak("Please load documents first")
            return None
        
        # Get question via voice if not provided
        if question is None:
            self.voice.speak("What is your question?")
            question = self.voice.listen(timeout=10, phrase_time_limit=15)
            
            if not question:
                print("❌ No question detected")
                self.voice.speak("I didn't hear a question. Please try again.")
                return None
        
        print("\n" + "=" * 60)
        print(f"❓ Question: {question}")
        print("=" * 60)
        
        # Retrieve relevant chunks
        print("\n🔍 Searching for relevant information...")
        self.voice.speak("Searching for an answer", async_mode=True)
        
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)
        
        if not retrieved_chunks:
            print("❌ No relevant information found.")
            self.voice.speak("I could not find relevant information in the documents.")
            return None
        
        print(f"✓ Found {len(retrieved_chunks)} relevant chunk(s)")
        
        # Generate answer
        print("\n💡 Generating answer...")
        answer_dict = self.answer_generator.generate_answer(question, retrieved_chunks)
        
        # Display answer
        print("\n" + "=" * 60)
        print("📝 TEXT ANSWER:")
        print(self.answer_generator.format_answer(answer_dict))
        print("=" * 60)
        
        # Speak answer
        print("\n🔊 VOICE ANSWER:")
        answer_text = answer_dict['answer']
        self.voice.speak(answer_text)
        
        return answer_dict
    
    def voice_interactive_mode(self):
        """Run in voice interactive Q&A mode"""
        if not self.is_ready:
            print("❌ Please load documents first!")
            self.voice.speak("Please load documents first")
            return
        
        print("\n" + "=" * 60)
        print("🎯 Voice Interactive Mode")
        print("=" * 60)
        print("Speak your questions clearly into the microphone")
        print("Say 'quit', 'exit', or 'stop' to end the session")
        print("=" * 60)
        
        self.voice.speak("Voice assistant ready. Speak your questions clearly.")
        
        while True:
            try:
                print("\n" + "-" * 60)
                self.voice.speak("What would you like to know?")
                
                # Listen for question
                question = self.voice.listen(timeout=15, phrase_time_limit=15)
                
                if not question:
                    continue
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'stop', 'goodbye', 'bye']:
                    print("\n👋 Ending session...")
                    self.voice.speak("Goodbye!")
                    break
                
                # Handle help command
                if question.lower() in ['help', 'commands']:
                    self._voice_help()
                    continue
                
                # Handle stats command
                if question.lower() in ['stats', 'statistics', 'status']:
                    self._voice_stats()
                    continue
                
                # Ask the question
                self.ask_voice(question=question, top_k=5)
                
                # Small pause between questions
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted")
                self.voice.speak("Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                self.voice.speak("An error occurred. Please try again.")
    
    def _voice_help(self):
        """Show help via voice"""
        help_text = "You can ask questions about your documents. Say quit or exit to stop."
        print(f"\n📖 {help_text}")
        self.voice.speak(help_text)
    
    def _voice_stats(self):
        """Show system statistics via voice"""
        stats = self.vector_store.get_stats()
        stats_text = f"I have processed {stats['source_count']} documents into {stats['total_chunks']} chunks."
        print(f"\n📊 {stats_text}")
        self.voice.speak(stats_text)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.voice:
            self.voice.stop()


def main():
    """Main entry point"""
    voice_rag = RAGVoiceAssistant()
    
    try:
        # Check for command line arguments
        if len(sys.argv) > 1:
            file_paths = sys.argv[1:]
            print(f"\n📁 Loading documents from command line: {file_paths}")
            if voice_rag.load_documents(file_paths):
                voice_rag.voice_interactive_mode()
        else:
            # Interactive file selection
            print("\n📁 Document Upload")
            print("-" * 60)
            
            # Option to test voice first
            print("\nWould you like to test your microphone first? (yes/no)")
            test_response = input("> ").strip().lower()
            
            if test_response in ['yes', 'y']:
                print("\n🧪 Testing microphone...")
                voice_rag.voice.test_microphone()
                print("\nPress Enter to continue...")
                input()
            
            # Get document paths
            print("\nEnter document paths (PDF, TXT, DOCX, etc.)")
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
                if voice_rag.load_documents(file_paths):
                    # Start voice interactive mode
                    voice_rag.voice_interactive_mode()
            else:
                print("No documents loaded. Exiting.")
    
    finally:
        # Cleanup
        voice_rag.cleanup()


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
