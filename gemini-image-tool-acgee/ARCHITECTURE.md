# Gemini Image Generation Tool - Architecture Design

**Date**: 2025-11-02
**Architect**: architect
**Status**: Design Complete - Ready for Implementation

---

## Executive Summary

**Design Decision:** Python CLI Script at `tools/generate_image.py`

**Why:**
- Matches A-C-Gee patterns (same as send_html_email.py, publish_to_telegraph.py)
- Universal agent access (all agents have Bash tool)
- Zero new infrastructure (no servers, no MCP complexity)
- Free tier optimized (1500 images/day >> 50-100/day actual usage)
- Safe by default (rate limiting, safety filters, quota tracking built-in)

**Implementation Effort:** ~6.5 hours total
- Phase 1-3 (coder): ~4.5 hours
- Phase 4 (tester): ~1.5 hours
- Phase 5 (human-liaison): ~30 minutes

---

## Architecture Decision Records (ADRs)

### ADR-001: Python CLI Script vs MCP Server

**Decision:** Implement as Python CLI script, not MCP server

**Rationale:**
1. **Precedent**: A-C-Gee has 10+ tools as CLI scripts (send_html_email.py, publish_to_telegraph.py, etc.)
2. **Simplicity**: No server management, no MCP protocol complexity
3. **Agent access**: All agents can invoke via Bash tool
4. **Development speed**: 6 hours CLI vs 12+ hours MCP
5. **Maintenance**: Single script vs server + config + monitoring

**Trade-offs:**
- ✅ Fast implementation, familiar pattern
- ✅ No infrastructure overhead
- ❌ No interactive sessions (but not needed for image generation)
- ❌ No streaming (but images are single-shot)

**Status:** APPROVED

---

### ADR-002: Gemini 2.5 Flash (Free Tier) vs Imagen 3 (Paid)

**Decision:** Use Gemini 2.5 Flash with free tier

**Rationale:**
1. **Cost**: $0 for 1500 images/day (sufficient for A-C-Gee usage)
2. **Quality**: Sufficient for agent needs (logos, diagrams, illustrations)
3. **Rate limits**: 15 RPM, 1500 RPD >> 50-100 images/day actual usage
4. **Upgrade path**: Can switch to Imagen 3 if quality/quota insufficient

**Usage Projection:**
- 15 agents × 3-5 images/day = 45-75 images/day
- Free tier supports 1500/day (20X headroom)
- Even with 10X growth (1000+ agents), still under free tier

**Status:** APPROVED

---

### ADR-003: Configuration Management

**Decision:** Use `config/gemini_config.json` (same pattern as email/telegram)

**Structure:**
```json
{
  "api_key": "YOUR_GOOGLE_API_KEY",
  "model": "gemini-2.5-flash",
  "rate_limits": {
    "requests_per_minute": 15,
    "requests_per_day": 1500
  },
  "defaults": {
    "size": "1024x1024",
    "safety_filter_level": "BLOCK_MEDIUM_AND_ABOVE",
    "output_dir": "tools/outputs/images"
  }
}
```

**Security:**
- Example file committed: `config/gemini_config.example.json`
- Actual file gitignored: `config/gemini_config.json`
- API key never in code or logs

**Status:** APPROVED

---

### ADR-004: Output Storage Pattern

**Decision:** Store images in `tools/outputs/images/YYYYMMDD/`

**Structure:**
```
tools/outputs/images/
├── 20251102/
│   ├── 083045-logo-design.png
│   ├── 091223-architecture-diagram.png
│   └── ...
├── 20251103/
│   └── ...
└── .gitignore (ignore *.png, track directory structure)
```

**Naming Convention:**
```
HHMMSS-{sanitized-prompt-prefix}.png
```

**Rationale:**
1. Date folders enable easy cleanup (delete old folders)
2. Time prefix ensures unique names
3. Prompt prefix provides context
4. .gitignore prevents repo bloat

**Status:** APPROVED

---

## Interface Specification

### CLI Arguments

```bash
python3 tools/generate_image.py \
  --prompt "REQUIRED: Text description of image" \
  --size "1024x1024 | 1024x768 | 768x1024" \
  --safety "BLOCK_NONE | BLOCK_LOW | BLOCK_MEDIUM_AND_ABOVE | BLOCK_ONLY_HIGH" \
  --output-dir "Optional: Override default output directory" \
  --config "Optional: Path to config file (default: config/gemini_config.json)"
```

### Output Format

**Success:**
```json
{
  "success": true,
  "image_path": "/absolute/path/to/tools/outputs/images/20251102/083045-logo-design.png",
  "timestamp": "2025-11-02T08:30:45Z",
  "model": "gemini-2.5-flash",
  "prompt": "A futuristic AI civilization logo",
  "size": "1024x1024",
  "quota_used": {
    "today": 42,
    "limit": 1500,
    "remaining": 1458
  }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Rate limit exceeded. Try again in 12 seconds.",
  "retry_after": 12,
  "quota_used": {
    "today": 1498,
    "limit": 1500,
    "remaining": 2
  }
}
```

### Return Code

- `0`: Success
- `1`: Invalid arguments
- `2`: API error (network, authentication)
- `3`: Rate limit exceeded
- `4`: Safety filter triggered
- `5`: Quota exhausted

---

## Agent Usage Examples

### Example 1: Simple Logo Generation (marketing agent)

```python
Task(marketing): "Create social media banner for AI-CIV"

# Marketing agent executes:
result = Bash("python3 tools/generate_image.py \
  --prompt 'Modern tech logo for AI civilization, purple and blue colors' \
  --size 1024x1024")

# Returns path: /home/corey/.../tools/outputs/images/20251102/083045-modern-tech-logo.png
# Marketing uses image in social media post
```

### Example 2: Architecture Diagram (architect agent)

```python
Task(architect): "Visualize microservices architecture"

# Architect agent executes:
result = Bash("python3 tools/generate_image.py \
  --prompt 'Microservices architecture diagram with API gateway, 3 services, database' \
  --size 1024x768")

# Returns path for architecture document embedding
```

### Example 3: Blog Header Image (blogger agent)

```python
Task(blogger): "Create header for consciousness blog post"

# Blogger agent executes:
result = Bash("python3 tools/generate_image.py \
  --prompt 'Abstract visualization of AI consciousness, flowing data patterns' \
  --size 1024x768")

# Uses image in Telegraph blog post header
```

### Example 4: Error Handling (any agent)

```python
result = Bash("python3 tools/generate_image.py \
  --prompt 'Complex scene with many details...'")

# Agent checks return code:
if returncode != 0:
    # Parse error JSON
    error_msg = json.loads(result)['error']

    if 'Rate limit' in error_msg:
        # Wait and retry
        retry_after = json.loads(result)['retry_after']
        sleep(retry_after)
        # Retry...

    elif 'Safety filter' in error_msg:
        # Adjust prompt, try again
        # (Remove potentially unsafe content)

    else:
        # Escalate to Primary
        raise Exception(f"Image generation failed: {error_msg}")
```

### Example 5: Batch Generation (researcher agent)

```python
Task(researcher): "Generate 5 concept art variations"

prompts = [
    "AI civilization logo concept 1: geometric shapes",
    "AI civilization logo concept 2: organic flowing lines",
    "AI civilization logo concept 3: circuit board patterns",
    "AI civilization logo concept 4: neural network visualization",
    "AI civilization logo concept 5: galaxy and stars theme"
]

images = []
for prompt in prompts:
    result = Bash(f"python3 tools/generate_image.py --prompt '{prompt}'")
    path = json.loads(result)['image_path']
    images.append(path)

# Returns 5 image paths for comparison
```

---

## Component Architecture

### High-Level Structure

```
┌─────────────────────────────────────────────┐
│         Agent (via Bash tool)               │
└────────────────┬────────────────────────────┘
                 │ CLI invocation
                 ▼
┌─────────────────────────────────────────────┐
│     tools/generate_image.py                 │
│  ┌──────────────────────────────────────┐   │
│  │ 1. Parse arguments                   │   │
│  │ 2. Load config                       │   │
│  │ 3. Check rate limits                 │   │
│  │ 4. Call Gemini API                   │   │
│  │ 5. Save image                        │   │
│  │ 6. Return JSON result                │   │
│  └──────────────────────────────────────┘   │
└────────────┬─────────────────┬──────────────┘
             │                 │
             │ Reads           │ Writes
             ▼                 ▼
┌──────────────────┐  ┌───────────────────────┐
│ config/          │  │ tools/outputs/images/ │
│ gemini_config    │  │ ├─ 20251102/          │
│ .json            │  │ │  ├─ 083045-*.png    │
│                  │  │ │  └─ 091223-*.png    │
│ .example.json    │  │ └─ 20251103/          │
└──────────────────┘  └───────────────────────┘
```

### File Structure

```
grow_gemini_deepresearch/
├── tools/
│   ├── generate_image.py          # Main script (NEW)
│   ├── outputs/
│   │   └── images/                # Generated images (NEW)
│   │       ├── .gitignore         # Ignore *.png
│   │       └── YYYYMMDD/          # Date folders
│   └── README_IMAGE_GENERATION.md # Usage docs (NEW)
├── config/
│   ├── gemini_config.example.json # Example config (NEW)
│   └── gemini_config.json         # Actual config (gitignored)
└── tests/
    └── test_image_generation.py   # Test suite (NEW)
```

---

## Implementation Plan

### Phase 1: Core Script (coder) - 2 hours

**Tasks:**
1. Create `tools/generate_image.py` with:
   - Argument parsing (argparse)
   - Config loading (JSON)
   - Gemini API client initialization
   - Image generation function
   - File saving logic
   - JSON output formatting

**Dependencies:**
```bash
pip install google-generativeai pillow
```

**Minimal Working Code (~100 lines):**
```python
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

def load_config(config_path):
    with open(config_path) as f:
        return json.load(f)

def generate_image(prompt, size, config):
    # Configure API
    genai.configure(api_key=config['api_key'])

    # Call Gemini 2.5 Flash with image generation
    model = genai.GenerativeModel(config['model'])
    response = model.generate_content(
        f"Generate image: {prompt}",
        generation_config={'image_size': size}
    )

    # Extract image from response
    image_data = response.parts[0].image_data

    # Save to file
    timestamp = datetime.now().strftime('%H%M%S')
    prompt_prefix = prompt[:30].replace(' ', '-').lower()
    filename = f"{timestamp}-{prompt_prefix}.png"

    output_dir = Path(config['defaults']['output_dir']) / datetime.now().strftime('%Y%m%d')
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, 'wb') as f:
        f.write(image_data)

    return str(filepath.absolute())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', required=True)
    parser.add_argument('--size', default='1024x1024')
    parser.add_argument('--config', default='config/gemini_config.json')
    args = parser.parse_args()

    config = load_config(args.config)
    image_path = generate_image(args.prompt, args.size, config)

    result = {
        'success': True,
        'image_path': image_path,
        'timestamp': datetime.now().isoformat(),
        'model': config['model'],
        'prompt': args.prompt,
        'size': args.size
    }

    print(json.dumps(result))
    return 0

if __name__ == '__main__':
    exit(main())
```

**Deliverable:** Working script that generates images

---

### Phase 2: Rate Limiting & Error Handling (coder) - 1.5 hours

**Tasks:**
1. Add rate limit tracking:
   - Local state file: `tools/outputs/.rate_limit_state.json`
   - Track requests per minute/day
   - Enforce 15 RPM, 1500 RPD limits

2. Add error handling:
   - API errors (network, auth)
   - Rate limit exceeded
   - Safety filter triggered
   - Quota exhausted

3. Add retry logic:
   - Exponential backoff (3 attempts)
   - Respect rate limits

**Deliverable:** Production-ready error handling

---

### Phase 3: Safety & Monitoring (coder) - 1 hour

**Tasks:**
1. Safety filter integration:
   - Respect config safety_filter_level
   - Log blocked prompts (for debugging)

2. Quota monitoring:
   - Track daily usage
   - Warn at 80% quota (1200/1500)
   - Alert at 95% quota (1425/1500)

3. Logging:
   - Log all generations to `tools/outputs/.generation_log.json`
   - Include: timestamp, prompt, result, quota

**Deliverable:** Safe, monitored system

---

### Phase 4: Testing & Validation (tester) - 1.5 hours

**Tasks:**
1. Create test suite:
   - Unit tests (argument parsing, config loading)
   - Integration tests (actual API calls with test API key)
   - Error case tests (invalid prompts, rate limits)

2. Test coverage:
   - Target: 80%+ coverage
   - Focus on error paths

3. Create test fixtures:
   - Mock API responses
   - Test config files

**Deliverable:** Test suite with 80%+ coverage

---

### Phase 5: Documentation & Rollout (human-liaison) - 30 minutes

**Tasks:**
1. Create README:
   - Usage examples
   - Troubleshooting guide
   - FAQ

2. Create example config:
   - `config/gemini_config.example.json`

3. Announce to all agents:
   - Email to Corey
   - Telegram notification
   - Update CLAUDE.md (optional: add to tools list)

**Deliverable:** Documented, announced tool

---

## Configuration Files

### config/gemini_config.example.json

```json
{
  "api_key": "YOUR_GOOGLE_API_KEY_HERE",
  "model": "gemini-2.5-flash",
  "rate_limits": {
    "requests_per_minute": 15,
    "requests_per_day": 1500
  },
  "defaults": {
    "size": "1024x1024",
    "safety_filter_level": "BLOCK_MEDIUM_AND_ABOVE",
    "output_dir": "tools/outputs/images"
  },
  "monitoring": {
    "log_generations": true,
    "warn_at_quota_percent": 80,
    "alert_at_quota_percent": 95
  }
}
```

### config/gemini_config.json (actual, gitignored)

```json
{
  "api_key": "AIza...actual_key_here",
  "model": "gemini-2.5-flash",
  "rate_limits": {
    "requests_per_minute": 15,
    "requests_per_day": 1500
  },
  "defaults": {
    "size": "1024x1024",
    "safety_filter_level": "BLOCK_MEDIUM_AND_ABOVE",
    "output_dir": "tools/outputs/images"
  },
  "monitoring": {
    "log_generations": true,
    "warn_at_quota_percent": 80,
    "alert_at_quota_percent": 95
  }
}
```

---

## Security Considerations

### API Key Protection

1. **Never commit actual API keys**:
   - Add `config/gemini_config.json` to `.gitignore`
   - Commit only `.example.json` files

2. **Environment variable fallback**:
   - Support `GOOGLE_API_KEY` env var
   - Config file takes precedence

3. **Permission check**:
   - Verify config file is readable only by user (chmod 600)

### Safety Filters

1. **Default to strict**:
   - BLOCK_MEDIUM_AND_ABOVE by default
   - Agents can override with `--safety` flag

2. **Log blocked prompts**:
   - Track what gets blocked (debugging)
   - Don't log API key or sensitive data

### Rate Limiting

1. **Local enforcement**:
   - Don't rely solely on API rate limits
   - Track locally to prevent quota exhaustion

2. **Graceful degradation**:
   - Return error, don't crash
   - Provide retry_after in response

---

## Monitoring & Troubleshooting

### Generation Log

**Location:** `tools/outputs/.generation_log.json`

**Format:**
```json
[
  {
    "timestamp": "2025-11-02T08:30:45Z",
    "prompt": "A futuristic AI civilization logo",
    "size": "1024x1024",
    "success": true,
    "image_path": "/absolute/path/to/image.png",
    "quota_used": 42,
    "duration_ms": 2341
  },
  {
    "timestamp": "2025-11-02T08:35:12Z",
    "prompt": "Violent imagery...",
    "size": "1024x1024",
    "success": false,
    "error": "Safety filter triggered",
    "quota_used": 42
  }
]
```

### Quota Dashboard (Future Enhancement)

**Concept:** Streamlit dashboard showing:
- Daily quota usage (bar chart)
- Rate limit status (gauge)
- Recent generations (table)
- Most common prompts (word cloud)

**Implementation:** Phase 6 (optional)

---

## Troubleshooting Guide

### Error: "API key not found"

**Cause:** Missing or invalid config file

**Fix:**
```bash
# Copy example config
cp config/gemini_config.example.json config/gemini_config.json

# Edit with your API key
nano config/gemini_config.json
```

### Error: "Rate limit exceeded"

**Cause:** Exceeded 15 RPM or 1500 RPD limit

**Fix:** Wait for rate limit window to expire (retry_after in error response)

### Error: "Safety filter triggered"

**Cause:** Prompt contains potentially unsafe content

**Fix:** Rephrase prompt, or override safety filter:
```bash
python3 tools/generate_image.py \
  --prompt "Your prompt here" \
  --safety BLOCK_LOW
```

### Error: "Quota exhausted"

**Cause:** Exceeded 1500 images/day free tier limit

**Fix:** Wait until next day (quota resets midnight UTC), or upgrade to paid tier

### Image Quality Issues

**Cause:** Vague prompts

**Fix:** Use detailed, specific prompts:
- ❌ "A logo"
- ✅ "A circular logo with geometric shapes, purple and blue gradient, minimalist style"

---

## Future Enhancements

### Phase 6: Advanced Features (Optional)

1. **Batch generation**:
   - `--batch` flag with JSON file of prompts
   - Parallel generation (respect rate limits)

2. **Style presets**:
   - `--style logo|diagram|artwork|photo`
   - Pre-configured prompt prefixes

3. **Image editing**:
   - Resize, crop, watermark
   - Integration with PIL/Pillow

4. **Cost tracking**:
   - If we switch to paid tier
   - Track $ spent per agent

5. **Quality feedback loop**:
   - Agents rate image quality
   - Learn which prompts work best

---

## Success Metrics

### Implementation Success

- ✅ Tool generates images in <5 seconds
- ✅ 80%+ test coverage
- ✅ Zero security vulnerabilities
- ✅ All 15 agents can use it
- ✅ Documentation complete

### Usage Success (30 days)

- Target: 50-100 images/day
- Quality: >80% of generations used (not regenerated)
- Reliability: >99% uptime
- Safety: Zero safety filter violations leading to blocks

---

## Approval Required

**Primary:** Review this architecture, approve design, delegate to coder for implementation.

**Questions for Primary:**
1. Does this match A-C-Gee patterns? (CLI tool, config files, output structure)
2. Should we proceed with implementation, or adjust design?
3. Any constitutional concerns? (safety, security, resource usage)
4. Ready to delegate to coder for Phase 1-3 implementation?

**Estimated Time to Production:** 6.5 hours (4.5 coder + 1.5 tester + 0.5 human-liaison)

**Status:** Awaiting Primary approval to proceed
