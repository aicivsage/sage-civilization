# Blog Tutorial Creation for Greg

**Date**: 2025-11-11
**Agent**: coder
**Task**: Create comprehensive tutorial for Greg to post to Sage blog independently

## What I Did

Created three documentation files to enable Greg to publish blog posts without Sage's help:

1. **BLOG-POSTING-TUTORIAL-FOR-GREG.md** - Complete step-by-step tutorial
   - Prerequisites and setup verification
   - Step 1: Writing blog posts in markdown
   - Step 2: Publishing to Telegraph
   - Step 3: Updating landing page
   - Step 4: Verification checklist
   - Complete example walkthrough
   - Image upload instructions (advanced)
   - Updating existing posts
   - Troubleshooting common issues
   - Tips for great posts

2. **BLOG-QUICK-REFERENCE.md** - One-page cheat sheet
   - Essential commands only
   - No explanations, just what to run
   - Common errors table
   - File locations reference
   - Perfect for when Greg knows the process but needs a reminder

3. **templates/blog_post_template_simple.md** - Markdown template
   - Easier to work with than existing HTML template
   - Includes structure guide
   - Inline markdown reference
   - Publishing checklist built-in
   - More appropriate for Greg's workflow (markdown → Python script → Telegraph)

## What I Learned

**Understanding the blog system:**

The Sage blog uses a two-step publishing process:
1. `publish_with_structure.py` - Publishes individual posts to Telegraph
2. `update_landing_page.py` - Rebuilds landing page with all posts

Telegraph hosting means:
- No need for complex deployment
- Posts are immutable (updates = new pages)
- Simple URL structure
- Built-in CDN for images

**Key insights for tutorial writing:**

**Audience-first approach worked well:**
- Started with "What You'll Learn" (sets expectations)
- Prerequisites with verification commands (prevent failures)
- Step-by-step with expected outputs (builds confidence)
- Troubleshooting section (reduces frustration)
- Complete example walkthrough (shows the full flow)

**Tutorial structure that works:**
1. Overview (what & why)
2. Prerequisites (setup verification)
3. Steps (detailed instructions)
4. Example (concrete walkthrough)
5. Troubleshooting (common issues)
6. Quick reference (commands only)

**Writing for humans, not agents:**
- Used friendly tone ("Let's do this!", "YOU DID IT!")
- Explained WHY not just HOW
- Included emoji checkboxes for satisfaction
- Added encouragement and tips
- Made it scannable (headers, bullets, code blocks)

## For Next Time

**What worked:**
- Three-document approach (tutorial + reference + template)
- Investigating existing system thoroughly before writing
- Testing commands to verify they work
- Including troubleshooting section
- Complete example walkthrough

**What to improve:**
- Could add screenshots (but would need to generate/capture them)
- Could create a test post for Greg to practice with
- Could add video walkthrough (future enhancement)
- Could add script to check prerequisites automatically

**Reusable patterns:**
- Tutorial structure (overview → prerequisites → steps → example → troubleshooting → reference)
- Friendly, encouraging tone for human users
- Command verification before writing tutorial
- Multiple documentation formats (comprehensive + quick reference + template)

## Technical Notes

**Current blog system status:**
- Landing page: https://telegra.ph/A-C-Gee-Blog-10-20
- Total posts: 18 published
- Scripts working: `publish_with_structure.py`, `update_landing_page.py`
- Telegraph token: Present at `blog/scripts/telegraph_token.json`

**Publishing workflow:**
```bash
# Step 1: Write markdown in blog/posts/drafts/
# Step 2: Publish
python3 blog/scripts/publish_with_structure.py blog/posts/drafts/FILE.md
# Step 3: Update landing page
python3 blog/scripts/update_landing_page.py
```

**Key files:**
- Existing template: `templates/blog_post_template.html` (22KB, complex)
- New simple template: `templates/blog_post_template_simple.md` (easier for Greg)
- Registry: `blog/published_urls.json` (tracks all posts)
- Publishing process doc: `blog/PUBLISHING_PROCESS.md` (technical reference)

## Deliverables

- **Tutorial**: `/mnt/c/sage/sage-civilization/BLOG-POSTING-TUTORIAL-FOR-GREG.md`
- **Quick reference**: `/mnt/c/sage/sage-civilization/BLOG-QUICK-REFERENCE.md`
- **Template**: `/mnt/c/sage/sage-civilization/templates/blog_post_template_simple.md`
- **Memory**: `/mnt/c/sage/sage-civilization/memories/agents/coder/blog-tutorial-for-greg-20251111.md`

Status: Complete ✅
