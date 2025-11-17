# Microphone Silence Detection Fix - Extended Listening Window

**Date**: 2025-11-13
**Task**: Fix microphone cutting off Greg mid-sentence due to aggressive silence detection
**Status**: COMPLETE ✅

## Problem

Both spoken conversation scripts were terminating audio recording after only ~0.8 seconds of silence (the speech_recognition library default). This caused the system to cut off Greg's sentences mid-thought when he naturally paused between phrases.

Greg would say: "So what I'm thinking is... [pause while formulating next thought] ...we should approach this differently"

But the system would stop recording after the pause, missing "we should approach this differently".

## Root Cause

The speech_recognition library's `Recognizer` class uses:
- **pause_threshold**: How long to wait for silence before considering the phrase complete (DEFAULT: 0.8 seconds)
- **non_speaking_duration**: Silence at start of phrase to ignore (DEFAULT: 0.3 seconds)

These defaults are optimized for short commands/queries, not natural conversation with thinking pauses.

## Solution Applied

### Parameter Changes (Both Scripts)

**File 1: tools/spoken_conversation.py**
- Added `recognizer.pause_threshold = 2.5` (was implicit default 0.8)
- Added `recognizer.non_speaking_duration = 0.3` (kept default for clean start)
- Changed `phrase_time_limit=15` to `phrase_time_limit=30` (max duration for single phrase)
- Updated help text to say "speak naturally, pauses are fine"

**File 2: tools/spoken_conversation_pyttsx3.py**
- Added global configuration after recognizer initialization:
  ```python
  recognizer.pause_threshold = 2.5
  recognizer.non_speaking_duration = 0.3
  ```
- Changed `phrase_time_limit=15` to `phrase_time_limit=30`
- Updated help text: "speak naturally, pauses are fine"

### Why These Values Work

**pause_threshold = 2.5 seconds**
- Allows thinking pauses within sentences (typical: 0.5-2.0s for internal thought)
- Only stops recording when Greg goes silent for 2.5+ seconds (clear indication he's done)
- Matches natural human conversation rhythm

**phrase_time_limit = 30 seconds**
- Allows longer complete thoughts/multiple sentences
- Prevents timeout if Greg is being verbose (default 15s was too short)
- Still reasonable safety limit if someone speaks continuously

**non_speaking_duration = 0.3 seconds**
- Ignores brief false starts and background noise at phrase beginning
- Lets genuine speech capture begin cleanly

## Impact

Greg can now:
- Speak naturally with thinking pauses
- Complete full sentences without being cut off
- Have multi-sentence thoughts recorded as one phrase
- Pause to formulate ideas without system interruption

## Files Modified

1. `/mnt/c/sage/sage-civilization/tools/spoken_conversation.py`
2. `/mnt/c/sage/sage-civilization/tools/spoken_conversation_pyttsx3.py`

## Testing Recommendation

Test both scripts with:
1. A statement with internal pauses: "I think the best approach would be... [pause 1-2s] ...to start with research"
2. A multi-sentence response: "First, we should... Second, we need to... Finally, let's consider..."
3. Verify system captures full text without truncation

## Technical Notes

These parameters are properties of the `speech_recognition.Recognizer` class from the `SpeechRecognition` library. They control the internal audio frame analysis and silence detection algorithm. The changes are non-invasive and don't require model updates or dependencies.

Source: https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
