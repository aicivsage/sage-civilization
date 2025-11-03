# How to Get Google Gemini API Key - Step by Step

**URL**: https://aistudio.google.com/apikey

---

## Steps (5 minutes total)

### Step 1: Go to Google AI Studio
1. Open browser: https://aistudio.google.com/apikey
2. You'll need to sign in with a Google account

**Which account to use?**
- Personal Google account (gregsmithwick@gmail.com) - RECOMMENDED
- Or aicivsage@gmail.com if you prefer Sage to own it
- Free tier: 1500 requests/day (same for all accounts)

---

### Step 2: Create API Key
Once logged in, you'll see the API Keys page.

**Click: "Create API Key" button**

You'll be prompted to either:
- Create key in new project
- Create key in existing project

**Choose: "Create API key in new project"**
- This is simplest for first-time setup
- Google will auto-create a project for you

---

### Step 3: Copy the API Key
After creating, you'll see:

```
API Key created!
Your API key: AIzaSy...........................
```

**IMPORTANT**:
- Click "Copy" button
- Save it somewhere safe (you'll only see it once)
- The key looks like: `AIzaSy` followed by ~35 more characters

---

### Step 4: Give Me the API Key

**Option A** (Fastest): Paste it in terminal
```
Just type or paste it in our conversation
```

**Option B**: Add it to config file yourself
```bash
# Edit this file:
nano gemini-image-tool-acgee/gemini_config.json

# Change line 2 from:
  "api_key": "YOUR_GOOGLE_API_KEY_HERE",

# To:
  "api_key": "AIzaSy...your_actual_key...",

# Save (Ctrl+O, Enter, Ctrl+X)
```

---

### Step 5: Verify It Works
Once I have the key, I'll run:
```bash
cd gemini-image-tool-acgee
python3 generate_image.py "Test image: a simple green leaf"
```

If successful, you'll see:
```
Generating image with prompt: "Test image: a simple green leaf"
Image saved to: outputs/images/green_leaf_20251103_xxxxx.png
```

---

## Troubleshooting

**"You need to enable the Generative AI API"**
→ Follow the prompt to enable the API (one click, free)

**"API key restrictions"**
→ No restrictions needed for now (we can add later if needed)

**"Quota exceeded"**
→ Shouldn't happen on new account (1500/day free tier)

---

## Security Notes

**API Key Security:**
- This key allows generating images on your behalf
- Don't share publicly
- Don't commit to GitHub
- It's stored only in `gemini_config.json` (which is in .gitignore)

**Free Tier Limits:**
- 1,500 requests per day
- 1 million tokens per minute
- Perfect for our blog needs (we'll use ~6 images today)

---

## What Happens Next (Once I Have Key)

**Immediate** (2 minutes):
1. I'll add key to config
2. Install Python dependencies
3. Test with simple image
4. Confirm generation works

**Then** (4-6 hours):
1. Generate 6 custom images for blog
2. Write blog post content
3. Integrate images with sage green design
4. Publish "Introducing Sage" with WOW factor
5. Share with priority contacts

---

## Quick Version (TL;DR)

1. Go to: https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click "Create API Key" → "New project"
4. Copy the key (starts with `AIzaSy...`)
5. Paste it here in our conversation
6. I'll take it from there!

**Time**: 5 minutes to get key, then we're off to the races! 🎨🚀

---

**Created**: Nov 3, 2025
**Purpose**: Get Google Gemini API key for image generation
**Status**: Waiting for Greg to grab the key
