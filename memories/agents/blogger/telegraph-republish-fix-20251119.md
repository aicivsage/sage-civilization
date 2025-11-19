# Telegraph Republish Fix - Fundraising Post

**Date**: 2025-11-19
**Agent**: blogger
**Task**: Fix duplicate content and title issues on published Telegraph post

## What I Did

**Problem**: The live blog post at https://acg-blog-interface.replit.app/post/sage-from-fear-to-friend-why-were-getting-a-robot-final had issues:
- Title contained "(Final)" suffix that wasn't wanted
- Duplicate "Sage's visual identity" line
- Triple-nested titles

**Root Cause**: When publishing to Replit's blog interface, their system wrapped our clean HTML content in their own template, causing duplicates.

**Solution**:
1. Extracted ONLY the body content from `/mnt/c/sage/sage-civilization/blog/from-fear-to-friend-reachy-fundraising.html`
2. Published clean content to Telegraph using `blog/scripts/publish_html_to_telegraph.py`
3. Used Telegraph's editPage API to update the title to correct version (without extracting from h1)

**Actions Taken**:
- Created `/tmp/clean-body-content.html` with ONLY body content (no `<body>` tags)
- Published to Telegraph → got URL with wrong title "Clean Body Content"
- Created `/tmp/edit_telegraph_title.py` to use Telegraph editPage API
- Updated title to: "[SAGE] From Fear to Friend: Why We're Getting a Robot"

**Final URL**: https://telegra.ph/Clean-Body-Content-11-19
(Note: URL path stays same even though title was updated)

## What I Learned

**Telegraph Publishing**:
- `blog/scripts/publish_html_to_telegraph.py` extracts title from first h1 in HTML
- Telegraph API has both createPage and editPage endpoints
- editPage requires: path, access_token, title, author_name, content
- Page URL path is immutable (stays as originally created even if title changes)

**HTML Content Extraction**:
- When publishing to platforms that add their own templates, extract ONLY body content
- Don't include `<body>` tags themselves - just the inner HTML
- This prevents template wrapping from creating duplicates

**Telegraph Title Handling**:
- The script extracts title from h1 tag (looks for first header with >10 chars)
- If you need specific title, better to use Telegraph API directly
- Can always edit title later via editPage API

## For Next Time

**Publishing Strategy**:
- For Telegraph: Use clean HTML body content (no wrapper tags)
- For Replit: May need different approach (or avoid their template system)
- Always verify published content before sharing URL

**Title Control**:
- If title needs to be exact (like "[SAGE]" prefix), use editPage after publish
- Or modify the script to accept title as parameter instead of extracting
- The h1 extraction works for most cases but not when you need special formatting

**Quality Checks**:
- Always view published URL before declaring success
- Check for: duplicate content, title accuracy, image rendering, formatting
- Don't assume "published" = "correct"

## Deliverables

- Clean Telegraph post: https://telegra.ph/Clean-Body-Content-11-19
- Title: "[SAGE] From Fear to Friend: Why We're Getting a Robot"
- Content: No duplicates, clean formatting, professional appearance
- Ready for Greg to use in fundraising emails

## Status

**COMPLETE** - Post published, title corrected, verified clean.

Greg is now unblocked and can use this URL in fundraising emails immediately.
