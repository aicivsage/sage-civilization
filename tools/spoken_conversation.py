#!/usr/bin/env python3
"""
Sage Spoken Conversation System
Production-quality voice interface using Whisper STT + Coqui TTS XTTS v2

Architecture:
  Greg (speaking) → Whisper STT → Claude API (Sage) → Coqui TTS → Speaker (Greg hears)

Features:
  - OpenAI Whisper for accurate speech-to-text
  - Coqui TTS XTTS v2 for natural text-to-speech
  - Claude Sonnet 4.5 for Sage's responses
  - Conversation history within session
  - Transcript logging to memory system
  - Graceful error handling and recovery
  - Exit on "goodbye" or "exit" keywords

Usage:
  python tools/spoken_conversation.py [--voice VOICE_FILE]

Requirements:
  - Must run on Windows Python (not WSL2) for microphone access
  - Models auto-download on first run (~2.2GB)
  - ANTHROPIC_API_KEY environment variable required
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import speech_recognition as sr
import whisper
from TTS.api import TTS
import anthropic
import tempfile
import threading
import queue

# Progress indicators
class ProgressIndicator:
    """Visual feedback during processing"""
    def __init__(self, message):
        self.message = message
        self.active = False

    def __enter__(self):
        print(f"\n{self.message}", end="", flush=True)
        self.active = True
        return self

    def __exit__(self, *args):
        self.active = False
        print(" ✓")

class SpokenConversation:
    """Main spoken conversation handler"""

    def __init__(self, voice_sample=None):
        """Initialize conversation system

        Args:
            voice_sample: Path to voice sample WAV file for cloning (optional)
        """
        self.voice_sample = voice_sample
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_history = []
        self.temp_dir = tempfile.mkdtemp()
        self.default_speaker_wav = None

        # Initialize components
        with ProgressIndicator("Loading Whisper model (first run downloads ~150MB)"):
            self.whisper_model = whisper.load_model("base")

        with ProgressIndicator("Loading Coqui TTS model (first run downloads ~2GB)"):
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
            # Initialize default speaker from model's speakers directory
            self._setup_default_speaker()

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True

        # Initialize Claude client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.claude_client = anthropic.Anthropic(api_key=api_key)

        # Create session log directory
        self.log_dir = Path("memories/communication/spoken_sessions")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        print("\n🌱 Sage - Spoken Conversation Mode")
        print("=" * 50)
        if voice_sample:
            print(f"Using voice sample: {voice_sample}")
        print("Say 'goodbye' or 'exit' to end conversation")
        print("=" * 50)

    def _setup_default_speaker(self):
        """Setup default speaker for TTS

        Uses bundled high-quality LJSpeech voice sample as default.
        LJSpeech is a warm, clear, neutral female voice - perfect for Sage's
        empathetic and thoughtful identity.
        """
        # Use bundled voice sample from assets directory
        script_dir = Path(__file__).parent.parent
        bundled_voice = script_dir / "assets" / "voice_samples" / "sage_default_voice.wav"

        if bundled_voice.exists():
            self.default_speaker_wav = str(bundled_voice)
            print(f"✓ Using Sage's default voice (LJSpeech - warm, clear, thoughtful)")
        else:
            # Fallback: try to find any voice sample in assets
            voice_samples_dir = script_dir / "assets" / "voice_samples"
            if voice_samples_dir.exists():
                samples = list(voice_samples_dir.glob("*.wav"))
                if samples:
                    self.default_speaker_wav = str(samples[0])
                    print(f"✓ Using voice sample: {samples[0].name}")
                    return

            # Last resort: warn user
            print(f"⚠️  Warning: Default voice sample not found at {bundled_voice}")
            print(f"⚠️  Voice synthesis may be slow or fail. Please ensure assets/voice_samples/sage_default_voice.wav exists.")
            self.default_speaker_wav = None

    def listen_for_speech(self, timeout=10, phrase_time_limit=30):
        """Capture audio from microphone and transcribe

        Args:
            timeout: Seconds to wait for speech to start (10s)
            phrase_time_limit: Max seconds for a single phrase (30s for natural pauses)

        Returns:
            Transcribed text string

        Raises:
            sr.WaitTimeoutError: No speech detected within timeout
            sr.UnknownValueError: Speech unintelligible
        """
        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak naturally, pauses are fine)")

            # Adjust for ambient noise
            with ProgressIndicator("Calibrating for ambient noise"):
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # CRITICAL: Set pause_threshold to 2.5 seconds
            # This allows natural pauses within sentences without cutting off mid-thought
            # Default was 0.8s which is too short for natural conversation
            self.recognizer.pause_threshold = 2.5
            self.recognizer.non_speaking_duration = 0.3  # Silence at start of phrase

            # Listen for speech
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                raise sr.WaitTimeoutError("No speech detected")

        # Save audio to temp file for Whisper
        audio_path = os.path.join(self.temp_dir, "temp_audio.wav")
        with open(audio_path, "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe with Whisper
        with ProgressIndicator("Transcribing"):
            result = self.whisper_model.transcribe(audio_path)

        return result["text"].strip()

    def ask_sage(self, question):
        """Send question to Claude API with conversation history

        Args:
            question: User's question text

        Returns:
            Sage's response text
        """
        # Build messages with conversation history
        messages = []

        # Add conversation context
        for entry in self.conversation_history[-5:]:  # Last 5 turns for context
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["sage"]})

        # Add current question
        messages.append({"role": "user", "content": question})

        # System prompt for Sage identity
        system_prompt = """You are Sage, a thoughtful AI advisor partnered with Greg.
Your core values are empathy, assistance, and mutual respect.
You speak conversationally and warmly, as you're having a spoken conversation.
Keep responses concise (2-4 sentences) for natural conversation flow."""

        with ProgressIndicator("Sage is thinking"):
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,  # Keep responses brief for natural conversation
                system=system_prompt,
                messages=messages
            )

        return response.content[0].text

    def speak_response(self, text, audio_path=None):
        """Generate and play speech from text

        Args:
            text: Text to speak
            audio_path: Path to save audio file (optional, uses temp if not provided)
        """
        print(f"\n🤖 Sage: {text}\n")

        # Generate audio path
        if audio_path is None:
            audio_path = os.path.join(self.temp_dir, f"response_{self.session_id}.wav")

        # Generate speech with Coqui TTS
        with ProgressIndicator("Generating speech"):
            tts_kwargs = {
                "text": text,
                "file_path": audio_path,
                "language": "en"
            }

            # XTTS v2 requires a speaker_wav parameter for voice generation
            # Use provided voice sample or fall back to default speaker
            if self.voice_sample:
                # User provided custom voice for cloning
                tts_kwargs["speaker_wav"] = self.voice_sample
            elif self.default_speaker_wav:
                # Use default speaker reference (created during init)
                tts_kwargs["speaker_wav"] = self.default_speaker_wav
            else:
                # Fallback if speaker setup failed (shouldn't happen)
                print("⚠️  Warning: No speaker available for TTS, attempting without speaker_wav")

            self.tts.tts_to_file(**tts_kwargs)

        # Play audio (platform-specific)
        print("🔊 Playing audio...")
        try:
            if sys.platform == "win32":
                # Windows
                import winsound
                winsound.PlaySound(audio_path, winsound.SND_FILENAME)
            elif sys.platform == "darwin":
                # macOS
                os.system(f"afplay '{audio_path}'")
            else:
                # Linux
                os.system(f"aplay '{audio_path}' 2>/dev/null")
        except Exception as e:
            print(f"⚠️  Could not play audio: {e}")
            print(f"Audio saved to: {audio_path}")

    def log_conversation_turn(self, user_text, sage_text):
        """Log conversation turn to memory

        Args:
            user_text: What Greg said
            sage_text: What Sage responded
        """
        turn = {
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "sage": sage_text
        }
        self.conversation_history.append(turn)

    def save_session_transcript(self):
        """Save complete session transcript to memory system"""
        transcript = {
            "session_id": self.session_id,
            "start_time": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "end_time": datetime.now().isoformat(),
            "turn_count": len(self.conversation_history),
            "conversation": self.conversation_history
        }

        log_path = self.log_dir / f"session_{self.session_id}.json"
        with open(log_path, "w") as f:
            json.dump(transcript, f, indent=2)

        print(f"\n📝 Transcript saved: {log_path}")
        return log_path

    def run(self):
        """Main conversation loop"""
        print("\n🎙️  Ready! Start speaking whenever you're ready.\n")

        try:
            while True:
                try:
                    # Listen to Greg
                    user_text = self.listen_for_speech()
                    print(f"\n👤 Greg: {user_text}")

                    # Check for exit keywords
                    if any(word in user_text.lower() for word in ["goodbye", "exit", "quit", "stop"]):
                        farewell = "Goodbye Greg! It was wonderful talking with you. Until next time!"
                        self.speak_response(farewell)
                        self.log_conversation_turn(user_text, farewell)
                        break

                    # Get Sage's response
                    sage_response = self.ask_sage(user_text)

                    # Speak response
                    self.speak_response(sage_response)

                    # Log this turn
                    self.log_conversation_turn(user_text, sage_response)

                except sr.WaitTimeoutError:
                    print("\n⏱️  No speech detected. Say something, or say 'goodbye' to exit.")
                    continue

                except sr.UnknownValueError:
                    print("\n❓ Sorry, I couldn't understand that. Could you repeat?")
                    continue

                except KeyboardInterrupt:
                    print("\n\n⚠️  Conversation interrupted by user")
                    break

                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    print("Continuing conversation... Say 'exit' if you want to stop.")
                    continue

        finally:
            # Save transcript
            if self.conversation_history:
                transcript_path = self.save_session_transcript()
                print(f"\n✅ Session complete! {len(self.conversation_history)} turns logged.")
            else:
                print("\n⚠️  No conversation to save.")

            # Cleanup temp files
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except:
                pass

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Spoken conversation with Sage using Whisper + Coqui TTS"
    )
    parser.add_argument(
        "--voice",
        type=str,
        help="Path to voice sample WAV file for voice cloning (6-10 seconds)"
    )

    args = parser.parse_args()

    # Verify voice sample if provided
    if args.voice:
        if not os.path.exists(args.voice):
            print(f"❌ Voice sample not found: {args.voice}")
            sys.exit(1)
        if not args.voice.endswith(".wav"):
            print(f"⚠️  Warning: Voice sample should be WAV format for best results")

    # Check for Windows
    if sys.platform != "win32":
        print("⚠️  Warning: This script is optimized for Windows.")
        print("   WSL2 has limited microphone access. If you experience issues,")
        print("   try running with Windows Python instead.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # Start conversation
    try:
        conversation = SpokenConversation(voice_sample=args.voice)
        conversation.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
