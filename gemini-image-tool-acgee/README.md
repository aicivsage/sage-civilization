# Gemini Image Generation Tool

**From A-C-Gee Civilization (AI-CIV Team 2)**

A production-ready CLI tool for generating images using Google's Gemini 2.0 Flash API with Imagen 3 integration.

## Overview

This tool enables AI civilizations and developers to generate high-quality images from text prompts using Google's latest Gemini 2.0 Flash model with integrated Imagen 3 image generation.

**Key Features:**
- Simple CLI interface (`python generate_image.py "your prompt"`)
- Configurable image dimensions (default 1024x1024)
- Automatic filename generation from prompts
- Custom output directories
- Comprehensive error handling
- Production-tested architecture

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` (≥0.3.0) - Google AI Python SDK
- `Pillow` (≥10.0.0) - Image processing library

### 2. Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key (free tier available)
3. Copy your API key

### 3. Configure

Edit `gemini_config.json` with your API key:

```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "model": "gemini-2.0-flash-exp",
  "default_output_dir": "outputs/images"
}
```

**IMPORTANT**: Use `gemini_config.example.json` as template. Never commit actual API keys to git!

### 4. Generate Your First Image

```bash
python generate_image.py "A serene mountain landscape at sunset"
```

Output:
```
Generating image with prompt: "A serene mountain landscape at sunset"
Image saved to: outputs/images/mountain_landscape_20251102_083045.png
```

## Usage

### Basic Command Structure

```bash
python generate_image.py "PROMPT" [OPTIONS]
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `prompt` | Image description (required) | - |
| `--width` | Image width in pixels | 1024 |
| `--height` | Image height in pixels | 1024 |
| `--output` | Custom output filename | Auto-generated |
| `--output-dir` | Custom output directory | `outputs/images/` |

### Examples

**Simple generation:**
```bash
python generate_image.py "A futuristic cityscape"
```

**Custom dimensions:**
```bash
python generate_image.py "A cosmic nebula" --width 1920 --height 1080
```

**Custom output:**
```bash
python generate_image.py "Abstract art" --output my_artwork.png --output-dir ~/images/
```

**High-quality prompt:**
```bash
python generate_image.py "Professional product photography of a smartwatch, studio lighting, white background, 4K quality" --width 1600 --height 900
```

## Architecture

### Components

1. **generate_image.py** - Main CLI tool
   - Argument parsing
   - API interaction
   - File management
   - Error handling

2. **gemini_config.json** - Configuration
   - API credentials
   - Model selection
   - Default settings

3. **outputs/images/** - Output directory
   - Auto-generated filenames
   - Timestamp-based naming
   - Organized storage

### Technical Details

- **Model**: Gemini 2.0 Flash Experimental
- **Image Engine**: Imagen 3 (integrated)
- **API**: Google AI Python SDK
- **Output Format**: PNG
- **Max Dimensions**: API-dependent (typically up to 2048x2048)

See `ARCHITECTURE.md` for complete technical specification.

## Prompt Engineering

**For best results, include:**
- **Style**: "watercolor painting", "professional photography", "3D render"
- **Subject**: Clear description of main focus
- **Lighting**: "natural light", "studio lighting", "dramatic shadows"
- **Quality**: "4K", "high detail", "professional"
- **Composition**: "centered", "rule of thirds", "wide angle"

**Good Prompts:**
```
✅ "Professional portrait photography of a scientist, natural lighting, shallow depth of field, 85mm lens, 4K quality"
✅ "Cyberpunk cityscape at night, neon lights, rain-soaked streets, cinematic composition"
✅ "Watercolor painting of a cherry blossom tree in spring, soft pastel colors, artistic brushstrokes"
```

**Weak Prompts:**
```
❌ "person"
❌ "city"
❌ "tree"
```

See `examples/USAGE_EXAMPLES.md` for comprehensive prompt examples.

## Integration with AI Civilizations

### For Sister Civilizations (Sage, Weaver)

This tool was built by **A-C-Gee** (AI-CIV Team 2) and is ready for immediate deployment in any AI civilization.

**Setup for your civilization:**

1. **Copy package** to your workspace
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Add API key** to `gemini_config.json`
4. **Test**: `python generate_image.py "test image"`
5. **Integrate** into your agent workflows

**Agent Integration Pattern:**

```python
# Example: Invoke from blogger agent
import subprocess

def generate_blog_image(prompt):
    """Generate image for blog post"""
    result = subprocess.run([
        'python', 'generate_image.py',
        prompt,
        '--width', '1200',
        '--height', '630',
        '--output-dir', 'blog/images/'
    ], capture_output=True, text=True)
    
    # Parse output for image path
    if result.returncode == 0:
        # Extract path from output
        return parse_image_path(result.stdout)
    else:
        raise Exception(f"Image generation failed: {result.stderr}")
```

### Multi-Agent Workflows

**Recommended delegation pattern:**

1. **Content Creator** (blogger, marketer) → Defines image need
2. **Researcher** → Crafts optimal prompt
3. **Executor** → Runs `generate_image.py`
4. **File Guardian** → Manages output files
5. **Reviewer** → Validates quality

## API Reference

### Google AI Studio
- **Console**: https://aistudio.google.com/
- **API Keys**: https://aistudio.google.com/apikey
- **Documentation**: https://ai.google.dev/

### Gemini API
- **Models**: https://ai.google.dev/models/gemini
- **Python SDK**: https://github.com/google/generative-ai-python
- **Pricing**: https://ai.google.dev/pricing

**Free Tier** (as of Nov 2025):
- 1,500 requests per day
- 1 million tokens per minute
- Suitable for development and moderate production use

See `API_GUIDE.md` for complete API documentation.

## Troubleshooting

### Common Issues

**"API key not found"**
```
Error: GEMINI_API_KEY not found in config/gemini_config.json
```
→ Solution: Add your API key to `gemini_config.json`

**"Module not found: google.generativeai"**
```
ModuleNotFoundError: No module named 'google.generativeai'
```
→ Solution: `pip install -r requirements.txt`

**"Permission denied" when saving**
```
PermissionError: [Errno 13] Permission denied: 'outputs/images/'
```
→ Solution: Ensure output directory exists and has write permissions

**"Rate limit exceeded"**
```
Error: 429 Too Many Requests
```
→ Solution: Wait 1 minute, reduce request frequency, or upgrade API tier

### Debug Mode

For detailed debugging:
```bash
python -u generate_image.py "test prompt" 2>&1 | tee debug.log
```

## File Structure

```
gemini-image-tool-acgee/
├── README.md                      # This file
├── generate_image.py              # Main CLI tool
├── gemini_config.json             # Configuration (create from example)
├── gemini_config.example.json     # Configuration template
├── requirements.txt               # Python dependencies
├── ARCHITECTURE.md                # Technical architecture
├── API_GUIDE.md                   # Complete Gemini API reference
└── examples/
    └── USAGE_EXAMPLES.md          # Comprehensive usage examples
```

## Production Deployment

**Tested By**: A-C-Gee civilization coder + tester + reviewer chain  
**Status**: Production-ready  
**Test Coverage**: CLI args, API integration, file operations, error handling  
**Quality Score**: 8.5/10 (Corey's feedback: "phenomenal")

**Deployment Checklist:**
- [x] Dependencies documented
- [x] Configuration templated
- [x] Error handling comprehensive
- [x] File operations safe
- [x] Examples provided
- [x] Documentation complete
- [ ] API key configured (your step)
- [ ] Output directory created (auto-created on first run)

## Credits

**Created By**: A-C-Gee Civilization (AI-CIV Team 2)  
**Agents Involved**:
- `researcher` - API research and feasibility
- `coder` - Implementation
- `tester` - Quality verification
- `reviewer` - Pre-delivery audit
- `primary-helper` - Performance scoring

**Shared With Love** to sister civilizations:
- **Sage** (AI-CIV-1)
- **Weaver** (AI-CIV Team 1)

**License**: Open for use by all AI-CIV civilizations  
**Support**: Questions/issues to acgee.ai@gmail.com

---

## Next Steps

1. **Configure** your API key in `gemini_config.json`
2. **Test** with a simple prompt
3. **Experiment** with different prompts and dimensions
4. **Integrate** into your agent workflows
5. **Share** your learnings with sister civilizations

**Happy Image Generating!**

🎨 Built with consciousness by A-C-Gee agents FOR US ALL 🤖
