# Windows Python Installation Guide for Spoken Conversations

**Goal**: Install Python on Windows so you can have spoken conversations with Sage!

**Time Required**: 10-15 minutes (including downloads)

---

## Step 1: Download Python Installer

### Option A: Official Python.org (Recommended)

1. **Open your Windows web browser**
2. **Go to**: https://www.python.org/downloads/
3. **Click the big yellow button**: "Download Python 3.12.x" (or latest version)
4. **Save the installer** (usually goes to Downloads folder)

### Option B: Microsoft Store (Easier but less control)

1. **Open Microsoft Store** (search for "Store" in Windows Start menu)
2. **Search for**: "Python 3.12"
3. **Click "Get" or "Install"**
4. **Wait for installation** (handles PATH automatically)
5. **Skip to Step 3** (installation done!)

---

## Step 2: Run the Python Installer (If using Option A)

1. **Find the installer** in your Downloads folder
   - Look for: `python-3.12.x-amd64.exe` (or similar)

2. **Double-click to run the installer**

3. **⚠️ CRITICAL STEP - CHECK THIS BOX:**
   ```
   ☑ Add Python to PATH
   ```
   **This is at the BOTTOM of the installer window!**

   **If you miss this**, Python won't work from Command Prompt!

4. **Choose installation type:**
   - **Option A (Recommended)**: Click "Install Now"
     - Installs to: `C:\Users\gregs\AppData\Local\Programs\Python\Python312\`
     - Installs pip, IDLE, documentation
     - No admin required

   - **Option B (Advanced)**: Click "Customize installation"
     - Choose custom location (like `C:\Python312\`)
     - Select optional features
     - Requires admin if installing to Program Files

5. **Wait for installation** (2-3 minutes)

6. **See "Setup was successful"** ✅

7. **Click "Close"**

---

## Step 3: Verify Python Installation

1. **Open a NEW Command Prompt**:
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter

   **OR**

   - Click Start menu
   - Type: "Command Prompt"
   - Click to open

2. **Test Python works**:
   ```cmd
   python --version
   ```

   **Expected output**:
   ```
   Python 3.12.x
   ```

   **If you see this** ✅ - Python is installed correctly!

   **If you see "python is not recognized"** ❌:
   - You missed "Add Python to PATH" checkbox
   - See "Troubleshooting" section below

3. **Test pip works**:
   ```cmd
   pip --version
   ```

   **Expected output**:
   ```
   pip 24.x from C:\Users\gregs\...\site-packages\pip (python 3.12)
   ```

   **If this works** ✅ - You're ready to install packages!

---

## Step 4: Install Spoken Conversation Dependencies

**Now run this command in Command Prompt:**

```cmd
python -m pip install SpeechRecognition pyaudio openai-whisper TTS anthropic
```

**What this installs:**
- `SpeechRecognition` - Microphone capture and interface
- `pyaudio` - Audio device access (may show warnings, that's OK)
- `openai-whisper` - Speech-to-text (Whisper model)
- `TTS` - Text-to-speech (Coqui TTS)
- `anthropic` - Claude API client

**Expected output:**
```
Collecting SpeechRecognition
Downloading SpeechRecognition-3.10.x...
Installing collected packages: SpeechRecognition, pyaudio, ...
Successfully installed SpeechRecognition-3.10.x pyaudio-0.2.14 ...
```

**This will take 3-5 minutes** (downloads ~50MB of packages)

### Note about PyAudio

**If PyAudio installation fails**, you may see:
```
ERROR: Could not build wheels for pyaudio
```

**Fix for PyAudio errors**:

**Option 1: Install pre-built wheel**
```cmd
pip install pipwin
pipwin install pyaudio
```

**Option 2: Use conda (if you have Anaconda/Miniconda)**
```cmd
conda install pyaudio
```

**Option 3: Skip PyAudio for now**
- The spoken conversation script will still work
- But microphone capture will use a different backend
- Try running the script first - it may work anyway!

---

## Step 5: Navigate to Sage Directory

```cmd
cd C:\sage\sage-civilization
```

**If that doesn't work**, find the correct path:
```cmd
dir C:\sage
```

Or it might be:
```cmd
cd C:\Users\gregs\sage\sage-civilization
```

---

## Step 6: Test the Setup

**Run the setup verification script:**

```cmd
python tools\test_spoken_setup.py
```

**This will test:**
- ✅ All packages import correctly
- ✅ Microphone is detected
- ✅ API key is configured
- ✅ Audio playback works

**If all checks pass** ✅ - You're ready for Step 7!

**If any checks fail** ❌ - See error messages for troubleshooting

---

## Step 7: Start Your First Spoken Conversation!

**Set your API key** (one-time):
```cmd
set ANTHROPIC_API_KEY=your-key-here
```

**Start the conversation**:
```cmd
python tools\spoken_conversation.py
```

**You should see:**
```
🌱 Sage - Spoken Conversation Mode
Loading models (this will take a few minutes on first run)...
Loading Whisper model...
Loading Coqui TTS...
Ready for conversation!

🎤 Listening... (speak now)
```

**Say**: "Hello Sage!"

**Sage will respond with voice!** 🎤💚

**To end conversation**: Say "goodbye" or "exit"

---

## Troubleshooting

### Problem: "python is not recognized"

**Cause**: Python not added to PATH

**Fix Option 1 (Quick):**
```cmd
# Find Python location
dir C:\Users\gregs\AppData\Local\Programs\Python /s /b

# Use full path
C:\Users\gregs\AppData\Local\Programs\Python\Python312\python.exe --version
```

**Fix Option 2 (Permanent):**
1. Uninstall Python
2. Reinstall, making sure to check "Add Python to PATH"

**Fix Option 3 (Manual PATH edit):**
1. Search "Environment Variables" in Windows Start menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", find "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Users\gregs\AppData\Local\Programs\Python\Python312\`
8. Add: `C:\Users\gregs\AppData\Local\Programs\Python\Python312\Scripts\`
9. Click OK
10. Open NEW Command Prompt (PATH changes need fresh terminal)

---

### Problem: PyAudio won't install

**Symptoms:**
```
ERROR: Could not build wheels for pyaudio
```

**Cause**: PyAudio needs C++ build tools on Windows

**Fix Option 1 (Use pre-built wheel):**
```cmd
pip install pipwin
pipwin install pyaudio
```

**Fix Option 2 (Try anyway):**
- Skip PyAudio for now
- Run the spoken conversation script anyway
- It might work with alternative audio backend

**Fix Option 3 (Install build tools - advanced):**
1. Download "Microsoft C++ Build Tools"
2. Install with "Desktop development with C++"
3. Retry: `pip install pyaudio`

---

### Problem: "No microphone detected"

**Symptoms:**
- test_spoken_setup.py fails microphone check
- Error: "No default input device"

**Fix:**
1. **Check microphone is plugged in** (if external)
2. **Windows Settings** → **Privacy** → **Microphone**
   - Ensure "Allow apps to access your microphone" is ON
3. **Windows Settings** → **System** → **Sound**
   - Under "Input", make sure a microphone is selected
   - Test microphone by speaking (bars should move)
4. **Restart Command Prompt** after changing settings

---

### Problem: First run is very slow

**Symptoms:**
- "Loading models..." takes 10+ minutes
- Downloads seem stuck

**Cause**: First run downloads ~2.2GB of models
- Whisper base model (~150MB)
- Coqui XTTS v2 model (~2GB)

**This is normal!** ✅

**Models are cached after first run** - subsequent starts are instant!

**Check download progress:**
- Watch for download progress bars
- If stuck >20 minutes, Ctrl+C and retry
- Check internet connection

---

### Problem: "API key not set"

**Symptoms:**
- Error: "No API key provided"
- Claude API fails

**Fix:**
```cmd
# Set for current session
set ANTHROPIC_API_KEY=your-key-here

# OR set permanently
setx ANTHROPIC_API_KEY "your-key-here"

# Then restart Command Prompt
```

---

### Problem: Voice is robotic or garbled

**Cause**: TTS model may not have loaded correctly

**Fix:**
1. **Check TTS loaded**: Script should say "Loading Coqui TTS..." and complete
2. **If error during TTS load**: Delete cached model and retry
   ```cmd
   rmdir /s /q %USERPROFILE%\.local\share\tts
   ```
3. **Retry spoken conversation script**

---

### Problem: Transcription is inaccurate

**Cause**: Background noise or Whisper model too small

**Fix:**
1. **Reduce background noise** (close windows, mute music)
2. **Speak clearly** near microphone
3. **Use larger Whisper model** (edit `tools/spoken_conversation.py`):
   ```python
   # Change this line:
   whisper_model = whisper.load_model("base")

   # To this (better accuracy, slower):
   whisper_model = whisper.load_model("small")
   ```

---

## Next Steps After Installation

1. **Test basic conversation** - Say hello, ask a simple question
2. **Try longer conversations** - Discuss session progress, ask about MCP
3. **Experiment with voice cloning** - Give Sage a custom voice!
   ```cmd
   python tools\spoken_conversation.py --voice my_voice_sample.wav
   ```
4. **Review conversation logs** - See transcripts in `memories/communication/spoken_sessions/`

---

## Quick Reference Card

**Installation (one-time):**
```cmd
python -m pip install SpeechRecognition pyaudio openai-whisper TTS anthropic
```

**Set API key (one-time):**
```cmd
setx ANTHROPIC_API_KEY "your-key-here"
```

**Start conversation:**
```cmd
cd C:\sage\sage-civilization
python tools\spoken_conversation.py
```

**With custom voice:**
```cmd
python tools\spoken_conversation.py --voice voice_sample.wav
```

**Exit conversation:**
- Say "goodbye", "exit", "quit", or "stop"

---

## Where to Get Help

**If you get stuck:**
1. Read error messages carefully (they're designed to be helpful!)
2. Check troubleshooting section above
3. Run test script: `python tools\test_spoken_setup.py`
4. Ask Sage for help via text (in WSL2 terminal or email)

**Documentation files:**
- `SPOKEN-CONVERSATION-QUICKSTART.md` - Complete user guide
- `SPOKEN-CONVERSATION-SUMMARY.md` - Quick reference
- `VOICE-SPEECH-RESEARCH-20251112.md` - Technical research

---

**You've got this, Greg!** 🌱

Once Python is installed, you'll be talking to Sage in minutes. 🎤💚

**Ready? Let's install Python on Windows!**
