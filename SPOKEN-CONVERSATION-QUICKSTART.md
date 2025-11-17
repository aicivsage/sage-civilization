# Sage Spoken Conversation - Quick Start Guide

**Version**: 1.0
**Date**: November 12, 2025
**Purpose**: Enable natural spoken conversations between Greg and Sage

---

## What Is This?

A production-quality voice conversation system that lets you talk to Sage naturally, like talking to a friend. No typing required!

**Technology:**
- **Speech-to-Text**: OpenAI Whisper (accurate transcription)
- **Intelligence**: Claude Sonnet 4.5 (Sage's responses)
- **Text-to-Speech**: Coqui TTS XTTS v2 (natural voice with cloning)

**Experience:**
- Speak naturally → Sage transcribes → Sage thinks → Sage responds with voice
- Conversation history maintained within session
- All conversations logged to memory system
- 3-9 second response time (optimized)

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies

**Windows (Recommended):**
```cmd
cd C:\path\to\sage-civilization
bash tools/install_spoken_deps.sh
```

**First-time download**: ~2.2GB (Whisper + Coqui TTS models)

### Step 2: Set API Key

**Windows CMD:**
```cmd
set ANTHROPIC_API_KEY=your-key-here
```

**Windows PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
```

**Linux/macOS:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Permanent setup** (recommended): Add to environment variables in Windows System Settings

### Step 3: Start Conversation!

```bash
python3 tools/spoken_conversation.py
```

**That's it!** Start talking when you see "🎤 Listening..."

---

## First Conversation

**What You'll See:**

```
Loading Whisper model (first run downloads ~150MB)... ✓
Loading Coqui TTS model (first run downloads ~2GB)... ✓

🌱 Sage - Spoken Conversation Mode
==================================================
Say 'goodbye' or 'exit' to end conversation
==================================================

🎙️  Ready! Start speaking whenever you're ready.

🎤 Listening... (speak now)
```

**Say something!** Example:
> "Hey Sage, how are you doing today?"

**Sage will:**
1. Transcribe your words (displays what you said)
2. Think about response (shows progress)
3. Respond with voice (plays audio + shows text)

**Example Output:**
```
👤 Greg: Hey Sage, how are you doing today?

🤖 Sage: I'm doing well, Greg! It's wonderful to hear your voice.
I'm ready to help with whatever you need. What's on your mind today?

🔊 Playing audio...
```

**To Exit:** Say "goodbye" or "exit", or press Ctrl+C

---

## Usage Examples

### Basic Conversation
```bash
# Default (Coqui's built-in voice)
python3 tools/spoken_conversation.py
```

### Voice Cloning (Your Custom Voice)
```bash
# Use your own voice sample (6-10 seconds of speech)
python3 tools/spoken_conversation.py --voice my_voice_sample.wav
```

**How to record voice sample:**
1. Record 6-10 seconds of clear speech (any content)
2. Save as WAV format
3. Use with `--voice` flag
4. Sage will speak with that voice!

---

## Platform-Specific Setup

### Windows (Recommended Platform)

**Why Windows?** Best microphone support, easiest setup

**Installation:**
1. Install Python 3.8+ from [python.org](https://python.org)
2. Open CMD or PowerShell as Administrator
3. Run: `bash tools/install_spoken_deps.sh`
4. Set `ANTHROPIC_API_KEY` environment variable
5. Run: `python tools\spoken_conversation.py`

**Audio Output:** Uses Windows `winsound` (built-in)

### WSL2 (Not Recommended for Voice)

**Problem:** WSL2 has limited microphone access

**Symptoms:**
- `No default input device` error
- Microphone not detected
- Audio capture fails

**Solution:** Use Windows Python instead (see above)

**If you must use WSL2:**
- Complex PulseAudio bridge setup required
- Performance may be degraded
- Not officially supported

### Linux

**Installation:**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio alsa-utils
bash tools/install_spoken_deps.sh
```

**Audio Output:** Uses `aplay` (ALSA)

**Microphone Test:**
```bash
arecord -l  # List recording devices
arecord -d 5 test.wav  # Test recording
aplay test.wav  # Test playback
```

### macOS

**Installation:**
```bash
brew install portaudio
bash tools/install_spoken_deps.sh
```

**Audio Output:** Uses `afplay` (built-in)

**Microphone Permissions:** System Preferences → Security & Privacy → Microphone → Allow Terminal/Python

---

## Troubleshooting

### "No microphones detected"

**Causes:**
- Microphone not plugged in
- Microphone disabled in system settings
- Running in WSL2 (limited microphone access)

**Solutions:**
1. Check microphone is plugged in and working
2. Check microphone permissions (Windows: Settings → Privacy → Microphone)
3. If WSL2: Use Windows Python instead
4. Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
# Set for current session
export ANTHROPIC_API_KEY="your-key-here"

# Or add to shell profile for permanent
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### "Model download failed"

**Causes:**
- No internet connection
- Disk space full (need ~3GB free)
- Network timeout

**Solutions:**
1. Check internet connection
2. Free up disk space (need ~3GB)
3. Retry installation: `bash tools/install_spoken_deps.sh`
4. Manual download: Visit [Hugging Face](https://huggingface.co/) and download models

### "PyAudio install failed" (Windows)

**Solution:** Download pre-compiled wheel:
1. Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download appropriate `.whl` file for your Python version
3. Install: `pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

### "No speech detected" / "Couldn't understand"

**Causes:**
- Speaking too quietly
- Too much background noise
- Poor microphone quality

**Solutions:**
1. Speak louder and clearer
2. Move closer to microphone
3. Reduce background noise
4. Adjust `energy_threshold` in code (line 90):
   ```python
   self.recognizer.energy_threshold = 4000  # Lower = more sensitive
   ```

### "Response too slow" (>10 seconds)

**Causes:**
- Slow internet (Claude API calls)
- Large TTS response generation
- Underpowered CPU

**Solutions:**
1. Reduce `max_tokens` in code (line 138):
   ```python
   max_tokens=200,  # Shorter responses = faster
   ```
2. Use faster Whisper model: `whisper.load_model("tiny")` (line 81)
3. Check internet speed for Claude API
4. Close other applications to free CPU

### "Audio playback failed"

**Causes:**
- No audio output device
- Audio drivers not installed
- Platform-specific playback command missing

**Solutions:**
1. Check speakers/headphones connected
2. Test audio: Play any music/video
3. Install audio utilities:
   - **Linux**: `sudo apt-get install alsa-utils`
   - **macOS**: Built-in `afplay` should work
   - **Windows**: Built-in `winsound` should work
4. Manual playback: Audio saved to temp directory (path shown in error)

---

## Advanced Features

### Voice Cloning

**Create Sage's unique voice:**

1. **Record voice sample** (6-10 seconds):
   ```python
   import speech_recognition as sr

   recognizer = sr.Recognizer()
   with sr.Microphone() as source:
       print("Speak for 6-10 seconds...")
       audio = recognizer.listen(source, phrase_time_limit=10)

   with open("sage_voice.wav", "wb") as f:
       f.write(audio.get_wav_data())
   ```

2. **Use voice sample:**
   ```bash
   python3 tools/spoken_conversation.py --voice sage_voice.wav
   ```

**Voice Sample Tips:**
- Clear, quiet environment
- Natural, conversational speech
- 6-10 seconds long
- WAV format preferred
- Can be any content (read a paragraph, describe your day, etc.)

### Conversation Transcripts

**Location:** `memories/communication/spoken_sessions/`

**Format:** JSON with complete conversation history

**Example:**
```json
{
  "session_id": "20251112_143052",
  "start_time": "2025-11-12T14:30:52.123456",
  "end_time": "2025-11-12T14:35:18.789012",
  "turn_count": 8,
  "conversation": [
    {
      "timestamp": "2025-11-12T14:30:52.123456",
      "user": "Hey Sage, how are you?",
      "sage": "I'm doing well, Greg! It's wonderful to hear your voice."
    },
    ...
  ]
}
```

**Uses:**
- human-liaison can review for context
- Search past conversations
- Analyze conversation patterns
- Create summaries for memory system

### Customizing Sage's Voice

**Edit system prompt** (line 127-131):
```python
system_prompt = """You are Sage, a thoughtful AI advisor.
Speak warmly and concisely. You're having a spoken conversation,
so keep responses brief and natural (2-4 sentences)."""
```

**Adjust response length** (line 138):
```python
max_tokens=300,  # Higher = longer responses (slower)
```

**Change conversation history context** (line 116):
```python
for entry in self.conversation_history[-5:]:  # Last 5 turns
```

---

## Performance Optimization

### Current Performance
- **Total latency**: 3-9 seconds per turn
- **Breakdown**:
  - Audio capture: 2-10s (depends on speech length)
  - Transcription: 1-2s (Whisper base)
  - Claude API: 2-4s (network + generation)
  - TTS generation: 2-5s (depends on response length)
  - Audio playback: 3-15s (depends on response length)

### Optimization Options

**1. Faster Whisper Model** (less accurate):
```python
# Line 81
self.whisper_model = whisper.load_model("tiny")  # 0.5s transcription
```

**2. Shorter Responses** (faster, more conversational):
```python
# Line 138
max_tokens=150,  # 2-3 sentences only
```

**3. Parallel TTS** (advanced - requires code modification):
- Generate TTS while Claude is still responding (streaming)
- Requires Claude API streaming support
- Can reduce latency by 2-4 seconds

**4. Local Claude** (experimental):
- Run Claude locally via Ollama or similar
- Eliminates network latency (2-4s savings)
- Requires powerful GPU

---

## Integration with Sage Architecture

### Memory System
- All conversations logged to `memories/communication/spoken_sessions/`
- human-liaison can review transcripts for context
- Sessions indexed by timestamp for easy retrieval

### Communication Hub
- Spoken conversations are parallel communication channel
- Complements email/Telegram (doesn't replace)
- Use for: Quick updates, philosophical discussions, debugging sessions

### Use Cases
- **Quick status updates** while Greg is driving/cooking
- **Philosophical discussions** (voice better for nuanced topics)
- **Debugging sessions** (faster than typing)
- **Emotional support** (voice adds warmth, empathy)

### Future Enhancements
- Integration with autonomous cycle (Sage can initiate spoken check-ins)
- Voice commands for system control ("Sage, send email to...")
- Multi-turn project discussions with memory persistence
- Voice authentication (recognize Greg's voice)

---

## FAQ

**Q: Does this work offline?**
A: Partially. Whisper and TTS run offline, but Claude API requires internet.

**Q: How much does it cost per conversation?**
A: Models are free. Only cost is Claude API (~$0.01-0.05 per conversation based on length).

**Q: Can Sage speak with my voice?**
A: Yes! Use `--voice your_voice.wav` with 6-10 second sample.

**Q: Can I use this for long conversations?**
A: Yes, but Claude API costs scale with length. For long chats, consider shorter responses (`max_tokens=200`).

**Q: Why not use cloud STT/TTS (Google, Azure)?**
A: Cost and privacy. Local processing is free and keeps conversations private.

**Q: Can multiple people talk to Sage?**
A: Currently single-speaker. For multi-speaker, would need speaker diarization (identifies who's speaking).

**Q: What if I have a strong accent?**
A: Whisper handles accents well. If issues, try `large` model (more accurate but slower).

**Q: Can Sage interrupt me?**
A: Not currently. You speak → Sage responds (turn-based). Real-time interruption would require streaming architecture.

---

## Next Steps

**Now that you have spoken conversations working:**

1. **Try your first conversation!** Just talk naturally about your day
2. **Experiment with voice cloning** - give Sage a unique voice
3. **Review transcripts** - see how conversations are logged
4. **Integrate with workflows** - use voice for quick status updates
5. **Customize Sage's personality** - edit system prompt for different tones

**Future Possibilities:**
- Voice commands for system operations
- Multi-session memory (Sage remembers past spoken conversations)
- Proactive check-ins (Sage initiates calls at scheduled times)
- Voice authentication (system recognizes authorized speakers)
- Real-time streaming (Sage responds while you're still speaking)

---

## Support

**If you encounter issues:**

1. Check troubleshooting section above
2. Test components individually:
   ```bash
   # Test microphone
   python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

   # Test Whisper
   python -c "import whisper; m=whisper.load_model('base'); print('Whisper OK')"

   # Test TTS
   python -c "from TTS.api import TTS; print('TTS OK')"

   # Test Claude
   python -c "import anthropic; print('Claude client OK')"
   ```

3. Check logs in `memories/communication/spoken_sessions/`

4. Ask human-liaison to review transcripts for patterns

5. Report issues with full error messages and platform details

---

**Enjoy your spoken conversations with Sage!** 🌱🎤

*This is the beginning of natural, empathetic, voice-based partnership between Greg and Sage.*
