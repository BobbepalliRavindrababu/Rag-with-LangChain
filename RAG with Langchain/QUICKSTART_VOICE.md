# Voice Assistant Quick Start Guide

Get up and running with the RAG Voice Assistant in minutes!

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd "RAG with Langchain"
pip install -r requirements.txt
```

**Note**: If PyAudio installation fails, see platform-specific instructions below.

### Step 2: Test Your Setup

Run the voice module test to ensure everything is working:

```bash
python test_voice.py
```

This will test:
- ✅ All imports
- ✅ Voice assistant initialization
- ✅ Text-to-speech functionality
- ✅ RAG integration

### Step 3: Run the Voice Assistant

```bash
python voice_app.py
```

When prompted:
1. Type `yes` to test your microphone (recommended first time)
2. Type `sample` to create and use example documents
3. Start asking questions via voice!

## 🎯 Platform-Specific PyAudio Setup

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### macOS
```bash
brew install portaudio
pip install pyaudio
```

### Windows
```bash
pip install pipwin
pipwin install pyaudio
```

Or download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

## 💡 First Time Usage

### Test Microphone
```bash
python voice_assistant.py
```

This standalone test will:
1. Initialize the voice system
2. List available voices
3. Test your microphone
4. Play back what you said

### Use Sample Documents
When running `voice_app.py`, type `sample` instead of document paths. This creates example documents about AI and Python.

## 🎤 Voice Commands

Once the system is running:

- **Ask any question** - Just speak naturally
- **"quit"** / **"exit"** / **"stop"** - End session  
- **"help"** / **"commands"** - Show help
- **"stats"** / **"statistics"** - Show system info

## 📝 Example Questions (for sample documents)

Try asking:
- "What is artificial intelligence?"
- "What is machine learning?"
- "Tell me about Python programming"
- "What are the applications of AI?"
- "What is deep learning?"

## 🔧 Troubleshooting

### "No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### "No module named 'pyttsx3'"
```bash
pip install pyttsx3
```

### "No module named 'pyaudio'"
Follow platform-specific PyAudio setup above.

### Microphone not detected
1. Check system permissions (microphone access)
2. Test with: `python -m speech_recognition`
3. List devices: 
```python
import speech_recognition as sr
print(sr.Microphone.list_microphone_names())
```

### "Could not understand audio"
- Speak more clearly
- Reduce background noise
- Move microphone closer
- Check microphone is working in other apps

### "Speech recognition service error"
- Check internet connection (Google Speech API requires internet)
- Try again (temporary service issue)

## 📖 Full Documentation

For complete documentation, see [README_VOICE_ASSISTANT.md](README_VOICE_ASSISTANT.md)

## 🎉 You're Ready!

The voice assistant is now set up and ready to use. Enjoy hands-free document querying!

---

**Need Help?** Check the full documentation or open an issue on GitHub.
