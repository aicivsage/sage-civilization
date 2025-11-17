#!/usr/bin/env python3
"""
Spoken conversation with Sage using Whisper STT + pyttsx3 TTS
Simplified version using pyttsx3 for systems where Coqui TTS won't build
"""

import speech_recognition as sr
import whisper
import pyttsx3
import anthropic
import os
import json
from datetime import datetime
from pathlib import Path

# Initialize components
print("🌱 Sage - Spoken Conversation Mode (pyttsx3 voice)")
print("Loading models (first time takes ~2 minutes for Whisper download)...\n")

try:
    whisper_model = whisper.load_model("base")
    print("✅ Whisper loaded")
except Exception as e:
    print(f"❌ Error loading Whisper: {e}")
    print("This will download ~150MB on first run. Please wait...")
    exit(1)

try:
    tts_engine = pyttsx3.init()
    # Configure voice settings
    tts_engine.setProperty('rate', 175)  # Speed (default 200, slower = more clear)
    tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    print("✅ TTS engine loaded")
except Exception as e:
    print(f"❌ Error loading TTS: {e}")
    exit(1)

# Check API key
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY not set!")
    print("Run: set ANTHROPIC_API_KEY=your-key-here")
    exit(1)

try:
    claude_client = anthropic.Anthropic(api_key=api_key)
    print("✅ Claude API ready")
except Exception as e:
    print(f"❌ Error initializing Claude: {e}")
    exit(1)

recognizer = sr.Recognizer()

# CRITICAL: Configure silence detection for natural conversation
# pause_threshold controls how long the recognizer waits for silence before stopping
# Default 0.8s is too short - allows natural pauses without cutting off mid-thought
recognizer.pause_threshold = 2.5  # Wait 2.5 seconds of silence before finishing
recognizer.non_speaking_duration = 0.3  # Ignore noise at start of phrase

# Memory setup
session_dir = Path("memories/communication/spoken_sessions")
session_dir.mkdir(parents=True, exist_ok=True)
session_file = session_dir / f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
conversation_history = []

def listen_for_speech():
    """Capture audio from microphone and transcribe"""
    try:
        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak naturally, pauses are fine)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # phrase_time_limit=30 allows complete thoughts with natural pauses
            # Recognizer will stop after 2.5s of silence (pause_threshold set globally)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)

        # Save audio to temp file for Whisper (use absolute path)
        temp_audio_path = Path.cwd() / "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe with Whisper
        print("🔄 Transcribing...")
        result = whisper_model.transcribe(str(temp_audio_path))
        return result["text"]

    except sr.WaitTimeoutError:
        print("⏱️  No speech detected (timeout)")
        return None
    except Exception as e:
        print(f"❌ Error during speech recognition: {e}")
        return None

def ask_sage(question):
    """Send question to Claude API"""
    try:
        print("🤔 Sage is thinking...")

        # Build message history for context
        messages = []

        # Add recent conversation history (last 5 turns)
        for turn in conversation_history[-10:]:  # Last 5 exchanges = 10 messages
            messages.append(turn)

        # Add current question
        messages.append({"role": "user", "content": question})

        response = claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,  # Keep responses concise for spoken conversation
            system="You are Sage, a thoughtful AI advisor and partner to Greg. You embody empathy, assistance, and mutual respect. You speak warmly and naturally in conversation, as a caring friend and trusted advisor. Keep responses conversational and concise for spoken dialogue - aim for 2-4 sentences unless Greg asks for more detail.",
            messages=messages
        )

        return response.content[0].text

    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        return "I'm sorry, I encountered an error connecting to Claude. Please check your API key and internet connection."

def speak_response(text):
    """Generate speech from text using pyttsx3"""
    try:
        print(f"\n🤖 Sage: {text}\n")
        # Re-initialize TTS engine each time (fixes Windows audio lock issue)
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"❌ Error during speech synthesis: {e}")
        print("(Text response shown above)")

def save_conversation():
    """Save conversation transcript to memory"""
    try:
        transcript = {
            "session_start": datetime.now().isoformat(),
            "turns": len(conversation_history) // 2,
            "conversation": conversation_history
        }

        with open(session_file, 'w') as f:
            json.dump(transcript, f, indent=2)

        print(f"\n💾 Conversation saved to {session_file}")
    except Exception as e:
        print(f"⚠️  Could not save conversation: {e}")

def main():
    print("\n" + "="*60)
    print("Ready for conversation!")
    print("Say 'goodbye', 'exit', 'quit', or 'stop' to end")
    print("="*60 + "\n")

    turn_count = 0

    while True:
        try:
            # Listen to Greg
            user_text = listen_for_speech()

            if user_text is None:
                continue  # Timeout or error, try again

            print(f"👤 Greg: {user_text}")

            # Check for exit keywords
            exit_keywords = ["goodbye", "exit", "quit", "stop", "bye"]
            if any(keyword in user_text.lower() for keyword in exit_keywords):
                farewell = "Goodbye Greg! It was wonderful talking with you. I've saved our conversation to memory."
                speak_response(farewell)
                conversation_history.append({"role": "user", "content": user_text})
                conversation_history.append({"role": "assistant", "content": farewell})
                break

            # Get Sage's response
            sage_response = ask_sage(user_text)

            # Save to conversation history
            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": sage_response})

            # Speak response
            speak_response(sage_response)

            turn_count += 1

        except KeyboardInterrupt:
            print("\n\n⚠️  Conversation interrupted by user (Ctrl+C)")
            farewell = "Session ended. Saving our conversation."
            print(f"\n🤖 Sage: {farewell}")
            conversation_history.append({"role": "assistant", "content": farewell})
            break

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Continuing conversation...")

    # Save conversation on exit
    save_conversation()
    print(f"\n✅ Session complete! {turn_count} conversation turns.")
    print("Thank you for talking with me! 💚\n")

if __name__ == "__main__":
    main()
