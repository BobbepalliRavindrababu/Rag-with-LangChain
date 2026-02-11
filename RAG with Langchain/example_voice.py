"""
Example: Using the Voice Assistant with RAG System
This example demonstrates how to use the voice assistant programmatically
"""
import os
import sys

def example_with_sample_docs():
    """Example: Using voice assistant with sample documents"""
    print("=" * 60)
    print("Example: Voice Assistant with Sample Documents")
    print("=" * 60)
    
    try:
        from voice_app import RAGVoiceAssistant, create_sample_documents, get_sample_document_paths
        
        # Initialize the voice assistant
        print("\n1️⃣  Initializing Voice Assistant...")
        voice_rag = RAGVoiceAssistant()
        
        # Create and load sample documents
        print("\n2️⃣  Creating sample documents...")
        create_sample_documents()
        
        sample_paths = get_sample_document_paths()
        print(f"\n3️⃣  Loading documents: {sample_paths}")
        
        if not voice_rag.load_documents(sample_paths):
            print("❌ Failed to load documents")
            return
        
        # Example: Ask a question programmatically (with voice output)
        print("\n4️⃣  Asking a sample question via text (with voice response)...")
        question = "What is artificial intelligence?"
        voice_rag.ask_voice(question=question, top_k=3)
        
        # Start interactive voice mode (commented out for example)
        # print("\n5️⃣  Starting interactive voice mode...")
        # print("   (Uncomment this section to test voice input)")
        # voice_rag.voice_interactive_mode()
        
        # Cleanup
        voice_rag.cleanup()
        print("\n✅ Example completed successfully!")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n💡 To run this example, install the required dependencies:")
        print("   pip install -r requirements.txt")
        print("\n   See QUICKSTART_VOICE.md for platform-specific PyAudio installation.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def example_custom_documents():
    """Example: Using voice assistant with custom documents"""
    print("=" * 60)
    print("Example: Voice Assistant with Custom Documents")
    print("=" * 60)
    
    try:
        from voice_app import RAGVoiceAssistant
        
        # Initialize the voice assistant
        print("\n1️⃣  Initializing Voice Assistant...")
        voice_rag = RAGVoiceAssistant()
        
        # Specify your document paths
        document_paths = [
            # Add your document paths here
            # Example:
            # "/path/to/document1.pdf",
            # "/path/to/document2.txt",
        ]
        
        if not document_paths:
            print("\n⚠️  No documents specified!")
            print("   Edit this example to add your document paths.")
            return
        
        print(f"\n2️⃣  Loading documents: {document_paths}")
        
        if not voice_rag.load_documents(document_paths):
            print("❌ Failed to load documents")
            return
        
        # Start interactive voice mode
        print("\n3️⃣  Starting interactive voice mode...")
        print("   Speak your questions when prompted!")
        voice_rag.voice_interactive_mode()
        
        # Cleanup
        voice_rag.cleanup()
        print("\n✅ Session completed!")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n💡 To run this example, install the required dependencies:")
        print("   pip install -r requirements.txt")
        print("\n   See QUICKSTART_VOICE.md for platform-specific PyAudio installation.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def example_voice_settings():
    """Example: Customizing voice settings"""
    print("=" * 60)
    print("Example: Customizing Voice Settings")
    print("=" * 60)
    
    try:
        from voice_assistant import VoiceAssistant
        
        # Initialize with custom settings
        print("\n1️⃣  Initializing with custom voice settings...")
        voice = VoiceAssistant(
            rate=180,    # Faster speech
            volume=1.0   # Maximum volume
        )
        
        # List available voices
        print("\n2️⃣  Available voices:")
        voices = voice.list_available_voices()
        
        # Change voice (example: use voice 0)
        if len(voices) > 0:
            print(f"\n3️⃣  Changing to voice 0...")
            voice.set_voice_properties(voice_id=0)
            voice.speak("Hello, this is voice zero")
        
        # Change voice again (example: use voice 1 if available)
        if len(voices) > 1:
            print(f"\n4️⃣  Changing to voice 1...")
            voice.set_voice_properties(voice_id=1)
            voice.speak("Hello, this is voice one")
        
        # Adjust speech rate
        print(f"\n5️⃣  Testing different speech rates...")
        
        voice.set_voice_properties(rate=100)
        voice.speak("This is slow speech at rate 100")
        
        voice.set_voice_properties(rate=200)
        voice.speak("This is fast speech at rate 200")
        
        voice.set_voice_properties(rate=150)
        voice.speak("This is normal speech at rate 150")
        
        # Cleanup
        voice.stop()
        print("\n✅ Voice settings example completed!")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\n💡 To run this example, install the required dependencies:")
        print("   pip install -r requirements.txt")
        print("\n   See QUICKSTART_VOICE.md for platform-specific PyAudio installation.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main menu"""
    print("\n" + "=" * 60)
    print("Voice Assistant Examples")
    print("=" * 60)
    print("\nChoose an example to run:")
    print("1. Voice Assistant with Sample Documents (recommended)")
    print("2. Voice Assistant with Custom Documents")
    print("3. Customize Voice Settings")
    print("4. Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        example_with_sample_docs()
    elif choice == "2":
        example_custom_documents()
    elif choice == "3":
        example_voice_settings()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and select 1-4.")


if __name__ == "__main__":
    main()
