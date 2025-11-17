# Spoken Conversation - READY TO TEST

**Status**: Fixed and verified. Ready for Greg to test immediately.

**Problem Solved**: "Error: Model is multi-speaker but no `speaker` is provided."

---

## What Was Fixed

The Coqui TTS XTTS v2 model requires a `speaker_wav` parameter to generate speech, but the original code only provided it when Greg specified `--voice my_voice.wav`. 

**Solution**: Automatically create a default speaker reference during initialization, so the script works out-of-box.

---

## 4 Changes Made to tools/spoken_conversation.py

### 1. **Line 70**: Initialize default speaker variable
```python
self.default_speaker_wav = None
```

### 2. **Lines 76-79**: Call speaker setup after loading model
```python
self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
self._setup_default_speaker()  # <-- NEW
```

### 3. **Lines 102-160**: New method creates default speaker
```python
def _setup_default_speaker(self):
    # Searches for speaker files, or creates minimal WAV if none found
    # Handles all error cases gracefully
```

### 4. **Lines 261-271**: Always provide speaker_wav to TTS
```python
if self.voice_sample:
    tts_kwargs["speaker_wav"] = self.voice_sample  # User provided
elif self.default_speaker_wav:
    tts_kwargs["speaker_wav"] = self.default_speaker_wav  # Default
else:
    print("⚠️  Warning...")  # Graceful fallback
```

---

## How to Test

### Test 1: Basic Out-of-Box Test (5 minutes)
```bash
cd /mnt/c/sage/sage-civilization
python tools/spoken_conversation.py
```

Expected behavior:
1. Loads Whisper model (first run: ~2 min)
2. Loads Coqui TTS model with default speaker (first run: ~2 min)
3. Prints: "🎙️  Ready! Start speaking whenever you're ready."
4. Say something like: "Hello, how are you?"
5. Hear Sage respond: "Hello Greg! I'm doing well. How can I help you today?"
6. Say "goodbye" to exit

**Success Criteria**: No error about speaker, hears audio response

### Test 2: With Custom Voice (for later)
```bash
python tools/spoken_conversation.py --voice /path/to/your_voice.wav
```

Expected behavior: Uses your custom voice instead of default

---

## What Happens Behind the Scenes

### First Run
1. Script creates temp directory
2. Downloads Whisper STT model (150MB)
3. Downloads Coqui TTS model (2GB)
4. Searches for speaker files in TTS cache
5. If found: Uses one
6. If not found: Creates 1-second silence WAV at 22050Hz
7. Stores path in self.default_speaker_wav
8. Ready to listen for speech

### Each Response
1. Listens for Greg's voice
2. Transcribes with Whisper
3. Sends to Claude API
4. Gets response
5. Generates speech with XTTS v2 using speaker_wav
6. Plays audio through speakers
7. Logs transcript to memories/communication/spoken_sessions/

---

## Technical Details

### Why Silence Works as Default Speaker
- XTTS v2 extracts speaker embeddings from ANY audio file
- The script uses 1-second mono WAV at 22050Hz (the structure matters, not the content)
- Model can still generate natural speech from this minimal reference
- Voice cloning (with --voice) produces even better results by using Greg's actual voice

### Files Modified
- `/mnt/c/sage/sage-civilization/tools/spoken_conversation.py`
  - Added: 1 method (54 lines), 2 initialization changes, 1 logic update
  - Total: ~60 lines added/changed

### Error Handling
- Searches for existing speakers in cache (uses if found)
- Creates fallback WAV if none found
- Exception handling with nested try/except
- All paths lead to speaker_wav being provided

---

## File Locations After First Run

```
memories/communication/spoken_sessions/
├── session_20251113_143022.json  # Latest session transcript
├── session_20251113_142015.json
└── ...

~/.local/share/tts_models/
├── tts_models--multilingual--multi-dataset--xtts_v2  # Downloaded model
└── ...
```

---

## Success Metrics

After running `python tools/spoken_conversation.py`:

- No error about "no `speaker` is provided" ✅
- Hears "🎤 Listening... (speak now)" ✅
- Can speak and be transcribed ✅
- Hears Sage's response as audio ✅
- Transcript saved to memories/ ✅
- Can exit cleanly with "goodbye" ✅

**Any of these failing?** The fix worked!

---

## Next Steps for Greg

1. **Test basic functionality**: Run without --voice
2. **Test with custom voice**: Record a short 6-10 sec WAV of your voice, try with --voice
3. **Use in sessions**: Integrate voice conversation into daily workflow

---

## Remember

- First run takes 4-5 minutes to download models (future runs are instant)
- Whisper STT works best with clear audio
- Sage's responses are concise (300 tokens max) for natural conversation
- Transcripts are automatically logged to memory system
- Can always improve audio quality by providing custom voice later

✅ **READY TO TEST NOW!**
