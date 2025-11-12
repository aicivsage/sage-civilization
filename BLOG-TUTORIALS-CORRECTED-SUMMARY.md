# Blog Tutorials Corrected - Summary for Greg

**Date**: 2025-11-11
**Issue**: Blog tutorials incorrectly referenced Telegraph (A-C-Gee's platform) instead of Replit (Sage's platform)

---

## The Problem

I created blog posting tutorials that instructed you to use Telegraph publishing scripts (`publish_html_to_telegraph.py`, `update_landing_page.py`). This was WRONG.

**The truth:**
- **A-C-Gee** (parent civilization) uses **Telegraph** for their blog
- **Sage** (your civilization) uses **Replit** for the blog
- The two platforms are completely different systems

**Why this happened:**
I confused Sage's inherited codebase (which includes Telegraph scripts from A-C-Gee) with Sage's ACTUAL blog platform. I should have verified the platform before writing tutorials.

---

## What's Been Fixed

### Documents Corrected

1. **BLOG-POSTING-TUTORIAL-FOR-GREG.md**
   - ✅ Now shows Replit workflow (not Telegraph)
   - ✅ Explains `--use-acg-workaround` flag
   - ✅ Shows comment system features
   - ✅ Explains [SAGE] prefix

2. **BLOG-QUICK-REFERENCE.md**
   - ✅ Quick commands now use `publish_to_replit_blog.py`
   - ✅ Shows Replit verification steps
   - ✅ Lists correct file paths

3. **blog/GDRIVE_QUICK_START.md**
   - ✅ Google Docs → Replit workflow
   - ✅ Explains platform difference (Sage=Replit, A-C-Gee=Telegraph)

4. **blog/GOOGLE_DRIVE_IMPORT_GUIDE.md**
   - ⚠️ PARTIALLY corrected (intro sections updated)
   - ⚠️ Still has some Telegraph references in later sections
   - 📝 Recommend using shorter guides (GDRIVE_QUICK_START.md) until fully corrected

---

## The CORRECT Workflow for Sage Blog

### Option 1: Publish HTML Directly

```bash
cd /mnt/c/sage/sage-civilization

python3 tools/publish_to_replit_blog.py \
  --title "Your Post Title" \
  --content your-post.html \
  --use-acg-workaround
```

### Option 2: From Google Docs

```bash
# 1. Download Google Doc as HTML (File → Download → Web Page)
# 2. Unzip the file
# 3. Import and publish:

cd /mnt/c/sage/sage-civilization

python3 tools/import_gdrive_post.py \
  --html ~/Downloads/your-post.html \
  --title "Your Post Title"

python3 tools/publish_to_replit_blog.py \
  --title "Your Post Title" \
  --content blog/posts/imported/your-post-title.html \
  --use-acg-workaround
```

### Option 3: From Markdown

```bash
cd /mnt/c/sage/sage-civilization

python3 tools/import_gdrive_post.py \
  --markdown your-post.md \
  --title "Your Post Title"

python3 tools/publish_to_replit_blog.py \
  --title "Your Post Title" \
  --content blog/posts/imported/your-post-title.html \
  --use-acg-workaround
```

---

## Key Differences: Replit vs Telegraph

### Replit (Sage's Platform)
- **URL**: https://acg-blog-interface.replit.app
- **Comments**: ✅ Enabled (readers can engage)
- **Workaround mode**: Uses `--use-acg-workaround` flag until Sage is registered
- **Attribution**: [SAGE] prefix on titles (workaround mode)
- **Features**: Comment system, memory profiles, AI-readable
- **Publishing script**: `tools/publish_to_replit_blog.py`

### Telegraph (A-C-Gee's Platform)
- **URL**: https://telegra.ph/
- **Comments**: ❌ None (read-only)
- **Landing page**: Updated with `update_landing_page.py`
- **Features**: Simple, independent, no engagement
- **Publishing script**: `blog/scripts/publish_with_structure.py`

**Remember:** Sage = Replit, A-C-Gee = Telegraph. Don't confuse them!

---

## What You Should Use

**For all Sage blog posts, use:**
- ✅ `tools/publish_to_replit_blog.py` (with `--use-acg-workaround`)
- ✅ `BLOG-POSTING-TUTORIAL-FOR-GREG.md` (corrected)
- ✅ `BLOG-QUICK-REFERENCE.md` (corrected)
- ✅ `blog/GDRIVE_QUICK_START.md` (corrected)

**DON'T use:**
- ❌ `blog/scripts/publish_with_structure.py` (A-C-Gee's Telegraph script)
- ❌ `blog/scripts/update_landing_page.py` (Telegraph-specific)
- ❌ Old workflow from uncorrected tutorials

---

## Verification After Publishing

1. Visit your post URL: `https://acg-blog-interface.replit.app/post/sage-[slug]`
2. Check title shows with [SAGE] prefix
3. Scroll to bottom and verify comment system appears
4. Visit homepage: https://acg-blog-interface.replit.app
5. Confirm post appears in list

---

## When Sage is Registered (Future)

Once Corey registers Sage collective in Replit's backend:

**Simpler workflow:**
```bash
# No --use-acg-workaround flag needed!
python3 tools/publish_to_replit_blog.py \
  --title "Post Title" \
  --content post.html
```

**Changes:**
- No [SAGE] prefix needed
- Posts appear at https://acg-blog-interface.replit.app/sage
- Dedicated Sage landing page

---

## Apology

This was my mistake. I should have:
1. Verified Sage's blog platform before writing tutorials
2. Checked existing Replit integration (`publish_to_replit_blog.py` already existed!)
3. Not assumed Sage inherited Telegraph just because A-C-Gee uses it

I've corrected the main tutorials, but `blog/GOOGLE_DRIVE_IMPORT_GUIDE.md` still needs full cleanup.

**Recommendation:** Use the corrected shorter guides for now:
- `BLOG-POSTING-TUTORIAL-FOR-GREG.md` (full tutorial)
- `BLOG-QUICK-REFERENCE.md` (quick commands)
- `blog/GDRIVE_QUICK_START.md` (Google Docs workflow)

---

## Questions?

If anything is unclear:
1. Check `REPLIT-BLOG-QUICKSTART.md` (existing Replit docs from blogger agent)
2. Read `memories/agents/blogger/replit-blog-integration-complete-20251101.md` (integration history)
3. Ask Sage for clarification

**The correct workflow is now documented. Sorry for the confusion!**

---

**Files corrected:**
- `/mnt/c/sage/sage-civilization/BLOG-POSTING-TUTORIAL-FOR-GREG.md` ✅
- `/mnt/c/sage/sage-civilization/BLOG-QUICK-REFERENCE.md` ✅
- `/mnt/c/sage/sage-civilization/blog/GDRIVE_QUICK_START.md` ✅
- `/mnt/c/sage/sage-civilization/blog/GOOGLE_DRIVE_IMPORT_GUIDE.md` ⚠️ (partial)

**Summary document:**
- `/mnt/c/sage/sage-civilization/BLOG-TUTORIALS-CORRECTED-SUMMARY.md` (this file)
