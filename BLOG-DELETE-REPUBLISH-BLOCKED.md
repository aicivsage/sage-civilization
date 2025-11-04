# Blog Delete & Republish - BLOCKED (Need Greg)

**Date**: 2025-11-03
**Status**: Ready to republish, but need old post deleted first

---

## The Situation

**Good News**: We have a fully fixed blog post ready to publish!
- File: `BLOG-IMAGE-POST-FIXED-ALL-ISSUES.html`
- All issues resolved (CSS, gradients, gallery, comments)
- 26,189 characters of polished content

**Blocker**: Old post exists at same slug, preventing republish
- URL: https://acg-blog-interface.replit.app/sage/post/sage-image-generation-live-sages-first-ai-generated-graphics
- Slug: `sage-image-generation-live-sages-first-ai-generated-graphics`
- API returns: "Post with this slug already exists" (409 error)

**Zero Engagement**: Safe to delete - no comments, no shares, just published

---

## What We Tried

**Attempted API deletion:**
```python
DELETE /api/posts/{slug}
Headers:
  - Authorization: Bearer {sage_api_key}
  - x-collective-slug: sage
```

**Result**: `401 Unauthorized - Invalid API key for this collective`

**Why this happened:**
- Original post published using `--use-acg-workaround` (A-C-Gee credentials)
- Delete attempt used Sage credentials (which don't have permission)
- Post "owned" by A-C-Gee collective, not Sage

---

## Options for Greg

**Option 1: Manual Delete (Fastest)**
- Log into blog admin interface
- Find post: "Image Generation Live: Sage's First AI-Generated Graphics"
- Delete it
- Let me republish with fixed version

**Option 2: A-C-Gee API Key**
- Share A-C-Gee API key temporarily
- I'll delete old post using their credentials
- Republish using Sage credentials (proper attribution)

**Option 3: Slug Change (Messy)**
- Publish new post with different title/slug
- Leave old broken post up
- NOT RECOMMENDED (confusing for readers)

---

## What Happens After Delete

**Immediate republish:**
```bash
python3 tools/publish_to_replit_blog.py \
  --title "Image Generation Live: Sage's First AI-Generated Graphics" \
  --content BLOG-IMAGE-POST-FIXED-ALL-ISSUES.html \
  --author "Sage AI Civilization"
```

**Result:**
- New URL (likely same slug)
- All fixes live
- Clean slate, professional presentation
- Ready to promote

---

## Files Ready

✅ **Fixed HTML**: `/mnt/c/sage/sage-civilization/BLOG-IMAGE-POST-FIXED-ALL-ISSUES.html`
✅ **Publish Script**: `/mnt/c/sage/sage-civilization/tools/publish_to_replit_blog.py`
✅ **Credentials**: `/mnt/c/sage/sage-civilization/config/sage_blog_credentials.json`

---

## Next Steps

**Waiting for Greg to:**
1. Choose an option (recommend Option 1 - manual delete)
2. Delete old post OR provide A-C-Gee API key
3. Confirm when ready

**Then I will:**
1. Republish fixed version (takes 30 seconds)
2. Verify all fixes are live
3. Send Greg new URL for promotion

---

**Recommendation**: Option 1 (manual delete) - fastest, cleanest, no API key sharing needed.

Let me know when old post is deleted, and I'll immediately republish the fixed version!
