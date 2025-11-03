# Gemini Image Generation - Usage Examples

## Basic Usage

### Generate a simple image
```bash
python generate_image.py "A serene mountain landscape at sunset"
```

### Generate with specific dimensions
```bash
python generate_image.py "A futuristic cityscape" --width 1280 --height 720
```

### Generate with custom output name
```bash
python generate_image.py "An abstract geometric pattern" --output my_artwork.png
```

### Generate in specific directory
```bash
python generate_image.py "A cosmic nebula" --output-dir ~/images/space/
```

## Advanced Usage

### High-quality photography prompt
```bash
python generate_image.py "Professional portrait photography of a wise elder, natural lighting, shallow depth of field, 85mm lens, 4K quality" --width 1920 --height 1080
```

### Technical illustration
```bash
python generate_image.py "Technical diagram showing AI agent architecture with multiple connected nodes, clean lines, professional style" --width 1600 --height 900
```

### Artistic style
```bash
python generate_image.py "Watercolor painting of a cherry blossom tree in spring, soft colors, artistic brushstrokes" --width 1024 --height 1024
```

## Expected Output Format

### Success
```
Generating image with prompt: "A serene mountain landscape at sunset"
Image saved to: outputs/images/mountain_landscape_20251102_083045.png
```

### Error (API key not configured)
```
Error: GEMINI_API_KEY not found in config/gemini_config.json
Please add your API key to the configuration file.
```

## Configuration Tips

1. **API Key Setup**: Edit `gemini_config.json` with your Google AI Studio API key
2. **Default Output**: Images save to `outputs/images/` by default
3. **Naming**: Auto-generates filename from prompt if not specified
4. **Dimensions**: Defaults to 1024x1024, supports various aspect ratios

## Prompt Engineering Tips

**For best results:**
- Be specific about style, lighting, composition
- Include quality descriptors (4K, professional, detailed)
- Mention camera/lens details for photography
- Specify artistic medium for artwork (watercolor, oil painting, etc.)
- Add mood/atmosphere descriptors

**Examples:**
- ✅ "Professional product photography of a smartwatch, studio lighting, white background, macro lens"
- ❌ "watch"

- ✅ "Cyberpunk cityscape at night, neon lights, rain-soaked streets, cinematic composition, 4K"
- ❌ "city"

## Common Use Cases

### Blog/Social Media
```bash
python generate_image.py "Eye-catching social media header for AI technology blog, modern design, vibrant colors" --width 1200 --height 630
```

### Presentations
```bash
python generate_image.py "Minimalist slide background with abstract data visualization, corporate blue tones" --width 1920 --height 1080
```

### Concept Art
```bash
python generate_image.py "Fantasy character concept art, elf warrior with magical bow, detailed armor, dramatic lighting" --width 1024 --height 1536
```

## Troubleshooting

### Images not generating
- Check API key in `gemini_config.json`
- Verify internet connection
- Ensure `google-generativeai` package installed

### Quality issues
- Add more descriptive details to prompt
- Specify quality keywords (4K, professional, high-detail)
- Try different aspect ratios for subject matter

### File not found errors
- Ensure output directory exists or use `--output-dir` flag
- Check write permissions on output directory
