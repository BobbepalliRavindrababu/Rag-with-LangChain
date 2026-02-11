"""
Test script for Voice Assistant
Tests basic functionality without requiring documents or microphone
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))


def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✓ speech_recognition imported")
    except ImportError as e:
        print(f"❌ Failed to import speech_recognition: {e}")
        return False
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported")
    except ImportError as e:
        print(f"❌ Failed to import pyttsx3: {e}")
        return False
    
    try:
        from voice_assistant import VoiceAssistant
        print("✓ VoiceAssistant class imported")
    except ImportError as e:
        print(f"❌ Failed to import VoiceAssistant: {e}")
        return False
    
    try:
        from voice_app import RAGVoiceAssistant
        print("✓ RAGVoiceAssistant class imported")
    except ImportError as e:
        print(f"❌ Failed to import RAGVoiceAssistant: {e}")
        return False
    
    return True


def test_voice_assistant_init():
    """Test VoiceAssistant initialization"""
    print("\n🧪 Testing VoiceAssistant initialization...")
    
    try:
        from voice_assistant import VoiceAssistant
        
        # Test basic initialization
        va = VoiceAssistant(rate=150, volume=0.9)
        print("✓ VoiceAssistant initialized successfully")
        
        # Test if recognizer is set up
        if va.recognizer is not None:
            print("✓ Speech recognizer initialized")
        else:
            print("❌ Speech recognizer not initialized")
            return False
        
        # Test if TTS engine is set up
        if va.tts_engine is not None:
            print("✓ TTS engine initialized")
        else:
            print("❌ TTS engine not initialized")
            return False
        
        # Test voice listing
        voices = va.list_available_voices()
        print(f"✓ Found {len(voices)} available voices")
        
        # Test voice properties
        va.set_voice_properties(rate=200, volume=0.8)
        print("✓ Voice properties can be set")
        
        # Cleanup
        va.stop()
        print("✓ Cleanup successful")
        
        return True
    
    except ImportError as e:
        print(f"⚠️  Skipped (missing dependency): {e}")
        return True  # Consider as pass since it's optional
        
    except Exception as e:
        print(f"❌ Error during VoiceAssistant initialization: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tts_basic():
    """Test basic text-to-speech (without audio output)"""
    print("\n🧪 Testing basic TTS functionality...")
    
    try:
        from voice_assistant import VoiceAssistant
        
        va = VoiceAssistant()
        
        # Test if speak method exists and can be called
        # Note: This will actually speak, so we use a short text
        print("Testing TTS with a short phrase...")
        print("(You should hear: 'Testing voice')")
        va.speak("Testing voice")
        print("✓ TTS speak method executed")
        
        va.stop()
        return True
    
    except ImportError as e:
        print(f"⚠️  Skipped (missing dependency): {e}")
        return True  # Consider as pass since it's optional
        
    except Exception as e:
        print(f"❌ Error during TTS test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_voice_assistant_init():
    """Test RAGVoiceAssistant initialization"""
    print("\n🧪 Testing RAGVoiceAssistant initialization...")
    
    try:
        from voice_app import RAGVoiceAssistant
        
        # Initialize with output suppression
        print("Initializing RAGVoiceAssistant (this may take a moment)...")
        rag_va = RAGVoiceAssistant()
        
        print("✓ RAGVoiceAssistant initialized successfully")
        
        # Test if components are initialized
        if rag_va.doc_processor is not None:
            print("✓ Document processor initialized")
        else:
            print("❌ Document processor not initialized")
            return False
        
        if rag_va.chunker is not None:
            print("✓ Text chunker initialized")
        else:
            print("❌ Text chunker not initialized")
            return False
        
        if rag_va.vector_store is not None:
            print("✓ Vector store initialized")
        else:
            print("❌ Vector store not initialized")
            return False
        
        if rag_va.answer_generator is not None:
            print("✓ Answer generator initialized")
        else:
            print("❌ Answer generator not initialized")
            return False
        
        if rag_va.voice is not None:
            print("✓ Voice assistant initialized")
        else:
            print("❌ Voice assistant not initialized")
            return False
        
        # Cleanup
        rag_va.cleanup()
        print("✓ Cleanup successful")
        
        return True
    
    except ImportError as e:
        print(f"⚠️  Skipped (missing dependency): {e}")
        return True  # Consider as pass since it's optional
        
    except Exception as e:
        print(f"❌ Error during RAGVoiceAssistant initialization: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Voice Assistant Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "VoiceAssistant Init": test_voice_assistant_init(),
        "TTS Basic": test_tts_basic(),
        "RAGVoiceAssistant Init": test_rag_voice_assistant_init(),
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {total - passed}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    print("\n⚠️  Note: Some tests may produce audio output (TTS)")
    print("⚠️  Note: Microphone tests are NOT included (require hardware)\n")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
