#!/usr/bin/env python3
"""
Interactive Voice Control Panel for Silero TTS
Allows real-time adjustment of SSML parameters for en_75 voice
"""

import sys
import os
from silero import silero_tts
import numpy as np
from scipy.io.wavfile import write as write_wav

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def generate_sample(model, params, custom_text, speaker='en_75'):
    """Generate audio sample with given parameters"""

    # Build SSML text - Silero ONLY supports: rate, pitch, breaks
    # (emphasis and volume are NOT supported!)

    if params['use_prosody']:
        sage_markup = f'<prosody rate="{params["rate"]}%" pitch="{params["pitch"]:+d}%">SAGE</prosody>'
    else:
        sage_markup = 'SAGE'

    # Use custom text if provided, otherwise use default
    if custom_text and custom_text != "default":
        # Replace [SAGE] placeholder with prosody-controlled SAGE
        text = f'<speak>{custom_text.replace("[SAGE]", sage_markup)}</speak>'
    else:
        # Default text
        text = f'<speak>Hello!'

        if params['pause_before'] > 0:
            text += f'<break time="{params["pause_before"]}ms"/>'

        text += f" I'm {sage_markup}."

        if params['pause_after'] > 0:
            text += f'<break time="{params["pause_after"]}ms"/>'

        text += ' I sit beside you as a thoughtful advisor with empathy and wit.</speak>'

    # Generate audio - USE ssml_text PARAMETER, NOT text!
    audio = model.apply_tts(ssml_text=text, speaker=speaker, sample_rate=48000)
    audio_np = audio.cpu().numpy()

    return audio_np, text

def save_sample(audio_np, filename):
    """Save audio to WAV file"""
    os.makedirs('voice_samples', exist_ok=True)
    filepath = f"voice_samples/{filename}"
    write_wav(filepath, 48000, (audio_np * 32767).astype(np.int16))
    return filepath

def show_menu(params, custom_text):
    """Display current parameters and menu"""
    clear_screen()
    print("=" * 70)
    print("🎤 SAGE VOICE CONTROL PANEL - en_75 Interactive Tuning")
    print("=" * 70)
    print()
    print("CURRENT PARAMETERS (Silero-supported only):")
    print(f"  1. Use Prosody:        {params['use_prosody']}")
    if params['use_prosody']:
        print(f"  2. Rate (speed):       {params['rate']}%  (lower = slower = more prominent)")
        print(f"  3. Pitch:              {params['pitch']:+d}%  (higher = more confident)")
    print(f"  4. Pause Before SAGE:  {params['pause_before']}ms")
    print(f"  5. Pause After SAGE:   {params['pause_after']}ms")
    print()
    if custom_text and custom_text != "default":
        print(f"CUSTOM TEXT: {custom_text[:60]}{'...' if len(custom_text) > 60 else ''}")
        print()
    print("ACTIONS:")
    print("  [1-5] Adjust parameter")
    print("  [T]   Enter custom text (use [SAGE] as placeholder)")
    print("  [G]   Generate & save sample")
    print("  [P]   Preview SSML markup")
    print("  [R]   Reset to defaults")
    print("  [Q]   Quit")
    print()
    print("=" * 70)

def adjust_parameter(params, choice):
    """Adjust a specific parameter"""
    if choice == '1':
        toggle = input("Use prosody controls? (y/n): ").strip().lower()
        params['use_prosody'] = (toggle == 'y')

    elif choice == '2' and params['use_prosody']:
        try:
            new_val = int(input("Enter rate % (50-200, default 100): ").strip())
            if 50 <= new_val <= 200:
                params['rate'] = new_val
        except ValueError:
            print("Invalid number.")

    elif choice == '3' and params['use_prosody']:
        try:
            new_val = int(input("Enter pitch % (-10 to +10): ").strip())
            if -10 <= new_val <= 10:
                params['pitch'] = new_val
        except ValueError:
            print("Invalid number.")

    elif choice == '4':
        try:
            new_val = int(input("Enter pause before SAGE (ms, 0-1000): ").strip())
            if 0 <= new_val <= 1000:
                params['pause_before'] = new_val
        except ValueError:
            print("Invalid number.")

    elif choice == '5':
        try:
            new_val = int(input("Enter pause after SAGE (ms, 0-1000): ").strip())
            if 0 <= new_val <= 1000:
                params['pause_after'] = new_val
        except ValueError:
            print("Invalid number.")

def get_default_params():
    """Return default parameters (Silero-supported only)"""
    return {
        'use_prosody': True,
        'rate': 70,      # SLOW = more prominent
        'pitch': 8,      # HIGH = confident
        'pause_before': 300,
        'pause_after': 400
    }

def main():
    print("Loading Silero TTS model...")
    model, _ = silero_tts(language='en', speaker='v3_en')
    print("✓ Model loaded!\n")

    params = get_default_params()
    custom_text = "default"
    sample_counter = 1

    while True:
        show_menu(params, custom_text)
        choice = input("Choose action: ").strip().upper()

        if choice == 'Q':
            print("\n👋 Goodbye!\n")
            break

        elif choice in ['1', '2', '3', '4', '5']:
            adjust_parameter(params, choice)

        elif choice == 'T':
            print("\n📝 Enter your custom text.")
            print("   Use [SAGE] where you want SAGE with prosody controls.")
            print("   Example: Hello! I'm [SAGE], your AI assistant.")
            print()
            new_text = input("Text: ").strip()
            if new_text:
                custom_text = new_text
                print(f"\n✓ Custom text set!")
            else:
                custom_text = "default"
                print(f"\n✓ Reset to default text")
            input("Press Enter to continue...")

        elif choice == 'G':
            print("\n🎵 Generating sample...")
            audio_np, ssml_text = generate_sample(model, params, custom_text)

            filename = f"en_75_custom_{sample_counter:03d}.wav"
            filepath = save_sample(audio_np, filename)

            duration = len(audio_np) / 48000
            size_kb = os.path.getsize(filepath) / 1024

            print(f"\n✅ Sample saved!")
            print(f"   File: {filepath}")
            print(f"   Duration: {duration:.1f}s")
            print(f"   Size: {size_kb:.0f} KB")
            print(f"\n📝 SSML used:")
            print(f"   {ssml_text}")

            sample_counter += 1
            input("\nPress Enter to continue...")

        elif choice == 'P':
            _, ssml_text = generate_sample(model, params, custom_text)
            print(f"\n📝 SSML Preview:")
            print(f"{ssml_text}")
            input("\nPress Enter to continue...")

        elif choice == 'R':
            params = get_default_params()
            custom_text = "default"
            print("\n🔄 Reset to defaults (params + text)")
            input("Press Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
        sys.exit(0)
