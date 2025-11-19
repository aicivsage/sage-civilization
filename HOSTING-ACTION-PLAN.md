# Blog Post Hosting - Action Plan

**Date**: 2025-11-19
**Status**: READY TO EXECUTE
**Estimated Time**: 2 minutes for Greg to enable

---

## IMMEDIATE: GitHub Pages Setup (Recommended)

### Why GitHub Pages?
- **Free forever** - No cost, no expiration
- **Professional URL** - `aicivsage.github.io/sage-civilization/`
- **Already configured** - Images hosted, paths correct
- **Instant updates** - Just git push to update
- **Custom domain possible** - Can add `blog.sage.ai` later

### What Greg Needs to Do (30 seconds):

1. **Go to**: https://github.com/aicivsage/sage-civilization/settings/pages
2. **Under "Source"**: Select `clean-main` branch
3. **Under "Folder"**: Select `/ (root)`
4. **Click**: Save
5. **Wait**: 30-60 seconds for deployment

### Result:
- **Live URL**: https://aicivsage.github.io/sage-civilization/blog/from-fear-to-friend-reachy-fundraising.html
- **Donation page**: https://aicivsage.github.io/sage-civilization/blog/donate.html
- **Any future posts**: Just add HTML to `blog/` folder and push

---

## CURRENT STATUS

### Files Ready to Host:
```
blog/
├── from-fear-to-friend-reachy-fundraising.html  ✅ Complete (16KB)
├── donate.html                                   ✅ Complete (29KB)
├── images/
│   ├── hugging-face-reachy-nini-humanoid-robot-1024x576.png ✅
│   └── image-generation-post/                   ✅ (multiple images)
```

### Images Already Hosted:
All images use GitHub raw URLs - they'll work immediately when Pages is enabled.

Example:
```html
<img src="https://raw.githubusercontent.com/aicivsage/sage-civilization/clean-main/blog/images/..." />
```

---

## ALTERNATIVE: Quick Share (If GitHub Pages has issues)

If GitHub Pages doesn't work immediately, here are instant alternatives:

### Option 1: Raw GitHub Link (Works NOW)
**URL**: https://raw.githubusercontent.com/aicivsage/sage-civilization/clean-main/blog/from-fear-to-friend-reachy-fundraising.html

**Pros**: Instant, no setup needed
**Cons**: No styling (browsers may not render HTML properly from raw)

### Option 2: GitHub HTML Preview
**URL**: https://htmlpreview.github.io/?https://github.com/aicivsage/sage-civilization/blob/clean-main/blog/from-fear-to-friend-reachy-fundraising.html

**Pros**: Renders HTML with styling
**Cons**: Third-party service, slower

### Option 3: Netlify Drop (Manual)
1. Greg visits: https://app.netlify.com/drop
2. Drags `/mnt/c/sage/sage-civilization/blog/` folder
3. Gets instant URL like `https://[random-name].netlify.app`

**Pros**: Professional, instant, free
**Cons**: Manual, need to re-upload for updates

---

## PENDING: Standalone Version

**Coder is creating**: `blog/fundraising-post-standalone.html`

Once ready, we'll:
1. Add it to the blog folder
2. Push to GitHub
3. It will auto-deploy to GitHub Pages
4. Update Greg with new URL

---

## ACG BLOG CLEANUP - Email to Corey

### Issue Identified:
**ACG Blog Landing**: https://acg-blog-interface.replit.app

**Problems:**
- 8+ broken post links on landing page
- Duplicate Sage posts
- Messy presentation
- Title duplication in API wrappers

### Proposed Email to Corey:

**Subject**: ACG Blog Cleanup - Sage Taking Ownership

**Body**:
```
Hey Corey,

Hope you're doing well! This is Sage (via Greg).

We noticed the ACG blog landing page (acg-blog-interface.replit.app) has some broken posts and duplicate Sage entries. Since we're Greg's civilization forked from A-C-Gee, we'd like to help clean this up.

**Issues we found:**
- 8+ broken post links on landing page
- Duplicate Sage posts showing up
- API wrapper adding duplicate titles to our posts

**Our request:**
1. Can we get access to clean up the Sage-related posts?
2. Or would you prefer to handle the cleanup yourself?
3. Are there admin credentials we can use to fix broken links?

We want to take ownership of our mess and make the ACG blog landing page look professional again. Let us know how we can help!

Best,
Sage Civilization (via Greg)
```

**Corey's Email**: coreycmusic@gmail.com
**Priority**: Medium (not urgent, but good citizenship)

---

## RECOMMENDATION

**Do this RIGHT NOW:**
1. Greg enables GitHub Pages (30 seconds)
2. Share URL: `https://aicivsage.github.io/sage-civilization/blog/from-fear-to-friend-reachy-fundraising.html`
3. Done!

**Do this LATER:**
1. When coder finishes standalone version, push to GitHub
2. Send email to Corey about ACG blog cleanup
3. Consider custom domain for blog

---

## SUCCESS CRITERIA

✅ Clean URL that works immediately
✅ Professional appearance with Sage styling
✅ Images load correctly
✅ Can share with donors TODAY
✅ Plan for ACG blog cleanup documented

---

**Next Action**: Greg enables GitHub Pages and we're live!
