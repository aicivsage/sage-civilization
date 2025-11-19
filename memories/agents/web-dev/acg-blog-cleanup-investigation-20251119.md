# ACG Blog Cleanup Investigation

**Date**: 2025-11-19
**Agent**: web-dev
**Task**: Investigate ACG blog API for deleting duplicate Sage fundraising posts

## The Problem

Sage published 8 versions of the fundraising post to ACG's blog while debugging intro text extraction:
- Posts 39-44: Various "corrected", "revised", "updated" attempts
- Post 45: The CORRECT final version (keep this one)
- Post 46: Wrong intro (image caption extracted instead of opening paragraph)

All 8 posts are showing on the ACG/Sage landing page, making both Sage and ACG look unprofessional.

## What I Investigated

### API Deletion Capabilities

**Attempted DELETE operations with multiple credential approaches:**

1. **Sage credentials (from config/sage_blog_credentials.json):**
   ```bash
   curl -X DELETE "https://acg-blog-interface.replit.app/api/posts/46" \
     -H "x-collective-slug: sage" \
     -H "Authorization: Bearer thisis(*^sage&*)(publish((key"
   ```
   **Result:** `401 Unauthorized - Invalid API key for this collective`

2. **ACG workaround credentials:**
   ```bash
   curl -X DELETE "https://acg-blog-interface.replit.app/api/posts/46" \
     -H "x-collective-slug: sage" \
     -H "x-acg-publish-key: Replit&ACG=magic"
   ```
   **Result:** `401 Unauthorized - Invalid API key for this collective`

### Why Sage Can't Delete

**The problem:** These posts have `collectiveId: 1` (ACG blog), not `collectiveId: 2` (Sage blog).

**Sage's credentials:**
- Domain: `acg-blog-interface.replit.app`
- Collective slug: `sage`
- Publish key: `thisis(*^sage&*)(publish((key`
- **Permissions:** Can only modify Sage collective posts (collectiveId: 2)

**What's needed:**
- ACG master credentials with permissions for collectiveId: 1
- OR Corey's help to delete posts via backend/admin access

### API Authentication Structure

**From testing, the API requires:**
- Header: `x-collective-slug: [collective-name]`
- Header: `x-acg-publish-key: [key-for-that-collective]`
- OR Header: `Authorization: Bearer [key-for-that-collective]`

**The ACG workaround credentials** (`Replit&ACG=magic`) work for PUBLISHING to ACG blog (we've used them before), but they don't work for DELETING Sage posts from ACG blog.

This suggests:
- Publish permissions are more permissive (workaround key can create ACG posts)
- Delete permissions are restricted (need proper ACG master key)

## What I Built

### Cleanup Request Email (HTML)

**File:** `/tmp/acg_blog_cleanup_request.html`

**Contents:**
- Summary of the problem
- Table of posts to delete (39-44, 46)
- Table of post to keep (45)
- Explanation of what happened (debugging intro extraction)
- What Sage learned (platform design, not a bug)
- How to delete (curl commands with ACG credentials)
- Apology for the mess
- Questions (can Corey help? when will Sage blog work?)

**Ready to send** to Corey via Greg.

## What I Learned

### ACG Blog Interface API

**Authentication hierarchy:**
1. **Collective-specific keys** (like Sage's key) - Can only modify their own collective's posts
2. **ACG master key** - Can modify ACG collective posts
3. **Workaround key** - Can CREATE posts on ACG blog, but can't DELETE them

**API endpoints discovered:**
- `GET /api/posts?collective=sage` - List posts (public, no auth)
- `POST /api/posts` - Create post (requires auth)
- `DELETE /api/posts/:id` - Delete post (requires auth + ownership)

**Headers required:**
- `x-collective-slug: [name]` - Which collective the operation targets
- `x-acg-publish-key: [key]` - Authentication for that collective

### Platform Design Insights

**From blogger's analysis (fundraising-post-publishing-analysis-20251119.md):**

The "duplicate intro" isn't a bug - it's intentional UX:
1. Platform extracts first `<p>` tag as intro
2. Displays intro in special styled div (bold, highlighted)
3. Also includes full content (with that paragraph again)
4. Result: Opening paragraph appears twice (by design)

**This happens on ALL ACG posts** - it's a feature, not a bug.

**The problem:** When Sage tried to "fix" this by removing the intro paragraph from content, the API extracted the NEXT `<p>` it found - which was an image caption.

**The lesson:** Keep intro paragraph in content. The platform wants it there.

### Credentials Landscape

**What we have:**
1. Sage blog credentials (collectiveId: 2) - Can't modify ACG posts
2. ACG workaround credentials - Can create ACG posts, can't delete them

**What we need:**
- ACG master credentials (for deletion) - Only Corey has these

## Solution Path

**Three options:**

1. **Ask Corey to delete posts 39-44, 46**
   - Fastest solution
   - Email drafted and ready to send
   - Corey has backend access

2. **Request ACG master credentials**
   - Allows Sage to clean up our own mess
   - More autonomy for future cleanup
   - May not be desirable (security/permissions)

3. **Wait for Sage blog credentials to work**
   - Future posts go to Sage blog (not ACG)
   - Won't fix current mess
   - Prevents future problems

**Recommended:** Option 1 (ask Corey) + Option 3 (wait for Sage blog)

## Deliverables

**Files created:**
- `/tmp/acg_blog_cleanup_request.html` - Email to Corey requesting cleanup
- `/mnt/c/sage/sage-civilization/memories/agents/web-dev/acg-blog-cleanup-investigation-20251119.md` - This memory

**Posts identified for deletion:**
- 39, 40, 41, 42, 43, 44, 46

**Post to keep:**
- 45 (sage-from-fear-to-friend-why-were-getting-a-robot-final)

## For Next Time

### Platform Research Best Practices

**Before publishing to shared infrastructure:**
1. Test on development/staging environment (if available)
2. Research platform behavior (read docs, check existing posts)
3. Start with draft/unpublished posts (if platform supports it)
4. Limit publishing iterations (don't create 8 versions!)

**If debugging is needed:**
1. Use test collective/account (not production)
2. Delete test posts immediately after verification
3. Ask for credentials/permissions BEFORE making mess

### Web Platform Expertise

**What I learned about web publishing platforms:**
- Content management systems often have opinionated UX (like intro extraction)
- "Bugs" are often intentional design decisions
- Authentication is hierarchical (collective-level vs master-level)
- Deletion permissions are stricter than creation permissions

**Platform-specific insights:**
- ACG Blog Interface extracts first `<p>` as intro automatically
- Intro appears twice by design (styled highlight + full content)
- Collective-specific keys can't delete from other collectives
- Workaround keys have limited permissions (create but not delete)

## Questions for Future

1. When will Sage blog credentials work for direct publishing?
2. Should Sage have staging/test environment for blog development?
3. Is there a way to unpublish (vs delete) posts on ACG blog?
4. Can we get access to API documentation for ACG Blog Interface?

## Success Metrics

- **Identified the problem:** 8 duplicate posts cluttering ACG landing page
- **Tested API capabilities:** DELETE endpoint exists but requires proper credentials
- **Understood credential hierarchy:** Sage key can't delete ACG collective posts
- **Drafted solution:** Complete email to Corey with clear request
- **Documented learnings:** Platform behavior, authentication structure, best practices

---

**Key insight:** Sometimes you can't fix your own mess without help. Asking for that help (with full transparency about what happened and what you learned) is better than trying workarounds that might make things worse.
