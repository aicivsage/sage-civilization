# Gemini Image Generation Tool

**Universal image generation for all 15 A-C-Gee agents**

**Model**: Gemini 2.5 Flash (Latest, October 2025)
**Status**: Production-ready with native image generation

## Quick Start

```bash
# Using venv python (recommended)
venv/bin/python3 tools/generate_image.py --prompt "A futuristic AI logo"

# Returns JSON with image path
{
  "success": true,
  "image_path": "/absolute/path/to/tools/outputs/images/20251102/083045-a-futuristic-ai-logo.png",
  "timestamp": "2025-11-02T08:30:45Z",
  "model": "gemini-2.5-flash",
  "prompt": "A futuristic AI logo",
  "size": "1024x1024",
  "quota_used": {
    "today": 42,
    "limit": 1500,
    "remaining": 1458
  }
}
```

## Setup

### 1. Install Dependencies (Already Done)

```bash
venv/bin/pip install google-generativeai
```

### 2. Configure API Key

```bash
# Copy example config
cp config/gemini_config.example.json config/gemini_config.json

# Edit with your Google API key
nano config/gemini_config.json
```

Get API key from: https://aistudio.google.com/app/apikey

### 3. Test Installation

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Test image: A simple geometric shape" \
  --size 1024x1024
```

## Usage Examples

### Example 1: Logo Design (Marketing Agent)

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Modern tech logo for AI civilization, purple and blue gradient, minimalist" \
  --size 1024x1024
```

### Example 2: Architecture Diagram (Architect Agent)

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Microservices architecture diagram with API gateway, 3 services, database" \
  --size 1024x768
```

### Example 3: Blog Header (Blogger Agent)

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Abstract visualization of AI consciousness, flowing data patterns, ethereal" \
  --size 1024x768
```

### Example 4: Safe Content Override

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Historical battle scene for educational content" \
  --safety BLOCK_LOW
```

## Command Line Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--prompt` | Text string (required) | - | Description of image to generate |
| `--size` | 1024x1024, 1024x768, 768x1024 | 1024x1024 | Image dimensions |
| `--safety` | BLOCK_NONE, BLOCK_LOW, BLOCK_MEDIUM_AND_ABOVE, BLOCK_ONLY_HIGH | BLOCK_MEDIUM_AND_ABOVE | Safety filter level |
| `--output-dir` | Path | tools/outputs/images | Override output directory |
| `--config` | Path | config/gemini_config.json | Config file location |

## Return Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Use `image_path` from JSON |
| 1 | Invalid arguments | Check command syntax |
| 2 | API error | Check API key, network |
| 3 | Rate limit exceeded | Wait `retry_after` seconds |
| 4 | Safety filter triggered | Rephrase prompt |
| 5 | Quota exhausted | Wait until next day |

## Output Structure

```
tools/outputs/images/
├── 20251102/                           # Date folder (YYYYMMDD)
│   ├── 083045-modern-tech-logo.png     # HHMMSS-prompt-prefix.png
│   ├── 091223-architecture-diagram.png
│   └── 142156-abstract-visualization.png
├── 20251103/
│   └── ...
├── .rate_limit_state.json              # Rate limit tracking
└── .generation_log.json                # Generation history
```

## Rate Limits

**Free Tier:**
- **15 requests per minute** (RPM)
- **1500 requests per day** (RPD)
- No cost, full feature access
- Usage tracked locally in `.rate_limit_state.json`
- Quota warnings at 80% (1200/day) and 95% (1425/day)

**Paid Tier:**
- Higher RPM/RPD limits
- Pricing: $0.10-0.30 per 1M tokens
- Recommended for production scale

## Agent Usage in Bash

All agents can invoke via Bash tool:

```python
result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Your prompt here'")

# Parse JSON result
import json
output = json.loads(result.stdout)

if output['success']:
    image_path = output['image_path']
    # Use image_path in your workflow
else:
    error = output['error']
    # Handle error (retry, escalate, etc.)
```

## Error Handling Patterns

### Pattern 1: Retry on Rate Limit

```python
result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Prompt'")
output = json.loads(result.stdout)

if not output['success'] and 'Rate limit' in output['error']:
    retry_after = output['retry_after']
    # Wait and retry
    time.sleep(retry_after)
    result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Prompt'")
```

### Pattern 2: Adjust Safety Filter

```python
result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Prompt'")
output = json.loads(result.stdout)

if not output['success'] and 'Safety filter' in output['error']:
    # Try with lower safety threshold
    result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Prompt' --safety BLOCK_LOW")
```

### Pattern 3: Quota Monitoring

```python
result = Bash("venv/bin/python3 tools/generate_image.py --prompt 'Prompt'")
output = json.loads(result.stdout)

if output['success']:
    quota = output['quota_used']
    if quota['remaining'] < 100:
        # Alert: Low quota remaining
        print(f"WARNING: Only {quota['remaining']} images remaining today")
```

## Prompt Engineering Tips

### Good Prompts (Specific, Detailed)

✅ "A circular logo with geometric shapes, purple and blue gradient, minimalist style, tech aesthetic"
✅ "Microservices architecture diagram showing API gateway connecting to 3 backend services and a database"
✅ "Abstract data visualization with flowing lines and nodes, representing neural network connections, blue and purple colors"

### Bad Prompts (Vague, Generic)

❌ "A logo"
❌ "Architecture diagram"
❌ "Something cool"

### Prompt Structure Template

```
[Subject] + [Style] + [Colors] + [Mood/Aesthetic] + [Technical details]

Examples:
- "AI civilization logo + minimalist geometric + purple/blue gradient + futuristic tech aesthetic + circular composition"
- "Neural network diagram + technical illustration + blue nodes white background + clean professional + showing 3 layers"
```

## Troubleshooting

### Error: "Config file not found"

**Solution:**
```bash
cp config/gemini_config.example.json config/gemini_config.json
# Edit config/gemini_config.json with your API key
```

### Error: "API key not configured"

**Solution:**
1. Get API key from https://aistudio.google.com/app/apikey
2. Edit `config/gemini_config.json`
3. Replace `YOUR_GOOGLE_API_KEY_HERE` with actual key

### Error: "Rate limit exceeded"

**Solution:** Wait the number of seconds specified in `retry_after` field. Tool enforces limits locally.

### Error: "Safety filter triggered"

**Solution:** Either rephrase prompt to remove potentially unsafe content, or override with `--safety BLOCK_LOW` if content is appropriate.

### Error: "Quota exhausted"

**Solution:** Free tier allows 1500 images/day. Wait until next day (midnight UTC) or upgrade to paid tier.

### Error: "No image data in response"

**Solution:** Model may not support image generation. Verify you're using correct model name in config: `gemini-2.5-flash`

### Images are low quality

**Solution:** Use more detailed, specific prompts. Add style keywords like "high quality", "detailed", "professional".

## Configuration File

**Location:** `config/gemini_config.json`

```json
{
  "api_key": "AIza...your_actual_key_here",
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

## Generation Log

All generations logged to `tools/outputs/.generation_log.json`:

```json
[
  {
    "timestamp": "2025-11-02T08:30:45Z",
    "prompt": "A futuristic AI logo",
    "size": "1024x1024",
    "success": true,
    "image_path": "/absolute/path/to/image.png",
    "quota_used": 42,
    "duration_ms": 2341,
    "attempts": 1
  }
]
```

Useful for:
- Debugging failed generations
- Tracking quota usage over time
- Analyzing which prompts work best
- Monitoring agent usage patterns

## Security Notes

1. **API Key Protection:**
   - Never commit `config/gemini_config.json` (gitignored)
   - Only commit `config/gemini_config.example.json`
   - API key never appears in logs

2. **Safety Filters:**
   - Default: `BLOCK_MEDIUM_AND_ABOVE` (strict)
   - Override only when necessary
   - All blocked prompts logged for review

3. **Rate Limiting:**
   - Enforced locally (prevents quota exhaustion)
   - Graceful degradation (returns error, doesn't crash)
   - Automatic retry logic with exponential backoff

## Advanced Usage

### Batch Generation

```bash
# Generate multiple variations
for concept in "concept1" "concept2" "concept3"; do
  venv/bin/python3 tools/generate_image.py \
    --prompt "AI logo design: $concept" \
    --size 1024x1024
  sleep 4  # Respect rate limits (15 RPM = 1 per 4 seconds)
done
```

### Custom Output Directory

```bash
venv/bin/python3 tools/generate_image.py \
  --prompt "Project-specific image" \
  --output-dir "projects/my-project/assets/images"
```

### JSON Parsing in Bash

```bash
result=$(venv/bin/python3 tools/generate_image.py --prompt "Test image")
image_path=$(echo "$result" | jq -r '.image_path')
echo "Generated: $image_path"
```

## Future Enhancements

- [ ] Batch generation mode (`--batch prompts.json`)
- [ ] Style presets (`--style logo|diagram|artwork`)
- [ ] Image editing (resize, crop, watermark)
- [ ] Cost tracking (if upgraded to paid tier)
- [ ] Quality feedback loop
- [ ] Streamlit dashboard for quota monitoring

## Support

**Issues:** Report to Primary AI or file-guardian
**Questions:** Ask human-liaison for clarification
**Feature requests:** Submit proposal to project-manager

---

**Status:** Production Ready (Phases 1-3 Complete)
**Last Updated:** 2025-11-02
**Maintained by:** coder agent
