# Voice Assistant Quick Reference

## 🚀 Quick Start (1 Minute)

```bash
cd "RAG with Langchain"
pip install -r requirements.txt
python voice_app.py
```

When prompted: type `sample` → start speaking!

## 🎤 Voice Commands

| Command | Action |
|---------|--------|
| *Any question* | Ask about your documents |
| `quit` / `exit` / `stop` | End session |
| `help` / `commands` | Show help |
| `stats` / `statistics` | Show system info |

## 📁 Key Files

| File | Purpose |
|------|---------|
| `voice_app.py` | Main voice application |
| `voice_assistant.py` | Core voice module |
| `example_voice.py` | Usage examples |
| `test_voice.py` | Test suite |

## 📖 Documentation

| Document | When to Use |
|----------|-------------|
| `QUICKSTART_VOICE.md` | First time setup |
| `README_VOICE_ASSISTANT.md` | Complete guide |
| `IMPLEMENTATION_SUMMARY.md` | Technical overview |

## 🔧 Troubleshooting

### PyAudio Won't Install?

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

### "Could not understand audio"?
- Speak more clearly
- Reduce background noise
- Check microphone is working

### "No speech detected"?
- Check microphone permissions
- Test with: `python voice_assistant.py`
- Speak sooner after prompt

### "Speech recognition service error"?
- Check internet connection
- Google API requires internet

## 💡 Example Questions

Try asking:
- "What is this document about?"
- "Tell me about machine learning"
- "What are the key points?"
- "Summarize the main topics"

## ⚙️ Customize Voice

```python
from voice_assistant import VoiceAssistant

# Adjust settings
va = VoiceAssistant(
    rate=180,    # Speech speed (100-200)
    volume=0.9   # Volume (0.0-1.0)
)

# List voices
va.list_available_voices()

# Change voice
va.set_voice_properties(voice_id=1)
```

## 🎯 Usage Patterns

### Pattern 1: Quick Query
```bash
python voice_app.py doc.pdf
# Speak your question
# Get instant answer
```

### Pattern 2: Extended Session
```bash
python voice_app.py
# Load documents
# Ask multiple questions
# Say "quit" when done
```

### Pattern 3: Programmatic
```python
from voice_app import RAGVoiceAssistant

rag = RAGVoiceAssistant()
rag.load_documents(['doc.pdf'])
rag.ask_voice(question="What is this about?")
```

## 📊 System Requirements

- ✅ Python 3.7+
- ✅ Microphone
- ✅ Speakers
- ✅ Internet (for speech recognition)

## 🔗 Quick Links

- Setup: `QUICKSTART_VOICE.md`
- Full Docs: `README_VOICE_ASSISTANT.md`
- Examples: `python example_voice.py`
- Tests: `python test_voice.py`

## 📞 Get Help

1. Check `QUICKSTART_VOICE.md` for setup
2. Check `README_VOICE_ASSISTANT.md` for details
3. Run `python example_voice.py` for examples
4. See troubleshooting section above

---

**Happy Voice Querying! 🎤**
