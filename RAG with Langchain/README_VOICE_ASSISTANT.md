# Voice Assistant for RAG System

A voice-enabled document question answering system that allows users to interact with their documents using speech. Ask questions by speaking and receive answers through both text and voice.

## 🎤 Features

- **Voice Input**: Ask questions naturally using your microphone
- **Voice Output**: Receive answers through text-to-speech
- **Hands-Free Operation**: Complete voice-driven interaction
- **Multi-Document Support**: Ask questions across multiple uploaded documents
- **Ambient Noise Calibration**: Automatically adjusts to your environment
- **Interactive Mode**: Continuous conversation until you say "quit"

## 📋 Prerequisites

### System Requirements

- **Microphone**: Working microphone for speech input
- **Speakers/Headphones**: For voice output
- **Internet Connection**: Required for Google Speech Recognition API

### Software Requirements

- Python 3.7 or higher
- All dependencies from `requirements.txt`

### Platform-Specific Requirements

#### Linux
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### macOS
```bash
brew install portaudio
```

#### Windows
PyAudio pre-built wheel is included in the requirements. If installation fails:
```bash
pip install pipwin
pipwin install pyaudio
```

## 🚀 Installation

1. **Install all dependencies**:
```bash
cd "RAG with Langchain"
pip install -r requirements.txt
```

2. **Test microphone** (optional but recommended):
```bash
python voice_assistant.py
```

## 💡 Usage

### Basic Usage

1. **Start the voice assistant**:
```bash
python voice_app.py
```

2. **Test microphone** (recommended on first run):
   - The system will ask if you want to test your microphone
   - Type `yes` and speak when prompted

3. **Load documents**:
   - Enter paths to your documents (PDF, TXT, DOCX, etc.)
   - Type `sample` to use example documents
   - Type `done` when finished

4. **Ask questions via voice**:
   - Wait for the prompt "What would you like to know?"
   - Speak your question clearly
   - Receive both text and voice answers

5. **End session**:
   - Say "quit", "exit", or "stop"
   - Or press Ctrl+C

### Command Line Usage

Load documents directly from command line:
```bash
python voice_app.py document1.pdf document2.txt
```

### Voice Commands

During interactive mode:
- **"quit"**, **"exit"**, **"stop"**: End the session
- **"help"**, **"commands"**: Get help information
- **"stats"**, **"statistics"**, **"status"**: View system statistics

## 📖 Example Session

```
🎤 RAG Voice Assistant
    Voice-Enabled Document Question Answering
============================================================

🚀 Initializing RAG System...
📄 Supported formats: pdf, docx, txt, csv, json, xlsx, xls, pptx, html, htm, md
✓ System initialized
============================================================

🎤 Initializing Voice Assistant...
🔧 Calibrating microphone for ambient noise...
✓ Microphone calibrated
✓ Voice Assistant initialized

📁 Document Upload
------------------------------------------------------------

Would you like to test your microphone first? (yes/no)
> yes

🧪 Testing microphone...
Say something...

🎤 Listening... (speak now)
✓ Recognized: hello testing
✓ Test successful! You said: hello testing
🔊 Speaking: You said: hello testing

Enter document paths (PDF, TXT, DOCX, etc.)
Type 'done' when finished, or 'sample' to use example docs

Document path: sample

Creating sample documents...
✓ Sample documents created in 'sample_documents' directory

📚 Loading documents...
🔊 Speaking: Loading documents

✂️  Chunking documents...
✓ Created 12 total chunks

🔢 Creating embeddings and building index...

📊 Index Statistics:
   • Total chunks: 12
   • Documents: 2
   • Embedding dimension: 384

✅ System ready for voice questions!
🔊 Speaking: System ready for questions

============================================================
🎯 Voice Interactive Mode
============================================================
Speak your questions clearly into the microphone
Say 'quit', 'exit', or 'stop' to end the session
============================================================
🔊 Speaking: Voice assistant ready. Speak your questions clearly.

------------------------------------------------------------
🔊 Speaking: What would you like to know?

🎤 Listening... (speak now)
✓ Recognized: what is artificial intelligence

============================================================
❓ Question: what is artificial intelligence
============================================================

🔍 Searching for relevant information...
🔊 Speaking: Searching for an answer
✓ Found 5 relevant chunk(s)

💡 Generating answer...

============================================================
📝 TEXT ANSWER:

💡 Answer:
Artificial intelligence (AI) is the simulation of human intelligence by 
machines. AI systems can perform tasks that typically require human 
intelligence, such as visual perception, speech recognition, 
decision-making, and language translation.

📊 Metadata:
   • Confidence: 0.92
   • Sources: 3 chunks
   • Method: extractive_concatenation

🔗 Source chunks: ai_overview.txt (3 references)
============================================================

🔊 VOICE ANSWER:
🔊 Speaking: Artificial intelligence (AI) is the simulation...

------------------------------------------------------------
🔊 Speaking: What would you like to know?

🎤 Listening... (speak now)
✓ Recognized: quit

👋 Ending session...
🔊 Speaking: Goodbye!
```

## ⚙️ Configuration

### Adjust Voice Settings

You can customize the voice assistant in `voice_app.py`:

```python
# Initialize with custom settings
voice = VoiceAssistant(
    rate=150,      # Speech rate (100-200 recommended)
    volume=0.9     # Volume (0.0 to 1.0)
)
```

### Change Voice

To use a different voice:
```python
# List available voices
voice.list_available_voices()

# Set voice by ID
voice.set_voice_properties(voice_id=1)
```

### Adjust Listening Timeouts

In `voice_app.py`, modify the `listen()` parameters:
```python
question = self.voice.listen(
    timeout=15,              # Max wait for speech to start
    phrase_time_limit=15     # Max duration of speech
)
```

## 🛠️ Troubleshooting

### Microphone Not Working

1. **Check permissions**: Ensure Python has microphone access
2. **Test microphone**: Run `python voice_assistant.py`
3. **List devices**: 
   ```python
   import speech_recognition as sr
   print(sr.Microphone.list_microphone_names())
   ```

### PyAudio Installation Issues

**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

### Speech Recognition Errors

- **"Could not understand audio"**: Speak more clearly or reduce background noise
- **"No speech detected (timeout)"**: Speak sooner after the listening prompt
- **"Speech recognition service error"**: Check internet connection (Google API requires internet)

### Poor Recognition Quality

1. **Calibrate microphone**: The system does this automatically on startup
2. **Reduce background noise**: Find a quieter environment
3. **Speak clearly**: Enunciate and speak at normal pace
4. **Adjust microphone**: Position microphone closer to mouth

## 🔧 Advanced Usage

### Offline Speech Recognition

For offline usage, you can use PocketSphinx (less accurate):

```python
# Install PocketSphinx
pip install pocketsphinx

# Modify voice_assistant.py listen() method:
text = self.recognizer.recognize_sphinx(audio)
```

### Custom Wake Word

Add a wake word feature:

```python
def wait_for_wake_word(self, wake_word="assistant"):
    while True:
        text = self.listen()
        if text and wake_word.lower() in text.lower():
            return True
```

### Voice Activity Detection

For better listening:
```python
self.recognizer.energy_threshold = 4000  # Adjust based on environment
self.recognizer.dynamic_energy_threshold = True
```

## 📊 Architecture

### Components

1. **voice_assistant.py**: Core voice functionality
   - Speech-to-text using Google Speech Recognition
   - Text-to-speech using pyttsx3
   - Microphone calibration and management

2. **voice_app.py**: Main application
   - Integrates voice with RAG system
   - Manages interactive voice sessions
   - Handles voice commands

3. **RAG System Components** (existing):
   - Document processing and chunking
   - Vector embeddings and similarity search
   - Extractive answer generation

### Data Flow

```
User Speech → Microphone → Speech Recognition → Text Question
                                                      ↓
                                            RAG System Processing
                                            (Retrieval + Answer)
                                                      ↓
Text Answer → Text-to-Speech → Speakers → User Hears Answer
```

## 🎯 Best Practices

1. **Test microphone first**: Always run the microphone test on first use
2. **Quiet environment**: Use in a quiet place for best recognition
3. **Clear speech**: Speak naturally but clearly
4. **Pause before speaking**: Wait for the "Listening..." prompt
5. **Formulate questions**: Think about your question before speaking
6. **Short questions**: Keep questions concise for better recognition

## 📝 Features in Detail

### Speech-to-Text
- Uses Google Speech Recognition API
- Automatic ambient noise adjustment
- Configurable timeout and phrase limits
- Error handling for unclear audio

### Text-to-Speech
- Uses pyttsx3 (works offline)
- Adjustable speech rate and volume
- Multiple voice options
- Async speaking option (non-blocking)

### Integration with RAG
- Seamless voice input for questions
- Voice feedback for system status
- Voice output of answers
- Voice statistics and help

## 🔒 Privacy & Security

- **Speech data**: Sent to Google Speech Recognition API (requires internet)
- **Documents**: Processed and stored locally
- **No data retention**: Google doesn't retain audio after processing
- **Offline TTS**: Text-to-speech works completely offline

## 🤝 Contributing

Feel free to enhance the voice assistant:
- Add more voice commands
- Improve error handling
- Add wake word detection
- Support for other languages
- Custom voice models

## 📚 Resources

- [SpeechRecognition Documentation](https://github.com/Uberi/speech_recognition)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/)

## 🐛 Known Issues

1. **PyAudio installation**: Can be tricky on some platforms - see troubleshooting
2. **Google API rate limits**: Free tier has usage limits
3. **Microphone permissions**: May require explicit permission on some systems
4. **Background noise**: Can affect recognition accuracy

## 📄 License

Same as the main RAG project.

---

**Note**: The voice assistant requires a working microphone and speakers. For the best experience, use in a quiet environment with a good quality microphone.
