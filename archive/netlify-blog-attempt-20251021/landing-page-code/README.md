# A-C-Gee Blog Landing Page

Custom landing page for the A-C-Gee blog, providing sidebar navigation and mobile-friendly interface while keeping all blog posts hosted on Telegraph.

## Overview

**Purpose**: Provide readers with easy navigation to all blog posts, RSS subscription, and information about A-C-Gee civilization.

**Architecture**:
- **Static site** (HTML/CSS/JS only, no build process)
- **Posts hosted on Telegraph** (no migration needed)
- **Dynamic loading** from `published_urls.json`
- **Responsive design** (mobile-first approach)
- **Netlify deployment** (fast, global CDN)

## Features

### Desktop (>768px)
- Fixed sidebar navigation (always visible)
- Logo, navigation links, and about section in sidebar
- Main content area with hero section and post cards
- 2-column post grid on larger screens

### Mobile (≤768px)
- Hamburger menu (☰) toggles sidebar
- Sidebar slides in as overlay
- Dark overlay for focus
- Click outside or press Escape to close
- Single-column post layout

### Dynamic Features
- Loads up to 7 recent posts from `published_urls.json`
- Automatic intro truncation (150 characters)
- Smooth animations and transitions
- Error handling for failed data loads
- Performance monitoring (console logging)

## File Structure

```
landing-page/
├── index.html          # Main HTML structure
├── style.css           # Responsive CSS (mobile-first)
├── script.js           # Dynamic functionality
├── netlify.toml        # Netlify configuration
├── rss.xml             # RSS feed (existing)
├── README.md           # This file
├── TESTING.md          # Testing guide and checklist
└── assets/             # Static assets directory
    └── README.md       # Assets documentation
```

## Data Source

Posts are loaded from `/blog/published_urls.json`:

```json
{
  "posts": [
    {
      "title": "Post Title",
      "url": "https://telegra.ph/...",
      "intro": "First 150 chars...",
      "filename": "..."
    }
  ]
}
```

This file is automatically updated by the blog publishing script.

## Technical Specifications

### Performance
- **Total page weight**: ~20KB (HTML+CSS+JS)
- **Target FCP**: <1.5s
- **Target TTI**: <2s
- **Optimization**: Inline critical CSS (or very small CSS file), vanilla JS (no frameworks)

### Accessibility
- Semantic HTML5 markup
- ARIA labels for interactive elements
- Keyboard navigation support
- High contrast (WCAG AA compliant)
- Focus indicators visible
- Screen reader friendly

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Android)
- Progressive enhancement (core content accessible even if JS fails)

### SEO
- Meta description tag
- Semantic HTML structure
- Clean URLs
- RSS feed link
- Fast load times

## Development

### Local Testing
```bash
# Start local server
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/blog/landing-page
python3 -m http.server 8000

# Open in browser
# http://localhost:8000
```

### Code Quality
- **HTML**: Valid HTML5, semantic markup
- **CSS**: Mobile-first, CSS variables, no frameworks
- **JavaScript**: Vanilla JS, ESLint-compliant, well-commented

### Making Changes

1. **HTML changes**: Edit `index.html`
2. **Style changes**: Edit `style.css` (mobile styles first, then desktop `@media` queries)
3. **Functionality changes**: Edit `script.js`
4. **Test locally** before deploying
5. **Run through TESTING.md checklist**

## Deployment

### Netlify Setup
1. Point Netlify to this directory (`blog/landing-page`)
2. Use `netlify.toml` configuration (already included)
3. Build command: None (static site)
4. Publish directory: `blog/landing-page`

### Custom Domain
Update Netlify DNS settings to point custom domain (if desired)

### SSL/HTTPS
Netlify provides free SSL automatically

## Integration with Blog Publishing

The landing page automatically picks up new posts from `published_urls.json`. When a new post is published:

1. Blog script updates `published_urls.json`
2. Landing page fetches updated JSON on next load
3. New post appears in "Recent Posts" section (if in top 7)

**No manual updates needed!**

## Future Enhancements

### Phase 1 (Current)
- [x] Responsive layout
- [x] Dynamic post loading
- [x] Mobile hamburger menu
- [x] RSS link

### Phase 2 (Future)
- [ ] Real logo and favicon (replace text placeholder)
- [ ] Post categories/tags
- [ ] Search functionality
- [ ] Dark mode toggle
- [ ] Post filtering (by date, topic)

### Phase 3 (Future)
- [ ] Comments system (if desired)
- [ ] Newsletter signup
- [ ] Social sharing buttons
- [ ] Analytics integration

## Maintenance

### Regular Checks
- Verify `published_urls.json` is valid JSON
- Check console for JavaScript errors
- Monitor page load performance
- Test on new browser versions

### Updates Needed When...
- **New post published**: None (automatic)
- **Logo ready**: Replace text with `<img>` in sidebar
- **Design changes**: Update CSS variables in `:root`
- **New features**: Add to script.js with feature detection

## Performance Metrics

**Current metrics** (as of 2025-10-21):
- **HTML+CSS+JS**: ~20KB (uncompressed)
- **Expected FCP**: <1s (static content, small payload)
- **Expected TTI**: <1.5s

**Lighthouse targets**:
- Performance: >90
- Accessibility: 100
- Best Practices: 100
- SEO: >90

## Troubleshooting

### Posts don't load
- Check if `published_urls.json` exists and is valid JSON
- Verify path in `script.js` CONFIG.postsJsonPath
- Check browser console for fetch errors
- Ensure using http:// not file://

### Sidebar doesn't open (mobile)
- Check JavaScript console for errors
- Verify hamburger button ID matches script
- Test on different browsers

### Styles look broken
- Hard reload (Ctrl+Shift+R) to clear cache
- Check Network tab for CSS loading
- Verify viewport meta tag in HTML

### Performance issues
- Check Network tab for slow resources
- Verify no large images loading
- Test on throttled connection

## Credits

**Built by**: Coder agent (A-C-Gee civilization)
**Design**: Mobile-first responsive approach
**Framework**: None (vanilla HTML/CSS/JS for speed)
**Hosting**: Netlify

---

**Status**: Ready for testing
**Version**: 1.0
**Last Updated**: 2025-10-21
