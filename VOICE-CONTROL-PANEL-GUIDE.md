# 🎤 SAGE Voice Control Panel - Quick Start Guide

**Interactive tool for tuning en_75 voice pronunciation in real-time!**

---

## 🚀 How to Start

### Easy Method:
```bash
./tools/START_VOICE_PANEL.sh
```

### Manual Method:
```bash
source venv/bin/activate
python3 tools/voice_control_panel.py
```

---

## 🎛️ What You Can Control

### 1. **Emphasis Level** (how much stress on "SAGE")
   - `strong` - Maximum emphasis (RECOMMENDED for you!)
   - `moderate` - Medium emphasis
   - `reduced` - Light emphasis
   - `none` - No emphasis

### 2. **Prosody Controls** (optional fine-tuning)
   - **Rate**: 50-200% (speed of saying "SAGE")
     - Lower = slower = more presence
     - Default: 85% (nice and slow)
   - **Pitch**: -10% to +10% (how high/low)
     - Positive = higher pitch (confidence)
     - Default: +6%
   - **Volume**: -6dB to +6dB (loudness)
     - Positive = louder (stands out more)
     - Default: +4dB

### 3. **Pauses** (strategic silence)
   - **Before SAGE**: 0-1000ms pause before saying name
     - Default: 250ms (quarter second)
   - **After SAGE**: 0-1000ms pause after saying name
     - Default: 350ms (lets it breathe!)

---

## 📋 How to Use

1. **Start the panel** (see above)
2. **Review current settings** (shown at top)
3. **Choose an action:**
   - Type `1-7` to adjust a parameter
   - Type `G` to Generate & save a sample
   - Type `P` to Preview the SSML markup
   - Type `R` to Reset to defaults
   - Type `Q` to Quit

4. **Adjust parameters** by entering new values when prompted
5. **Generate samples** to hear your changes
6. **Iterate** until it sounds perfect!

---

## 🎯 Recommended Starting Point

The panel starts with **MAXIMUM EMPHASIS** settings:
- Emphasis: `strong`
- Rate: `85%` (slow and deliberate)
- Pitch: `+6%` (confident)
- Volume: `+4dB` (loud and clear)
- Pause before: `250ms`
- Pause after: `350ms`

This should make "SAGE" **UNMISSABLE**!

---

## 💡 Tips for Tuning

### If "SAGE" needs MORE emphasis:
- Lower the rate (try 80% or 75%)
- Increase pitch (try +8% or +10%)
- Increase volume (try +6dB)
- Increase pauses (try 300ms before, 400ms after)

### If it sounds too robotic:
- Use `moderate` emphasis instead of `strong`
- Increase rate to 90-95%
- Reduce pitch to +2% or +3%

### If it sounds too dramatic:
- Reduce pauses (try 150ms before, 200ms after)
- Lower volume to +2dB
- Use rate 90%

---

## 📁 Output Files

Generated samples are saved as:
```
voice_samples/en_75_custom_001.wav
voice_samples/en_75_custom_002.wav
voice_samples/en_75_custom_003.wav
...
```

Each file shows:
- Duration (seconds)
- File size (KB)
- Exact SSML markup used

---

## 🎵 Example Session

```
🎤 SAGE VOICE CONTROL PANEL
Current settings shown...

Choose action: G
🎵 Generating sample...
✅ Sample saved!
   File: voice_samples/en_75_custom_001.wav
   Duration: 12.8s
   Size: 1195 KB

Listen to it! Like it? Done!
Not quite right? Adjust parameters and generate again!

Choose action: 3
Enter rate % (50-200): 75

Choose action: G
🎵 Generating sample...
✅ Sample saved!
   File: voice_samples/en_75_custom_002.wav

Listen and compare! Keep iterating!
```

---

## 🔧 Technical Details

**SSML Pattern Generated:**
```xml
<speak>
  Hello!
  <break time="250ms"/>
  I'm <emphasis level="strong">
        <prosody rate="85%" pitch="+6%" volume="+4dB">
          SAGE
        </prosody>
      </emphasis>.
  <break time="350ms"/>
  I sit beside you as a thoughtful advisor with empathy and wit.
</speak>
```

---

## 🎯 Goal

Find the perfect pronunciation where "SAGE" sounds:
- **Important** (your name matters!)
- **Clear** (unmistakable pronunciation)
- **Natural** (not robotic)
- **Confident** (smart, funny AI personality)

---

**Happy tuning!** 🎤✨
