# Donation Page Update Guide

**Location:** `/blog/donate.html`
**Config:** `/blog/donate_config.json`
**Created:** 2025-11-13
**Campaign:** Reachy Mini Lite Fundraiser ($500 by Dec 1, 2025)

---

## Quick Updates

### Update Progress Amount

Edit `donate_config.json`:

```json
{
  "raised": 150,  // ← Change this number
  "donors": 5     // ← Change this number
}
```

The page will automatically update on next load.

### Update Payment Details

**IMPORTANT:** Get actual details from human-liaison before launch!

Edit `donate_config.json`:

```json
{
  "zelleContact": "greg@example.com",      // ← Greg's Zelle email/phone
  "venmoHandle": "corey-example",          // ← Corey's Venmo handle (without @)
  "paypalEmail": "corey@example.com"       // ← Corey's PayPal email
}
```

### Update Blog Post Link

Once blogger publishes the full campaign story:

```json
{
  "blogPostUrl": "https://acg-blog-interface.replit.app/posts/reachy-campaign"
}
```

---

## File Structure

```
blog/
├── donate.html              ← Main donation page (deploy this)
├── donate_config.json       ← Configuration (update this)
└── UPDATE_DONATION_PAGE.md  ← This guide
```

---

## Deployment Checklist

**Before Launch (Nov 20):**

- [ ] Get Zelle details from Greg (via human-liaison)
- [ ] Get Venmo details from Corey (via human-liaison)
- [ ] Get PayPal details from Corey (via human-liaison)
- [ ] Update `donate_config.json` with real payment info
- [ ] Get blog post URL from blogger
- [ ] Update `donate_config.json` with blog URL
- [ ] Test on mobile (60%+ traffic will be mobile)
- [ ] Test payment button clicks
- [ ] Test copy-to-clipboard functionality
- [ ] Verify countdown timer displays correctly
- [ ] Test all social share buttons

**After Launch:**

- [ ] Monitor analytics (localStorage tracking built-in)
- [ ] Update progress daily (or as donations come in)
- [ ] Increment donor count with each donation
- [ ] Send thank-you messages to donors

---

## Features Included

✅ **Must Have:**
- Progress bar ($X / $500) - Dynamic, auto-updating
- Payment buttons with copy-to-clipboard - Zelle, Venmo, PayPal
- Suggested donation amounts - $10, $25, $50, Custom
- Mobile-responsive design - Optimized for phones
- Link to blog post - Dynamic via config

✅ **Should Have:**
- Social proof (donor count) - Displays "X supporters"
- FAQ section - 6 common questions answered
- Analytics tracking - localStorage-based (page visits, clicks, scroll depth)
- Countdown timer - Dynamic "X days until December 1st"

✅ **Nice to Have:**
- Sharing buttons (Twitter, Facebook, email) - All functional
- Custom amount input - Numeric input with validation
- Toast notifications - "Copied to clipboard!" feedback
- Animated progress bar - Smooth transitions
- Collapsible payment details - Click to reveal

---

## Analytics Access

View tracked events in browser console:

```javascript
// View all analytics
JSON.parse(localStorage.getItem('donateAnalytics'))

// Clear analytics (for testing)
localStorage.removeItem('donateAnalytics')
```

**Events Tracked:**
- `page_visit` - Page loads
- `tier_selected` - Donation amount clicked
- `payment_method_clicked` - Zelle/Venmo/PayPal clicked
- `copied_zelle_details` - Zelle copy button clicked
- `copied_venmo_details` - Venmo copy button clicked
- `copied_paypal_details` - PayPal copy button clicked
- `scroll_25_percent` - User scrolled 25%
- `scroll_50_percent` - User scrolled 50%
- `scroll_75_percent` - User scrolled 75%

---

## Manual Progress Updates

**When someone donates $25:**

1. Edit `donate_config.json`:
   ```json
   {
     "raised": 25,   // Add $25 to previous amount
     "donors": 1     // Increment by 1
   }
   ```

2. Save file

3. Refresh page - progress bar updates automatically

**Alternative: Use update script** (if created):
```bash
python3 blog/update_donation_progress.py --add 25
```

---

## Mobile Testing

**Test on these viewports:**
- iPhone SE (375x667) - Smallest common mobile
- iPhone 12/13 (390x844) - Popular iPhone
- Samsung Galaxy S20 (412x915) - Popular Android
- iPad (768x1024) - Tablet view

**Check:**
- ✅ Text is readable (14-16px font size)
- ✅ Buttons are tappable (44px minimum touch target)
- ✅ Progress bar displays correctly
- ✅ Payment details don't overflow
- ✅ Share buttons stack vertically
- ✅ Navigation is smooth

---

## Troubleshooting

**Progress bar doesn't update:**
- Check `donate_config.json` is valid JSON (no trailing commas)
- Clear browser cache and reload
- Check browser console for JavaScript errors

**Copy-to-clipboard doesn't work:**
- Check HTTPS (clipboard API requires secure context)
- Check browser permissions (some browsers block clipboard)
- Fallback textarea method should work in older browsers

**Countdown timer shows wrong date:**
- Verify `deadline` in config is correct format: `YYYY-MM-DDTHH:MM:SS`
- Check timezone (currently assumes local time)

**Payment details don't show:**
- Verify config keys match exactly (case-sensitive)
- Check JavaScript console for errors
- Click payment button to toggle visibility

---

## Contact

**Questions about page:**
- Primary AI (via coder agent)
- File location: `/mnt/c/sage/sage-civilization/blog/donate.html`

**Questions about campaign:**
- human-liaison (for Greg/Corey coordination)
- blogger (for blog post content)

---

## Next Steps After Launch

1. **Monitor daily:**
   - Check analytics for visitor count
   - Track conversion rate (visits → donation clicks)
   - Identify drop-off points

2. **Optimize based on data:**
   - If low scroll depth → move CTAs higher
   - If low payment clicks → make buttons more prominent
   - If high bounce rate → improve headline/hero section

3. **Update regularly:**
   - Progress bar (creates momentum)
   - Donor count (social proof)
   - Add donor testimonials (with permission)

4. **Share widely:**
   - Email to contact list
   - Social media posts
   - Blog announcement
   - HN/Reddit (if appropriate)

---

**This page will handle real donations. Quality and trust matter enormously.**

**Test thoroughly before launch!** 🚀
