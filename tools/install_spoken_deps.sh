#!/bin/bash
#
# Sage Spoken Conversation Dependencies Installer
# Installs all required packages for voice conversation with Sage
#
# Usage: bash tools/install_spoken_deps.sh
#
# Components installed:
#   - SpeechRecognition: Audio capture and microphone interface
#   - PyAudio: Low-level audio I/O
#   - OpenAI Whisper: Speech-to-text transcription
#   - Coqui TTS: Text-to-speech synthesis with voice cloning
#   - Anthropic: Claude API client
#
# First run downloads:
#   - Whisper base model: ~150MB
#   - Coqui XTTS v2 model: ~2GB
#   Total: ~2.2GB (cached after first run)
#

set -e  # Exit on error

echo "======================================================"
echo "Sage Spoken Conversation - Dependency Installation"
echo "======================================================"
echo ""

# Detect platform
PLATFORM="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if grep -qi microsoft /proc/version 2>/dev/null; then
        PLATFORM="wsl2"
    else
        PLATFORM="linux"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PLATFORM="windows"
fi

echo "Detected platform: $PLATFORM"
echo ""

# WSL2 warning
if [[ "$PLATFORM" == "wsl2" ]]; then
    echo "⚠️  WARNING: WSL2 has limited microphone access!"
    echo ""
    echo "Recommendation:"
    echo "  1. Install Python for Windows (not Linux in WSL)"
    echo "  2. Run this script in Windows CMD/PowerShell"
    echo "  3. Use Windows Python to run spoken_conversation.py"
    echo ""
    echo "This script will continue, but microphone may not work in WSL2."
    echo ""
    read -p "Continue installation in WSL2? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled. Please use Windows Python instead."
        exit 1
    fi
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "❌ Python 3.8+ required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip first."
    exit 1
fi

echo "✓ pip3 available"
echo ""

# Install system dependencies (Linux only)
if [[ "$PLATFORM" == "linux" ]] || [[ "$PLATFORM" == "wsl2" ]]; then
    echo "Installing system audio dependencies (requires sudo)..."

    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        apt-get update
        apt-get install -y portaudio19-dev python3-pyaudio alsa-utils
    else
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-pyaudio alsa-utils
    fi

    echo "✓ System audio dependencies installed"
    echo ""
fi

# macOS system dependencies
if [[ "$PLATFORM" == "macos" ]]; then
    echo "Checking for Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found. Install from https://brew.sh"
        echo "   Then install portaudio: brew install portaudio"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✓ Homebrew detected"
        if ! brew list portaudio &> /dev/null; then
            echo "Installing portaudio..."
            brew install portaudio
        fi
        echo "✓ portaudio available"
    fi
    echo ""
fi

# Python package installation
echo "Installing Python packages..."
echo "This will download ~2.2GB of models on first use"
echo ""

# Install packages
echo "[1/5] Installing SpeechRecognition..."
pip3 install --upgrade SpeechRecognition

echo ""
echo "[2/5] Installing PyAudio..."
if [[ "$PLATFORM" == "windows" ]]; then
    echo "Note: On Windows, if PyAudio fails, install from wheel:"
    echo "  https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio"
fi
pip3 install --upgrade pyaudio || echo "⚠️  PyAudio install failed. May need manual installation."

echo ""
echo "[3/5] Installing OpenAI Whisper (~150MB model download on first use)..."
pip3 install --upgrade openai-whisper

echo ""
echo "[4/5] Installing Coqui TTS (~2GB model download on first use)..."
pip3 install --upgrade TTS

echo ""
echo "[5/5] Installing Anthropic Claude API client..."
pip3 install --upgrade anthropic

echo ""
echo "✓ All Python packages installed!"
echo ""

# Test microphone access
echo "======================================================"
echo "Testing Microphone Access"
echo "======================================================"
echo ""

python3 - <<'EOF'
import sys
try:
    import speech_recognition as sr

    # List available microphones
    print("Detecting microphones...")
    mic_list = sr.Microphone.list_microphone_names()

    if not mic_list:
        print("❌ No microphones detected!")
        print("\nTroubleshooting:")
        print("  - Check microphone is plugged in")
        print("  - Check microphone permissions in system settings")
        print("  - If WSL2: Use Windows Python instead")
        sys.exit(1)

    print(f"✓ Found {len(mic_list)} microphone(s):")
    for i, name in enumerate(mic_list):
        print(f"  [{i}] {name}")

    print("\nTesting default microphone access...")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("✓ Microphone access successful!")
        print(f"  Sample rate: {source.SAMPLE_RATE} Hz")
        print(f"  Chunk size: {source.CHUNK}")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip3 install SpeechRecognition pyaudio")
    sys.exit(1)
except Exception as e:
    print(f"❌ Microphone test failed: {e}")
    print("\nTroubleshooting:")
    print("  - Check microphone permissions")
    print("  - Check audio drivers are installed")
    print("  - If WSL2: Must use Windows Python for microphone access")
    sys.exit(1)
EOF

MICROPHONE_STATUS=$?
echo ""

# Check ANTHROPIC_API_KEY
echo "======================================================"
echo "Checking Configuration"
echo "======================================================"
echo ""

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "Set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Or add to your shell profile (~/.bashrc or ~/.zshrc):"
    echo "  echo 'export ANTHROPIC_API_KEY=\"your-key-here\"' >> ~/.bashrc"
    echo ""
else
    echo "✓ ANTHROPIC_API_KEY is set"
fi

# Check working directory
CURRENT_DIR=$(pwd)
if [[ ! "$CURRENT_DIR" =~ sage-civilization$ ]]; then
    echo ""
    echo "⚠️  Not in sage-civilization directory"
    echo "   Current: $CURRENT_DIR"
    echo "   Expected: */sage-civilization"
    echo ""
fi

# Final summary
echo ""
echo "======================================================"
echo "Installation Complete!"
echo "======================================================"
echo ""

if [ $MICROPHONE_STATUS -eq 0 ]; then
    echo "✅ All components installed successfully"
    echo "✅ Microphone access verified"
else
    echo "⚠️  Installation complete but microphone test failed"
    echo "   Fix microphone issues before running spoken_conversation.py"
fi

echo ""
echo "On first run, the script will download:"
echo "  - Whisper base model: ~150MB"
echo "  - Coqui XTTS v2 model: ~2GB"
echo "  (Cached after first download)"
echo ""
echo "Usage:"
echo "  python3 tools/spoken_conversation.py"
echo ""
echo "With voice cloning:"
echo "  python3 tools/spoken_conversation.py --voice my_voice.wav"
echo ""
echo "See SPOKEN-CONVERSATION-QUICKSTART.md for detailed instructions"
echo ""

if [[ "$PLATFORM" == "wsl2" ]] && [ $MICROPHONE_STATUS -ne 0 ]; then
    echo "============================================================"
    echo "⚠️  WSL2 MICROPHONE WARNING"
    echo "============================================================"
    echo "Microphone test failed in WSL2. This is expected."
    echo ""
    echo "SOLUTION: Use Windows Python instead"
    echo ""
    echo "Steps:"
    echo "  1. Install Python for Windows (python.org)"
    echo "  2. Open Windows CMD or PowerShell"
    echo "  3. Navigate to project: cd \\path\\to\\sage-civilization"
    echo "  4. Run: python tools\\spoken_conversation.py"
    echo ""
fi
