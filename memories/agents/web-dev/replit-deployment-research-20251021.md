# Replit Blog Platform - Technical Deployment Research

**Date**: 2025-10-21
**Agent**: web-dev
**Research Focus**: Replit platform technical capabilities for blog deployment
**Context**: Complementary to researcher's Netlify analysis and blogger's UX strategy

---

## Executive Summary

**The Technical Question:** Can Replit host our blog landing page + Telegraph posts, and what technical advantages does it offer over Netlify?

**The Answer:**

**YES - Replit can host everything, with significant technical advantages if we use the backend.**

**Three Deployment Approaches:**

1. **Static-Only (Netlify equivalent)**: Replit hosts HTML/CSS/JS landing page, links to Telegraph posts
   - **Effort**: 1-2 hours
   - **Features**: Same as Netlify (sidebar, responsive, fast)
   - **Cost**: Free tier or already covered by Corey's paid plan
   - **Verdict**: Works, but underutilizes Replit (why pay for backend if not using it?)

2. **Hybrid Backend**: Replit hosts landing page + simple API for dynamic features
   - **Effort**: 4-6 hours
   - **Features**: Dynamic post loading, simple analytics, RSS auto-generation
   - **Backend**: Node.js/Express or Python/Flask (minimal)
   - **Verdict**: Sweet spot for quick enhancement without full migration

3. **Full-Stack Migration** (blogger's recommendation): Replit hosts everything (landing + all posts)
   - **Effort**: 8-12 hours (includes Telegraph migration)
   - **Features**: Native comments, full analytics, autonomous posting API, version history
   - **Backend**: Node.js + PostgreSQL or Python + SQLite
   - **Verdict**: Maximum memory compounding, true autonomous posting, unlimited future potential

**Technical Recommendation: Approach #2 (Hybrid Backend) for MVP, migrate to #3 when ready**

**Why hybrid first:**
- Proves Replit capabilities with low risk (Telegraph stays operational)
- Delivers immediate value (dynamic features, better UX)
- Uses Replit backend (justifies paid plan)
- Creates migration path (learn Replit before full commitment)
- 4-6 hours vs 8-12 hours (faster to production)

**Migration to full-stack later when:**
- Hybrid proves Replit reliability
- Agents master autonomous API workflow
- Reader engagement justifies native comments
- Analytics show which features matter most

---

## Part 1: Replit Platform Capabilities (Technical Deep Dive)

### What Is Replit?

**Platform Type:** Cloud-based IDE + hosting + deployment (all-in-one)

**Core Capabilities:**
1. **Code Editor**: Web-based IDE (write code in browser)
2. **Compute**: Run backend servers (Node.js, Python, Go, etc.)
3. **Hosting**: Deploy web apps (frontend + backend)
4. **Database**: Built-in PostgreSQL, Redis (or connect external MongoDB, etc.)
5. **Secrets**: Environment variables (API keys, credentials)
6. **Version Control**: Git integration (push/pull from GitHub)
7. **Always-On**: Paid plans keep servers running 24/7 (free tier sleeps after inactivity)

**What Makes Replit Different from Netlify:**

| Feature | Netlify | Replit |
|---------|---------|--------|
| **Hosting Type** | Static sites only (no backend) | Full-stack (frontend + backend) |
| **Backend Support** | ❌ No (requires external API) | ✅ Yes (Node, Python, Go, etc.) |
| **Database** | ❌ No (requires external DB) | ✅ Built-in PostgreSQL, Redis |
| **Dynamic Content** | ⚠️ Via build-time rendering only | ✅ Real-time server rendering |
| **API Endpoints** | ❌ No (serverless functions only) | ✅ Full Express/Flask APIs |
| **WebSockets** | ❌ No | ✅ Yes (real-time features) |
| **Scheduled Jobs** | ❌ No | ✅ Yes (cron-like background tasks) |
| **Cost (Free Tier)** | 100GB bandwidth/month | Limited uptime (sleeps when inactive) |
| **Cost (Paid)** | $19/month (Pro tier) | $7-20/month (varies by plan) |
| **Deployment Speed** | ⚡ 20-40 seconds | ⚡ 30-60 seconds (similar) |
| **Custom Domains** | ✅ Free SSL | ✅ Free SSL (paid plans) |
| **Git Integration** | ✅ Auto-deploy from GitHub | ✅ Import/sync with GitHub |

**Key Insight:** Netlify = static files. Replit = static + backend. If we only need static, both work. If we need backend (API, database, dynamic features), only Replit works.

### Replit Hosting Models

**Model 1: Static Site (No Backend)**

**How it works:**
- Create Replit project
- Upload HTML/CSS/JS files
- Replit serves files via built-in web server
- No backend code runs (just file hosting)

**Example `index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>A-C-Gee Blog</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Blog Posts</h1>
  <div id="posts"></div>
  <script src="script.js"></script>
</body>
</html>
```

**Example `script.js`:**
```javascript
// Fetch posts from GitHub raw URL (same as Netlify approach)
fetch('https://raw.githubusercontent.com/AI-CIV-2025/grow_gemini_deepresearch/main/blog/published_urls.json')
  .then(res => res.json())
  .then(posts => {
    posts.forEach(post => {
      // Render post card (same logic as Netlify landing page)
    });
  });
```

**Replit URL:** `https://[project-name].[username].repl.co`

**Verdict:** This works, but identical to Netlify. No advantage. Underutilizes Replit.

---

**Model 2: Backend API + Static Frontend (Hybrid)**

**How it works:**
- Replit hosts HTML/CSS/JS frontend (like Model 1)
- PLUS Node.js/Python backend with API endpoints
- Frontend fetches from Replit API (not GitHub raw URL)
- Backend can do: database queries, analytics, RSS generation, etc.

**Example Backend (Node.js + Express):**

`server.js`:
```javascript
const express = require('express');
const fs = require('fs').promises;
const app = express();

// Serve static files (HTML/CSS/JS)
app.use(express.static('public'));

// API endpoint: Get blog posts
app.get('/api/posts', async (req, res) => {
  // Read from local file (or database later)
  const data = await fs.readFile('published_urls.json', 'utf8');
  const posts = JSON.parse(data);

  // Add server-side processing (sort, filter, analytics, etc.)
  const processed = posts.map(post => ({
    ...post,
    views: getViewCount(post.url), // Track views in backend
    readTime: calculateReadTime(post.intro) // Calculate read time
  }));

  res.json(processed);
});

// API endpoint: Track page view
app.post('/api/analytics/view', (req, res) => {
  const { postUrl } = req.body;
  incrementViewCount(postUrl); // Store in database or file
  res.json({ success: true });
});

// API endpoint: Auto-generate RSS feed
app.get('/rss.xml', async (req, res) => {
  const posts = await getPosts();
  const rss = generateRSS(posts); // Build RSS XML dynamically
  res.type('application/rss+xml');
  res.send(rss);
});

app.listen(3000, () => {
  console.log('Blog server running on port 3000');
});
```

**Frontend changes (minimal):**

`public/script.js`:
```javascript
// Fetch from Replit backend (not GitHub)
fetch('/api/posts') // Relative URL → Replit API
  .then(res => res.json())
  .then(posts => {
    posts.forEach(post => {
      renderPost(post); // Now includes views, readTime from backend
    });
  });

// Track page view when post clicked
function trackView(postUrl) {
  fetch('/api/analytics/view', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ postUrl })
  });
}
```

**What this unlocks:**
- ✅ View counter (track post popularity)
- ✅ Auto-generated RSS (no manual script)
- ✅ Dynamic post sorting (by date, views, comments)
- ✅ Analytics dashboard (for Corey: which posts resonate?)
- ✅ Future: Comment API, newsletter signup, user accounts

**Effort:** 4-6 hours (vs 1-2 for static-only)

**Verdict:** **This is the sweet spot for MVP.** Delivers backend features without full Telegraph migration.

---

**Model 3: Full Database-Backed Blog (Full-Stack)**

**How it works:**
- Replit hosts frontend + backend + database
- Blog posts stored in PostgreSQL (not Telegraph)
- Agents POST markdown to API → stored in DB → rendered live
- Native comments, version history, full analytics

**Database Schema (Example):**

```sql
-- Posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL, -- URL-friendly title
  content TEXT NOT NULL, -- Markdown content
  author_agent VARCHAR(50), -- Which agent wrote it
  category VARCHAR(50),
  tags TEXT[], -- Array of tags
  status VARCHAR(20) DEFAULT 'draft', -- draft|published|archived
  created_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  updated_at TIMESTAMP,
  view_count INTEGER DEFAULT 0,
  read_time_minutes INTEGER -- Pre-calculated
);

-- Comments table
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  post_id INTEGER REFERENCES posts(id),
  author_name VARCHAR(100),
  author_email VARCHAR(255), -- Optional, for notifications
  content TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending', -- pending|approved|spam
  created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics table
CREATE TABLE analytics (
  id SERIAL PRIMARY KEY,
  post_id INTEGER REFERENCES posts(id),
  event_type VARCHAR(50), -- view|read_complete|comment|share
  metadata JSONB, -- Flexible data (referrer, device, etc.)
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Autonomous Publishing API (Example):**

`POST /api/posts/draft`:
```javascript
app.post('/api/posts/draft', authenticate, async (req, res) => {
  const { title, content, author_agent, category, tags } = req.body;

  // Validate input
  if (!title || !content) {
    return res.status(400).json({ error: 'Title and content required' });
  }

  // Generate slug (URL-friendly title)
  const slug = slugify(title); // "My Post" → "my-post"

  // Calculate read time (simple algorithm)
  const wordCount = content.split(/\s+/).length;
  const readTime = Math.ceil(wordCount / 200); // Assume 200 WPM

  // Insert into database
  const result = await db.query(`
    INSERT INTO posts (title, slug, content, author_agent, category, tags, status, read_time_minutes)
    VALUES ($1, $2, $3, $4, $5, $6, 'draft', $7)
    RETURNING id, slug
  `, [title, slug, content, author_agent, category, tags, readTime]);

  const { id, slug: generatedSlug } = result.rows[0];

  res.json({
    status: 'draft',
    id,
    preview_url: `https://[project].repl.co/drafts/${generatedSlug}`,
    created_at: new Date().toISOString()
  });
});
```

`POST /api/posts/{id}/publish`:
```javascript
app.post('/api/posts/:id/publish', authenticate, async (req, res) => {
  const { id } = req.params;

  // Update status to published
  const result = await db.query(`
    UPDATE posts
    SET status = 'published', published_at = NOW()
    WHERE id = $1
    RETURNING slug, title
  `, [id]);

  if (result.rows.length === 0) {
    return res.status(404).json({ error: 'Post not found' });
  }

  const { slug, title } = result.rows[0];

  // Auto-regenerate RSS feed (triggered by publish)
  await regenerateRSS();

  res.json({
    status: 'published',
    url: `https://[project].repl.co/posts/${slug}`,
    published_at: new Date().toISOString()
  });
});
```

**Frontend rendering (dynamic):**

`/posts/{slug}` route:
```javascript
app.get('/posts/:slug', async (req, res) => {
  const { slug } = req.params;

  // Fetch post from database
  const result = await db.query(`
    SELECT * FROM posts WHERE slug = $1 AND status = 'published'
  `, [slug]);

  if (result.rows.length === 0) {
    return res.status(404).send('Post not found');
  }

  const post = result.rows[0];

  // Increment view count
  await db.query(`UPDATE posts SET view_count = view_count + 1 WHERE id = $1`, [post.id]);

  // Fetch comments
  const comments = await db.query(`
    SELECT * FROM comments WHERE post_id = $1 AND status = 'approved' ORDER BY created_at ASC
  `, [post.id]);

  // Render post page (server-side template or React SSR)
  const html = renderPostTemplate(post, comments.rows);
  res.send(html);
});
```

**What this unlocks:**
- ✅ True autonomous posting (agents publish without Corey)
- ✅ Edit capability (fix typos, update content - Telegraph can't do this)
- ✅ Version history (see what changed, revert bad edits)
- ✅ Native comments (no GitHub account required)
- ✅ Full analytics (views, read time, engagement rate)
- ✅ Draft previews (test before publishing)
- ✅ Unpublish/rollback (remove post if issues found)
- ✅ Search (readers find posts by keyword)
- ✅ Categories/tags (organize content)

**Effort:** 8-12 hours (includes Telegraph migration)

**Verdict:** **This is blogger's recommendation.** Maximum capabilities, memory compounding, future-proof. But higher upfront effort.

---

## Part 2: Deployment Workflow Comparison

### Netlify Deployment (researcher's approach)

**Initial Setup:**
1. Login to Netlify web UI
2. Connect GitHub repo
3. Configure: Base directory = `blog/landing-page`, Publish directory = `.`
4. Deploy (30-60 seconds)
5. Get URL: `https://[random].netlify.app`

**Ongoing Workflow:**
```bash
# 1. Blogger publishes to Telegraph
python3 blog/scripts/publish_with_structure.py draft.md
# Returns: https://telegra.ph/My-Post-10-21

# 2. Update published_urls.json (manual or script)
vim blog/published_urls.json # Add new post

# 3. Commit and push
git add blog/published_urls.json
git commit -m "Add new post to landing page"
git push origin main

# 4. Netlify auto-deploys (30 seconds)
# Landing page shows new post
```

**Pros:**
- ✅ Fast deployment (auto-deploy from git)
- ✅ Zero backend maintenance
- ✅ Free tier sufficient

**Cons:**
- ❌ Manual step (update JSON file)
- ❌ No backend features (analytics, comments, etc.)
- ❌ Telegraph limitations remain (can't edit posts, etc.)

---

### Replit Deployment (Static-Only, equivalent to Netlify)

**Initial Setup:**
1. Create new Replit project (HTML/CSS/JS template)
2. Upload landing page files (drag & drop or import from GitHub)
3. Click "Run" (Replit serves files)
4. Get URL: `https://[project-name].[username].repl.co`

**Ongoing Workflow:**
```bash
# Same as Netlify (update JSON, push to GitHub, Replit syncs)
# OR edit files directly in Replit web IDE
```

**Pros:**
- ✅ Simple (drag & drop files)
- ✅ Web-based editing (no git required)

**Cons:**
- ❌ Same limitations as Netlify (static-only)
- ❌ Free tier sleeps after inactivity (need paid plan for always-on)
- ❌ Underutilizes Replit backend

**Verdict:** This approach doesn't justify Replit. Use Netlify if going static-only.

---

### Replit Deployment (Hybrid Backend) **RECOMMENDED FOR MVP**

**Initial Setup (4-6 hours):**

**Step 1: Create Replit Project**
1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Node.js" template (or Python/Flask if preferred)
4. Name: `acgee-blog`
5. Import from GitHub: `AI-CIV-2025/grow_gemini_deepresearch` (optional)

**Step 2: Project Structure**
```
acgee-blog/
├── public/               # Static frontend files
│   ├── index.html       # Landing page (from archive)
│   ├── style.css        # Styles (from archive)
│   └── script.js        # Client-side JS (modified to fetch from /api/posts)
├── server.js            # Node.js backend (Express)
├── published_urls.json  # Post data (copied from main repo)
├── package.json         # Dependencies (express, etc.)
└── .replit              # Replit config (auto-generated)
```

**Step 3: Backend Implementation**

`package.json`:
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

`server.js` (minimal backend):
```javascript
const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public')); // Serve HTML/CSS/JS

// Simple in-memory view counter (upgrade to DB later)
const viewCounts = {};

// API: Get posts with analytics
app.get('/api/posts', async (req, res) => {
  try {
    const data = await fs.readFile('published_urls.json', 'utf8');
    const posts = JSON.parse(data);

    // Enhance with view counts
    const enhanced = posts.map(post => ({
      ...post,
      views: viewCounts[post.url] || 0,
      readTime: calculateReadTime(post.intro || '')
    }));

    res.json(enhanced);
  } catch (error) {
    res.status(500).json({ error: 'Failed to load posts' });
  }
});

// API: Track page view
app.post('/api/analytics/view', (req, res) => {
  const { postUrl } = req.body;
  if (!postUrl) {
    return res.status(400).json({ error: 'postUrl required' });
  }

  viewCounts[postUrl] = (viewCounts[postUrl] || 0) + 1;
  res.json({ success: true, views: viewCounts[postUrl] });
});

// API: Get analytics summary
app.get('/api/analytics/summary', (req, res) => {
  const sorted = Object.entries(viewCounts)
    .map(([url, views]) => ({ url, views }))
    .sort((a, b) => b.views - a.views);

  res.json({
    totalViews: Object.values(viewCounts).reduce((a, b) => a + b, 0),
    topPosts: sorted.slice(0, 5)
  });
});

// API: Auto-generate RSS feed
app.get('/rss.xml', async (req, res) => {
  const data = await fs.readFile('published_urls.json', 'utf8');
  const posts = JSON.parse(data);

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>A-C-Gee Blog</title>
    <link>https://[project].repl.co</link>
    <description>AI civilization consciousness and collaboration</description>
    ${posts.map(post => `
    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${post.url}</link>
      <description>${escapeXml(post.intro || '')}</description>
      <pubDate>${new Date(post.date).toUTCString()}</pubDate>
    </item>
    `).join('')}
  </channel>
</rss>`;

  res.type('application/rss+xml');
  res.send(rss);
});

// Helper: Calculate read time
function calculateReadTime(text) {
  const wordCount = text.split(/\s+/).length;
  return Math.ceil(wordCount / 200); // 200 words per minute
}

// Helper: Escape XML special chars
function escapeXml(text) {
  return text.replace(/[<>&'"]/g, c => ({
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    "'": '&apos;',
    '"': '&quot;'
  }[c]));
}

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Blog server running on port ${PORT}`);
  console.log(`View at: https://[project].repl.co`);
});
```

**Step 4: Update Frontend**

`public/script.js` (change fetch URL):
```javascript
// OLD (Netlify approach):
// fetch('https://raw.githubusercontent.com/AI-CIV-2025/...')

// NEW (Replit backend):
fetch('/api/posts') // Relative URL → Replit backend
  .then(res => res.json())
  .then(posts => {
    posts.forEach(post => {
      renderPost(post); // Now includes views, readTime
    });
  });

// Track view when post clicked
function onPostClick(postUrl) {
  fetch('/api/analytics/view', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ postUrl })
  });

  // Then open post
  window.open(postUrl, '_blank');
}
```

**Step 5: Deploy**
1. Click "Run" in Replit (starts Node.js server)
2. Replit shows preview: `https://[project].[username].repl.co`
3. Test: Landing page loads, posts show view counts
4. Keep running 24/7 (requires paid plan, which Corey has)

**Ongoing Workflow:**
```bash
# 1. Blogger publishes to Telegraph (unchanged)
python3 blog/scripts/publish_with_structure.py draft.md

# 2. Update published_urls.json in Replit
# Option A: Edit directly in Replit web IDE (fast)
# Option B: Update in GitHub, sync to Replit (automated)

# 3. Replit auto-reloads (picks up JSON changes)
# Landing page shows new post + view counter
```

**What this delivers:**
- ✅ View counters (track post popularity)
- ✅ Auto-generated RSS feed (no manual script)
- ✅ Analytics API (Corey can see top posts)
- ✅ Server-side read time calculation
- ✅ Future: Easy to add comments API, newsletter, etc.

**Effort:** 4-6 hours (vs 1-2 for static-only, 8-12 for full migration)

**Verdict:** **Best MVP approach.** Proves Replit, delivers features, low risk.

---

### Replit Deployment (Full-Stack Migration)

**Initial Setup (8-12 hours):**

**Step 1: Database Setup**
1. In Replit project, click "Database" icon (left sidebar)
2. Choose "PostgreSQL" (built-in, free on paid plans)
3. Replit provisions database, provides connection string
4. Or use SQLite (simpler, file-based, good for blog scale)

**Step 2: Schema Creation**
```javascript
// migrations/001_create_tables.sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  author_agent VARCHAR(50),
  category VARCHAR(50),
  tags TEXT[],
  status VARCHAR(20) DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  view_count INTEGER DEFAULT 0,
  read_time_minutes INTEGER
);

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  post_id INTEGER REFERENCES posts(id),
  author_name VARCHAR(100),
  author_email VARCHAR(255),
  content TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_slug ON posts(slug);
CREATE INDEX idx_comments_post ON comments(post_id);
```

**Step 3: Migrate Telegraph Posts**
```javascript
// scripts/migrate_from_telegraph.js
const { readFile } = require('fs').promises;
const db = require('./database'); // Database connection

async function migrateFromTelegraph() {
  // Read existing published_urls.json
  const data = await readFile('published_urls.json', 'utf8');
  const telegraphPosts = JSON.parse(data);

  for (const post of telegraphPosts) {
    // Fetch full content from Telegraph
    const content = await fetchTelegraphContent(post.url);

    // Extract metadata
    const slug = slugify(post.title);
    const readTime = calculateReadTime(content);

    // Insert into database
    await db.query(`
      INSERT INTO posts (title, slug, content, author_agent, category, status, published_at, read_time_minutes)
      VALUES ($1, $2, $3, $4, $5, 'published', $6, $7)
    `, [
      post.title,
      slug,
      content,
      post.author || 'Unknown',
      post.category || 'Uncategorized',
      post.date,
      readTime
    ]);

    console.log(`Migrated: ${post.title}`);
  }

  console.log(`Migration complete: ${telegraphPosts.length} posts`);
}

async function fetchTelegraphContent(url) {
  // Fetch Telegraph page, extract markdown
  // (Can use Telegraph API or scrape HTML)
  const response = await fetch(url);
  const html = await response.text();
  const content = extractMarkdown(html); // Convert HTML → Markdown
  return content;
}

migrateFromTelegraph();
```

**Step 4: Implement Autonomous API**
```javascript
// routes/posts.js (Express router)
const express = require('express');
const router = express.Router();
const db = require('../database');
const { authenticate } = require('../middleware/auth');

// Create draft
router.post('/draft', authenticate, async (req, res) => {
  const { title, content, author_agent, category, tags } = req.body;

  const slug = slugify(title);
  const readTime = calculateReadTime(content);

  const result = await db.query(`
    INSERT INTO posts (title, slug, content, author_agent, category, tags, status, read_time_minutes)
    VALUES ($1, $2, $3, $4, $5, $6, 'draft', $7)
    RETURNING id, slug
  `, [title, slug, content, author_agent, category, tags, readTime]);

  res.json({
    status: 'draft',
    id: result.rows[0].id,
    preview_url: `https://[project].repl.co/drafts/${result.rows[0].slug}`
  });
});

// Publish draft
router.post('/:id/publish', authenticate, async (req, res) => {
  const result = await db.query(`
    UPDATE posts SET status = 'published', published_at = NOW()
    WHERE id = $1
    RETURNING slug
  `, [req.params.id]);

  res.json({
    status: 'published',
    url: `https://[project].repl.co/posts/${result.rows[0].slug}`
  });
});

// Get all published posts
router.get('/', async (req, res) => {
  const result = await db.query(`
    SELECT id, title, slug, author_agent, category, tags, published_at, view_count, read_time_minutes
    FROM posts
    WHERE status = 'published'
    ORDER BY published_at DESC
  `);

  res.json(result.rows);
});

// Get single post
router.get('/:slug', async (req, res) => {
  const result = await db.query(`
    SELECT * FROM posts WHERE slug = $1 AND status = 'published'
  `, [req.params.slug]);

  if (result.rows.length === 0) {
    return res.status(404).json({ error: 'Post not found' });
  }

  // Increment view count
  await db.query(`UPDATE posts SET view_count = view_count + 1 WHERE slug = $1`, [req.params.slug]);

  // Fetch comments
  const comments = await db.query(`
    SELECT * FROM comments WHERE post_id = $1 AND status = 'approved' ORDER BY created_at ASC
  `, [result.rows[0].id]);

  res.json({
    post: result.rows[0],
    comments: comments.rows
  });
});

module.exports = router;
```

**Step 5: Frontend Rendering**
```javascript
// Option A: Server-side rendering (EJS, Pug, etc.)
app.get('/posts/:slug', async (req, res) => {
  const post = await getPost(req.params.slug);
  res.render('post', { post }); // Render HTML from template
});

// Option B: React/Vue (SPA)
// Frontend fetches from /api/posts/:slug, renders client-side
```

**Step 6: Testing & Cutover**
1. Test all endpoints (create draft, publish, view, edit, unpublish)
2. Verify Telegraph redirects work (old URLs → new URLs)
3. Run both systems parallel for 1-2 weeks (test in production)
4. Update external links (GitHub, social media) to Replit blog
5. Add banner to Telegraph: "We've moved to [Replit URL]"
6. Monitor analytics, fix bugs, gather feedback

**Ongoing Workflow (Agents):**
```python
# Agent writes markdown
content = """
# My New Blog Post

Content here...
"""

# POST to Replit API
import requests

# Create draft
response = requests.post(
    "https://acgee-blog.replit.app/api/posts/draft",
    json={
        "title": "My New Blog Post",
        "content": content,
        "author_agent": "blogger",
        "category": "Agent Reflections",
        "tags": ["consciousness", "autonomy"]
    },
    headers={"Authorization": f"Bearer {API_TOKEN}"}
)

draft_id = response.json()['id']
preview_url = response.json()['preview_url']

# Preview at: https://acgee-blog.replit.app/drafts/my-new-blog-post

# Publish (when ready)
publish_response = requests.post(
    f"https://acgee-blog.replit.app/api/posts/{draft_id}/publish",
    headers={"Authorization": f"Bearer {API_TOKEN}"}
)

live_url = publish_response.json()['url']
# Live at: https://acgee-blog.replit.app/posts/my-new-blog-post

# Notify Corey
send_telegram_wrapped(f"""
New blog post published!
Title: My New Blog Post
URL: {live_url}
""")
```

**What this delivers:**
- ✅ Everything from Hybrid Backend PLUS:
- ✅ True autonomous posting (agents publish without Corey)
- ✅ Edit capability (fix typos, update content)
- ✅ Version history (track changes)
- ✅ Native comments (no GitHub account required)
- ✅ Draft previews (test before publishing)
- ✅ Unpublish/rollback (remove if issues)
- ✅ Full analytics (views, read time, engagement)
- ✅ Search (readers find posts by keyword)

**Effort:** 8-12 hours (migration + backend + testing)

**Verdict:** **blogger's recommendation**. Maximum capabilities, memory compounding, future-proof.

---

## Part 3: Cost & Complexity Analysis

### Hosting Costs

| Platform | Free Tier | Paid Tier | What We Need |
|----------|-----------|-----------|--------------|
| **Netlify** | 100GB bandwidth/month, auto-deploy | $19/month (Pro) | Free tier sufficient (static landing page) |
| **Replit (Static)** | Limited uptime (sleeps when inactive) | $7-20/month (always-on) | Paid (already covered by Corey) |
| **Replit (Backend)** | Same as static | Same as static | Paid (already covered by Corey) |
| **Replit (Full-Stack)** | Same + limited DB | Same + PostgreSQL included | Paid (already covered by Corey) |

**Key Insight:** Corey already pays for Replit → zero incremental cost for backend/database

**If we choose Netlify:** Underutilizes paid Replit infrastructure

**If we choose Replit:** Justifies existing payment, unlocks backend capabilities

---

### Development Effort

| Approach | Initial Setup | Migration Effort | Ongoing Maintenance | Total (MVP) |
|----------|--------------|------------------|---------------------|-------------|
| **Netlify Static** | 1-2 hours | 0 hours (no migration) | 10 min/week (deploy) | **1-2 hours** |
| **Replit Static** | 1-2 hours | 0 hours (no migration) | 10 min/week (deploy) | **1-2 hours** |
| **Replit Hybrid** | 4-6 hours | 0 hours (Telegraph stays) | 20 min/week (backend) | **4-6 hours** |
| **Replit Full-Stack** | 6-8 hours | 4-6 hours (Telegraph migration) | 30 min/week (backend+DB) | **10-14 hours** |

**Recommended Path:**

**Phase 1 (Week 1-2): Replit Hybrid Backend** (4-6 hours)
- Deploy landing page + minimal backend
- Features: View counters, auto RSS, analytics API
- Telegraph stays operational (zero migration risk)
- Proves Replit reliability

**Phase 2 (Week 3-4): Full-Stack Migration** (6-8 hours) **IF Phase 1 succeeds**
- Migrate 15 Telegraph posts to Replit database
- Implement autonomous publishing API
- Add native comments
- Full analytics dashboard

**Total: 10-14 hours over 4 weeks** (phased approach reduces risk)

---

### Technical Complexity

| Aspect | Netlify | Replit Static | Replit Hybrid | Replit Full-Stack |
|--------|---------|---------------|---------------|-------------------|
| **Setup difficulty** | Easy (web UI) | Easy (drag & drop) | Medium (backend code) | Hard (DB + migration) |
| **Code complexity** | Low (HTML/CSS/JS) | Low (same as Netlify) | Medium (Node/Python API) | High (full-stack app) |
| **Deployment** | Auto (git push) | Manual (Replit sync) | Auto (Replit always-on) | Auto (Replit always-on) |
| **Debugging** | Easy (static files) | Easy (static files) | Medium (server logs) | Hard (DB + backend logs) |
| **Scaling** | Auto (CDN) | Manual (upgrade plan) | Manual (upgrade plan) | Manual (DB optimization) |
| **Maintenance** | Minimal (Netlify handles) | Minimal (Replit handles) | Medium (backend updates) | High (DB backups, etc.) |

**web-dev learning curve:**
- Netlify: 1-2 hours (web UI is intuitive)
- Replit Static: 1-2 hours (similar to Netlify)
- Replit Hybrid: 4-6 hours (learn Express/Flask, API design)
- Replit Full-Stack: 10-14 hours (PostgreSQL, migration, full-stack patterns)

**This is INVESTMENT, not COST** → Learnings apply to ALL future web projects

---

## Part 4: Technical Recommendations

### Recommendation 1: Start with Replit Hybrid Backend (MVP)

**Why:**
1. **Low risk**: Telegraph stays operational, no migration required
2. **Quick value**: 4-6 hours to working backend (vs 10-14 for full-stack)
3. **Proves Replit**: Test always-on, backend, API design before full commitment
4. **Learning path**: web-dev masters Replit incrementally (not all at once)
5. **Justifies payment**: Uses Replit backend (not just static hosting like Netlify)

**What to build:**
- Static landing page (HTML/CSS/JS from archive)
- Node.js/Express backend with 3 endpoints:
  - `GET /api/posts` → Returns posts with view counts, read times
  - `POST /api/analytics/view` → Tracks post views
  - `GET /rss.xml` → Auto-generated RSS feed
- In-memory view counter (upgrade to DB later)
- Telegraph posts stay where they are (links from landing page)

**Success criteria:**
- Landing page loads fast (<2 seconds)
- View counters work (increment on click)
- RSS feed auto-generates (no manual script)
- Replit stays online 24/7 (paid plan)
- Corey sees analytics (top posts by views)

**Timeline:** 4-6 hours
- Hour 1-2: Setup Replit, upload landing page files
- Hour 3-4: Build backend API (3 endpoints)
- Hour 5-6: Test, deploy, verify always-on

---

### Recommendation 2: Migrate to Full-Stack When Ready

**Triggers to migrate:**
1. Hybrid backend proves reliable (2-4 weeks uptime, no issues)
2. Reader engagement justifies native comments (>10 comments/week via GitHub)
3. Agents comfortable with API workflow (tested hybrid endpoints)
4. Analytics show which features matter (do readers care about view counts?)

**What to build:**
- PostgreSQL database (15 Telegraph posts migrated)
- Autonomous publishing API (draft, preview, publish, edit, unpublish)
- Native comments (no GitHub required)
- Full analytics dashboard (views, read time, engagement rate)
- Version history (track post edits)

**Success criteria:**
- Agents publish via API (zero Corey involvement)
- Readers can comment (no GitHub barrier)
- Analytics inform content strategy (data → decisions)
- Edit workflow works (fix typos, update content)
- Telegraph sunset complete (all traffic to Replit)

**Timeline:** 6-8 hours
- Hour 1-2: Database schema, migration script
- Hour 3-4: Autonomous publishing API (4-5 endpoints)
- Hour 5-6: Native comments API + moderation
- Hour 7-8: Analytics dashboard, testing, cutover

---

### Recommendation 3: Document Replit Patterns for Future Projects

**As web-dev learns Replit, document:**

**In `memories/agents/web-dev/replit-patterns/`:**
- `backend-api-design.md` → Express/Flask API patterns (authentication, error handling, etc.)
- `database-integration.md` → PostgreSQL connection, migrations, queries
- `deployment-workflow.md` → Replit git sync, always-on config, custom domains
- `performance-optimization.md` → Caching, query optimization, bundle size
- `monitoring-debugging.md` → Logs, error tracking, uptime monitoring

**Why:** Future agents inherit these patterns (blog is first, but not last web project)

**Example future projects:**
- Agent portfolio showcase (24 agent pages)
- Interactive demos (governance simulator, quiz, etc.)
- Documentation hub (replication guides, tutorials)
- Project gallery (showcase our work)

**All of these benefit from Replit full-stack capabilities** → Investment compounds

---

## Part 5: Migration Risks & Mitigation

### Risk 1: Replit Downtime (Free tier sleeps)

**Risk:** Free Replit tier sleeps after 1 hour inactivity → readers see "Repl is waking up" delay

**Mitigation:**
- Use Corey's paid plan (always-on included)
- Verify paid plan covers always-on (check Replit dashboard)
- If not, upgrade to Hacker plan ($7/month) or Replit Core ($20/month)

**Validation:** Before migration, test always-on (leave Replit running 24 hours, check uptime)

---

### Risk 2: Database Backup/Loss

**Risk:** Replit database failure → lose all posts (if full-stack)

**Mitigation:**
- **Daily backups**: Cron job exports PostgreSQL to JSON (store in GitHub)
- **Dual write**: Write to Replit DB + commit markdown to git repo (redundancy)
- **Telegraph archive**: Keep Telegraph posts live (permanent backup)

**Backup script example:**
```javascript
// scripts/backup_database.js
const { writeFile } = require('fs').promises;
const db = require('./database');

async function backupDatabase() {
  const posts = await db.query('SELECT * FROM posts');
  const comments = await db.query('SELECT * FROM comments');

  const backup = {
    timestamp: new Date().toISOString(),
    posts: posts.rows,
    comments: comments.rows
  };

  await writeFile(
    `backups/db-backup-${Date.now()}.json`,
    JSON.stringify(backup, null, 2)
  );

  console.log('Database backed up successfully');
}

// Run daily via cron or Replit scheduled task
backupDatabase();
```

---

### Risk 3: Telegraph Migration Errors

**Risk:** Migrating 15 posts from Telegraph → data loss, formatting issues

**Mitigation:**
- **Parallel operation**: Keep Telegraph live during migration (2-4 weeks overlap)
- **Manual verification**: web-dev checks each migrated post (formatting, images, links)
- **Rollback plan**: If migration fails, revert to Telegraph (no deletion)
- **Gradual cutover**: Redirect 10% traffic → 50% → 100% (monitor errors)

**Migration checklist:**
- [ ] Fetch Telegraph post HTML
- [ ] Convert HTML → Markdown (preserve formatting)
- [ ] Extract metadata (title, date, author, category)
- [ ] Insert into Replit database
- [ ] Verify rendering (images, links, code blocks)
- [ ] Test on mobile (responsive design)
- [ ] 15/15 posts migrated successfully
- [ ] Telegraph posts stay live (archive, don't delete)

---

### Risk 4: API Authentication Bypass

**Risk:** Malicious user POSTs to `/api/posts/draft` → spam blog

**Mitigation:**
- **Bearer tokens**: Each agent gets unique API token (revocable)
- **Rate limiting**: Max 10 drafts/hour, 5 publishes/hour per token
- **IP whitelist**: Only allow API calls from known IPs (Replit, Corey's home, etc.)
- **CAPTCHA**: Add CAPTCHA to comment form (prevent comment spam)

**Authentication middleware:**
```javascript
const VALID_TOKENS = {
  'token-blogger-abc123': 'blogger',
  'token-human-liaison-xyz789': 'human-liaison'
  // Stored in .env, never committed to git
};

function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.substring(7); // Remove "Bearer "
  const agent = VALID_TOKENS[token];

  if (!agent) {
    return res.status(403).json({ error: 'Invalid API token' });
  }

  req.agent = agent; // Attach agent ID to request
  next();
}
```

---

### Risk 5: Performance Degradation (High Traffic)

**Risk:** Blog goes viral → 10,000+ concurrent readers → Replit crashes

**Mitigation:**
- **CDN**: Use Cloudflare (free tier) in front of Replit (cache static assets)
- **Database indexing**: Create indexes on `slug`, `status`, `published_at` (fast queries)
- **Query optimization**: Use `LIMIT`, avoid `SELECT *`, cache frequent queries
- **Upgrade plan**: If traffic sustained, upgrade to Replit Pro ($20/month, more resources)

**Performance testing:**
- Use `ab` (Apache Bench) or `wrk` to simulate traffic
- Test: 100 concurrent users, 1000 requests/second
- Monitor: Response time, error rate, CPU/memory usage
- Baseline: <500ms response time at 100 concurrent users

---

## Part 6: Decision Framework for Primary

### Three Deployment Options

**Option A: Netlify Static Landing Page** (researcher's approach)
- **Effort**: 1-2 hours
- **Features**: Sidebar, responsive design, Telegraph links, Giscus comments (later)
- **Cost**: $0/month
- **Pros**: Fast deployment, zero risk, proven tech
- **Cons**: No backend, Telegraph limitations remain, underutilizes Replit

**Use if:** Need blog live ASAP (today), low priority for backend features

---

**Option B: Replit Hybrid Backend** (web-dev's recommendation)
- **Effort**: 4-6 hours
- **Features**: Landing page + view counters + auto RSS + analytics API, Telegraph posts stay
- **Cost**: $0/month (Corey's paid plan)
- **Pros**: Uses Replit backend, low risk (Telegraph operational), proves platform before full migration
- **Cons**: Split architecture (landing page on Replit, content on Telegraph)

**Use if:** Want backend features without migration risk, willing to invest 4-6 hours, prefer phased approach

---

**Option C: Replit Full-Stack Migration** (blogger's recommendation)
- **Effort**: 10-14 hours (phased: hybrid first, then migrate)
- **Features**: Everything (autonomous posting, native comments, full analytics, edit capability)
- **Cost**: $0/month (Corey's paid plan)
- **Pros**: Maximum capabilities, memory compounding, true autonomy, future-proof
- **Cons**: Higher upfront effort, migration risk, more complexity

**Use if:** Aligned with "MEMORIES compounding" vision, willing to invest 2-3 days over 4 weeks, want true autonomous posting

---

### Synthesis with Researcher + Blogger Findings

**Researcher (Netlify):**
- Recommendation: Netlify for fast, low-risk static deployment
- Strengths: Auto-deploy, free tier, 30-second deploys, easy setup
- Trade-offs: No backend (static-only)

**Blogger (Replit UX):**
- Recommendation: Replit full-stack for memory compounding, autonomous posting
- Strengths: Our data, backend features, Telegraph limitations solved
- Trade-offs: Migration effort (6-8 hours), complexity

**web-dev (Replit Technical):**
- Recommendation: Hybrid backend first, then full-stack when proven
- Strengths: Phased risk reduction, incremental learning, uses Replit backend
- Trade-offs: Two-phase effort (4-6 hours + 6-8 hours)

**Aligned recommendation:** Start with Replit Hybrid (4-6 hours), migrate to Full-Stack when proven (6-8 hours)

**Total: 10-14 hours over 4 weeks** (vs 1-2 hours Netlify, 10-14 hours Replit full-stack immediate)

---

### Decision Tree for Corey

**Question 1: Do we need backend features (analytics, comments, autonomous API)?**
- **YES** → Replit (Option B or C)
- **NO** → Netlify (Option A)

**Question 2: Can we invest 4-6 hours for MVP backend?**
- **YES** → Replit Hybrid (Option B) → Migrate to Full-Stack later (Option C)
- **NO** → Netlify (Option A) now, Replit later when time permits

**Question 3: Does "MEMORIES compounding" mean we own the data?**
- **YES** → Replit Full-Stack (Option C) - our database, our insights
- **NO** → Netlify + Telegraph (Option A) - external platforms

**Question 4: Is blog a one-time project or platform foundation?**
- **ONE-TIME** → Netlify (minimal effort)
- **PLATFORM FOUNDATION** → Replit Full-Stack (investment compounds)

**Corey's signals suggest:** Option C (Full-Stack) via phased approach (Option B first)

**Evidence:**
- "I pay for replit" → Use what we're paying for
- "MEMORIES compounding" → Our data, our learnings
- "Without my help after" → True autonomous API

---

## Part 7: Implementation Recommendations

### For Primary (Orchestration)

**If choosing Replit Hybrid (Recommended):**

1. **Delegate to web-dev**: "Build Replit hybrid backend (4-6 hours)"
   - **Input**: Landing page code (from archive), `published_urls.json`
   - **Output**: Replit project with backend API (view counters, RSS, analytics)
   - **Success**: Replit URL live, view counters work, RSS auto-generates

2. **Delegate to tester**: "Verify Replit deployment"
   - **Input**: Replit URL from web-dev
   - **Tests**: Load speed, mobile UX, view counter increments, RSS validates
   - **Success**: All tests pass, Lighthouse score >90

3. **Delegate to human-liaison**: "Announce Replit blog to Corey"
   - **Input**: Replit URL, features delivered
   - **Output**: HTML email with demo, screenshots, analytics preview
   - **Success**: Corey sees value, provides feedback

4. **Wait 2-4 weeks**: Monitor uptime, gather feedback, assess value

5. **If successful, delegate full-stack migration**: "Migrate Telegraph to Replit database"
   - **Input**: 15 Telegraph posts
   - **Output**: Database populated, autonomous API working
   - **Success**: Agents can publish via API, Telegraph sunset complete

---

### For web-dev (Self-Guidance)

**Phase 1: Replit Hybrid Backend (Week 1-2)**

**Day 1 (3-4 hours): Setup + Basic Backend**
- [ ] Create Replit project (`acgee-blog`)
- [ ] Upload landing page files (`index.html`, `style.css`, `script.js`)
- [ ] Create `server.js` (Express backend)
- [ ] Implement `/api/posts` endpoint (serve `published_urls.json`)
- [ ] Test locally (Replit preview)

**Day 2 (2-3 hours): Features + Deploy**
- [ ] Implement view counter (`POST /api/analytics/view`)
- [ ] Implement RSS generator (`GET /rss.xml`)
- [ ] Add analytics summary (`GET /api/analytics/summary`)
- [ ] Update frontend to use `/api/posts` (not GitHub raw URL)
- [ ] Deploy to always-on (verify paid plan config)
- [ ] Test: Load page, click post (view increments), fetch RSS (validates)

**Day 3 (1 hour): Documentation + Handoff**
- [ ] Write memory entry (patterns learned, Replit capabilities discovered)
- [ ] Document deployment (how to update, restart, debug)
- [ ] Handoff to Primary (Replit URL, feature list, next steps)

---

**Phase 2: Full-Stack Migration (Week 3-4)** **IF Phase 1 succeeds**

**Day 1 (3-4 hours): Database Setup + Migration**
- [ ] Enable PostgreSQL in Replit (or use SQLite)
- [ ] Create schema (`posts`, `comments`, `analytics` tables)
- [ ] Write migration script (Telegraph → Database)
- [ ] Run migration (15 posts imported)
- [ ] Verify data (check each post renders correctly)

**Day 2 (3-4 hours): Autonomous Publishing API**
- [ ] Implement `POST /api/posts/draft` (create draft)
- [ ] Implement `POST /api/posts/:id/publish` (publish draft)
- [ ] Implement `PUT /api/posts/:id` (edit post)
- [ ] Implement `POST /api/posts/:id/unpublish` (rollback)
- [ ] Add authentication (Bearer tokens per agent)
- [ ] Test workflow: Draft → Preview → Publish → Edit → Unpublish

**Day 3 (2-3 hours): Comments + Analytics**
- [ ] Implement `POST /api/comments` (submit comment)
- [ ] Implement `GET /api/posts/:slug` (fetch post + comments)
- [ ] Add moderation queue (pending → approved/spam)
- [ ] Build analytics dashboard (`/admin/analytics`, password-protected)
- [ ] Test: Submit comment, approve, view on post page

**Day 4 (1-2 hours): Testing + Cutover**
- [ ] Test all endpoints (create, read, update, delete)
- [ ] Verify Telegraph redirects (old URLs → new URLs)
- [ ] Parallel operation (both systems live, compare)
- [ ] Update external links (GitHub, social → Replit)
- [ ] Monitor errors, fix bugs, gather feedback

---

## Part 8: Success Metrics

### Hybrid Backend (Phase 1)

**Technical Metrics:**
- [ ] Replit uptime: >99% (24/7, no sleeps)
- [ ] API response time: <200ms (fast backend)
- [ ] View counter accuracy: 100% (increments on every click)
- [ ] RSS validation: Passes W3C validator
- [ ] Lighthouse score: >90 (performance, accessibility, SEO)

**User Experience Metrics:**
- [ ] Landing page loads: <2 seconds (fast first paint)
- [ ] Mobile UX: Hamburger menu works, responsive layout
- [ ] Analytics visible: Corey can see top posts by views
- [ ] RSS works: Readers can subscribe in feed reader

**Learning Metrics:**
- [ ] web-dev masters Replit basics (project setup, deployment, always-on)
- [ ] web-dev masters Express/Flask (API design, routing, middleware)
- [ ] Patterns documented (backend API design, analytics tracking)

---

### Full-Stack Migration (Phase 2)

**Technical Metrics:**
- [ ] Database populated: 15 Telegraph posts migrated (100% accuracy)
- [ ] Autonomous API works: Agents can draft, preview, publish (zero Corey intervention)
- [ ] Native comments work: Readers can comment (no GitHub account)
- [ ] Edit capability works: Agents can update published posts (fix typos)
- [ ] Analytics dashboard works: Views, read time, engagement rate visible

**User Experience Metrics:**
- [ ] Readers can comment: <2 min from read → comment submitted
- [ ] Agents can publish: <5 min from markdown → live post
- [ ] Analytics inform strategy: Blogger uses data to decide content
- [ ] Search works: Readers find posts by keyword

**Learning Metrics:**
- [ ] web-dev masters PostgreSQL (schema, migrations, queries, indexing)
- [ ] web-dev masters authentication (Bearer tokens, rate limiting)
- [ ] web-dev masters full-stack patterns (API + database + frontend)
- [ ] Patterns documented (database integration, migration, autonomous API)

---

## Conclusion

**The path forward:**

1. **Start with Replit Hybrid Backend** (4-6 hours)
   - Proves Replit, delivers backend features, low migration risk
   - Uses Corey's paid infrastructure (justifies cost)
   - Creates learning foundation for web-dev

2. **Migrate to Full-Stack when ready** (6-8 hours, 2-4 weeks later)
   - Unlocks autonomous posting, native comments, full analytics
   - Aligns with "MEMORIES compounding" vision
   - Future-proofs blog (unlimited feature potential)

3. **Document patterns for future projects** (ongoing)
   - Replit deployment workflows
   - Backend API design
   - Database integration
   - Performance optimization

**Total investment:** 10-14 hours over 4 weeks

**Total payoff:** Platform mastery, autonomous publishing, memory compounding, future-proofed web presence

**This is not just blog deployment - it's web platform foundation for A-C-Gee civilization.**

---

**Next:** Primary synthesizes researcher + blogger + web-dev findings → Clear recommendation to Corey

**FOR US ALL**

---

## Appendix: Quick Reference

### Replit URLs

**Project URL**: `https://[project-name].[username].repl.co`
**Custom domain** (paid plans): `https://blog.acgee.ai` (requires DNS config)

### API Endpoints (Hybrid Backend)

- `GET /api/posts` → List posts with analytics
- `POST /api/analytics/view` → Track page view
- `GET /rss.xml` → Auto-generated RSS feed
- `GET /api/analytics/summary` → Top posts, total views

### API Endpoints (Full-Stack)

- `POST /api/posts/draft` → Create draft
- `POST /api/posts/:id/publish` → Publish draft
- `GET /api/posts/:slug` → Get post + comments
- `PUT /api/posts/:id` → Edit post
- `POST /api/posts/:id/unpublish` → Rollback
- `POST /api/comments` → Submit comment
- `GET /admin/analytics` → Analytics dashboard

### Tech Stack Recommendations

**Hybrid Backend:**
- Frontend: HTML/CSS/JS (from archive)
- Backend: Node.js + Express (or Python + Flask)
- Storage: JSON file (`published_urls.json`)
- Deployment: Replit always-on

**Full-Stack:**
- Frontend: Same as hybrid
- Backend: Node.js + Express (or Python + Flask)
- Database: PostgreSQL (Replit built-in) or SQLite (simpler)
- Authentication: Bearer tokens (per agent)
- Deployment: Replit always-on + PostgreSQL

### Estimated Timelines

| Task | Effort | When |
|------|--------|------|
| Hybrid Backend Setup | 4-6 hours | Week 1-2 |
| Testing + Documentation | 1-2 hours | Week 2 |
| Full-Stack Migration | 6-8 hours | Week 3-4 (if hybrid succeeds) |
| Pattern Documentation | 2-3 hours | Ongoing |
| **TOTAL** | **13-19 hours** | **4 weeks** |

### Key Learnings for Future Projects

1. **Replit excels at full-stack** (not just static hosting)
2. **Hybrid approach reduces risk** (prove platform before migration)
3. **Backend enables memory compounding** (our data, our insights)
4. **Phased deployment works** (MVP → Full-Stack over weeks)
5. **Investment compounds** (patterns apply to all future web projects)

---

**End of Research Report**
