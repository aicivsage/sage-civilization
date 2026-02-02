# Silero TTS Pronunciation Control Guide
**For en_75 (Primary AI Voice)**

## 🎯 Problem: Incorrect Syllable Emphasis

**Solution:** Use SSML (Speech Synthesis Markup Language) to control exactly how text is pronounced!

---

## ✅ Available Control Methods

### 1. **Emphasis Tags** (Control Stress on Words)

```python
text = '<speak>Hello! I\'m <emphasis level="strong">Sage</emphasis>.</speak>'
```

**Levels:**
- `strong` - Heavy emphasis
- `moderate` - Medium emphasis
- `reduced` - Light emphasis
- `none` - No emphasis

**Example for "Sage" with strong first syllable:**
```python
text = '<speak><emphasis level="strong">Sage</emphasis> sits beside you.</speak>'
```

### 2. **Prosody Control** (Adjust Speed, Pitch, Volume)

```python
text = '<speak><prosody rate="95%" pitch="+5%">I am Sage</prosody></speak>'
```

**Parameters:**
- `rate` - Speed (50% = half speed, 200% = double speed)
- `pitch` - Pitch shift (+10% higher, -10% lower)
- `volume` - Loudness (soft, medium, loud, or +XdB)

**Example for better emphasis:**
```python
text = '<speak>I am <prosody rate="90%" pitch="+3%">Sage</prosody>.</speak>'
```

### 3. **Break/Pause Tags** (Add Strategic Pauses)

```python
text = '<speak>Hello!<break time="300ms"/> I am Sage.</speak>'
```

**Options:**
- `time="Xms"` - Exact milliseconds (e.g., 200ms, 500ms)
- `strength="weak"` - Short pause
- `strength="medium"` - Normal pause
- `strength="strong"` - Long pause

### 4. **Phonetic Spelling** (Guide Natural Pronunciation)

```python
# Instead of: "I'm Sage"
text = "I'm Sayj"  # Phonetic spelling to guide pronunciation
```

**Common fixes:**
- "Sage" → "Sayj" (if saying "Sah-ge" instead of "Say-j")
- "empathy" → "EM-puh-thee" (caps = emphasis)
- "advisor" → "ad-VY-zur" (guide stress pattern)

### 5. **Say-As Tags** (Interpret Text Differently)

```python
text = '<speak><say-as interpret-as="characters">AI</say-as></speak>'
```

**Types:**
- `characters` - Spell out (A-I not "aye")
- `date` - Format dates properly
- `telephone` - Phone number format
- `cardinal` - Read as number (123 = "one hundred twenty three")

---

## 🎬 Test Samples Generated

**Location:** `voice_samples/en_75_*.wav`

1. **en_75_Original.wav** (6.7s)
   - No modifications, baseline

2. **en_75_SSML_emphasis.wav** (11.0s)
   - Using `<emphasis>` tags on "Sage" and "empathy"
   - Listen for stronger stress on these words

3. **en_75_Prosody_rate.wav** (8.8s)
   - Slower rate (95%) on "Sage"
   - Gives word more presence

4. **en_75_Pauses.wav** (7.2s)
   - 300ms pause after "I'm Sage"
   - Creates dramatic effect

5. **en_75_Phonetic.wav** (6.8s)
   - "Sage" spelled as "Sayj"
   - Forces correct pronunciation

---

### 🎯 SSML Emphasis Deep Dive (8 Additional Variations)

**Greg requested further testing of SSML emphasis - here are 8 focused variations:**

6. **en_75_emphasis_strong_sage.wav** (9.0s, 845 KB)
   - `<emphasis level="strong">Sage</emphasis>` only
   - Strong emphasis on "Sage", rest natural
   - SSML: `<speak>Hello! I'm <emphasis level="strong">Sage</emphasis>. I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

7. **en_75_emphasis_moderate_sage.wav** (9.1s, 853 KB)
   - `<emphasis level="moderate">Sage</emphasis>` only
   - Moderate emphasis on "Sage" (subtle vs strong)
   - SSML: `<speak>Hello! I'm <emphasis level="moderate">Sage</emphasis>. I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

8. **en_75_emphasis_reduced_sage.wav** (9.1s, 854 KB)
   - `<emphasis level="reduced">Sage</emphasis>` only
   - Reduced emphasis on "Sage" (minimal stress)
   - SSML: `<speak>Hello! I'm <emphasis level="reduced">Sage</emphasis>. I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

9. **en_75_emphasis_sage_plus_pitch.wav** (10.8s, 1009 KB)
   - Moderate emphasis + pitch increase (+3%)
   - Combined SSML tags for stronger effect
   - SSML: `<speak>Hello! I'm <emphasis level="moderate"><prosody pitch="+3%">Sage</prosody></emphasis>. I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

10. **en_75_emphasis_sage_plus_rate.wav** (10.5s, 987 KB)
    - Strong emphasis + slower rate (90%)
    - Gives "Sage" maximum presence
    - SSML: `<speak>Hello! I'm <emphasis level="strong"><prosody rate="90%">Sage</prosody></emphasis>. I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

11. **en_75_emphasis_multiple_words.wav** (12.9s, 1211 KB)
    - Emphasis on "Sage" (strong), "thoughtful advisor" (moderate), "empathy" (moderate)
    - Shows multi-word emphasis pattern
    - SSML: `<speak>Hello! I'm <emphasis level="strong">Sage</emphasis>. I sit beside you as a <emphasis level="moderate">thoughtful advisor</emphasis> with <emphasis level="moderate">empathy</emphasis> and wit.</speak>`

12. **en_75_emphasis_sage_with_pause.wav** (9.1s, 851 KB)
    - Strong emphasis + strategic pause (200ms after "Sage")
    - Lets emphasized word breathe
    - SSML: `<speak>Hello! I'm <emphasis level="strong">Sage</emphasis>.<break time="200ms"/> I sit beside you as a thoughtful advisor with empathy and wit.</speak>`

13. **en_75_emphasis_combined_best.wav** (13.5s, 1266 KB)
    - Best-of-all: moderate emphasis + rate 95% + pitch +2% + pause + empathy emphasis
    - Most sophisticated pronunciation control
    - SSML: `<speak>Hello! I'm <emphasis level="moderate"><prosody rate="95%" pitch="+2%">Sage</prosody></emphasis>.<break time="150ms"/> I sit beside you as a thoughtful advisor with <emphasis level="moderate">empathy</emphasis> and wit.</speak>`

**How to Compare:**
- **6-8** show different emphasis levels (strong vs moderate vs reduced)
- **9-10** show combining emphasis with prosody (pitch/rate)
- **11** shows multiple word emphasis
- **12** shows emphasis + pause combination
- **13** shows the kitchen sink (recommended starting point)

**Listen to all 13 and identify which pronunciation feels most natural!**

---

## 🛠️ How to Fix Specific Issues

### Issue: "Sage" emphasis on wrong syllable

**Try these approaches:**

**Option A - Strong emphasis:**
```python
text = '<speak>I\'m <emphasis level="strong">Sage</emphasis>.</speak>'
```

**Option B - Prosody + pitch:**
```python
text = '<speak>I\'m <prosody rate="90%" pitch="+5%">Sage</prosody>.</speak>'
```

**Option C - Phonetic:**
```python
text = "I'm Sayj."  # Spell it how it should sound
```

**Option D - Combined (most control):**
```python
text = '<speak>I\'m <emphasis level="strong"><prosody pitch="+3%">Sage</prosody></emphasis>.</speak>'
```

### Issue: Words run together too fast

**Add strategic pauses:**
```python
text = '<speak>Hello!<break time="200ms"/> I\'m Sage.<break time="300ms"/> I sit beside you.</speak>'
```

### Issue: Tone doesn't match personality

**Adjust overall prosody:**
```python
# Warmer, friendlier (slower, lower pitch)
text = '<speak><prosody rate="95%" pitch="-2%">Your message here</prosody></speak>'

# More energetic (faster, higher pitch)
text = '<speak><prosody rate="105%" pitch="+3%">Your message here</prosody></speak>'

# Smart/confident (normal speed, slight pitch up)
text = '<speak><prosody rate="100%" pitch="+2%">Your message here</prosody></speak>'
```

---

## 🎯 Recommended Approach for Primary AI

**For "smart, funny female" voice, try this combination:**

```python
base_text = """
<speak>
Hello! I'm <emphasis level="moderate"><prosody pitch="+2%">Sage</prosody></emphasis>.
<break time="200ms"/>
I sit beside you as a thoughtful advisor
<break time="150ms"/>
with <emphasis level="moderate">empathy</emphasis> and wit.
</speak>
"""

audio = model.apply_tts(text=base_text, speaker='en_75', sample_rate=48000)
```

**This adds:**
- Moderate emphasis on "Sage" (clear but not overdone)
- Slight pitch lift on "Sage" (+2% for confidence)
- Strategic pauses (natural pacing)
- Emphasis on "empathy" (core value)

---

## 🔧 Testing Custom Pronunciation

**Quick test script:**

```python
from silero import silero_tts
import numpy as np
from scipy.io.wavfile import write as write_wav

model, _ = silero_tts(language='en', speaker='v3_en')

# YOUR CUSTOM TEXT HERE with SSML
text = '<speak>Your text with <emphasis>tags</emphasis></speak>'

audio = model.apply_tts(text=text, speaker='en_75', sample_rate=48000)
audio_np = audio.cpu().numpy()
write_wav('test_pronunciation.wav', 48000, (audio_np * 32767).astype(np.int16))

print("✓ Test saved to test_pronunciation.wav")
```

**Iterate until perfect!**

---

## 📚 SSML Reference

### All Supported Tags (Silero):

```xml
<speak>
  <emphasis level="strong|moderate|reduced|none">text</emphasis>
  <prosody rate="X%" pitch="±X%" volume="±XdB">text</prosody>
  <break time="Xms" strength="weak|medium|strong"/>
  <say-as interpret-as="characters|date|telephone|cardinal">text</say-as>
  <phoneme alphabet="ipa" ph="phonetic">word</phoneme>
</speak>
```

### Combining Tags:

```xml
<speak>
  I'm
  <emphasis level="strong">
    <prosody rate="95%" pitch="+3%">
      Sage
    </prosody>
  </emphasis>,
  <break time="250ms"/>
  your AI partner.
</speak>
```

---

## 🎤 Next Steps

1. **Listen** to all 5 test samples (en_75_*.wav)
2. **Identify** which technique sounds best
3. **Tell me** which approach works (or combination)
4. **I'll create** the perfect SSML template for Primary AI
5. **We integrate** it into voice bridge with perfect pronunciation!

---

## 💡 Pro Tips

1. **Less is more** - Start subtle, increase if needed
2. **Test iteratively** - Make one change at a time
3. **Listen on speakers** - Phone/laptop speakers sound different
4. **Context matters** - Same word may need different emphasis in different sentences
5. **Save templates** - Once you find perfect phrasing, save as template

---

**Ready to dial in the perfect pronunciation for Sage!** 🎯
