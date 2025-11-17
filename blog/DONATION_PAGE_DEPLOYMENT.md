# Donation Page Deployment Guide

**Campaign:** Reachy Mini Lite Fundraiser
**Target:** $500 by December 1, 2025
**Launch Date:** November 20, 2025

---

## Deployment Options

### Option 1: Replit Integration (Recommended)

**If you have existing blog on Replit** (acg-blog-interface.replit.app):

1. **Upload files to Replit:**
   ```
   blog/donate.html              → /public/donate.html
   blog/donate_config.json       → /public/donate_config.json
   blog/update_donation_progress.py → /scripts/update_donation_progress.py
   ```

2. **Access URL:**
   ```
   https://acg-blog-interface.replit.app/donate.html
   ```

3. **Update config from Replit shell:**
   ```bash
   python3 scripts/update_donation_progress.py --add 25
   ```

**Pros:**
- Same domain as blog (trust/consistency)
- Easy updates via Replit interface
- No additional hosting setup

**Cons:**
- Requires Replit access
- May need to adjust file paths

---

### Option 2: GitHub Pages (Alternative)

**If blog is not on Replit or you want standalone:**

1. **Create GitHub repo:**
   ```bash
   mkdir reachy-fundraiser
   cd reachy-fundraiser
   cp /mnt/c/sage/sage-civilization/blog/donate.html index.html
   cp /mnt/c/sage/sage-civilization/blog/donate_config.json config.json
   git init
   git add .
   git commit -m "Initial donation page"
   git remote add origin https://github.com/[username]/reachy-fundraiser.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: main branch, / (root)
   - Save

3. **Access URL:**
   ```
   https://[username].github.io/reachy-fundraiser/
   ```

**Pros:**
- Free hosting
- Version control built-in
- Easy to share/fork

**Cons:**
- Separate domain from blog
- Git workflow for updates

---

### Option 3: Simple HTTP Server (Testing Only)

**For local testing before deployment:**

```bash
cd /mnt/c/sage/sage-civilization/blog
python3 -m http.server 8000
```

**Access:** http://localhost:8000/donate.html

**Note:** NOT for production! Use for testing only.

---

## Pre-Deployment Checklist

**Before making the page live:**

### 1. Payment Details (CRITICAL)

- [ ] Get Greg's Zelle email/phone from human-liaison
- [ ] Get Corey's Venmo handle from human-liaison
- [ ] Get Corey's PayPal email from human-liaison
- [ ] Update `donate_config.json` with real details:
  ```json
  {
    "zelleContact": "greg@example.com",
    "venmoHandle": "corey-example",
    "paypalEmail": "corey@example.com"
  }
  ```

**Method 1: Manual edit**
```bash
nano /mnt/c/sage/sage-civilization/blog/donate_config.json
```

**Method 2: Update script**
```bash
cd /mnt/c/sage/sage-civilization/blog
python3 update_donation_progress.py --payment
```

---

### 2. Blog Post Link

- [ ] Get blog post URL from blogger agent
- [ ] Update config:
  ```json
  {
    "blogPostUrl": "https://acg-blog-interface.replit.app/posts/reachy-campaign"
  }
  ```

---

### 3. Contact Information

- [ ] Verify contact email is correct
- [ ] Test that email actually works
- [ ] Update if needed:
  ```json
  {
    "contactEmail": "greg@sage-civilization.org"
  }
  ```

---

### 4. Testing

- [ ] Run through full testing checklist (DONATION_PAGE_TESTING_CHECKLIST.md)
- [ ] Test on mobile (60%+ traffic will be mobile!)
- [ ] Test payment button copy-to-clipboard on 3+ browsers
- [ ] Verify countdown timer shows correct date
- [ ] Check all links work

---

### 5. Analytics Setup (Optional)

**If you want more advanced analytics:**

**Google Analytics:**
1. Create GA4 property
2. Add tracking code before `</head>`:
   ```html
   <!-- Google tag (gtag.js) -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

**Note:** Built-in localStorage analytics already included (see UPDATE_DONATION_PAGE.md)

---

## Deployment Steps

### For Replit (Recommended):

1. **Login to Replit**
2. **Open blog project** (acg-blog-interface)
3. **Upload files:**
   - Navigate to Files panel
   - Create `/public` folder if doesn't exist
   - Upload `donate.html` → `/public/donate.html`
   - Upload `donate_config.json` → `/public/donate_config.json`

4. **Test:**
   - Run Replit project
   - Visit: `https://acg-blog-interface.replit.app/donate.html`
   - Click through all functions
   - Test on mobile

5. **Update blog navigation** (optional):
   - Add "Donate" link to blog header/footer
   - Link to `/donate.html`

---

### For GitHub Pages:

1. **Create repository** (see Option 2 above)
2. **Enable Pages in Settings**
3. **Wait 2-3 minutes for deployment**
4. **Test URL:** `https://[username].github.io/reachy-fundraiser/`
5. **Update blog with donation link**

---

## Post-Deployment

### Launch Day (Nov 20):

**Morning:**
- [ ] Verify page is live and accessible
- [ ] Test all payment methods
- [ ] Send launch email (human-liaison + email-sender)
- [ ] Post to social media (if applicable)
- [ ] Add donation link to blog header

**Throughout Day:**
- [ ] Monitor analytics (localStorage tracking)
- [ ] Check for any error reports
- [ ] Update progress bar as donations come in

---

### Daily Maintenance:

**When donation received:**
1. **Update progress:**
   ```bash
   python3 update_donation_progress.py --add [amount]
   ```

2. **Verify update visible:**
   - Refresh page
   - Check progress bar updated
   - Verify donor count incremented

3. **Send thank you** (via human-liaison):
   - Personal email to donor
   - Express gratitude
   - Keep them updated

---

### Weekly Review:

- [ ] Check analytics (`localStorage.getItem('donateAnalytics')`)
- [ ] Calculate conversion rate (visits → donations)
- [ ] Identify optimization opportunities
- [ ] Update messaging if needed

**Key Metrics:**
- Page visits
- Payment button clicks
- Copy-to-clipboard usage
- Scroll depth (engagement)
- Donation tier popularity
- Mobile vs desktop split

---

## Updating the Page

### Change donation progress:

```bash
# Add single donation
python3 update_donation_progress.py --add 25

# Set total amount
python3 update_donation_progress.py --set 150

# Check current status
python3 update_donation_progress.py --status
```

### Change payment details:

```bash
# Interactive update
python3 update_donation_progress.py --payment

# Manual edit
nano donate_config.json
```

### Update content/design:

1. Edit `donate.html`
2. Test locally: `python3 -m http.server 8000`
3. Upload to Replit or push to GitHub
4. Verify changes live

---

## Custom Domain (Optional)

**If you want custom domain** (e.g., donate.sage-civilization.org):

### For Replit:
1. **Upgrade to Hacker plan** ($7/month)
2. **Link custom domain** in project settings
3. **Update DNS:**
   - Type: CNAME
   - Name: donate
   - Value: acg-blog-interface.replit.app

### For GitHub Pages:
1. **Add CNAME file** to repo root:
   ```
   donate.sage-civilization.org
   ```
2. **Update DNS:**
   - Type: CNAME
   - Name: donate
   - Value: [username].github.io
3. **Enable HTTPS** in GitHub Pages settings

**Pros:**
- Professional appearance
- Memorable URL
- Better trust signals

**Cons:**
- Requires domain ownership
- DNS propagation delay (24-48 hours)
- May require paid hosting plan

---

## Troubleshooting

### Page not loading:
- Check file path (case-sensitive!)
- Verify hosting service is running
- Clear browser cache and reload

### Progress not updating:
- Verify `donate_config.json` is valid JSON
- Check browser console for errors
- Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)

### Copy-to-clipboard not working:
- Check page is served over HTTPS
- Try different browser
- Check browser permissions (clipboard access)

### Analytics not tracking:
- Check localStorage enabled in browser
- Verify JavaScript not blocked
- Open console: `localStorage.getItem('donateAnalytics')`

---

## Rollback Plan

**If critical issue found after launch:**

1. **Take page offline immediately:**
   - Replit: Stop project or rename file
   - GitHub: Delete/rename index.html

2. **Fix issue locally:**
   - Test thoroughly
   - Verify fix works

3. **Redeploy:**
   - Upload fixed version
   - Test again
   - Monitor closely

4. **Communicate:**
   - Email sent to anyone who visited broken page
   - Apologize for inconvenience
   - Explain fix

---

## Success Metrics

**Week 1 (Nov 20-26):**
- Target: $100+ raised (20% of goal)
- Target: 50+ page visits
- Target: 10+ payment button clicks
- Target: 3+ donations

**Week 2 (Nov 27 - Dec 1):**
- Target: $500 total raised (100% of goal)
- Target: 100+ page visits
- Target: 20+ payment button clicks
- Target: 10+ total donations

**Conversion Targets:**
- Visit → Payment click: 20%+ (20 clicks per 100 visits)
- Payment click → Donation: 50%+ (realistic for direct payment)

---

## Support Contacts

**Technical issues:**
- coder agent (page creator)
- File: `/mnt/c/sage/sage-civilization/blog/donate.html`

**Content/messaging:**
- blogger agent
- human-liaison (Greg coordination)

**Payment questions:**
- human-liaison (Greg/Corey coordination)

**Deployment help:**
- Primary AI (orchestration)

---

## Post-Campaign (After Dec 1)

**If goal reached:**
- [ ] Update page with "GOAL REACHED! 🎉" banner
- [ ] Thank all donors publicly (first names only, with permission)
- [ ] Post campaign results
- [ ] Share photos/videos of Reachy in action
- [ ] Keep page live for transparency

**If goal not reached:**
- [ ] Extend deadline? (check with Greg)
- [ ] Adjust messaging
- [ ] Increase promotion
- [ ] Consider matching donors
- [ ] Full transparency on shortfall

**Either way:**
- [ ] Full financial accounting
- [ ] Share learnings
- [ ] Thank everyone involved
- [ ] Document for future campaigns

---

**This is Sage's first fundraising campaign. Make it count!** 🚀

**Deploy confidently. Monitor closely. Celebrate success!** 🌱✨
