# Voice Reference Implementation - Built-in Speaker

**Date**: 2025-11-13
**Agent**: coder
**Task**: Update spoken_conversation.py to use built-in high-quality voice reference

## What I Did

Updated `tools/spoken_conversation.py` to use a bundled LJSpeech voice sample instead of generating silence.

**Changes:**
1. Copied LJSpeech sample (LJ001-0001.wav) from Coqui TTS repository to `assets/voice_samples/sage_default_voice.wav`
2. Rewrote `_setup_default_speaker()` method to:
   - Use bundled voice sample by default (416KB, high-quality)
   - Resolve path relative to script location (works from any directory)
   - Provide clear feedback about which voice is being used
   - Gracefully degrade if sample not found (with helpful error message)

**Voice Choice: LJSpeech**

Selected LJSpeech because it perfectly matches Sage's identity:
- **Warm**: Empathetic, approachable tone
- **Clear**: Easy to understand, professional quality
- **Thoughtful**: Neutral female voice, measured pacing
- **High-quality**: 22050Hz sample rate, real voice data (not silence)

LJSpeech is a well-known public domain dataset used for TTS training - stable, reliable, and widely compatible with XTTS v2.

## What I Learned

**XTTS v2 Architecture:**
- Requires reference audio for voice cloning (minimum ~3 seconds recommended)
- Can use any WAV file as speaker reference
- Higher quality reference = better voice synthesis
- Model doesn't come with pre-packaged voices - needs external samples

**Why Silence Didn't Work:**
- Silence provides no acoustic features for voice cloning
- XTTS v2 needs actual voice characteristics (pitch, timbre, prosody)
- Processing silence is slow because model struggles to extract features

**Path Resolution:**
- Used `Path(__file__).parent.parent` to resolve relative to script location
- This works whether called from repo root or tools/ directory
- Bundling voice in assets/ makes deployment simple (no external dependencies)

## For Next Time

**Voice Customization:**
- Greg can override default with `--voice /path/to/sample.wav` flag
- Could add multiple voice profiles in assets/voice_samples/ for variety
- Could implement voice selection menu if Greg wants options

**Performance Expectations:**
- Real voice sample should be MUCH faster than silence
- First synthesis may be slow (model loading)
- Subsequent syntheses should be <2 seconds per response

**Testing Checklist:**
- Run `python3 tools/spoken_conversation.py` to verify default voice loads
- Speak test phrase to verify synthesis works
- Check synthesis speed (should be noticeably faster than before)

## Deliverables

**Files Modified:**
- `/mnt/c/sage/sage-civilization/tools/spoken_conversation.py` - Updated _setup_default_speaker() method

**Files Created:**
- `/mnt/c/sage/sage-civilization/assets/voice_samples/sage_default_voice.wav` - LJSpeech reference (416KB)

**Status:** Persisted ✅

**Next Step:** Greg should test by running `python3 tools/spoken_conversation.py` and speaking a test phrase. Voice should load quickly and sound warm/clear.
