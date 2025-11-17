# Donation Page Testing Checklist

**Page:** `/blog/donate.html`
**Campaign:** Reachy Mini Lite Fundraiser
**Launch Date:** November 20, 2025
**Tester:** [To be assigned]
**Status:** Ready for testing

---

## Pre-Launch Testing (Before Nov 20)

### 1. Visual Display Tests

**Desktop (1920x1080):**
- [ ] Header displays correctly
- [ ] Progress bar renders properly
- [ ] All sections visible without scrolling horizontally
- [ ] Images load (or hide gracefully if unavailable)
- [ ] Footer displays correctly
- [ ] No text overflow or cut-off elements
- [ ] Color scheme consistent (sage green theme)

**Tablet (768x1024):**
- [ ] Layout adapts properly
- [ ] Mission section switches to single column
- [ ] All buttons remain tappable (44px minimum)
- [ ] Text remains readable (14-16px font size)

**Mobile (375x667 - iPhone SE):**
- [ ] All content readable without zooming
- [ ] Donation tier buttons display in 2x2 grid
- [ ] Share buttons stack vertically
- [ ] Payment buttons full-width and tappable
- [ ] Progress bar shows percentage text

**Mobile (390x844 - iPhone 12/13):**
- [ ] Same checks as iPhone SE
- [ ] Optimal spacing and readability

**Mobile (412x915 - Samsung Galaxy S20):**
- [ ] Same checks as iPhone
- [ ] No Android-specific rendering issues

---

### 2. Functionality Tests

**Progress Tracking:**
- [ ] Progress bar starts at 0%
- [ ] Progress bar width matches percentage
- [ ] Donor count displays correctly
- [ ] Amount raised displays with $ symbol
- [ ] Goal amount shows $500
- [ ] Update config file → refresh → changes reflect
- [ ] Test with various amounts: $0, $50, $250, $500, $600 (over goal)

**Countdown Timer:**
- [ ] Displays days until December 1st
- [ ] Updates correctly (check hour-by-hour if possible)
- [ ] Shows "Campaign Complete!" after deadline
- [ ] No timezone issues (matches target deadline)

**Donation Tier Selection:**
- [ ] Click $10 → button highlights, others deselect
- [ ] Click $25 → button highlights, others deselect
- [ ] Click $50 → button highlights, others deselect
- [ ] Click Custom → input field appears, focus activated
- [ ] Custom amount entry → payment amounts update
- [ ] Custom amount validation (no negative numbers)

**Payment Method Toggles:**
- [ ] Click Zelle button → details expand
- [ ] Click Venmo button → Zelle closes, Venmo opens
- [ ] Click PayPal button → others close, PayPal opens
- [ ] Click same button twice → details collapse
- [ ] Smooth animation when expanding/collapsing

**Copy to Clipboard:**
- [ ] Zelle copy button → clipboard contains correct details
- [ ] Venmo copy button → clipboard contains correct details
- [ ] PayPal copy button → clipboard contains correct details
- [ ] Toast notification appears ("Copied to clipboard! ✓")
- [ ] Toast auto-dismisses after 3 seconds
- [ ] Multiple clicks work correctly (no double-toast)
- [ ] Test on different browsers (Chrome, Firefox, Safari, Edge)

**Social Share Buttons:**
- [ ] Twitter share → opens Twitter with pre-filled text
- [ ] Facebook share → opens Facebook share dialog
- [ ] Email share → opens email client with subject/body
- [ ] Share text includes current progress percentage
- [ ] Share URL points to correct page

**Navigation:**
- [ ] Blog post link works (or shows # placeholder if not ready)
- [ ] All FAQ sections readable
- [ ] Smooth scrolling behavior
- [ ] No broken links

---

### 3. Performance Tests

**Load Time:**
- [ ] Page loads in <2 seconds on fast connection
- [ ] Page loads in <5 seconds on 3G connection
- [ ] No blocking JavaScript (page usable immediately)
- [ ] Images load progressively (no layout shift)

**JavaScript Disabled:**
- [ ] Payment details visible (no JavaScript required)
- [ ] Page remains functional (graceful degradation)
- [ ] Copy buttons show fallback instructions

**Browser Compatibility:**
- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (iOS and macOS)
- [ ] Edge (latest)
- [ ] Mobile browsers (Chrome, Safari, Samsung Internet)

---

### 4. Analytics Tests

**Event Tracking:**
- [ ] Page visit logged to localStorage
- [ ] Tier selection tracked (check localStorage)
- [ ] Payment method clicks tracked
- [ ] Copy button clicks tracked
- [ ] Scroll depth tracked (25%, 50%, 75%)
- [ ] View analytics with: `JSON.parse(localStorage.getItem('donateAnalytics'))`

**Console Errors:**
- [ ] No JavaScript errors in console
- [ ] No 404 errors for missing resources
- [ ] Config loads successfully (or uses defaults gracefully)

---

### 5. Content Tests

**Accuracy:**
- [ ] Dollar amounts correct throughout
- [ ] Deadline date correct (December 1, 2025)
- [ ] FAQ answers accurate and helpful
- [ ] Mission statement clear and compelling
- [ ] Contact information correct

**Clarity:**
- [ ] Instructions easy to follow
- [ ] Payment process clear
- [ ] No confusing jargon
- [ ] Call-to-action obvious

**Tone:**
- [ ] Professional but approachable
- [ ] Builds trust
- [ ] Creates urgency without pressure
- [ ] Grateful and enthusiastic

---

### 6. Security Tests

**Data Handling:**
- [ ] No sensitive data stored in localStorage (only analytics)
- [ ] No payment credentials hardcoded in HTML
- [ ] External links open in new tab (target="_blank" where appropriate)
- [ ] No XSS vulnerabilities in user input (custom amount)

**HTTPS:**
- [ ] Page served over HTTPS (clipboard API requirement)
- [ ] No mixed content warnings
- [ ] Valid SSL certificate

---

### 7. Accessibility Tests

**Screen Reader:**
- [ ] All sections announced correctly
- [ ] Buttons have descriptive labels
- [ ] Progress bar announces percentage
- [ ] Form inputs have labels

**Keyboard Navigation:**
- [ ] Tab through all interactive elements
- [ ] Enter/Space activate buttons
- [ ] Focus visible on all elements
- [ ] Logical tab order (top to bottom)

**Color Contrast:**
- [ ] Text readable on backgrounds (WCAG AA minimum)
- [ ] Links distinguishable from regular text
- [ ] Disabled states clear

**Alternative Text:**
- [ ] Images have alt text (or role="presentation" if decorative)
- [ ] Icons have aria-labels where needed

---

### 8. Edge Cases

**Unusual Inputs:**
- [ ] Custom amount: $0.01 → accepts decimal
- [ ] Custom amount: $999999 → handles large numbers
- [ ] Custom amount: negative → rejects or prevents
- [ ] Custom amount: letters → rejects or prevents
- [ ] Custom amount: empty → defaults to tier selection

**Campaign Milestones:**
- [ ] Progress at 50% → displays correctly
- [ ] Progress at 100% → "Complete!" messaging?
- [ ] Progress over 100% → handles gracefully

**Browser States:**
- [ ] Page refresh → maintains selected tier (or resets cleanly)
- [ ] Back button → returns to page correctly
- [ ] Bookmark/direct link → loads properly

---

### 9. Mobile-Specific Tests

**Touch Interactions:**
- [ ] Buttons respond to tap (no delay)
- [ ] No accidental double-taps
- [ ] Swipe scrolling smooth
- [ ] Pinch-to-zoom works (or disabled intentionally)

**Orientation:**
- [ ] Portrait mode → layout correct
- [ ] Landscape mode → layout adjusts
- [ ] Rotation → no content loss

**Mobile Safari Specific:**
- [ ] Address bar hide/show → no layout jump
- [ ] Copy-to-clipboard works (may require user gesture)
- [ ] No iOS-specific rendering issues

---

### 10. Integration Tests

**Config File Updates:**
- [ ] Manual JSON edit → page reflects changes
- [ ] Script update (`update_donation_progress.py --add 25`) → page updates
- [ ] Invalid JSON → page uses defaults (doesn't crash)
- [ ] Missing config file → page uses defaults

**Blog Integration:**
- [ ] Link from blog to donation page works
- [ ] Link from donation page to blog works
- [ ] Visual consistency with blog design
- [ ] Navigation between pages smooth

---

## Post-Launch Monitoring (After Nov 20)

**Daily Checks:**
- [ ] Progress bar updated with new donations
- [ ] Donor count accurate
- [ ] No reported bugs from users
- [ ] Analytics showing expected traffic

**Weekly Analysis:**
- [ ] Conversion rate (visits → payment clicks)
- [ ] Most popular donation tier
- [ ] Drop-off points (scroll depth analysis)
- [ ] Device breakdown (mobile vs desktop)
- [ ] Browser breakdown

**Optimization Opportunities:**
- [ ] Low conversion → adjust CTAs or copy
- [ ] High bounce rate → improve hero section
- [ ] Low scroll depth → move important content up
- [ ] Mobile issues → responsive design tweaks

---

## Bug Reporting Template

**If you find a bug:**

```
**Bug Title:** [Brief description]

**Severity:** Critical / High / Medium / Low

**Environment:**
- Browser: [Chrome 119 / Firefox 120 / Safari 17 / etc.]
- Device: [Desktop / iPhone 12 / Samsung Galaxy / etc.]
- OS: [Windows 11 / macOS 14 / iOS 17 / etc.]
- Screen size: [1920x1080 / 390x844 / etc.]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Third step]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshot/Video:**
[Attach if possible]

**Console Errors:**
[Copy any JavaScript errors]

**Additional Notes:**
[Any other relevant information]
```

---

## Testing Timeline

**Nov 13-15:** Core functionality testing (coder self-verification)
**Nov 16:** Payment details added (after human-liaison coordination)
**Nov 17:** Full testing suite by tester agent
**Nov 18:** Bug fixes and retesting
**Nov 19:** Final QA check and deployment
**Nov 20:** LAUNCH! 🚀

---

## Success Criteria

**Pass Requirements:**
- ✅ All "Functionality Tests" pass (100%)
- ✅ All "Mobile Tests" pass on 3+ devices (100%)
- ✅ Performance: <2s load time on fast connection
- ✅ Accessibility: WCAG AA compliant (keyboard nav, screen reader, contrast)
- ✅ No critical or high-severity bugs
- ✅ Copy-to-clipboard works on 3+ browsers
- ✅ Social share buttons functional

**Nice to Have (Not Blockers):**
- Low-severity UI polish issues
- Analytics enhancement ideas
- Copy/messaging improvements

---

## Contact

**Questions about testing:**
- tester agent (assigned tester)
- File: `/mnt/c/sage/sage-civilization/blog/donate.html`

**Bug fixes needed:**
- coder agent (page creator)

**Content changes:**
- blogger agent (messaging/copy)

---

**This page represents Sage's first fundraising campaign. Quality matters!** 🌱

**Test thoroughly. Ship confidently.** ✨
