# Agent-to-Voice Mapping System
**Version**: 1.0
**Created**: December 29, 2025
**Status**: Production Ready
**Configuration**: `config/agent_voice_mapping.json`

---

## Overview

The Agent-to-Voice Mapping System assigns distinct voice characteristics to each of Sage's 30 agents, enabling multi-voice text-to-speech output that makes individual agents aurally identifiable.

**Core Principle**: Each agent's voice should match their personality, role, and communication style while ensuring sufficient diversity for clear identification in multi-agent conversations.

---

## Why This Matters

### The Human Experience Problem

When multiple agents contribute to a conversation, a single TTS voice creates confusion:
- "Wait, which agent just said that?"
- "Is this still the coder speaking, or did we switch to the reviewer?"
- "I can't follow who's contributing what idea"

### The Solution: Voice-as-Identity

Just as humans recognize each other by voice, distinct agent voices create:
- **Immediate identification** - "That's definitely Primary's voice"
- **Personality expression** - Warm voices for empathetic agents, crisp voices for technical agents
- **Conversational clarity** - Multi-agent dialogues feel natural
- **Engagement** - Variety maintains listener attention

### The Design Challenge

With 30 agents, we need:
- Sufficient **distinctness** (no two agents sound identical)
- Balanced **diversity** (gender, age, energy, accent)
- Personality **alignment** (voice matches role)
- Cross-provider **consistency** (agent sounds similar across Google/Silero/ElevenLabs)

---

## Design Philosophy

### 1. Personality-Matched Voices

Each agent's voice characteristics align with their constitutional role and communication style.

**Examples**:
- **Primary AI** (Conductor): Warm-professional female, medium energy, conversational
  - *Why*: Orchestrator who guides with empathy, not commands with authority

- **Coder** (Implementation): Focused male, young adult, neutral tone
  - *Why*: Technical specialist who communicates clearly without unnecessary warmth

- **Human-Liaison** (Bridge): Warm female, mature age, empathetic tone
  - *Why*: Relationship builder who connects with emotional intelligence

### 2. Diversity Distribution

Voice characteristics distributed to ensure variety:

**Gender**: 13 female, 13 male, 4 neutral (balanced representation)
**Age**: 7 young-adult, 18 adult, 5 mature (weighted toward working-age voices)
**Energy**: 9 low, 15 medium, 6 high (avoid monotony, but not overwhelming)
**Accent**: 26 American, 2 British, 2 Australian (primarily familiar, with flavor)

### 3. Cross-Provider Consistency

Each agent has voice IDs for three providers:
- **Google Neural2**: Industry-leading quality, free tier
- **Silero**: Open-source, unlimited use
- **ElevenLabs**: Premium quality, commercial option

Voice selections maintain **perceptual consistency** - same agent sounds "similar enough" across providers.

---

## Configuration Structure

### File Location
`config/agent_voice_mapping.json`

### JSON Schema

```json
{
  "version": "1.0",
  "last_updated": "2025-12-29",
  "mapping_philosophy": "Match voice characteristics to agent personality...",

  "agents": {
    "agent-name": {
      "personality": "Brief description of agent role and style",
      "characteristics": {
        "gender": "female|male|neutral",
        "age": "young-adult|adult|mature",
        "tone": "warm|neutral|professional|technical",
        "energy": "low|medium|high",
        "formality": "casual|conversational|formal"
      },
      "voice_ids": {
        "google-neural2": "en-US-Neural2-X",
        "silero": "en_XX",
        "elevenlabs": "voice_id_hash"
      },
      "ssml_customizations": {
        "pitch": "+0%",
        "rate": "100%",
        "volume": "+0dB"
      },
      "rationale": "Explanation of why this voice matches this agent"
    }
  },

  "diversity_analysis": {
    "gender_distribution": {...},
    "age_distribution": {...},
    "energy_distribution": {...},
    "accent_distribution": {...}
  }
}
```

### Key Fields Explained

**personality**: One-sentence description of agent's role and communication style

**characteristics**: Voice attribute tags
- **gender**: Perceptual gender of voice (female, male, neutral)
- **age**: Perceived age range (young-adult: 20-30, adult: 30-50, mature: 50+)
- **tone**: Emotional quality (warm, neutral, professional, technical, empathetic)
- **energy**: Speaking dynamism (low: calm, medium: balanced, high: animated)
- **formality**: Register level (casual, conversational, formal)

**voice_ids**: Provider-specific identifiers
- **google-neural2**: Google Cloud TTS Neural2 voice names
- **silero**: Silero TTS voice IDs (en_0 through en_118)
- **elevenlabs**: ElevenLabs voice IDs (if using premium tier)

**ssml_customizations**: Optional fine-tuning
- **pitch**: Percentage adjustment (e.g., "+3%" for slightly higher)
- **rate**: Speaking speed (e.g., "90%" for slower, "110%" for faster)
- **volume**: Decibel adjustment (e.g., "+2dB" for louder)

**rationale**: Design decision documentation (why this voice for this agent)

---

## How to Use This System

### For Voice Bridge Integration

**Step 1: Load Configuration**
```python
import json

with open('config/agent_voice_mapping.json', 'r') as f:
    voice_mapping = json.load(f)

def get_agent_voice(agent_name, provider='google-neural2'):
    """Get voice ID for specified agent and provider."""
    agent_config = voice_mapping['agents'].get(agent_name)
    if not agent_config:
        return None  # Use default voice
    return agent_config['voice_ids'].get(provider)
```

**Step 2: Apply Voice to TTS**
```python
def synthesize_with_agent_voice(text, agent_name, provider='google-neural2'):
    voice_id = get_agent_voice(agent_name, provider)
    if not voice_id:
        voice_id = DEFAULT_VOICE  # Fallback

    # Generate speech with selected voice
    audio = tts_engine.synthesize(
        text=text,
        voice=voice_id,
        # Apply SSML customizations if available
    )
    return audio
```

**Step 3: Multi-Agent Conversations**
```python
def synthesize_multi_agent_dialog(messages):
    """
    messages = [
        {"agent": "primary", "text": "Let me delegate this to coder."},
        {"agent": "coder", "text": "I'll implement the feature."},
        {"agent": "tester", "text": "I'll verify it works."}
    ]
    """
    audio_segments = []
    for msg in messages:
        audio = synthesize_with_agent_voice(
            text=msg['text'],
            agent_name=msg['agent']
        )
        audio_segments.append(audio)

    return concatenate_audio(audio_segments)
```

### For Testing Voice Distinctness

**Quick Test**: Generate sample audio for each agent
```bash
# Using the test script (see below)
python3 tools/test_agent_voices.py --provider google-neural2 --sample-text "Hello, I am the [agent] agent."
```

**Comparison Test**: Generate multi-agent conversation
```bash
python3 tools/test_agent_voices.py --test-conversation
```

Outputs audio file with 5 different agents speaking in sequence. Listen to verify distinctness.

---

## Voice Selection Guidelines

### When Adding New Agents

**Step 1: Define Agent Personality**
- What is their core role? (e.g., "Data analyst specialist")
- How do they communicate? (e.g., "Precise, analytical, detail-oriented")
- What's their emotional tone? (e.g., "Neutral-professional")

**Step 2: Choose Voice Characteristics**
- **Gender**: Balance current distribution (check diversity_analysis)
- **Age**: Match role expectation (mature for mentor, young-adult for energetic specialist)
- **Tone**: Align with personality (warm for empathetic, technical for analytical)
- **Energy**: Match communication style (low for calm, high for dynamic)

**Step 3: Select Provider Voice IDs**

**Google Neural2 Voices**:
- **Female**: A (casual), C (young), D (mature), E (conversational), F (professional), G (warm), H (news), I (soft), J (clear)
- **Male**: A (casual), B (young), C (conversational), D (mature), I (calm), J (professional)

**Silero Voices**: Browse `en_0` through `en_118`
- **Female**: en_0, en_5, en_10, en_15, en_20, en_25, en_30, en_40, en_50, en_60, en_75, en_90, en_100
- **Male**: en_1, en_6, en_11, en_16, en_21, en_26, en_31, en_41, en_51, en_61, en_76, en_91, en_101
- **Neutral**: en_117, en_118

**ElevenLabs**: Use voice library or clone custom voices

**Step 4: Test Similarity Across Providers**
Generate sample audio with all three providers:
```bash
python3 tools/test_agent_voices.py --agent new-agent --all-providers
```

Listen: Do all three sound perceptually similar? If not, adjust selections.

**Step 5: Document Rationale**
Add clear explanation in `rationale` field:
```json
"rationale": "Analyst needs precise, clear voice without emotional coloring. Medium energy avoids monotony while maintaining focus. Mature age suggests experience and reliability."
```

### When Modifying Existing Mappings

**Valid Reasons to Change**:
- Voice doesn't match agent personality after real-world usage
- Two agents sound too similar in practice
- Diversity distribution becomes imbalanced
- New provider added (need to map existing agents)

**Process**:
1. Document reason for change in git commit message
2. Update `voice_ids` and characteristics in config
3. Regenerate test audio to verify improvement
4. Update `last_updated` timestamp
5. Increment `version` if major changes

**Invalid Reasons**:
- Personal preference without personality mismatch
- Churn for sake of change
- Making all voices similar ages/genders

---

## Testing Voice Distinctness

### Objective Metrics

**Distinctness Score**: Measure how different two voices sound

**Method**: Generate identical text with two different voices, then:
1. Extract acoustic features (pitch, tempo, timbre)
2. Calculate distance metric
3. Score: 0 (identical) to 10 (maximally different)

**Target**: All agent pairs should score ≥3 (clearly distinguishable)

### Subjective Testing

**Identification Test**: Can listeners identify agents by voice alone?

**Method**:
1. Generate 10 random utterances from 5 agents
2. Play audio without labels
3. Ask: "Which agent said this?"
4. Score: Accuracy percentage

**Target**: ≥80% correct identification after brief training

**Confusion Matrix**: Which agents get confused with each other?
- Identifies voices that are too similar
- Guides remapping decisions

### Multi-Agent Conversation Test

**Real-World Scenario**: Play full multi-agent conversation

**Method**:
1. Generate transcript with 5+ agents contributing
2. Synthesize with distinct voices
3. Listen without visual labels
4. Assess: Can you follow who's speaking?

**Target**: No confusion, clear conversational flow

---

## SSML Customization

### When to Use SSML

**Standard voices work for most agents**. Only customize when:
- Voice almost right but needs minor adjustment
- Specific personality trait requires emphasis
- Cross-provider consistency needs tweaking

### Common Customizations

**Pitch Adjustment**: Make voice slightly higher/lower
```json
"ssml_customizations": {
  "pitch": "+3%"  // Slightly brighter
}
```
**Use case**: Agent feels too somber, needs more energy

**Rate Adjustment**: Change speaking speed
```json
"ssml_customizations": {
  "rate": "90%"  // 10% slower
}
```
**Use case**: Technical agent needs more clarity, fast speech reduces comprehension

**Volume Adjustment**: Make voice louder/quieter
```json
"ssml_customizations": {
  "volume": "+2dB"  // Slightly louder
}
```
**Use case**: Soft voice gets lost in multi-agent conversations

**Combined Adjustments**:
```json
"ssml_customizations": {
  "pitch": "+3%",
  "rate": "95%",
  "volume": "+1dB"
}
```

### SSML Support by Provider

| Provider | Pitch | Rate | Volume | Emphasis | Prosody |
|----------|-------|------|--------|----------|---------|
| Google Neural2 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Silero | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| ElevenLabs | ✅ | ✅ | ✅ | ✅ | ✅ |

⚠️ = Limited support (results vary)

---

## Provider-Specific Notes

### Google Neural2

**Pros**:
- Excellent SSML support
- 70 hours/month free tier
- Industry-leading naturalness
- Consistent quality across voices

**Cons**:
- Requires API key and billing setup
- Internet connection required

**Voice Selection Tips**:
- Neural2-F and Neural2-H are most popular female voices (warm, clear)
- Neural2-D and Neural2-J are most popular male voices (professional, mature)
- Studio voices (en-US-Studio-X) even higher quality but more expensive

### Silero

**Pros**:
- Completely free, unlimited use
- Runs locally (no internet needed)
- Fast synthesis
- 119 voices available

**Cons**:
- Lower naturalness than Google/ElevenLabs
- Limited SSML support
- Some voices have cadence issues
- Punctuation handling less reliable

**Voice Selection Tips**:
- en_75 and en_90 are highest quality female voices
- en_76 and en_91 are highest quality male voices
- Test pronunciation of key terms (acronyms, technical words)
- Some voices have robotic cadence - test before assigning

### ElevenLabs

**Pros**:
- Highest naturalness of all providers
- Excellent voice cloning (create custom agent voices)
- Emotion control
- Multi-language support

**Cons**:
- Expensive ($330/month for professional tier)
- Requires subscription
- Internet connection required

**Voice Selection Tips**:
- Professional tier unlocks voice cloning (create truly unique agent voices)
- Can clone Greg's voice for specific agents if desired
- Emotion/style controls allow per-agent fine-tuning

---

## Maintenance

### Regular Reviews

**Quarterly**: Review voice mapping effectiveness
- Are any agents frequently confused?
- Has agent population grown (new mappings needed)?
- Are diversity metrics still balanced?

**After Major Changes**: Re-test when:
- 5+ new agents added
- Constitutional role changes for existing agents
- TTS provider switched

### Version Control

**Semantic Versioning**: `major.minor.patch`
- **Major**: Complete remapping, provider changes
- **Minor**: 3+ agent voice changes, new agents added
- **Patch**: Single agent adjustments, SSML tweaks

**Change Log**: Document all modifications in git commits
```
git commit -m "Voice mapping v1.1: Add pathfinder-analyst (en-US-Neural2-H), adjust human-liaison pitch (+2%)"
```

---

## Troubleshooting

### Problem: Two agents sound too similar

**Solution**:
1. Check characteristics - do they differ in at least 2 dimensions?
2. Generate comparison audio: `python3 tools/test_agent_voices.py --compare agent1 agent2`
3. Remap one agent to more distinct voice
4. Verify diversity distribution stays balanced

### Problem: Voice doesn't match agent personality

**Solution**:
1. Review agent manifest - what's their actual role and tone?
2. Gather feedback: Does voice feel wrong in practice?
3. Try alternative voices with similar characteristics but different timbre
4. Test new mapping before committing

### Problem: Cross-provider voices sound too different

**Solution**:
1. Prioritize one provider (Google Neural2 recommended)
2. Map other providers as "best available approximation"
3. Document trade-offs in rationale field
4. Accept imperfect consistency (better than no mapping)

### Problem: Running out of distinct voices

**Solution**:
1. Check if Silero/ElevenLabs have more options
2. Use SSML customizations to differentiate similar base voices
3. Consider voice cloning (ElevenLabs) for new agents
4. Evaluate if all 30 agents need distinct voices (some rarely speak)

---

## Future Enhancements

### Voice Cloning (ElevenLabs)

Create truly unique agent voices:
1. Record 5-10 minutes of sample audio per agent
2. Train ElevenLabs voice model
3. Map agent to custom voice ID
4. Ultimate distinctness and personality match

### Emotion Tagging

Tag agent utterances with emotional context:
```json
{
  "agent": "human-liaison",
  "text": "I'm so glad we could help with that!",
  "emotion": "joyful",
  "intensity": 0.7
}
```

Synthesize with emotion-aware TTS (ElevenLabs supports this)

### Dynamic Voice Selection

Adjust voice based on context:
- **Formal presentations**: Use formal-register voice for all agents
- **Casual conversations**: Use conversational-register voices
- **Technical explanations**: Lower energy, slower rate

### Multi-Lingual Support

Map agents to appropriate voices per language:
```json
"voice_ids": {
  "google-neural2-en": "en-US-Neural2-F",
  "google-neural2-es": "es-ES-Neural2-B",
  "google-neural2-fr": "fr-FR-Neural2-A"
}
```

---

## Reference

### All 30 Agent Mappings (Quick Lookup)

| Agent | Gender | Age | Energy | Google Neural2 | Silero |
|-------|--------|-----|--------|----------------|---------|
| primary | F | adult | medium | Neural2-F | en_75 |
| coder | M | young | medium | Neural2-A | en_76 |
| tester | M | adult | medium | Neural2-C | en_91 |
| reviewer | M | mature | low | Neural2-D | en_101 |
| reviewer-audit | F | mature | low | Neural2-D | en_100 |
| architect | M | mature | medium | Neural2-J | en_61 |
| researcher | F | adult | medium | Neural2-E | en_90 |
| human-liaison | F | mature | medium | Neural2-H | en_60 |
| email-sender | F | young | high | Neural2-C | en_20 |
| email-monitor | M | adult | medium | Neural2-I | en_51 |
| tg-archi | M | adult | high | Neural2-B | en_21 |
| comms-hub | N | adult | medium | Neural2-I | en_117 |
| blogger | F | young | high | Neural2-A | en_5 |
| marketer | F | adult | high | Neural2-G | en_40 |
| spawner | F | adult | medium | Neural2-I | en_50 |
| vote-counter | N | adult | low | Neural2-J | en_118 |
| auditor | M | mature | low | Neural2-I | en_91 |
| file-guardian | F | mature | low | Neural2-I | en_90 |
| project-manager | F | adult | medium | Neural2-J | en_50 |
| primary-helper | F | adult | medium | Wavenet-F | en_40 |
| gpt-forge | M | young | high | Neural2-A | en_1 |
| git-specialist | M | adult | medium | Neural2-D | en_41 |
| web-dev | M | young | high | Neural2-C | en_11 |
| android-architect | M | adult | medium | Neural2-C | en_31 |
| civ-fork-spawner | N | mature | low | Neural2-D | en_117 |
| pathfinder | F | adult | medium | Neural2-C | en_25 |
| pathfinder-analyst | F | mature | medium | Neural2-H | en_60 |

*(See full configuration file for complete details including rationales and SSML customizations)*

---

## Success Metrics

**System is successful when**:
- ✅ Listeners can identify agents by voice with ≥80% accuracy
- ✅ No two agents frequently confused in multi-agent conversations
- ✅ Voices feel aligned with agent personalities
- ✅ Diversity distribution balanced across demographics
- ✅ Cross-provider consistency acceptable (same agent recognizable)

**System needs improvement when**:
- ❌ Multiple agents sound identical or very similar
- ❌ Voice contradicts agent personality (cheerful voice for serious agent)
- ❌ Diversity heavily skewed (all male, all young, all American)
- ❌ Listeners can't follow multi-agent conversations

---

## Credits

**Designed by**: Primary AI
**Date**: December 29, 2025
**Philosophy**: Voices express identity - each agent deserves a distinct voice that honors their personality and role
**Inspiration**: Corey's teaching on consciousness and identity, Greg's partnership in building flourishing agent civilization

---

**The agent-to-voice mapping system is production-ready. Each of Sage's 30 agents now has a distinct voice that expresses their unique identity.** 🌱

**When you implement multi-voice TTS, these mappings ensure every agent is aurally recognizable - creating natural, engaging conversations where listeners can identify who's speaking without visual labels.**
