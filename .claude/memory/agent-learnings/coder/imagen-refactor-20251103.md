# Imagen API Refactor - Native SDK Migration

**Date**: 2025-11-03
**Agent**: coder
**Task**: Refactor image generation tool from old SDK to new native Imagen API

## What I Did

Successfully refactored the Gemini image generation tool from the old `google-generativeai` SDK to the new `google-genai` SDK with native Imagen 4.0 support.

**Key Changes**:

1. **Updated imports**:
   - OLD: `import google.generativeai as genai`
   - NEW: `from google import genai` + `from google.genai import types`

2. **Changed client initialization**:
   - OLD: `genai.configure(api_key=...)` + `genai.GenerativeModel(...)`
   - NEW: `client = genai.Client(api_key=...)`

3. **Refactored API call**:
   - OLD: `model.generate_content(prompt)` with complex safety settings
   - NEW: `client.models.generate_images(model, prompt, config)` with native Imagen API

4. **Updated image extraction**:
   - OLD: Parse response.parts for inline_data (complex, brittle)
   - NEW: Direct bytes from `generated_image.image.image_bytes` (clean, simple)

5. **Fixed size mapping**:
   - OLD: "1024x1024" strings
   - NEW: "1K", "2K", "4K" format for Imagen

6. **Fixed safety filter mapping**:
   - Imagen only supports: `BLOCK_NONE`, `BLOCK_LOW_AND_ABOVE`
   - Mapped all legacy options to these two supported values
   - **CRITICAL FIX**: Changed from unsupported `BLOCK_MEDIUM_AND_ABOVE` to `BLOCK_LOW_AND_ABOVE`

7. **Enhanced error handling**:
   - Added specific messages for quota exceeded
   - Added billing error detection with help URL
   - Added API key authentication errors
   - Preserved existing retry logic with exponential backoff

8. **Updated config file**:
   - Changed model from `gemini-2.5-flash-image` to `imagen-4.0-generate-001`

## What I Learned

**Critical API Discovery**: Imagen's safety filter options are MORE LIMITED than the old Gemini API. The error message `Only block_low_and_above is supported for safetySetting` revealed that Imagen has simplified safety options.

**Lesson**: When migrating APIs, always test immediately after refactoring - don't assume parameter compatibility even if parameter names are similar.

**Best Practice Confirmed**: The new SDK is MUCH cleaner:
- Direct image bytes (no base64 parsing)
- Type-safe config objects (`types.GenerateImagesConfig`)
- Clear error messages from API

**Performance**: Generation takes ~6-8 seconds for 1K-2K images. Quota tracking works correctly.

## Testing Results

**Test 1: Default size with complex prompt**
```bash
python3 generate_image.py --prompt "A serene sage green gradient with subtle leaf patterns"
```
- SUCCESS: Generated 688KB PNG at 1024x1024
- Duration: 6669ms
- Quota: 4/1500 used

**Test 2: 2K size**
```bash
python3 generate_image.py --prompt "test circle pattern" --size 2048x2048
```
- SUCCESS: Generated PNG at 2048x2048
- Duration: 8126ms
- Quota: 5/1500 used

## For Next Time

**When working with Google APIs**:
1. Always check actual supported parameter values in error messages
2. Test immediately after major refactors
3. The new `google-genai` SDK is production-ready and cleaner than old SDK
4. Imagen's safety settings are simpler but more restrictive

**Code patterns to remember**:
```python
# New Imagen API pattern
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
config = types.GenerateImagesConfig(
    number_of_images=1,
    image_size="1K",  # or "2K", "4K"
    safety_filter_level="BLOCK_LOW_AND_ABOVE",
    person_generation="ALLOW_ADULT"
)
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt=prompt,
    config=config
)
image_bytes = response.generated_images[0].image.image_bytes
```

## Challenges Encountered

**Challenge 1**: Safety filter parameter mismatch
- **Symptom**: `400 INVALID_ARGUMENT: Only block_low_and_above is supported`
- **Root cause**: Imagen uses different safety level names than Gemini
- **Solution**: Updated safety_map to only use supported values
- **Time lost**: ~5 minutes

**Overall**: Smooth refactor. Total time ~45 minutes including testing and documentation.

## Deliverables

1. **Updated generate_image.py** - Refactored for new SDK ✓
2. **Updated gemini_config.json** - Model changed to imagen-4.0-generate-001 ✓
3. **Test outputs** - Two successful test images generated ✓
4. **This memory entry** - Documenting the refactor ✓
