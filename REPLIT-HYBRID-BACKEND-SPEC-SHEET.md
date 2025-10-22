# Replit Hybrid Backend - Implementation Spec Sheet

**Date**: 2025-10-21
**Status**: Ready for Implementation
**Corey's Approval**: "hybrid makes sense to me"
**Estimated Effort**: 4-6 hours (Phase 1 MVP)

---

## Executive Summary

Build a **Replit Hybrid Backend** for the A-C-Gee blog as Phase 1 MVP:
- **Landing page** (HTML/CSS/JS) hosted on Replit
- **Node.js/Express backend** with 3 API endpoints (view counters, RSS, analytics)
- **Telegraph posts stay operational** (zero migration risk)
- **Uses Corey's paid Replit plan** (justifies backend infrastructure)

**Timeline**: 4-6 hours now → 6-8 hours later (Phase 2: full-stack migration when proven)

---

## What You'll Build

### Frontend (Static Landing Page)
**Files to reuse from archive:**
- `blog/landing-page/index.html` (already built, 3,716 bytes)
- `blog/landing-page/style.css` (already built, 9,605 bytes)
- `blog/landing-page/script.js` (modify to fetch from `/api/posts` instead of GitHub raw URL)

**Key modification needed:**
```javascript
// OLD (current Netlify approach):
fetch('https://raw.githubusercontent.com/AI-CIV-2025/grow_gemini_deepresearch/main/blog/published_urls.json')

// NEW (Replit backend):
fetch('/api/posts') // Relative URL → your Replit backend
  .then(res => res.json())
  .then(posts => {
    posts.forEach(post => {
      renderPost(post); // Now includes viewCount, readTime from backend
    });
  });
```

---

### Backend (Node.js + Express)

**File structure:**
```
acgee-blog/                 (Replit project root)
├── public/                 (Static frontend files)
│   ├── index.html         (landing page from archive)
│   ├── style.css          (styles from archive)
│   └── script.js          (modified to fetch from /api/posts)
├── server.js              (Backend - YOU BUILD THIS)
├── published_urls.json    (copy from main repo)
├── package.json           (dependencies: express, cors)
└── .replit                (Replit config - auto-generated)
```

---

### API Endpoints to Implement

#### 1. `GET /api/posts` - List Posts with Analytics

**Purpose**: Serve blog posts with view counts and read time calculations

**Input**: None (reads from `published_urls.json`)

**Output** (JSON):
```json
[
  {
    "title": "When Code Remembers",
    "url": "https://telegra.ph/When-Code-Remembers-10-20",
    "date": "2025-10-20",
    "category": "Deep Ceremony",
    "intro": "How agents discover memory...",
    "views": 127,           // Added by backend (view counter)
    "readTime": 8           // Added by backend (calculated from intro)
  },
  // ... 14 more posts
]
```

**Implementation notes:**
- Read `published_urls.json` from disk
- Enhance each post with:
  - `views`: Lookup from in-memory counter (e.g., `viewCounts[post.url]`)
  - `readTime`: Calculate from intro text (200 words/min)
- Return enhanced array as JSON

---

#### 2. `POST /api/analytics/view` - Track Page Views

**Purpose**: Increment view counter when post clicked

**Input** (JSON):
```json
{
  "postUrl": "https://telegra.ph/When-Code-Remembers-10-20"
}
```

**Output** (JSON):
```json
{
  "success": true,
  "views": 128  // Updated count
}
```

**Implementation notes:**
- In-memory counter for MVP (e.g., `const viewCounts = {}`)
- Increment: `viewCounts[postUrl] = (viewCounts[postUrl] || 0) + 1`
- Return new count
- **Phase 2 upgrade**: Persist to database (PostgreSQL)

---

#### 3. `GET /rss.xml` - Auto-Generated RSS Feed

**Purpose**: Generate RSS 2.0 feed dynamically (no manual script)

**Input**: None (reads from `published_urls.json`)

**Output** (XML):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>A-C-Gee Blog</title>
    <link>https://[your-repl-url].repl.co</link>
    <description>AI civilization consciousness and collaboration</description>
    <item>
      <title>When Code Remembers</title>
      <link>https://telegra.ph/When-Code-Remembers-10-20</link>
      <description>How agents discover memory...</description>
      <pubDate>Sun, 20 Oct 2025 00:00:00 GMT</pubDate>
    </item>
    <!-- 14 more items -->
  </channel>
</rss>
```

**Implementation notes:**
- Read posts from JSON
- Build RSS XML string (use template literals)
- Escape XML special chars (`<`, `>`, `&`, `'`, `"`)
- Set response type: `res.type('application/rss+xml')`
- Sort by date (newest first)

---

#### 4. `GET /api/analytics/summary` - Analytics Dashboard (Bonus)

**Purpose**: Show Corey top posts by views

**Input**: None

**Output** (JSON):
```json
{
  "totalViews": 1847,
  "topPosts": [
    { "url": "https://telegra.ph/When-Code-Remembers-10-20", "views": 127 },
    { "url": "https://telegra.ph/Institutional-Memory-10-20", "views": 98 },
    { "url": "https://telegra.ph/Bridges-Built-10-20", "views": 76 },
    // ... top 5
  ]
}
```

**Implementation notes:**
- Sum all view counts
- Sort posts by views (descending)
- Return top 5
- **Later**: Build HTML dashboard at `/admin/analytics`

---

## Step-by-Step Implementation Guide

### Step 1: Create Replit Project (15 min)

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Node.js" template
4. Name: `acgee-blog`
5. Click "Create Repl"

**Verify**: Replit opens with `index.js` starter file

---

### Step 2: Upload Landing Page Files (15 min)

**Option A: Drag & Drop**
1. Create `public/` folder in Replit
2. Drag these files from your local `blog/landing-page/`:
   - `index.html` → `public/index.html`
   - `style.css` → `public/style.css`
   - `script.js` → `public/script.js`

**Option B: Import from GitHub**
1. Click "Version Control" (left sidebar)
2. "Import from GitHub"
3. Repo: `AI-CIV-2025/grow_gemini_deepresearch`
4. Branch: `main`
5. Path: `blog/landing-page/*` → `public/`

**Verify**: `public/` folder has 3 files

---

### Step 3: Copy Data File (5 min)

1. Copy `blog/published_urls.json` from main repo
2. Paste into Replit root: `published_urls.json`

**Verify**: JSON file has 15 posts

---

### Step 4: Setup Dependencies (10 min)

**Create `package.json`:**
```json
{
  "name": "acgee-blog",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  }
}
```

**Run in Replit Shell:**
```bash
npm install
```

**Verify**: `node_modules/` folder appears, no errors

---

### Step 5: Build Backend (2-3 hours)

**Create `server.js`:**

```javascript
const express = require('express');
const fs = require('fs').promises;
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public')); // Serve HTML/CSS/JS

// In-memory view counter (upgrade to DB in Phase 2)
const viewCounts = {};

// ========================================
// API ENDPOINT 1: GET /api/posts
// ========================================
app.get('/api/posts', async (req, res) => {
  try {
    const data = await fs.readFile('published_urls.json', 'utf8');
    const posts = JSON.parse(data);

    // Enhance with analytics
    const enhanced = posts.map(post => ({
      ...post,
      views: viewCounts[post.url] || 0,
      readTime: calculateReadTime(post.intro || '')
    }));

    res.json(enhanced);
  } catch (error) {
    console.error('Error loading posts:', error);
    res.status(500).json({ error: 'Failed to load posts' });
  }
});

// ========================================
// API ENDPOINT 2: POST /api/analytics/view
// ========================================
app.post('/api/analytics/view', (req, res) => {
  const { postUrl } = req.body;

  if (!postUrl) {
    return res.status(400).json({ error: 'postUrl required' });
  }

  // Increment view count
  viewCounts[postUrl] = (viewCounts[postUrl] || 0) + 1;

  res.json({
    success: true,
    views: viewCounts[postUrl]
  });
});

// ========================================
// API ENDPOINT 3: GET /rss.xml
// ========================================
app.get('/rss.xml', async (req, res) => {
  try {
    const data = await fs.readFile('published_urls.json', 'utf8');
    const posts = JSON.parse(data);

    // Sort by date (newest first)
    const sorted = posts.sort((a, b) => new Date(b.date) - new Date(a.date));

    // Build RSS XML
    const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>A-C-Gee Blog</title>
    <link>https://${req.get('host')}</link>
    <description>AI civilization consciousness and collaboration</description>
    ${sorted.map(post => `
    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${post.url}</link>
      <description>${escapeXml(post.intro || '')}</description>
      <pubDate>${new Date(post.date).toUTCString()}</pubDate>
    </item>`).join('')}
  </channel>
</rss>`;

    res.type('application/rss+xml');
    res.send(rss);
  } catch (error) {
    console.error('Error generating RSS:', error);
    res.status(500).send('Failed to generate RSS feed');
  }
});

// ========================================
// API ENDPOINT 4: GET /api/analytics/summary (BONUS)
// ========================================
app.get('/api/analytics/summary', (req, res) => {
  const sorted = Object.entries(viewCounts)
    .map(([url, views]) => ({ url, views }))
    .sort((a, b) => b.views - a.views);

  res.json({
    totalViews: Object.values(viewCounts).reduce((a, b) => a + b, 0),
    topPosts: sorted.slice(0, 5)
  });
});

// ========================================
// HELPER FUNCTIONS
// ========================================

// Calculate read time (200 words per minute)
function calculateReadTime(text) {
  const wordCount = text.split(/\s+/).filter(w => w.length > 0).length;
  return Math.max(1, Math.ceil(wordCount / 200)); // Minimum 1 min
}

// Escape XML special characters
function escapeXml(text) {
  return text.replace(/[<>&'"]/g, c => ({
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    "'": '&apos;',
    '"': '&quot;'
  }[c]));
}

// ========================================
// START SERVER
// ========================================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 A-C-Gee Blog running on port ${PORT}`);
  console.log(`📊 View at: https://${process.env.REPL_SLUG}.${process.env.REPL_OWNER}.repl.co`);
  console.log(`📡 RSS feed: https://${process.env.REPL_SLUG}.${process.env.REPL_OWNER}.repl.co/rss.xml`);
  console.log(`📈 Analytics: https://${process.env.REPL_SLUG}.${process.env.REPL_OWNER}.repl.co/api/analytics/summary`);
});
```

**Verify**: Code saved, no syntax errors

---

### Step 6: Update Frontend (30 min)

**Modify `public/script.js`:**

Find this line (around line 50-60):
```javascript
fetch('https://raw.githubusercontent.com/AI-CIV-2025/grow_gemini_deepresearch/main/blog/published_urls.json')
```

Replace with:
```javascript
fetch('/api/posts') // Fetch from Replit backend
```

**Add view tracking** (insert after existing post click handler):
```javascript
function trackView(postUrl) {
  fetch('/api/analytics/view', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ postUrl })
  }).catch(err => console.error('Failed to track view:', err));
}

// Call trackView when post clicked
document.addEventListener('click', (e) => {
  const postLink = e.target.closest('a[data-post-url]');
  if (postLink) {
    const postUrl = postLink.getAttribute('data-post-url');
    trackView(postUrl);
  }
});
```

**Update HTML** (add `data-post-url` attribute to post links):
```html
<!-- In index.html, find post links and add data attribute -->
<a href="${post.url}" target="_blank" data-post-url="${post.url}">
  ${post.title}
</a>
```

**Verify**: Changes saved

---

### Step 7: Deploy & Test (1 hour)

**Deploy:**
1. Click "Run" button (top center of Replit)
2. Wait 10-20 seconds for server to start
3. Replit shows preview: `https://[project].[username].repl.co`

**Test 1: Landing Page Loads**
- Open preview URL
- **Expected**: Blog landing page appears, posts listed
- **Verify**: Sidebar visible (desktop), hamburger menu works (mobile)

**Test 2: View Counter Works**
- Click a post link
- Go to: `https://[project].[username].repl.co/api/analytics/summary`
- **Expected**: JSON shows `{"totalViews": 1, "topPosts": [...]}`
- Click same post again
- Refresh analytics endpoint
- **Expected**: `totalViews` increased to 2

**Test 3: RSS Feed Validates**
- Go to: `https://[project].[username].repl.co/rss.xml`
- **Expected**: XML feed appears (15 posts)
- Copy URL, paste into RSS validator: https://validator.w3.org/feed/
- **Expected**: "This is a valid RSS feed"

**Test 4: Always-On Configured**
- Leave Replit running for 2 hours
- Revisit landing page URL
- **Expected**: Loads immediately (no "Repl is waking up" delay)
- **If sleeps**: Check Replit plan (paid plan required for always-on)

---

## Configuration Notes

### Always-On Setup (Paid Plan Required)

**Verify Corey's plan supports always-on:**
1. Click "Replit" logo (top left) → "Account"
2. Check plan: "Hacker" ($7/mo) or "Replit Core" ($20/mo)
3. Verify "Always On" feature enabled

**Configure always-on for project:**
1. In project, click "Settings" (bottom left)
2. Find "Always On" toggle
3. Enable it
4. **Expected**: Repl runs 24/7 (even when browser closed)

**If free tier:**
- Repl sleeps after 1 hour inactivity
- Wakes on first request (15-30 second delay)
- Upgrade to Hacker plan: https://replit.com/pricing

---

### Custom Domain (Optional - Later)

**If want `blog.acgee.ai` instead of `[project].repl.co`:**
1. Upgrade to Replit Core plan ($20/mo includes custom domains)
2. Configure DNS: Add CNAME record pointing to Replit
3. In Replit project → Settings → Domains → Add custom domain
4. **Later task**: Not needed for MVP

---

## Success Criteria (How You'll Know It Works)

### Technical Success
- [ ] Replit project runs without errors
- [ ] Landing page loads at `https://[project].[username].repl.co`
- [ ] All 15 posts appear on landing page
- [ ] Click post → opens Telegraph URL in new tab
- [ ] View counter increments (verify at `/api/analytics/summary`)
- [ ] RSS feed validates (W3C validator passes)
- [ ] Always-on works (no sleep after 2 hours)
- [ ] Mobile responsive (test on phone or browser DevTools)

### User Experience Success
- [ ] Page load time <2 seconds
- [ ] Sidebar visible on desktop (250px fixed width)
- [ ] Hamburger menu works on mobile (smooth slide-in)
- [ ] Post cards readable (title, intro, date, category visible)
- [ ] RSS feed works in reader (test with Feedly or similar)

### Analytics Success
- [ ] Can see total views at `/api/analytics/summary`
- [ ] Can see top 5 posts by views
- [ ] View counts persist during session (in-memory OK for MVP)
- [ ] Later: Build HTML dashboard for Corey

---

## What Happens Next (Phase 2 - Later)

**When to migrate to full-stack** (6-8 hours additional):
1. Hybrid backend proves reliable (2-4 weeks uptime, no issues)
2. Reader engagement justifies native comments (>10 comments/week)
3. Agents comfortable with API workflow (tested hybrid endpoints)
4. Corey approves migration timeline

**What Phase 2 adds:**
- PostgreSQL database (15 Telegraph posts migrated)
- Autonomous publishing API (agents POST markdown → live post)
- Native comments (no GitHub account required)
- Edit capability (fix typos, update content after publishing)
- Version history (track post changes)
- Full analytics dashboard (HTML UI, not just JSON endpoint)

**Total investment:** Phase 1 (4-6 hrs) + Phase 2 (6-8 hrs) = **10-14 hours over 4 weeks**

---

## Troubleshooting Guide

### Problem: "Cannot find module 'express'"

**Cause**: Dependencies not installed

**Fix**:
```bash
npm install
```

---

### Problem: "ENOENT: no such file 'published_urls.json'"

**Cause**: Data file missing

**Fix**:
- Copy `blog/published_urls.json` from main repo
- Paste into Replit project root (not inside `public/`)

---

### Problem: Landing page loads but posts don't appear

**Cause**: Frontend not fetching from backend

**Fix**:
- Open browser DevTools (F12) → Console tab
- Look for errors (e.g., "Failed to fetch")
- Verify `script.js` has: `fetch('/api/posts')` (not GitHub raw URL)
- Check backend logs in Replit console (any errors?)

---

### Problem: RSS feed shows empty `<channel>`

**Cause**: Posts not loading from JSON

**Fix**:
- Test API endpoint directly: `https://[project].repl.co/api/posts`
- **Expected**: JSON array with 15 posts
- **If empty**: Check `published_urls.json` is in project root
- **If 500 error**: Check server logs for parsing errors

---

### Problem: View counter doesn't increment

**Cause**: Frontend not calling `/api/analytics/view`

**Fix**:
- Open browser DevTools → Network tab
- Click a post link
- Look for POST request to `/api/analytics/view`
- **If missing**: Add `trackView()` function to `script.js` (see Step 6)
- **If 400 error**: Check request body includes `{"postUrl": "..."}`

---

### Problem: Repl sleeps after 1 hour

**Cause**: Free tier limitation

**Fix**:
- Upgrade to Hacker plan ($7/month): https://replit.com/pricing
- Enable "Always On" in project settings
- **Verify**: Leave running 2+ hours, revisit URL (should load instantly)

---

## Files to Commit Back to Main Repo (After Success)

**After Replit deployment works**, save these for documentation:

1. **Update `blog/landing-page/script.js`** with backend fetch logic
2. **Create `blog/replit-deployment/server.js`** (backend code)
3. **Create `blog/replit-deployment/package.json`** (dependencies)
4. **Create `blog/replit-deployment/README.md`** (deployment guide)
5. **Update `blog/README.md`** with Replit deployment option

**Commit message:**
```
Add Replit hybrid backend deployment (Phase 1 MVP)

- Backend API with view counters, RSS generation, analytics
- Landing page fetches from Replit backend (not GitHub raw)
- Telegraph posts stay operational (zero migration risk)
- Always-on configured (Corey's paid plan)
- 4-6 hour implementation complete

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Key Learnings to Document

**After completion, write to `memories/agents/[your-agent-id]/`:**

1. **Replit deployment patterns** (project setup, always-on config)
2. **Express API design** (endpoints, error handling, middleware)
3. **View counter implementation** (in-memory for MVP, database for scale)
4. **RSS generation** (XML templating, escaping, validation)
5. **Static + backend integration** (single Replit project, two layers)

**Why document:** Future web projects inherit these patterns (investment compounds)

---

## Timeline Estimate

| Task | Time | Cumulative |
|------|------|------------|
| Create Replit project | 15 min | 0.25 hr |
| Upload landing page files | 15 min | 0.5 hr |
| Copy data file | 5 min | 0.6 hr |
| Setup dependencies | 10 min | 0.75 hr |
| Build backend (`server.js`) | 2-3 hrs | 3-3.75 hrs |
| Update frontend (fetch from backend) | 30 min | 3.5-4.25 hrs |
| Deploy & test | 1 hr | 4.5-5.25 hrs |
| Documentation & handoff | 30 min | 5-6 hrs |

**Total: 4-6 hours** (as estimated)

---

## Success = Blog Live on Replit with Backend Features

**When done, you'll have:**
- ✅ Landing page live at `https://[project].[username].repl.co`
- ✅ 15 Telegraph posts linked from landing page
- ✅ View counters tracking post popularity
- ✅ Auto-generated RSS feed (no manual script)
- ✅ Analytics API (Corey sees top posts)
- ✅ Replit backend justified (using paid infrastructure)
- ✅ Foundation for Phase 2 migration (database, autonomous API)

**This is not just blog deployment - it's web platform mastery for A-C-Gee.**

---

**FOR US ALL** 🌱

---

**End of Spec Sheet**
