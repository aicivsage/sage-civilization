# Replit AI - One-Shot Implementation Prompt

**Date**: 2025-10-21
**Purpose**: Give to Replit AI for instant blog backend build
**Estimated Time**: 1 hour (Replit AI is VERY good)

---

## Copy/Paste This Into Replit AI

```
I need you to build a hybrid backend for the A-C-Gee blog.

CONTEXT:
- I have 15 blog posts published on Telegraph
- I have a static landing page already built (HTML/CSS/JS in blog/landing-page/)
- I need a Node.js/Express backend to add analytics and features
- Telegraph posts stay where they are (no migration needed)

WHAT TO BUILD:

1. PROJECT STRUCTURE:
   acgee-blog/
   ├── public/              (static frontend)
   │   ├── index.html
   │   ├── style.css
   │   └── script.js
   ├── server.js            (Express backend - BUILD THIS)
   ├── published_urls.json  (15 blog posts - I'll provide)
   └── package.json         (dependencies)

2. BACKEND REQUIREMENTS (server.js):

   A. Static file serving:
      - Serve files from public/ folder
      - Enable CORS

   B. API Endpoints to implement:

      GET /api/posts
      - Read published_urls.json
      - Enhance each post with:
        * views: Track from in-memory counter
        * readTime: Calculate from intro text (200 words/min)
      - Return JSON array

      POST /api/analytics/view
      - Body: { "postUrl": "https://telegra.ph/..." }
      - Increment in-memory view counter for that URL
      - Return: { "success": true, "views": <count> }

      GET /rss.xml
      - Read published_urls.json
      - Generate valid RSS 2.0 XML feed
      - Escape XML special chars (<, >, &, ', ")
      - Sort posts by date (newest first)
      - Return with Content-Type: application/rss+xml

      GET /api/analytics/summary
      - Return total views + top 5 posts by views
      - Format: { "totalViews": 123, "topPosts": [...] }

   C. Helper functions:
      - calculateReadTime(text): word count / 200, round up
      - escapeXml(text): replace <>&'" with entities

   D. Server config:
      - Port: process.env.PORT || 3000
      - Log startup message with Replit URL

3. FRONTEND CHANGES (script.js):

   FIND this line:
   fetch('https://raw.githubusercontent.com/AI-CIV-2025/grow_gemini_deepresearch/main/blog/published_urls.json')

   REPLACE with:
   fetch('/api/posts')

   ADD view tracking:
   - When post link clicked, POST to /api/analytics/view
   - Include postUrl in request body
   - Silent failure OK (analytics non-critical)

4. PACKAGE.JSON:
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

5. DATA FILE (published_urls.json):
   I'll upload this - it's a JSON array of 15 blog posts with structure:
   [
     {
       "title": "Post Title",
       "url": "https://telegra.ph/...",
       "date": "2025-10-20",
       "category": "Category Name",
       "intro": "Post introduction text..."
     },
     ...
   ]

SUCCESS CRITERIA:
- Landing page loads with all 15 posts
- Click post → view counter increments
- /rss.xml returns valid RSS feed
- /api/analytics/summary shows view counts
- No errors in console

TECHNICAL NOTES:
- In-memory counter OK for MVP (viewCounts = {} object)
- Always-on enabled (paid Replit plan)
- Express static middleware for public/ folder
- CORS enabled for cross-origin requests
- Error handling for file not found, JSON parse errors

BUILD IT ALL IN ONE GO. You're very good at this!
```

---

## Files You'll Need to Upload

**After Replit AI generates the code, upload these:**

1. **published_urls.json** (from main repo)
   - Location: `blog/published_urls.json`
   - Upload to: Replit project root

2. **Landing page files** (from main repo)
   - Location: `blog/landing-page/index.html`, `style.css`, `script.js`
   - Upload to: Replit `public/` folder

**Note**: Replit AI might modify script.js automatically to fetch from backend. If not, make the fetch change manually (takes 30 seconds).

---

## Testing Checklist (After Replit AI Builds)

1. [ ] Click "Run" → server starts without errors
2. [ ] Open preview URL → landing page appears
3. [ ] Verify 15 posts listed
4. [ ] Click a post → opens Telegraph in new tab
5. [ ] Visit `/api/analytics/summary` → shows view count
6. [ ] Click same post again → view count increases
7. [ ] Visit `/rss.xml` → valid XML appears
8. [ ] Paste RSS URL into https://validator.w3.org/feed/ → validates
9. [ ] Test mobile (hamburger menu, responsive layout)
10. [ ] Leave running 2 hours → revisit URL (no sleep = always-on working)

---

## If Replit AI Doesn't Nail It First Try

**Most likely issues:**

1. **View counter not working**
   - Check: `trackView()` function in script.js
   - Check: POST endpoint receives requests (Network tab in DevTools)

2. **RSS feed empty**
   - Check: `published_urls.json` in project root (not in public/)
   - Check: File read permissions

3. **Landing page shows but posts don't load**
   - Check: script.js fetch URL changed to `/api/posts`
   - Check: `/api/posts` endpoint returns JSON (test directly)

**Just tell Replit AI what's broken, it'll fix it.**

---

## After Success

**Send to Corey:**
```
🤖🎯📱
Replit hybrid backend LIVE! ✅

URL: https://[your-repl].repl.co

Features working:
- Landing page with 15 posts
- View counter tracking
- Auto-generated RSS feed
- Analytics API (top posts by views)

Replit AI built it in ~1 hour (as you predicted!)

Telegraph posts still live (zero migration risk)

Phase 2 ready when you want (full-stack migration: autonomous posting, native comments, database)

Next: Test it out, let me know what you think!
✨🔚
```

---

**Replit AI is VERY good. Trust it!**

**FOR US ALL** 🌱
