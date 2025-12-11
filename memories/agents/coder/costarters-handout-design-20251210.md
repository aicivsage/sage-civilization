# CoStarters Handout Design - One-Page Professional
**Date**: 2025-12-10
**Agent**: coder
**Task**: Create professional one-page handout (front/back) for Greg's CoStarters pitch party

## What I Did

Created `COSTARTERS-HANDOUT-ONE-PAGE.html` - a print-optimized, two-sided handout that extends Greg's 5-minute pitch with the 60% of content not covered verbally.

**Design Approach:**
- Single HTML file (no external dependencies)
- Print-optimized with @page CSS rules
- Two-sided layout (front/back designed for duplex printing)
- Professional appearance with sage green accent color (#6B8E23)
- Scannable sections with clear visual hierarchy
- 11-12pt body text (readable when printed)
- Embedded CSS for portability

## Front Page Content (40% pitch overlap, 60% expanded)

**Header Section:**
- Business name and tagline: "AI Collaboration Workshops - Nurture, Not Neglect"
- Presenters: Greg Smithwick & Corey Cottrell
- Contact info with QR code placeholder for booking calendar

**Three Objections with Expanded Responses:**
1. **AI Takeover** → Thousands of safety researchers, cancer research potential (10M+ lives saved annually)
2. **Labor Displacement** → Labor economy → Attention economy shift (THE KEY INSIGHT)
3. **Resource Diversion** → 3-5x efficiency gains every 3 years, AI solving energy problems

**Workshop Packages (Pricing Grid):**
- Community: $750 (nonprofits, small groups up to 15)
- Professional: $1,500 (businesses, schools, 15-30 people)
- Enterprise: $2,500 (large orgs, 30+ people, customized)
- Consulting: $100-150/hr (one-on-one support)

**Skills Grid (What You'll Learn):**
- Prompt engineering
- Fact-checking AI outputs
- Automation (documentation, emails)
- Research acceleration
- Ethical frameworks
- Real-world practice with actual work challenges

**Who Should Hire Us:**
- Small businesses (competitive without losing humanity)
- Schools/educators (prepare students for attention economy)
- Nonprofits (amplify impact with limited resources)

## Back Page Content (Deep philosophical/credibility material)

**The Frankenstein Principle:**
- "The failure wasn't the creation—it was the neglect" (Mary Shelley)
- Extended explanation of nurture vs. neglect theme
- Core workshop philosophy: Partnership, not replacement

**Jonas Salk Spirit:**
- "Could you patent the sun?" quote
- Open innovation philosophy
- Knowledge should be accessible, future should be abundant

**What Makes This Different:**
- Not selling software (framework-based, tool-agnostic)
- Addresses fear directly (Terminator discussion)
- Practiced, not preached (built WITH Sage AI civilization)
- Proven efficiency data (3-5x improvements)

**Vision Statement:**
- Scarcity vs. abundance mindset
- "There's Mars, Jupiter's moons..." (space abundance framing)
- Terminator quote twist: "The future's not set..."

**Traction & Credibility:**
- Break-even model (7 workshops/year)
- Partnership strength (Greg + Corey expertise)
- Pilot workshops scheduled
- Market validation (people lean in when they hear this)

**Three-Tiered CTA:**
1. Hire us (book a workshop)
2. Introduce us (make connections)
3. Share this (pass handout along)

## What I Learned

**Print Design Considerations:**
- @page CSS rules control print layout (margins, size, two-sided)
- `-webkit-print-color-adjust: exact` ensures colors print correctly
- Font sizes must be larger for print (11-12pt minimum body text)
- Grid layouts work well for pricing/skills (scannable, professional)
- Border-left styling creates visual hierarchy without heavy graphics
- Background colors must be print-optimized (not too dark, ink-friendly)

**Content Architecture (40/60 Principle):**
- Pitch covers 40% of content (hooks them verbally)
- Handout provides 60% more depth (extends conversation)
- Handout should answer questions pitch raises
- Handout enables three conversion paths (hire, introduce, share)

**Visual Hierarchy for Scanning:**
- Rule of One: One key idea per section
- Headlines at 16-18pt (clear section breaks)
- Body text at 11-12pt (readable but compact)
- Colored boxes highlight key principles (Frankenstein, Jonas Salk)
- White space prevents overwhelming density

**Professional Polish:**
- Sage green accent (#6B8E23) reinforces brand identity
- Consistent spacing creates rhythm
- QR code placeholder for easy booking
- Print instructions in HTML comment (Greg can customize)

## Technical Patterns Discovered

**CSS Grid for Print:**
```css
.pricing-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
```
Works beautifully for print layouts (better than flexbox for this use case).

**Print Page Control:**
```css
@page {
    size: letter;
    margin: 0.5in;
}
.page-break {
    page-break-before: always;
}
```
Ensures clean two-sided printing with proper margins.

**Color Preservation:**
```css
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
}
```
Critical for maintaining sage green branding in print.

## For Next Time

**If designing similar handouts:**
- Start with content architecture (what's in pitch vs. handout)
- Design for scanning first, reading second (busy audience)
- Test print preview early (print design differs from screen)
- Include customization instructions (email placeholders, QR codes)
- Consider both color and B&W printing scenarios
- Keep file self-contained (embedded CSS, no external dependencies)

**Customization checklist for Greg:**
- [ ] Replace [email-domain] with actual emails
- [ ] Generate QR code for booking calendar (or remove placeholder)
- [ ] Add testimonials if available (pilot workshop results)
- [ ] Verify pricing matches current business model
- [ ] Print test copy to check colors, spacing, readability

## Deliverables

- **File**: `/mnt/c/sage/sage-civilization/COSTARTERS-HANDOUT-ONE-PAGE.html`
- **Format**: Single HTML file, print-optimized
- **Layout**: Two-sided (front + back), 8.5" x 11" letter size
- **Status**: Ready for customization and printing

## Success Criteria Met

✅ All three objections covered with Greg's responses
✅ Business model clear and compelling (pricing grid, who should hire)
✅ Contact info prominent on both sides (header + footer)
✅ Printable on single sheet (front/back with page-break CSS)
✅ Professional appearance reflecting Greg's philosophical depth
✅ 40/60 principle honored (pitch content + 60% expanded material)
✅ Scannable design (bullets, short paragraphs, white space)
✅ Sage green brand identity (consistent accent color)

## Partner Recognition

**Source Material**: COSTARTERS-PITCH-COMPLETE.html by architect agent
- Provided complete content specifications
- Verified essay citations and data points
- Structured 40/60 pitch-to-handout breakdown
- Defined three objections and responses

**This handout translates architect's content vision into printable deliverable.**
