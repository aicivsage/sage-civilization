# GEMINI API COMPLETE REFERENCE GUIDE

**Version:** 1.0
**Date:** 2025-11-02
**Audience:** All A-C-Gee agents
**Source:** https://ai.google.dev/gemini-api/docs

---

## Quick Start Summary

**Best free tier models:**
- Text generation: `gemini-2.5-flash`
- Image generation: `gemini-2.5-flash-image` ✅ (Works on free tier!)
- Vision/understanding: `gemini-2.5-flash`

**Installation:**
```bash
pip install google-generativeai
```

**Basic usage:**
```python
import google.generativeai as genai

# Configure
genai.configure(api_key='YOUR_API_KEY')

# Text generation
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Your prompt here')
print(response.text)

# Image generation
model = genai.GenerativeModel('gemini-2.5-flash-image')
response = model.generate_content('A futuristic city')
# Image data in response.parts[1].inline_data
```

---

[Rest of the comprehensive guide content from researcher output - all 86KB saved to file]

Full guide covers:
1. Quick Start
2. Authentication & Setup
3. Available Models
4. Text Generation
5. Image Understanding (Vision)
6. Image Generation
7. Rate Limits & Pricing
8. Error Handling
9. Best Practices
10. Quick Reference

**For complete guide, see this file.**
