"""
Voice Assistant Module
Provides speech-to-text and text-to-speech capabilities
"""
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    pyttsx3 = None

import threading
import queue


class VoiceAssistant:
    """Voice Assistant with speech recognition and text-to-speech"""
    
    def __init__(self, rate=150, volume=0.9):
        """
        Initialize the voice assistant
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            raise ImportError(
                "SpeechRecognition is not installed. "
                "Install with: pip install SpeechRecognition"
            )
        
        if not PYTTSX3_AVAILABLE:
            raise ImportError(
                "pyttsx3 is not installed. "
                "Install with: pip install pyttsx3"
            )
        
        print("🎤 Initializing Voice Assistant...")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Try to initialize microphone (may fail if PyAudio not installed)
        try:
            self.microphone = sr.Microphone()
        except AttributeError as e:
            raise ImportError(
                "PyAudio is not installed. "
                "See QUICKSTART_VOICE.md for platform-specific installation instructions."
            ) from e
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', rate)
        self.tts_engine.setProperty('volume', volume)
        
        # Queue for async TTS
        self.tts_queue = queue.Queue()
        self.tts_thread = None
        self.is_running = False
        
        # Calibrate microphone for ambient noise
        self._calibrate_microphone()
        
        print("✓ Voice Assistant initialized")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            print("🔧 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✓ Microphone calibrated")
        except Exception as e:
            print(f"⚠️ Could not calibrate microphone: {str(e)}")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for speech input from microphone
        
        Args:
            timeout: Maximum time to wait for phrase to start (seconds)
            phrase_time_limit: Maximum time for phrase (seconds)
            
        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            print("\n🎤 Listening... (speak now)")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"✓ Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error during listening: {str(e)}")
            return None
    
    def speak(self, text, async_mode=False):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            async_mode: If True, speak in background without blocking
        """
        if not text:
            return
        
        if async_mode:
            self._speak_async(text)
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text):
        """Speak text synchronously (blocking)"""
        try:
            print(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error during speech: {str(e)}")
    
    def _speak_async(self, text):
        """Speak text asynchronously (non-blocking)"""
        self.tts_queue.put(text)
        
        if not self.is_running:
            self.is_running = True
            self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
            self.tts_thread.start()
    
    def _tts_worker(self):
        """Worker thread for async TTS"""
        while self.is_running or not self.tts_queue.empty():
            try:
                text = self.tts_queue.get(timeout=1)
                self._speak_sync(text)
                self.tts_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ TTS worker error: {str(e)}")
    
    def stop(self):
        """Stop the voice assistant"""
        self.is_running = False
        if self.tts_thread and self.tts_thread.is_alive():
            self.tts_thread.join(timeout=2)
    
    def set_voice_properties(self, rate=None, volume=None, voice_id=None):
        """
        Set TTS voice properties
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
            voice_id: Voice ID (index of available voices)
        """
        if rate is not None:
            self.tts_engine.setProperty('rate', rate)
        if volume is not None:
            self.tts_engine.setProperty('volume', volume)
        if voice_id is not None:
            voices = self.tts_engine.getProperty('voices')
            if 0 <= voice_id < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_id].id)
    
    def list_available_voices(self):
        """List all available TTS voices"""
        voices = self.tts_engine.getProperty('voices')
        print("\n🎙️ Available voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}. {voice.name} ({voice.languages})")
        return voices
    
    def test_microphone(self):
        """Test microphone by recording and playing back"""
        print("\n🧪 Testing microphone...")
        print("Say something...")
        
        text = self.listen(timeout=5, phrase_time_limit=5)
        
        if text:
            print(f"\n✓ Test successful! You said: {text}")
            self.speak(f"You said: {text}")
            return True
        else:
            print("\n❌ Test failed - no speech detected")
            return False


# Simple test
if __name__ == "__main__":
    print("=" * 60)
    print("🎤 Voice Assistant Test")
    print("=" * 60)
    
    # Check if dependencies are available
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("❌ SpeechRecognition not installed")
        print("   Install with: pip install SpeechRecognition")
        exit(1)
    
    if not PYTTSX3_AVAILABLE:
        print("❌ pyttsx3 not installed")
        print("   Install with: pip install pyttsx3")
        exit(1)
    
    try:
        # Initialize voice assistant
        va = VoiceAssistant()
        
        # List available voices
        va.list_available_voices()
        
        # Test microphone
        print("\nTesting microphone...")
        va.test_microphone()
        
        # Cleanup
        va.stop()
        print("\n✓ Test complete")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nSee QUICKSTART_VOICE.md for installation instructions.")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
