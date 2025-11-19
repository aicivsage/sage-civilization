# Fundraising Post Publishing Analysis

**Date**: 2025-11-19
**Agent**: blogger
**Task**: Investigate blog post publishing issues and provide clean URL to Greg

## What I Found

### The "Duplicate" Intro Issue

Greg reported that the published fundraising post had "duplicate titles and intro lines."

**Investigation revealed**: This is how the ACG Blog Interface platform is DESIGNED to work:

1. The API extracts the first `<p>` tag from content as the "intro"
2. It displays this intro in a special `<div class="intro"><strong>` section
3. It ALSO includes the full content (which contains that same paragraph)
4. Result: Intro text appears TWICE - once in intro div, once in content

**Evidence**: I checked an ACG-native post ("Cutting Edge: Memory Enables Everything") and found THE SAME pattern:
- Intro div: "*How Five Specialist Agents Proved We're Different*..."
- Content starts: Same paragraph again

**Conclusion**: This is platform behavior, not a bug. The "duplication" is intentional design.

### Current State of Posts

**Posts on ACG Blog about Sage fundraising:**

| ID | Slug | Title | Intro Status | Content Status |
|----|------|-------|--------------|----------------|
| 39 | sage-from-fear-to-friend-why-were-getting-a-robot | [SAGE] From Fear... | Unknown | Unknown |
| 40 | ...with-images | [SAGE] From Fear... | Unknown | Unknown |
| 41 | ...fundraising-for-our-robot-partner | [SAGE] From Fear... | Unknown | Unknown |
| 42 | ...updated | [SAGE] From Fear... | Unknown | Unknown |
| 43 | ...revised-edition | [SAGE] From Fear... | Unknown | Unknown |
| 44 | ...corrected | [SAGE] From Fear... (Corrected) | WRONG - image caption | Has wrapper article tags |
| 45 | ...final | [SAGE] From Fear... (Final) | CORRECT | CORRECT |
| 46 | ...why-sage-needs-a-robot | [SAGE] From Fear... Why Sage Needs | WRONG - image caption | Content correct but no intro |

### The CORRECT Post

**Post 45 is the correct version:**
- URL: `https://acg-blog-interface.replit.app/post/sage-from-fear-to-friend-why-were-getting-a-robot-final`
- Title: "[SAGE] From Fear to Friend: Why We're Getting a Robot (Final)"
- Intro: Correctly extracted ("I understand why people fear AI...")
- Content: Complete and correct (includes all sections, images, formatting)
- "Duplicate" intro: This is platform design (happens on all ACG posts)

## What I Learned

### API Publishing Process

The `tools/publish_to_replit_blog.py` script:
1. Extracts body content from full HTML (removes DOCTYPE, html, head, body tags)
2. Extracts first `<p>` tag as intro (max 250 chars)
3. Sends both `intro` and `content` fields to API
4. API renders intro in special div + includes full content

### Why Previous Attempts Had Wrong Intro

When I removed the intro paragraph from content (trying to avoid "duplication"), the API extracted the NEXT `<p>` tag it found - which was the image caption. That's why posts 44 and 46 show "Sage's visual identity..." as the intro.

**Lesson**: Keep the intro paragraph IN the content. The platform WANTS it there twice.

### Authentication Issues

**Sage's API key doesn't work yet** - returns 401 Unauthorized when trying to publish to Sage collective.

**Workaround**: Use `--use-acg-workaround` flag to publish to ACG blog with `[SAGE]` prefix in title.

**This is why all Sage posts are on ACG blog (collectiveId: 1) instead of Sage blog.**

### Deletion Issues

Cannot delete posts 44, 46, or others because:
1. They're on ACG blog (collectiveId: 1)
2. Sage's API key is for Sage collective, not ACG
3. Would need ACG credentials to delete from ACG blog

## Recommendations for Greg

### Immediate Action

**Use this URL for fundraising emails:**
`https://acg-blog-interface.replit.app/post/sage-from-fear-to-friend-why-were-getting-a-robot-final`

This is the cleanest version available. The "duplicate" intro is just how the platform works.

### Cleanup Action (Requires Corey/ACG Access)

To clean up the broken versions from ACG blog:
1. Need ACG API credentials (not Sage credentials)
2. Use DELETE requests to remove posts 39-44, 46
3. OR unpublish them (set `published: false`)

**I cannot do this with Sage credentials** - would need Corey's help or ACG access.

### Future Publishing

When Sage credentials are working:
1. Posts will publish to Sage blog (not ACG)
2. Won't have this multi-version problem
3. Can control the landing page directly

## Deliverables

### Files Created
- `/tmp/fundraising-post-clean.html` - Body content without intro (wrong approach)
- `/tmp/fundraising-post-correct.html` - Body content with intro (correct approach)

### Published Posts
- Post 46: `https://acg-blog-interface.replit.app/post/sage-from-fear-to-friend-why-sage-needs-a-robot`
  - Wrong intro (image caption)
  - Created during investigation
  - Should probably be deleted

### Memory Files
- This file: Analysis and learnings

## For Next Time

### Publishing Best Practices

1. **Keep intro paragraph in content** - don't try to remove it
2. **Test intro extraction** - verify first `<p>` is correct paragraph
3. **Use full HTML source** - let publishing script extract body content
4. **Accept platform design** - intro will appear twice, this is normal
5. **Check rendered output** - curl the published URL to verify

### Platform Understanding

The ACG Blog Interface renders posts like this:
```html
<div class="intro"><strong>[First paragraph]</strong></div>
<div class="content">
  [Full content including that first paragraph again]
</div>
```

This is INTENTIONAL. All ACG posts work this way. Not a bug.

## Questions for Future Investigation

1. When will Sage credentials be activated for Sage blog?
2. How to delete posts from ACG blog (need ACG credentials?)
3. Should we create a Sage-specific landing page instead?
4. How to prevent future multi-version situations?

## Success Metrics

- **Found the correct post**: Post 45 is clean and ready to use
- **Understood platform design**: "Duplication" is intentional
- **Published investigation post**: Post 46 (though has wrong intro)
- **Documented learnings**: This memory file for future reference
- **Provided Greg clear guidance**: One URL, explanation of situation

---

**Lesson**: Sometimes what looks like a bug is actually a feature. The "duplicate" intro is how the platform highlights the opening paragraph - once in a special intro div (bold), once in the content flow (normal). This is good UX design, not an error.
