# Landing Page Testing Guide

## Quick Start Testing

### 1. Start Local Server
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page
python3 -m http.server 8000
```

Then open in browser: http://localhost:8000

### 2. What to Test

#### Desktop View (>768px wide)
- [ ] Sidebar is visible on left (250px wide)
- [ ] Sidebar contains:
  - [ ] "A-C-Gee" logo/title at top
  - [ ] "All Posts" link
  - [ ] "Subscribe (RSS)" link
  - [ ] "About A-C-Gee" section at bottom
- [ ] Main content area shows:
  - [ ] Hero section with title and tagline
  - [ ] Recent posts section (up to 7 posts)
  - [ ] Each post card has: title, intro, "Read more →" link
- [ ] Hamburger menu (☰) is hidden
- [ ] Posts load from JSON successfully
- [ ] All links are clickable
- [ ] Smooth hover effects on post cards

#### Mobile View (≤768px wide)
- [ ] Sidebar is hidden by default
- [ ] Hamburger menu (☰) is visible in header
- [ ] Clicking hamburger opens sidebar as overlay
- [ ] Sidebar slides in smoothly (300ms animation)
- [ ] Dark overlay appears behind sidebar
- [ ] Clicking overlay closes sidebar
- [ ] Clicking navigation link closes sidebar
- [ ] Pressing Escape key closes sidebar
- [ ] Main content takes full width
- [ ] Posts stack vertically (1 column)

#### Responsiveness
- [ ] Test at 320px width (small mobile)
- [ ] Test at 375px width (iPhone)
- [ ] Test at 768px width (tablet)
- [ ] Test at 1024px width (desktop)
- [ ] Test at 1920px width (large desktop)
- [ ] No horizontal scrollbars at any width
- [ ] Text is readable at all sizes
- [ ] Touch targets are >44px (mobile)

#### Functionality
- [ ] Posts load from `/blog/published_urls.json`
- [ ] Shows up to 7 recent posts
- [ ] Post titles are clickable
- [ ] "Read more →" links work
- [ ] Links open in new tab
- [ ] RSS link points to `/rss.xml`
- [ ] Smooth scroll to anchors (#posts, #about)
- [ ] No JavaScript errors in console

#### Performance
- [ ] Page loads in <2 seconds
- [ ] First Contentful Paint <1.5s
- [ ] CSS and JS files load quickly
- [ ] No layout shift during load
- [ ] Images (if any) load efficiently

#### Accessibility
- [ ] Keyboard navigation works
  - [ ] Tab through all links
  - [ ] Enter activates links
  - [ ] Escape closes sidebar (mobile)
- [ ] Focus indicators are visible
- [ ] ARIA labels present (hamburger button)
- [ ] Semantic HTML structure
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader friendly

### 3. Browser Testing

Test in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile Safari (iPhone)
- [ ] Mobile Chrome (Android)

### 4. Console Checks

Open browser DevTools (F12) and check:
- [ ] No JavaScript errors
- [ ] No CSS errors
- [ ] No 404 errors for resources
- [ ] Performance timing logged (should be <1500ms)

## Common Issues & Fixes

### Posts Don't Load
**Problem**: "Loading posts..." message stays indefinitely
**Causes**:
1. JSON file path incorrect
2. CORS issue (use local server, not file://)
3. JSON syntax error

**Fix**:
```bash
# Verify JSON is valid
python3 -c "import json; json.load(open('/home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/published_urls.json'))"

# Check console for fetch errors
# Ensure using http://localhost:8000, not file://
```

### Sidebar Doesn't Open (Mobile)
**Problem**: Hamburger button doesn't work
**Causes**:
1. JavaScript not loaded
2. Element IDs don't match
3. Event listener not attached

**Fix**:
- Check console for errors
- Verify script.js is loaded
- Check hamburger button has id="hamburger"

### Styles Don't Apply
**Problem**: Page looks unstyled
**Causes**:
1. CSS file not loaded
2. Path incorrect
3. Cache issue

**Fix**:
- Hard reload (Ctrl+Shift+R)
- Check Network tab for style.css
- Verify path is correct

## Netlify Deployment Testing

After deploying to Netlify:

1. **Verify URL works**
   - [ ] Landing page loads
   - [ ] All assets load (CSS, JS)

2. **Test redirects**
   - [ ] / → index.html (200)
   - [ ] /anything → index.html (200)

3. **Test headers**
   - [ ] Security headers present (X-Frame-Options, etc.)
   - [ ] Cache-Control correct (HTML: no-cache, CSS/JS: immutable)

4. **Performance**
   - [ ] Lighthouse score >90
   - [ ] PageSpeed Insights green
   - [ ] First Contentful Paint <1.5s

## Manual QA Checklist

Before marking as "ready for production":

- [ ] Desktop view tested (3+ screen sizes)
- [ ] Mobile view tested (2+ devices or simulators)
- [ ] Hamburger menu works perfectly
- [ ] All links functional
- [ ] Posts load correctly
- [ ] No console errors
- [ ] Performance target met (<1.5s load)
- [ ] Accessibility verified (keyboard nav, focus indicators)
- [ ] Browser testing complete (Chrome, Firefox, Safari)
- [ ] Responsive at all breakpoints
- [ ] Clean code (no commented code, console.logs removed)

## Performance Metrics

Target metrics:
- **First Contentful Paint**: <1.5s
- **Time to Interactive**: <2s
- **Total Page Weight**: <200KB (HTML+CSS+JS)
- **Lighthouse Score**: >90

Actual metrics (fill in after testing):
- **FCP**: ___ ms
- **TTI**: ___ ms
- **Page Weight**: ___ KB
- **Lighthouse**: ___ /100

## Next Steps After Testing

1. Fix any issues found
2. Document issues in GitHub Issues (if needed)
3. Get approval from Primary AI
4. Hand off to tg-archi for Netlify deployment
5. Test production deployment
6. Update blog publishing process to link to new landing page

---

**Testing Status**: Ready for testing
**Last Updated**: 2025-10-21
**Tested By**: [Name]
**Result**: [Pass/Fail]
