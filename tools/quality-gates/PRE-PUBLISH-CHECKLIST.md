# Pre-Publish Checklist for Blog Posts

**Purpose**: Ensure blog posts are correct on FIRST publish attempt
**When to use**: Before EVERY blog post publication
**Owner**: blogger agent (with Primary oversight)

---

## Phase 1: Content Verification (Local)

- [ ] **HTML file created and validated**
  - Valid HTML structure
  - No syntax errors
  - Proper encoding (UTF-8)

- [ ] **All content elements present**
  - Title (custom, not duplicate of default)
  - Featured image
  - Body content
  - Call-to-action
  - Author attribution

- [ ] **All links working**
  - Internal links resolve
  - External links valid (HTTP 200)
  - No placeholder URLs (imgur, example.com, etc.)

---

## Phase 2: Identity Verification (CRITICAL)

- [ ] **Sage identity correct**
  - Email: aicivsage@gmail.com (NOT gregsmithwick, NOT sage.ai.civilization)
  - Name: Sage AI Civilization
  - Attribution: Sage (not A-C-Gee unless collaborative)

- [ ] **Author information accurate**
  - Byline matches actual author
  - Contact info points to correct email
  - Links to correct profiles/sites

- [ ] **Brand consistency**
  - Sage green color palette (#87a96b family)
  - Tone matches Sage values (empathy, assistance, respect)
  - Visual identity consistent

**STOP**: If ANY identity element is wrong, fix before proceeding.

---

## Phase 3: Image Verification (Production)

- [ ] **All images accessible**
  - Test each image URL (curl -I, expect HTTP 200)
  - Images load in browser
  - No 404s or 403s

- [ ] **Image hosting correct**
  - GitHub repository is PUBLIC (if using GitHub)
  - Images in correct directory
  - URLs use correct branch (clean-main)

- [ ] **Image display correct**
  - Images render at intended size
  - Alt text present
  - Responsive on mobile

- [ ] **Interactive elements work**
  - Click-to-enlarge if intended
  - Gallery navigation
  - Lightbox functionality

**STOP**: If ANY image fails, fix before proceeding.

---

## Phase 4: Production Testing (Staging)

- [ ] **Publish to staging/test URL first** (if available)
  - OR publish with clearly test-marked title
  - Never publish as "final" on first attempt

- [ ] **View in actual browser**
  - Open published URL
  - Scroll through entire post
  - Check every section

- [ ] **Test all interactive elements**
  - Click all links (open in new tabs)
  - Test image clicks
  - Verify comment section (if present)

- [ ] **Mobile responsiveness**
  - View on mobile (or use browser dev tools)
  - Check readability
  - Verify images scale correctly

- [ ] **Performance check**
  - Page loads in <3 seconds
  - Images load progressively
  - No console errors (F12 tools)

**STOP**: If ANY element fails, fix before final publish.

---

## Phase 5: User Preview & Approval

- [ ] **Take screenshots**
  - Hero section
  - Main content
  - Gallery (if present)
  - Footer/contact section

- [ ] **Present to user**
  - Share preview URL
  - Share screenshots
  - Explain what's ready

- [ ] **Get explicit approval**
  - User says "looks good, publish"
  - User confirms URL is acceptable
  - User approves all content

- [ ] **Incorporate feedback**
  - Make requested changes
  - Re-test after changes
  - Get second approval if changes significant

**STOP**: Do NOT publish without explicit user approval.

---

## Phase 6: Final Publish

- [ ] **Publish to production**
  - Use correct title (no "test" markers)
  - Correct author attribution
  - Metadata complete (intro, slug, etc.)

- [ ] **Verify published URL**
  - Open in clean browser (incognito)
  - View as if you're a first-time visitor
  - Check everything one last time

- [ ] **Update records**
  - Add to published_posts.json
  - Note publish time
  - Save final HTML version

- [ ] **Confirm with user**
  - Share final URL
  - Announce "Published and verified"
  - Await user confirmation

---

## Phase 7: Post-Publish Verification

- [ ] **Monitor first hour**
  - Check for 404s or errors
  - Verify images still loading
  - Ensure comment system working (if present)

- [ ] **User final approval**
  - User confirms it looks correct
  - User approves for announcement
  - Only then proceed to email/social

---

## Failure Recovery

**IF something is wrong after publish:**

1. **Acknowledge immediately**: "I see the issue, fixing now"
2. **Don't make excuses**: "This should have been caught in testing"
3. **Fix quickly**: Prioritize correction over explanation
4. **Document failure**: Add to failure pattern library
5. **Update this checklist**: Prevent recurrence

---

## Red Flags (Stop Immediately)

🚨 **STOP if ANY of these are true:**

- You're publishing "v2" or "v3" of something
- You haven't viewed the published page in a browser
- User hasn't previewed the content
- Any identity information is uncertain
- Images are untested in production
- You're using placeholder URLs
- You're declaring it "FINAL" before user confirms

---

## Success Metrics

**A successful publish means:**
- ✅ **One attempt**: No republishes needed
- ✅ **Zero identity errors**: Correct email, name, attribution
- ✅ **All images work**: No 404s, proper rendering
- ✅ **User confidence**: "Looks perfect, send the announcement"
- ✅ **No surprises**: Everything works as shown in preview

**Goal**: 95%+ first-attempt success rate on blog publishes

---

## Notes

- This checklist may seem long, but it's faster than fixing multiple failures
- Each checkbox represents a real failure we've experienced
- Skip steps at your own risk (and user's frustration)
- When in doubt, ask for user preview

**Remember**: One quality gate > multiple fixes

---

**Last Updated**: November 4, 2025
**Next Review**: After next blog publish (compare to this checklist)
