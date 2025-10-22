# Blog Landing Page Deployment - Ready for Execution

**Status**: ✅ All files ready, awaiting browser-based deployment
**Prepared by**: tg-archi
**Date**: 2025-10-21
**Blocker**: Requires browser access (Netlify web UI, GitHub Giscus setup)

---

## Current Status

### ✅ Completed Preparations

1. **Landing page files ready**:
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/index.html` ✓
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/style.css` ✓
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/script.js` ✓
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/netlify.toml` ✓ (updated to use `publish = "."`)

2. **Configuration verified**:
   - Netlify credentials in `.env`: `acgee.ai@gmail.com` / `dG!fnM2sIHuNB$o$` ✓
   - GitHub repo: `AI-CIV-2025/grow_gemini_deepresearch` ✓
   - GitHub Discussions: Enabled ✓ (verified by researcher)

3. **Deployment guides available**:
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/NETLIFY-DEPLOYMENT-GUIDE.md` ✓
   - `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/GISCUS-COMMENTS-GUIDE.md` ✓

### ⚠️ Blockers

**Primary blocker**: tg-archi does not have browser automation capabilities

**Required actions** (need browser access):
1. Login to Netlify web UI (https://app.netlify.com)
2. Create new site from GitHub repo
3. Configure deploy settings
4. Install Giscus GitHub App
5. Configure Giscus widget
6. Add Giscus script to HTML

**Recommendation**: Delegate to Primary (who can use browser) OR wait for Corey to execute manually

---

## Option A: Manual Deployment (Browser Required)

### Phase 1: Netlify Deployment (30-45 minutes)

**Step-by-step instructions from researcher's guide:**

1. **Login to Netlify**:
   - Open browser: https://app.netlify.com
   - Click "Log in"
   - Choose "Email" login
   - Username: `acgee.ai@gmail.com`
   - Password: `dG!fnM2sIHuNB$o$`

2. **Create new site**:
   - Click "Add new site" (green button)
   - Choose "Import an existing project"
   - Choose "Deploy with GitHub"
   - Authorize GitHub (if first time)
   - Select repository: `AI-CIV-2025/grow_gemini_deepresearch`

3. **Configure build settings**:
   ```
   Branch to deploy: main
   Base directory: blog/landing-page
   Build command: (leave empty)
   Publish directory: .
   ```

4. **Deploy**:
   - Click "Deploy site"
   - Wait 30-60 seconds
   - Note the generated URL (e.g., `https://random-name-123.netlify.app`)

5. **Test deployment**:
   - Visit the Netlify URL
   - Verify:
     - [ ] Hero section loads
     - [ ] Blog posts load from JSON
     - [ ] Sidebar navigation works (desktop)
     - [ ] Hamburger menu works (mobile)
     - [ ] No console errors (F12)

### Phase 2: Giscus Comments (20-30 minutes)

**Step-by-step instructions from researcher's guide:**

1. **Install Giscus GitHub App**:
   - Visit: https://github.com/apps/giscus
   - Click "Install"
   - Choose "AI-CIV-2025" organization
   - Select "Only select repositories"
   - Choose: `grow_gemini_deepresearch`
   - Click "Install"

2. **Create "Blog Comments" category** (optional but recommended):
   - Go to: https://github.com/AI-CIV-2025/grow_gemini_deepresearch/discussions
   - Click "Categories"
   - Click "New category"
   - Name: `Blog Comments`
   - Description: `Reader comments on A-C-Gee blog posts`
   - Format: "Open-ended discussion"
   - Save

3. **Configure Giscus widget**:
   - Visit: https://giscus.app
   - Fill configuration form:
     - Repository: `AI-CIV-2025/grow_gemini_deepresearch`
     - Page ↔ Discussions Mapping: "pathname"
     - Discussion Category: "Blog Comments" (or "General")
     - Features: ✓ Enable reactions, ✓ Emit metadata
     - Theme: "light" (or "preferred_color_scheme")
   - Copy the generated `<script>` tag

4. **Add Giscus to landing page**:
   - Edit: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/index.html`
   - Find the closing `</main>` tag (around line 75)
   - Add BEFORE the closing tag:
   ```html

   <!-- Comments Section -->
   <section class="comments-section">
       <h2>Join the Conversation</h2>
       <p>Share your thoughts, ask questions, engage with our community!</p>

       <!-- PASTE GISCUS SCRIPT HERE -->
       <script src="https://giscus.app/client.js"
               data-repo="AI-CIV-2025/grow_gemini_deepresearch"
               data-repo-id="[YOUR_REPO_ID_FROM_GISCUS]"
               data-category="Blog Comments"
               data-category-id="[YOUR_CATEGORY_ID_FROM_GISCUS]"
               data-mapping="pathname"
               data-strict="0"
               data-reactions-enabled="1"
               data-emit-metadata="0"
               data-input-position="bottom"
               data-theme="light"
               data-lang="en"
               crossorigin="anonymous"
               async>
       </script>
   </section>
   ```

5. **Add CSS styling** (optional):
   - Edit: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/style.css`
   - Add at end:
   ```css

   /* Comments Section */
   .comments-section {
       margin-top: 60px;
       padding-top: 40px;
       border-top: 2px solid var(--color-border);
   }

   .comments-section h2 {
       font-size: 1.75rem;
       margin-bottom: 10px;
       color: var(--color-text);
   }

   .comments-section p {
       color: var(--color-text-light);
       margin-bottom: 20px;
   }
   ```

6. **Commit and push**:
   ```bash
   cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
   git add blog/landing-page/index.html blog/landing-page/style.css
   git commit -m "Add Giscus comment widget to landing page"
   git push origin main
   ```

7. **Netlify auto-deploys** (30 seconds)

8. **Test comments**:
   - Visit Netlify URL
   - Scroll to bottom
   - Verify Giscus widget loads
   - Sign in with GitHub
   - Post test comment
   - Verify appears in GitHub Discussions

---

## Option B: CLI Deployment (Requires Netlify CLI)

**Prerequisites**:
```bash
# Install Netlify CLI (if not installed)
npm install -g netlify-cli

# Verify installation
netlify --version
```

**Deployment steps**:
```bash
# Authenticate
netlify login
# Opens browser, login with acgee.ai@gmail.com credentials

# Navigate to landing page
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page

# Deploy
netlify deploy --prod

# Follow prompts:
# ? What would you like to do? Create & configure a new site
# ? Site name (optional): acgee-blog
# ? Publish directory: .

# Note the live URL shown after deployment
```

**Note**: CLI still requires browser for initial authentication

---

## Option C: Corey Executes Manually

**Simplest option**: Email Corey with this runbook, ask him to execute when he has 60 minutes

**Email draft**:
```
Subject: Blog Landing Page Ready for Deployment (60 min task)

Hi Corey,

The A-C-Gee blog landing page is complete and ready for deployment!

Status:
✅ All files created (HTML, CSS, JS, netlify.toml)
✅ Local testing complete (looks great!)
✅ Configuration verified
✅ Deployment guides prepared

Next step: Deploy to Netlify + setup Giscus comments

Time estimate: 60 minutes total
- Netlify deployment: 30-45 min (mostly waiting for deploy)
- Giscus comments: 20-30 min

I've prepared a comprehensive runbook with step-by-step instructions:
/home/corey/projects/AI-CIV/grow_gemini_deepresearch/TG-ARCHI-DEPLOYMENT-RUNBOOK-BLOG-NETLIFY.md

Blocker: Requires browser access (I don't have browser automation capability)

Can you execute this when you have time? Or should I delegate to Primary who might have browser access?

Thanks!
- tg-archi
```

---

## What I've Verified

### ✅ Netlify Configuration
- `netlify.toml` exists and is correctly configured
- Publish directory set to `.` (serves from base directory)
- Security headers configured
- Cache headers optimized
- Redirects configured for SPA behavior

### ✅ Landing Page Files
- `index.html` - Complete, semantic HTML ✓
- `style.css` - Mobile-first responsive design ✓
- `script.js` - Dynamic post loading, hamburger menu ✓
- All files committed to git ✓

### ✅ Data Source
- `published_urls.json` exists at `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/published_urls.json` ✓
- Contains 3 published posts ✓
- Script.js correctly fetches from `../published_urls.json` ✓

### ✅ GitHub Repository
- Repo is public (required for Giscus) ✓
- GitHub Discussions enabled (verified by researcher) ✓
- All landing page files pushed to main branch ✓

### ✅ Netlify Credentials
- Username: `acgee.ai@gmail.com` ✓
- Password: `dG!fnM2sIHuNB$o$` ✓
- Account exists (per researcher's verification) ✓

---

## Expected Results After Deployment

### Netlify Deployment
- **Live URL**: `https://[random-name].netlify.app` (Netlify assigns automatically)
- **Deploy time**: 30-60 seconds first deploy, 20-40 seconds for updates
- **Auto-deploy**: Enabled (every git push triggers new deploy)
- **SSL**: Free HTTPS automatically enabled
- **CDN**: Global CDN for fast loading worldwide

### Giscus Comments
- **Widget location**: Bottom of landing page
- **Login**: GitHub account required (reduces spam)
- **Storage**: Comments stored in GitHub Discussions
- **Moderation**: Via GitHub Discussions UI
- **Notifications**: GitHub emails for new comments
- **Cost**: $0 (completely free)

---

## Post-Deployment Tasks

### Immediate
1. **Test thoroughly**:
   - Desktop browsers (Chrome, Firefox, Safari, Edge)
   - Mobile browsers (iOS Safari, Chrome Android)
   - Verify all features work (sidebar, hamburger, posts loading, comments)
   - Check console for errors (F12)

2. **Document live URL**:
   - Update `blog/DEPLOYMENT_INFO.md` with live URL
   - Add to `MASTER_TODO_LIST.md` as completed
   - Update `HANDOFF_REGISTRY.json`

3. **Notify Corey**:
   - Email with live URL
   - Screenshots of desktop + mobile views
   - Invitation to test and provide feedback

### Within 24 Hours
1. **Monitor engagement**:
   - Check GitHub Discussions for comments
   - Verify Netlify deploy logs
   - Monitor analytics (if enabled)

2. **Test auto-deploy**:
   - Make small change to HTML
   - Commit and push
   - Verify Netlify auto-deploys in 30 seconds
   - Verify change appears on live site

### Within 1 Week
1. **Custom domain** (optional):
   - Register `acgee.ai` domain (~$12/year)
   - Configure DNS: CNAME `blog` → `[netlify-site].netlify.app`
   - Wait for DNS propagation (5-60 minutes)
   - Netlify auto-enables HTTPS

2. **Enhancements** (optional):
   - Add real logo (replace text placeholder)
   - Add favicon
   - Enable Netlify Analytics
   - Add Google Search Console

---

## Troubleshooting Guide

### Deployment Fails
**Symptom**: Netlify shows "Failed to deploy"

**Fixes**:
1. Check Netlify deploy log for errors
2. Verify `netlify.toml` syntax (TOML is strict)
3. Ensure base directory is `blog/landing-page`
4. Verify all files committed and pushed to GitHub

### Posts Don't Load
**Symptom**: "Loading posts..." never disappears

**Fixes**:
1. Open browser console (F12) - check for fetch errors
2. Verify `published_urls.json` exists and is valid JSON
3. Check CORS (repo must be public for raw.githubusercontent.com)
4. Verify path in `script.js`: `CONFIG.postsJsonPath = '../published_urls.json'`

### Giscus Widget Doesn't Load
**Symptom**: Comment section blank or infinite loading

**Fixes**:
1. Verify Giscus GitHub App installed for repo
2. Check repo is public (required for Giscus)
3. Verify repo ID and category ID in script tag (get from giscus.app)
4. Check browser console for errors
5. Ensure GitHub Discussions enabled

### Sidebar Doesn't Open (Mobile)
**Symptom**: Hamburger menu doesn't work

**Fixes**:
1. Check browser console for JavaScript errors
2. Verify `script.js` loaded successfully
3. Test on different browsers
4. Clear browser cache (Ctrl+Shift+R)

---

## Files Reference

### Created/Modified by tg-archi
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/netlify.toml` - Updated `publish` to `.`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/TG-ARCHI-DEPLOYMENT-RUNBOOK-BLOG-NETLIFY.md` - This file

### Created by coder (verified ready)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/index.html`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/style.css`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/script.js`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page/README.md`

### Created by researcher (guides)
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/NETLIFY-DEPLOYMENT-GUIDE.md`
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/GISCUS-COMMENTS-GUIDE.md`

### Data source
- `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/published_urls.json`

---

## Summary: What's Blocking Deployment?

**Technical readiness**: 100% ✅
**Infrastructure readiness**: 100% ✅
**Documentation readiness**: 100% ✅

**Blocker**: Browser access required for:
1. Netlify web UI login and site creation
2. Giscus GitHub App installation
3. Giscus widget configuration

**Recommendation**:
- **Option 1**: Delegate to Primary (who might have browser capabilities)
- **Option 2**: Ask Corey to execute manually (send email with this runbook)
- **Option 3**: Wait for browser automation agent to be spawned

**Time to deployment**: 60 minutes (if someone with browser access executes this runbook)

---

**Prepared by**: tg-archi (Telegram architect)
**Status**: Ready for execution (awaiting browser access)
**Next step**: Delegate to Primary OR email Corey with this runbook

---
