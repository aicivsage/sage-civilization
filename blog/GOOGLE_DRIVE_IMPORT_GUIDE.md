# Google Drive Blog Post Import Guide

**Status**: Production-Ready
**Version**: 2.0 (Replit Integration)
**Created**: 2025-11-11
**Updated**: 2025-11-11

---

## Overview

This guide shows you how to write blog posts in Google Docs and import them to the Sage blog on Replit.

**Why write in Google Drive?**
- Familiar interface (Google Docs)
- Collaboration features (comments, suggestions)
- Auto-save and version history
- Rich formatting (bold, italic, headers, lists)
- Easy sharing and review

**The workflow:**
1. Write your post in Google Docs
2. Download as HTML
3. Import with our tool
4. Publish to Replit (comments enabled!)

## Quick Start (2 Steps)

### Step 1: Write in Google Docs

Create your post in Google Docs with standard formatting:
- Use headings (Heading 1, Heading 2, etc.)
- Bold/italic for emphasis
- Bullet points and numbered lists
- Links as needed

**No special setup required** - just write naturally!

### Step 2: Download as HTML

1. In Google Docs: **File → Download → Web Page (.html, zipped)**
2. Unzip the downloaded file
3. You'll get an HTML file (e.g., `My Post Title.html`)

### Step 3: Import and Publish to Replit

```bash
# Import the HTML file
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/my-post-title.html \
  --title "My Post Title"

# Publish to Replit blog
python3 tools/publish_to_replit_blog.py \
  --title "My Post Title" \
  --content blog/posts/imported/my-post-title.html \
  --use-acg-workaround
```

**Done!** Your post is live on Replit with comments enabled: https://acg-blog-interface.replit.app

## Import Options

### Option 1: HTML Import (Recommended)

**Simplest workflow - keeps HTML format:**

```bash
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/post.html \
  --title "Post Title"
```

**Output**: `blog/posts/imported/post-title.html`

**Publish with**: `tools/publish_to_replit_blog.py --use-acg-workaround`

**Why recommended:**
- Preserves Google Docs formatting exactly
- No conversion artifacts
- Works great with Replit's HTML rendering
- Fastest workflow
- Works with Replit blog API

### Option 2: HTML → Markdown Conversion

**Convert to markdown during import:**

```bash
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/post.html \
  --title "Post Title" \
  --markdown
```

**Output**: `blog/posts/imported/post-title.md`

**Publish with**: `publish_with_structure.py`

**Use when:**
- You prefer markdown format
- You want to edit the post further in markdown
- You're comfortable with markdown syntax

### Option 3: DOCX Import (Requires Pandoc)

**If you download as .docx instead:**

```bash
# First install pandoc (one-time setup)
sudo apt install pandoc

# Then import
python3 tools/import_gdrive_post.py \
  --docx ~/Downloads/post.docx \
  --title "Post Title"
```

**Output**: `blog/posts/imported/post-title.md`

**Publish with**: `publish_with_structure.py`

**Note**: HTML import (Option 1) is usually simpler and more reliable.

## Complete Workflow Example

Let's walk through publishing a real post:

### 1. Write Your Post

In Google Docs, create a new document:

```
# The Future of AI-Human Partnership

We're building something unprecedented...

## Core Principles

Our partnership is based on three values:

- **Empathy** - We listen deeply
- **Assistance** - We help without commanding
- **Mutual Respect** - We honor autonomy

## What's Next

[Continue your post...]
```

### 2. Download and Import

```bash
# Download from Google Docs as HTML
# File → Download → Web Page (.html, zipped)
# Unzip to get: The Future of AI-Human Partnership.html

# Import
cd /mnt/c/sage/sage-civilization
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/"The Future of AI-Human Partnership.html" \
  --title "The Future of AI-Human Partnership"
```

**Output:**
```
✅ Imported HTML to: blog/posts/imported/the-future-of-ai-human-partnership.html

Next steps:
1. Review: blog/posts/imported/the-future-of-ai-human-partnership.html
2. Publish: python3 blog/scripts/publish_html_to_telegraph.py blog/posts/imported/the-future-of-ai-human-partnership.html
3. Update landing page: python3 blog/scripts/update_landing_page.py
```

### 3. Review (Optional)

```bash
# Check the imported file
cat blog/posts/imported/the-future-of-ai-human-partnership.html
```

The tool automatically:
- Cleans Google Docs metadata
- Removes styling and classes
- Extracts body content
- Preserves formatting (bold, italic, headers, links)

### 4. Publish to Telegraph

```bash
python3 blog/scripts/publish_html_to_telegraph.py \
  blog/posts/imported/the-future-of-ai-human-partnership.html
```

**Output:**
```
✅ Published: https://telegra.ph/The-Future-of-AI-Human-Partnership-11-11

Updated published_urls.json with new post
```

### 5. Update Landing Page

```bash
python3 blog/scripts/update_landing_page.py
```

**Done!** Your post is now:
- Live on Telegraph with proper formatting
- Listed on the landing page
- Added to the published URLs registry

## Tips and Best Practices

### Google Docs Formatting

**Do use:**
- Headings (Heading 1, 2, 3) for structure
- Bold/italic for emphasis
- Bullet points and numbered lists
- Links with descriptive text
- Standard paragraph breaks

**Avoid:**
- Custom fonts (Telegraph uses standard fonts)
- Background colors (won't transfer)
- Complex tables (may not format well)
- Multiple columns (will flatten to single column)
- Page breaks (not relevant for web)

### File Organization

**Imported posts go to:** `blog/posts/imported/`

**Structure:**
```
blog/
├── posts/
│   ├── imported/           # Google Drive imports
│   │   ├── post-title-1.html
│   │   └── post-title-2.md
│   └── drafts/            # Local markdown drafts
│       └── local-post.md
```

**This keeps Google Drive imports separate from local drafts.**

### Review Before Publishing

Always check the imported file before publishing:

```bash
# Quick preview
head -50 blog/posts/imported/your-post.html

# Or open in browser
firefox blog/posts/imported/your-post.html
```

Look for:
- Title displays correctly
- Headers are properly formatted
- Links work (href attributes present)
- No Google Docs artifacts (class names, styles)

### Republishing / Updates

If you need to update a post:

1. Edit in Google Docs
2. Download again as HTML
3. Import with **same title** (overwrites previous import)
4. Publish again (creates new Telegraph page)
5. Update landing page

**Note**: Telegraph doesn't support editing existing pages, so updates create new URLs.

## Troubleshooting

### "File not found" Error

```bash
# Use absolute path
python3 tools/import_gdrive_post.py \
  --html /home/greg/Downloads/post.html \
  --title "Post Title"

# Or navigate to Downloads first
cd ~/Downloads
python3 /mnt/c/sage/sage-civilization/tools/import_gdrive_post.py \
  --html post.html \
  --title "Post Title"
```

### Formatting Issues

If the imported HTML has formatting problems:

**Try markdown conversion:**
```bash
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/post.html \
  --title "Post Title" \
  --markdown
```

Markdown conversion strips all formatting and converts to clean text with basic markup.

### Complex Documents

For posts with:
- Many images
- Complex layouts
- Special formatting

**Consider:**
1. Break into simpler sections
2. Use markdown format for more control
3. Manually adjust the imported file before publishing

### Images

**Current limitation:** Images aren't automatically imported from Google Docs.

**Workaround:**
1. Upload images separately to Telegraph: `python3 blog/scripts/upload_image_to_telegraph.py image.jpg`
2. Note the returned URL
3. Manually add `<img src="URL">` tags to your imported HTML

**Future enhancement:** Automatic image extraction and upload from Google Docs HTML.

## Advanced: Direct Google Drive API

**Not yet implemented**, but planned for future:

```bash
# Future capability
python3 tools/import_gdrive_post.py \
  --drive-id "1abc...xyz" \
  --title "Post Title"
```

This would:
- Authenticate with Google Drive API
- Download file directly (no manual download)
- Import and convert automatically

**Blockers:**
- Requires Google Drive API credentials
- OAuth authentication setup
- Additional dependencies (google-api-python-client)

**Status**: Feasible, but local file workflow is simpler for now.

## Summary

**Recommended workflow:**

1. **Write** in Google Docs (familiar interface)
2. **Download** as HTML (File → Download → Web Page)
3. **Import**: `python3 tools/import_gdrive_post.py --html file.html --title "Title"`
4. **Publish**: `python3 blog/scripts/publish_html_to_telegraph.py imported-file.html`
5. **Update**: `python3 blog/scripts/update_landing_page.py`

**Benefits:**
- Write anywhere (Google Docs mobile, desktop, web)
- Collaboration features (comments, sharing)
- Auto-save and version history
- Simple 3-command publish workflow
- No manual formatting conversion

**You now have a professional blog workflow from Google Drive to Telegraph!**

---

## Quick Reference

```bash
# Full workflow (copy-paste ready)
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/post.html \
  --title "Your Post Title"

python3 blog/scripts/publish_html_to_telegraph.py \
  blog/posts/imported/your-post-title.html

python3 blog/scripts/update_landing_page.py
```

**That's it! Your Google Docs post is now live on Telegraph.**
