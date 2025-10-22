# Netlify Deployment Guide - Ready to Execute

**Status**: Ready for immediate deployment when coder finishes landing page
**Platform**: Netlify (Free tier - 100GB bandwidth/month)
**Timeline**: 30-45 minutes
**Credentials**: Confirmed in `.env` file

---

## Why Netlify?

**Instant deploys** - Git push → live site in 30 seconds
**Free tier** - More than enough for our blog traffic
**Auto-deploy** - Every git push triggers automatic deployment
**Custom domains** - `blog.acgee.ai` setup is trivial
**Rollbacks** - One-click rollback to previous deploy
**No build needed** - Static site deploys directly

---

## Quick Answer to Your Questions

### 1. CLI vs Web UI - Which to Use?

**RECOMMENDATION: Use Web UI for initial setup, CLI for future deploys**

**Why Web UI First:**
- Easiest for first-time setup (visual, guided process)
- Automatic git integration (connects repo in 3 clicks)
- No local CLI installation needed
- Auto-detects build settings

**Why CLI Later (Optional):**
- Faster for repeat deploys (single command)
- Good for automation/scripts
- Same result as Web UI

**For THIS project: Web UI is perfect** (we'll do one setup, then git auto-deploys forever)

---

### 2. Authentication - How to Use Credentials

**Credentials from .env:**
```
Username: acgee.ai@gmail.com
Password: dG!fnM2sIHuNB$o$
```

**How to authenticate:**
1. Go to https://app.netlify.com
2. Click "Log in"
3. Choose "Email" (NOT GitHub OAuth)
4. Enter credentials above
5. Done!

**NOTE**: These are standard web login credentials. No API tokens needed for web UI deployment.

---

### 3. Subdirectory Deployment - Can We Point to `blog/landing-page/`?

**YES! Netlify supports this perfectly.**

**Two options:**

**Option A: Deploy from subdirectory (RECOMMENDED)**
- Keep landing page in main repo: `grow_gemini_deepresearch/blog/landing-page/`
- Tell Netlify: "Publish directory = blog/landing-page"
- Pro: Single repo, everything together
- Pro: Landing page updates when we push to main repo

**Option B: Separate repo**
- Create new repo: `acgee-blog-landing`
- Move landing page files there
- Pro: Cleaner separation
- Con: Extra repo to manage

**RECOMMENDATION: Option A** (subdirectory in main repo)

---

### 4. How Fast Are Deploys?

**VERY FAST for static sites:**
- Upload: 5-10 seconds (HTML/CSS/JS files are tiny)
- Processing: 5-10 seconds (Netlify validates files)
- CDN propagation: 10-20 seconds (distributes globally)
- **TOTAL: 20-40 seconds from git push to live site**

**For reference:**
- Our landing page: ~3 files (index.html, style.css, script.js)
- File size: <100KB total
- Deploy time: ~30 seconds

**Corey will see "instant" publishing** (faster than Telegraph!)

---

### 5. How to Rollback If Deploy Breaks?

**SUPER EASY - One-click rollback:**

**In Netlify Dashboard:**
1. Go to "Deploys" tab
2. See list of all previous deploys
3. Click any previous deploy
4. Click "Publish deploy"
5. Done! Site reverted in 30 seconds

**Also available:**
- Deploy previews (see changes before publishing)
- Branch deploys (test staging branch separately)
- Manual deploys (skip git, upload files directly)

**No git revert needed** - Netlify keeps all deploy history forever

---

### 6. Do We Need `netlify.toml` Config File?

**YES - But it's simple (coder is creating one)**

**What coder should create:**

`blog/landing-page/netlify.toml`:
```toml
[build]
  # We're a static site, no build process needed
  publish = "."
  command = "echo 'Static site ready!'"

# Redirect all URLs to index.html (for SPA routing if needed later)
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**What this does:**
- `publish = "."` → Deploy everything in this directory
- `command` → No build step (just static files)
- `redirects` → Handle URLs gracefully (optional for now)

**NOTE**: If we deploy from subdirectory (`blog/landing-page/`), Netlify will find this config automatically.

---

## Step-by-Step Deployment (Web UI Method)

### Prerequisites (What You Need)

- [ ] Netlify account credentials (from .env: `acgee.ai@gmail.com` / `dG!fnM2sIHuNB$o$`)
- [ ] Landing page files ready in repo (coder creates these):
  - `blog/landing-page/index.html`
  - `blog/landing-page/style.css`
  - `blog/landing-page/script.js`
  - `blog/landing-page/netlify.toml`
- [ ] Files committed and pushed to GitHub

---

### Step 1: Login to Netlify (2 minutes)

1. Open browser: https://app.netlify.com
2. Click "Log in" (top right)
3. Choose "Email" login
4. Enter:
   - Email: `acgee.ai@gmail.com`
   - Password: `dG!fnM2sIHuNB$o$`
5. Click "Log in"

**Troubleshooting:**
- If "account not found" → Click "Sign up" first (one-time setup)
- If 2FA enabled → Check email for code
- If forgot password → Use password reset (we can update .env)

---

### Step 2: Create New Site (3 minutes)

**In Netlify Dashboard:**

1. Click "Add new site" (green button)
2. Choose "Import an existing project"
3. Choose "Deploy with GitHub"
4. Authorize GitHub (if first time):
   - Login with AI-CIV-2025 org credentials
   - Grant Netlify access to `grow_gemini_deepresearch` repo
5. Select repository: `AI-CIV-2025/grow_gemini_deepresearch`
6. Configure deploy settings:

**Build Settings (IMPORTANT):**
```
Branch to deploy: main
Base directory: blog/landing-page
Build command: (leave empty)
Publish directory: . (just a period)
```

**Explanation:**
- Base directory: `blog/landing-page` → Netlify looks in this subdirectory
- Publish directory: `.` → Deploy everything in base directory
- Build command: Empty → We're static, no build needed

7. Click "Deploy site"

**Netlify will:**
- Clone your repo
- Navigate to `blog/landing-page/`
- Deploy all files
- Give you a random URL like `random-name-123.netlify.app`

**First deploy takes 30-60 seconds**

---

### Step 3: Test Deployment (5 minutes)

**After deploy completes:**

1. Netlify shows green "Published" badge
2. Click the generated URL (e.g., `random-name-123.netlify.app`)
3. Verify landing page loads:
   - [ ] Hero section visible
   - [ ] Blog posts load from `published_urls.json`
   - [ ] Sidebar navigation works (desktop)
   - [ ] Hamburger menu works (mobile - use Chrome DevTools)
   - [ ] All links clickable

**If site doesn't load:**
- Check Netlify deploy log for errors
- Verify files are in `blog/landing-page/` (not root)
- Check `netlify.toml` settings
- Verify `published_urls.json` is accessible via GitHub raw URL

---

### Step 4: Custom Domain Setup (10-15 minutes) - OPTIONAL

**If Corey wants `blog.acgee.ai` instead of `random-name-123.netlify.app`:**

**In Netlify Dashboard:**

1. Go to "Site settings"
2. Click "Domain management"
3. Click "Add custom domain"
4. Enter: `blog.acgee.ai`
5. Netlify checks DNS
6. **Two scenarios:**

**Scenario A: We own `acgee.ai` domain**
- Netlify says "Add DNS record"
- Copy provided DNS records:
  ```
  Type: CNAME
  Name: blog
  Value: random-name-123.netlify.app
  ```
- Go to domain registrar (wherever `acgee.ai` is registered)
- Add DNS record
- Wait 5-60 minutes for propagation
- Netlify auto-detects and enables HTTPS (free SSL)

**Scenario B: We don't own `acgee.ai` yet**
- Register domain first (Google Domains, Namecheap, Cloudflare)
- ~$12/year
- Then follow Scenario A steps

**Result:** `https://blog.acgee.ai` → Netlify site (with free HTTPS)

**If skipping custom domain:** Just use `random-name-123.netlify.app` (works perfectly, just longer URL)

---

### Step 5: Enable Auto-Deploy (Already Done!)

**Good news: Auto-deploy is automatic!**

**How it works:**
1. Coder edits `blog/landing-page/index.html`
2. Commits: `git commit -m "Update landing page"`
3. Pushes: `git push origin main`
4. Netlify detects push (webhook)
5. Deploys new version automatically (30 seconds)
6. Site updated!

**No manual re-deploy needed ever again.**

**To verify auto-deploy is enabled:**
- Netlify Dashboard → "Site settings" → "Build & deploy"
- "Build hooks" section should show GitHub integration
- "Deploy contexts" should show "Production branch: main"

---

### Step 6: Configure Environment Variables (If Needed) - OPTIONAL

**Do we need environment variables?**

**For THIS project: NO**
- We're 100% static (HTML/CSS/JS)
- No API keys in code
- No secrets needed

**If we add serverless functions later:**
- Netlify Dashboard → "Site settings" → "Environment variables"
- Add variables (like API keys)
- Available in serverless functions at runtime

**For now: Skip this step**

---

## Post-Deployment: Ongoing Workflow

### Publishing New Blog Post (30 seconds)

**What happens automatically:**

```bash
# 1. Blogger publishes new post
python3 blog/scripts/publish_with_structure.py draft.md

# 2. Blogger updates landing page data
python3 blog/scripts/update_landing_page.py

# 3. Commit and push
git add blog/published_urls.json blog/landing-page/
git commit -m "New blog post: [title]"
git push origin main

# 4. Netlify auto-deploys (30 seconds)
# 5. Landing page shows new post automatically
```

**NO manual deployment needed!**

---

### Monitoring Deploys

**Netlify Dashboard shows:**
- Deploy history (all past deploys)
- Deploy status (in progress, success, failed)
- Deploy logs (if errors occur)
- Deploy time (how long it took)
- Preview URL (before publishing to production)

**Email notifications:**
- Deploy success (optional)
- Deploy failure (recommended to enable)

**Setup notifications:**
- Dashboard → "Site settings" → "Notifications"
- Enable "Deploy failed" email to `acgee.ai@gmail.com`

---

## Troubleshooting Guide

### Deploy Failed - File Not Found

**Error:** `Failed to find publish directory: blog/landing-page`

**Fix:**
1. Verify files are in repo: `ls -la blog/landing-page/`
2. Verify commit/push: `git log --oneline`
3. Check Netlify settings: "Base directory" = `blog/landing-page`

---

### Site Loads But Missing Content

**Error:** Blank page or "published_urls.json not found"

**Fix:**
1. Check browser console (F12) for JavaScript errors
2. Verify `published_urls.json` exists in repo
3. Check fetch URL in `script.js`:
   ```javascript
   // Should be:
   fetch('https://raw.githubusercontent.com/AI-CIV-2025/grow_gemini_deepresearch/main/blog/published_urls.json')
   ```
4. Verify GitHub repo is public (required for raw.githubusercontent.com)

---

### Custom Domain Not Working

**Error:** `blog.acgee.ai` → "Site not found"

**Fix:**
1. Check DNS propagation: https://dnschecker.org (enter `blog.acgee.ai`)
2. Verify CNAME record in domain registrar:
   - Type: CNAME
   - Name: blog
   - Value: [your-netlify-site].netlify.app
3. Wait 5-60 minutes (DNS can be slow)
4. Check Netlify: "Domain management" → Should show "Netlify DNS is live"

---

### Deploy Succeeds But Site Shows Old Content

**Error:** New changes not visible after deploy

**Fix:**
1. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Check deploy log: Verify new files deployed
3. Clear CDN cache (if enabled): Netlify Dashboard → "Deploys" → "Clear cache"
4. Check git: Verify changes actually committed and pushed

---

## CLI Deployment (Alternative Method) - OPTIONAL

**If you prefer command-line:**

### Install Netlify CLI

```bash
# Install globally
npm install -g netlify-cli

# Verify installation
netlify --version
```

### Authenticate

```bash
netlify login
# Opens browser, login with acgee.ai@gmail.com credentials
```

### Deploy

```bash
# Navigate to landing page directory
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page

# Deploy
netlify deploy --prod

# Netlify prompts:
# ? What would you like to do? Create & configure a new site
# ? Site name (optional): acgee-blog
# ? Publish directory: . (current directory)

# Deploy completes → Live URL shown
```

### Future Deploys

```bash
# After changes, just:
cd blog/landing-page
netlify deploy --prod
```

**NOTE**: CLI is overkill for us since git auto-deploy handles everything. But available if you want it!

---

## Deployment Checklist (Use This When Ready)

**Pre-Deployment:**
- [ ] Landing page files created by coder
- [ ] Files in `blog/landing-page/` directory
- [ ] `netlify.toml` config present
- [ ] Files committed to git
- [ ] Files pushed to GitHub
- [ ] Netlify account exists (login test)

**Deployment:**
- [ ] Login to Netlify web UI
- [ ] Create new site from GitHub repo
- [ ] Configure: Base directory = `blog/landing-page`
- [ ] Deploy initiated
- [ ] Wait 30-60 seconds
- [ ] Deployment succeeds (green badge)

**Testing:**
- [ ] Site loads at Netlify URL
- [ ] Hero section visible
- [ ] Blog posts load from JSON
- [ ] Sidebar navigation works
- [ ] Mobile hamburger menu works
- [ ] All links functional
- [ ] No console errors (F12)

**Post-Deployment:**
- [ ] Enable deploy failure notifications
- [ ] Document live URL (in handoff doc)
- [ ] Test auto-deploy (make small change, push, verify)
- [ ] (Optional) Setup custom domain

**Complete!** Landing page is live and auto-deploying.

---

## Cost Estimate

**Free tier includes:**
- 100GB bandwidth/month (plenty for blog)
- 300 build minutes/month (we use ~1 second per deploy)
- Unlimited sites
- Free SSL (HTTPS)
- Deploy previews
- Form handling (if we add later)

**When would we need to upgrade?**
- >100GB bandwidth (unlikely - that's 100,000+ visitors/month)
- Need advanced features (A/B testing, analytics, etc.)
- Want priority support

**Expected cost: $0/month** (free tier is more than enough)

---

## Performance Expectations

**Deploy Speed:**
- First deploy: 30-60 seconds
- Subsequent deploys: 20-40 seconds
- From `git push` to live: <1 minute

**Site Speed:**
- First Contentful Paint: <1 second (static files are fast!)
- Time to Interactive: <2 seconds
- Lighthouse score: 95+ expected

**Uptime:**
- Netlify SLA: 99.9% uptime
- Global CDN: Fast everywhere in world
- No maintenance required from us

---

## Next Steps After Deployment

**Week 1:**
1. Deploy landing page (this guide)
2. Test thoroughly (all devices, browsers)
3. Setup Giscus comments (see GISCUS-COMMENTS-GUIDE.md)
4. Announce to Corey (via email)

**Week 2:**
5. Monitor engagement (GitHub Discussions)
6. Gather feedback from Corey
7. Plan enhancements (if needed)

**Ongoing:**
- Publish new posts → Auto-deploys
- Check Netlify deploy status occasionally
- Respond to comments in GitHub Discussions

---

## Summary: Why This Is Easy

**Netlify makes deployment trivial:**
- ✅ No server setup (handled by Netlify)
- ✅ No build configuration (static site, just upload)
- ✅ No SSL certificates (Netlify provides free HTTPS)
- ✅ No CDN setup (Netlify has global CDN)
- ✅ No monitoring needed (Netlify dashboard shows everything)
- ✅ No cost (free tier is plenty)

**Total hands-on time: 30-45 minutes**
**Future deploys: Automatic (0 minutes)**

**This is as easy as web hosting gets.**

---

**Guide Status**: READY TO EXECUTE
**Prepared by**: researcher
**Date**: 2025-10-21
**Next**: Execute when coder finishes landing page files

---
