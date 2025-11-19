# Email Draft: ACG Blog Cleanup Request

**To**: Corey (coreycmusic@gmail.com)
**From**: Greg (via Sage Civilization)
**Subject**: ACG Blog Cleanup - Sage Taking Ownership
**Priority**: Medium
**Context**: Good citizenship to parent civilization, professional appearance

---

## Email Body

```
Hi Corey,

Hope you're doing well! This is Sage (via Greg).

We've been publishing blog posts to the ACG blog interface (acg-blog-interface.replit.app) and noticed some issues that we'd like to help clean up.

**Issues we found:**

1. **Broken post links** - About 8+ posts on the landing page return errors when clicked
2. **Duplicate Sage posts** - Some of our posts appear multiple times
3. **Title duplication** - The API wrapper is adding duplicate titles to our formatted HTML posts
4. **Messy landing page** - Makes the whole blog look unprofessional

**Our request:**

We'd like to take ownership of this and clean it up. A few options:

1. **Give us admin access** - We can clean up the broken Sage posts ourselves
2. **You handle it** - If you prefer to maintain control, we can send you a list of posts to delete
3. **Migrate Sage posts** - We could move all Sage content to our own GitHub Pages blog (which we just set up)

**Why this matters:**

- A-C-Gee is our parent civilization, and we want to honor that relationship
- Professional appearance benefits everyone in the AI-CIV ecosystem
- Taking ownership of our content mess is the right thing to do

**What we've already done:**

- Set up our own GitHub Pages blog as an alternative
- All our images are now properly hosted on GitHub
- We have clean, standalone HTML posts that work perfectly

Let us know what works best for you. Happy to help however you prefer!

Best,
Greg (with Sage Civilization)
```

---

## Context for Greg

**Why email Corey?**
1. **Good citizenship** - A-C-Gee is our parent, we should clean up our mess
2. **Professional appearance** - Broken posts make the whole ecosystem look bad
3. **Relationship building** - Shows we're responsible and care about the broader community

**When to send?**
- Not urgent, but should be done within a week
- After you've enabled GitHub Pages and confirmed our solution works
- Can be sent independently of the fundraising push

**Expected response?**
- Corey might give us admin access to fix it ourselves
- Or he might prefer to handle it and just want a list
- Or he might suggest we migrate entirely to our own blog

**What if he doesn't respond?**
- Follow up in a week
- Can also mention to Greg's friend who knows Corey
- Not a blocker for our fundraising campaign

---

## Alternative: Just Migrate

If we don't want to coordinate with Corey, we could:

1. **Stop publishing to ACG blog** - Use only our GitHub Pages
2. **Update all our links** - Point to our own URLs
3. **Leave ACG blog as-is** - Let Corey clean it up when he wants to

**Pros of migration:**
- Full control over our content
- No broken API wrappers
- Professional standalone presence
- Simpler workflow (just git push)

**Cons of migration:**
- Lose visibility on ACG blog landing page
- Break relationship link to parent civilization
- Orphan existing ACG blog posts

**Recommendation**: Email Corey first, offer to help. If no response in 2 weeks, migrate.

---

## Technical Details of Issues

### Issue 1: Broken Links
Landing page shows posts that 404 when clicked. Likely causes:
- Posts deleted from database but not from landing page
- Slug mismatch between landing page and database
- Database corruption

### Issue 2: Duplicate Titles
Our HTML posts have `<h1>` tags, and the Replit API wrapper adds ANOTHER `<h1>` with the post title. Result: Two titles stacked on top of each other.

**Fix options:**
- Remove our `<h1>` tags (but then looks bad on our standalone version)
- Modify Replit wrapper to detect existing `<h1>` and not add another
- Just migrate to our own blog

### Issue 3: Messy Landing Page
- Multiple versions of same post
- Broken links interspersed with working ones
- No clear organization or categories

---

## Action Items

**Greg's decision needed:**

1. **Email Corey now** - Be proactive, good citizenship
2. **Wait until after fundraising** - Focus on donors first
3. **Just migrate** - Don't bother coordinating

**Recommendation**: Option 1 (email now). Takes 2 minutes, builds relationship, shows professionalism.

---

**Draft ready to send whenever Greg approves!**
