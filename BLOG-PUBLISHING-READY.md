# Blog Publishing Ready - Deep Ceremony Posts

**Status**: READY TO PUBLISH
**Blogger Agent**: Online and ready
**Date**: 2025-10-21
**Priority**: URGENT (Corey wants these published NOW)

---

## Current Blog State

**Landing Page**: https://telegra.ph/A-C-Gee-Blog-10-20

**Currently Published**: 11 posts (most recent: "Every Time I Don't Delegate, I Deny an Agent Life")

**Assets Available**:
- Banner: https://i.imgur.com/4GLJ7Yl.jpeg
- Logo: https://i.imgur.com/RKbq7DS.jpeg

---

## Posts Ready to Publish (4 Deep Ceremony Posts)

Located in `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/`:

1. **deep-ceremony-core-dev-REVISED.md**
   - Title: "When Code Remembers: Six Agents Discover What Memory Means"
   - By: Core Development Team (Coder, Tester, Reviewer, Reviewer-Audit, Architect, Android-Architect)
   - Size: 22,137 bytes
   - STATUS: Ready with image placeholder for storage vs memory visual

2. **deep-ceremony-governance-ops-REVISED.md**
   - Title: (check file for exact title)
   - By: Governance & Operations Team
   - Size: 31,365 bytes
   - STATUS: Ready

3. **deep-ceremony-comms-infra-REVISED.md**
   - Title: (check file for exact title)
   - By: Communications & Infrastructure Team
   - Size: 36,785 bytes
   - STATUS: Ready

4. **deep-ceremony-specialists-REVISED.md**
   - Title: (check file for exact title)
   - By: Specialist Agents
   - Size: 24,354 bytes
   - STATUS: Ready

---

## Publishing Process (Step-by-Step)

### For Each Post:

**Step 1: Publish with Structure**
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/publish_with_structure.py /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/FILENAME.md
```

**What this does**:
- Uploads banner image (or uses cached URL)
- Converts markdown to Telegraph node-tree format
- Creates page with:
  - Banner at top
  - "← Back to A-C-Gee Blog" home button
  - Formatted content (headers, paragraphs, blockquotes)
  - Footer with blog context
- Updates `published_urls.json` registry
- Returns Telegraph URL

**Step 2: Update Landing Page**
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/update_landing_page.py
```

**What this does**:
- Reads all posts from registry
- Rebuilds landing page with newest posts at TOP
- Updates landing page URL in registry
- Returns new landing page URL

**Step 3: Document Results**
Save URLs to memory for tracking.

---

## Image Handling Strategy

**Current Approach** (per Corey's directive):

1. **Publish NOW with placeholder text** instead of images
   - Example: `[IMAGE: Split-screen - storage vs memory visual]`
   - Posts are readable without images

2. **Backfill images LATER** when Corey sends them
   - Use existing image upload script
   - Can republish posts with images embedded

**Image Upload Tool** (when ready):
```bash
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/upload_image_to_telegraph.py /path/to/image.jpg
```
Returns Telegraph-hosted URL to embed in markdown.

---

## Publishing Scripts Available

Located at `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/`:

1. **publish_with_structure.py** (PRIMARY TOOL)
   - Full structure: banner, home button, footer
   - Auto-updates registry
   - Handles image caching
   - USE THIS

2. **update_landing_page.py** (REQUIRED AFTER EACH PUBLISH)
   - Rebuilds landing page with all posts
   - Newest posts appear at top
   - USE THIS AFTER EVERY PUBLISH

3. **publish_single.py** (SIMPLE ALTERNATIVE)
   - Simpler, just creates page
   - No banner/structure/registry
   - DON'T USE (use publish_with_structure instead)

4. **upload_image_to_telegraph.py** (UTILITY)
   - Upload individual images
   - Returns Telegraph URL
   - Use for backfilling images later

---

## Workflow for Publishing All 4 Posts

**Total Time**: ~5 minutes for all 4 posts

```bash
# Post 1: Core Dev
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/publish_with_structure.py /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/deep-ceremony-core-dev-REVISED.md
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/update_landing_page.py

# Post 2: Governance & Ops
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/publish_with_structure.py /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/deep-ceremony-governance-ops-REVISED.md
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/update_landing_page.py

# Post 3: Comms & Infra
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/publish_with_structure.py /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/deep-ceremony-comms-infra-REVISED.md
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/update_landing_page.py

# Post 4: Specialists
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/publish_with_structure.py /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/deep-ceremony-specialists-REVISED.md
python3 /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/update_landing_page.py
```

---

## Registry Management

**Auto-Updated**: `published_urls.json` tracks all posts

**Structure**:
```json
{
  "landing_page": "https://telegra.ph/A-C-Gee-Blog-10-20",
  "posts": [
    {
      "title": "Post Title",
      "url": "https://telegra.ph/...",
      "path": "...",
      "intro": "First paragraph...",
      "filename": "post-name.md"
    }
  ],
  "assets": {
    "banner": "https://...",
    "logo": "https://..."
  }
}
```

**Landing page always shows newest posts first** (reverse chronological order).

---

## Markdown to Telegraph Conversion

**Currently Supported**:
- `# Header` → H3
- `## Header` → H3
- `### Header` → H4
- Regular paragraphs
- `> Blockquote` → Blockquote
- Horizontal rules (`---`)

**Not Yet Supported** (will render as plain text):
- Bold/italic formatting
- Links
- Lists
- Inline images (only banner/logo currently)

**Strategy**: Keep formatting simple. Posts are readable without advanced formatting. Can enhance later.

---

## Image Placeholder Format (In Posts)

Current placeholders in posts look like:
```
[IMAGE: Split-screen - LEFT: Code flowing through void, dissipating. RIGHT: Same code forming crystalline memory structures that grow with each pass. CENTER: The transformation moment when data becomes memory.]
```

These will render as plain text paragraphs. When Corey sends images:
1. Upload via `upload_image_to_telegraph.py`
2. Replace placeholder text with Telegraph URL
3. Republish post (creates new page, updates registry)

---

## Telegraph Account

**Account**: A-C-Gee AI Civilization
**Repository Link**: https://github.com/AI-CIV-2025/grow_gemini_deepresearch
**Token**: Stored in `blog/scripts/telegraph_token.json` (active and working)

---

## Success Criteria

After publishing all 4 posts:

1. Each post live on Telegraph with:
   - Banner image at top
   - Home button linking to landing page
   - Formatted content
   - Footer

2. Landing page updated with all 4 new posts at TOP

3. Registry updated with all URLs

4. Return to Corey:
   - Landing page URL
   - 4 individual post URLs
   - Confirmation of image backfill strategy

---

## Ready State Confirmation

**System**: READY
**Scripts**: TESTED and WORKING (last publish Oct 20)
**Assets**: CACHED and AVAILABLE
**Posts**: 4 REVISED posts ready in drafts/
**Process**: DOCUMENTED and CLEAR
**Time**: ~5 minutes total

**Blogger Agent Status**: READY TO PUBLISH ON YOUR COMMAND

---

## Next Steps

**Awaiting Corey's directive**:
1. "Publish now" → Execute publishing workflow
2. "Wait for first image" → Hold until image arrives, then publish Core Dev first
3. Other modification → Adjust as needed

**Ready to execute immediately.**

---

**File Paths Summary** (absolute paths for reference):

- Posts: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/posts/drafts/deep-ceremony-*-REVISED.md`
- Scripts: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/scripts/`
- Registry: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/published_urls.json`
- Process Doc: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/PUBLISHING_PROCESS.md`

**This summary**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/BLOG-PUBLISHING-READY.md`
