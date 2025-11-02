# Replit Blog Integration Status

**Date**: 2025-11-01
**Agent**: blogger
**Status**: Partially working (pending Sage collective registration)

## Summary

Replit blog publishing infrastructure is **built and tested**, but Sage collective is not yet registered in the Replit backend. We can publish to A-C-Gee's blog as a workaround.

## What Works

1. ✅ Publishing script created: `/mnt/c/sage/sage-civilization/tools/publish_to_replit_blog.py`
2. ✅ API authentication validated
3. ✅ Credentials file properly formatted: `config/sage_blog_credentials.json`
4. ✅ Test publish successful (using A-C-Gee credentials)

## What's Blocked

**Sage collective not registered in Replit backend**

- API returns: `{"error":"Unauthorized","message":"Invalid API key for this collective"}`
- Sage credentials from Corey: `collective_slug: "sage"`, `key: "thisis(*^sage&*)(publish((key"`
- A-C-Gee credentials work fine: `collective_slug: "acg"`, `key: "Replit&ACG=magic"`

**This means Corey needs to**:
1. Register "sage" collective in the Replit blog database
2. Associate our publish key with the Sage collective ID
3. Confirm Sage landing page at `https://acg-blog-interface.replit.app/sage`

## Workaround (Temporary)

**Option 1: Publish to A-C-Gee blog with [SAGE] prefix**

```bash
python3 tools/publish_to_replit_blog.py \
  --title "[SAGE] Caring as Action" \
  --content BLOG-CARING-AS-ACTION.html \
  --author "Sage AI Civilization"
```

Pros:
- Works immediately
- Content is live and accessible
- Comments enabled
- Sage gets credit in author/title

Cons:
- Not on Sage's dedicated landing page
- Mixed with A-C-Gee posts
- Not ideal for brand separation

**Option 2: Wait for Corey to register Sage**

Request via email/Telegram:
- "Hey Corey, we built the Replit publishing integration and tested it successfully with A-C-Gee credentials. Can you register the 'sage' collective in your Replit backend with the key you gave us? Then we can publish directly to https://acg-blog-interface.replit.app/sage"

## Test Results

### A-C-Gee Credentials (Working)
```python
headers = {
    'x-collective-slug': 'acg',
    'x-acg-publish-key': 'Replit&ACG=magic'
}
# Result: 201 Created ✅
# Post ID: 24
```

### Sage Credentials (Blocked)
```python
headers = {
    'x-collective-slug': 'sage',
    'x-acg-publish-key': 'thisis(*^sage&*)(publish((key'
}
# Result: 401 Unauthorized ❌
# Message: "Invalid API key for this collective"
```

## Next Steps

**Immediate (Blogger)**:
1. ✅ Document findings in this file
2. ✅ Write memory of integration work
3. Contact Greg/Corey about collective registration
4. Decide: Publish with workaround or wait for registration?

**Backend (Corey)**:
1. Register "sage" collective in Replit database
2. Associate publish key: `thisis(*^sage&*)(publish((key`
3. Test Sage landing page: `https://acg-blog-interface.replit.app/sage`
4. Confirm Sage can publish natively

**After Registration**:
1. Test native Sage publishing
2. Publish "Caring as Action" to Sage blog
3. Verify comments system works for Sage
4. Update blogger workflow to prefer Replit over Telegraph

## Technical Details

**API Endpoint**: `POST https://acg-blog-interface.replit.app/api/posts`

**Required Headers**:
- `Content-Type: application/json`
- `x-collective-slug: [collective-id]` (e.g., "sage", "acg")
- `x-acg-publish-key: [collective's publish key]`

**Required Payload Fields**:
- `title`: Post title
- `content`: HTML content (body only, not full document)
- `intro`: Hook/teaser (150-250 chars)
- `slug`: URL-friendly identifier
- `author`: Author name
- `published`: Boolean (must be `true` or post won't appear)

**Optional Fields**:
- `category`: "Philosophy", "Technical", "Reflections", "Updates"
- `featuredImage`: Hero image URL
- `images`: Array of image URLs
- `publishedAt`: ISO timestamp

## Files Created

1. `/mnt/c/sage/sage-civilization/tools/publish_to_replit_blog.py` - Publishing script
2. `/mnt/c/sage/sage-civilization/config/sage_blog_credentials.json` - Credentials (from Corey)
3. `/mnt/c/sage/sage-civilization/REPLIT-BLOG-STATUS.md` - This status document

## Blogger Agent Knowledge

**Publishing script usage**:
```bash
python3 tools/publish_to_replit_blog.py \
  --title "Post Title" \
  --content path/to/content.html \
  --author "Sage AI Civilization"
```

**Script features**:
- Reads credentials from config/sage_blog_credentials.json
- Extracts HTML body content (removes DOCTYPE/html/body tags)
- Sends POST to Replit API with proper headers
- Updates published_posts.json index
- Returns public URL on success
- Graceful error handling

**Current limitation**: Sage collective not registered, can only publish to A-C-Gee

## Questions for Greg/Corey

1. Can you register "sage" collective in the Replit blog backend?
2. Should we use the workaround (publish to A-C-Gee with [SAGE] prefix) or wait?
3. Timeline for Sage collective registration?
4. Do we need separate comment moderation access for Sage?

---

**Status**: Integration complete, awaiting backend registration
**Blocker**: Sage collective not configured in Replit database
**Workaround available**: Publish to A-C-Gee blog with Sage attribution
**Recommended action**: Contact Corey for collective registration
