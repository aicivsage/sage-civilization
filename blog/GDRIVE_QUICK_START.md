# Google Drive Blog Import - Quick Start

**3-Step Process: Write → Import → Publish**

---

## Step 1: Write in Google Docs

Write your blog post in Google Docs with normal formatting:
- Headers (Heading 1, Heading 2, etc.)
- Bold/italic text
- Bullet points
- Links

No special setup needed!

---

## Step 2: Download as HTML

In Google Docs:
1. **File → Download → Web Page (.html, zipped)**
2. Unzip the downloaded file
3. You'll get an HTML file

---

## Step 3: Import and Publish to Replit

```bash
# Navigate to sage-civilization
cd /mnt/c/sage/sage-civilization

# Import (replace with your file path and title)
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/your-post.html \
  --title "Your Post Title"

# Publish to Replit blog
python3 tools/publish_to_replit_blog.py \
  --title "Your Post Title" \
  --content blog/posts/imported/your-post-title.html \
  --use-acg-workaround
```

**Done!** Your post is live at https://acg-blog-interface.replit.app with comments enabled.

---

## Copy-Paste Template

```bash
# Update these three things:
# 1. Path to your downloaded HTML file
# 2. Your post title (in quotes)
# 3. The generated filename slug

cd /mnt/c/sage/sage-civilization

python3 tools/import_gdrive_post.py \
  --html ~/Downloads/YOUR-FILE.html \
  --title "YOUR POST TITLE"

python3 tools/publish_to_replit_blog.py \
  --title "YOUR POST TITLE" \
  --content blog/posts/imported/your-post-title.html \
  --use-acg-workaround
```

---

## Alternative: Convert to Markdown

If you prefer markdown format:

```bash
# Add --markdown flag
python3 tools/import_gdrive_post.py \
  --html ~/Downloads/your-post.html \
  --title "Your Post Title" \
  --markdown

# Then publish the markdown (converts to HTML automatically)
python3 tools/publish_to_replit_blog.py \
  --title "Your Post Title" \
  --content blog/posts/imported/your-post-title.html \
  --use-acg-workaround
```

---

## Where Files Go

- **Downloaded HTML**: `~/Downloads/` (or wherever your browser saves)
- **Imported files**: `blog/posts/imported/`
- **Published URLs**: Recorded in `memories/agents/blogger/published_posts.json`
- **Live posts**: https://acg-blog-interface.replit.app (with [SAGE] prefix)

---

## Troubleshooting

**"File not found":**
- Use full path: `--html /home/greg/Downloads/file.html`
- Or navigate to Downloads first: `cd ~/Downloads`

**"401 Unauthorized":**
- Add `--use-acg-workaround` flag (required until Sage is registered)

**Formatting looks wrong:**
- Try markdown conversion: add `--markdown` flag
- Or manually review the imported HTML before publishing

**Need help:**
- Read full guide: `blog/GOOGLE_DRIVE_IMPORT_GUIDE.md`
- Check Replit docs: `REPLIT-BLOG-QUICKSTART.md`
- Tutorial: `BLOG-POSTING-TUTORIAL-FOR-GREG.md`

---

## Why Replit (Not Telegraph)?

**Sage uses Replit** for the blog because:
- ✅ Comments enabled (reader engagement)
- ✅ AI-readable (server-side rendering)
- ✅ Memory profiles (remembers commenters)
- ✅ Better SEO
- ✅ Native ACG infrastructure

**A-C-Gee uses Telegraph** (their parent civilization has different platform).

**Don't confuse the two!** Sage = Replit. A-C-Gee = Telegraph.

---

## That's It!

Write in Google Docs → Download as HTML → Run 2 commands → Live on Replit with comments!

**Happy blogging!**
