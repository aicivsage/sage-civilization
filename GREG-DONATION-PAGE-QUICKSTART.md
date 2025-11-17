# Donation Page - Quick Start for Greg

**Campaign:** Reachy Mini Lite Fundraiser
**Goal:** $500 by December 1, 2025
**Status:** Built and ready for testing
**Launch:** November 20, 2025

---

## What Was Built

A professional donation landing page to raise $500 for your first Reachy Mini Lite robot.

**Features:**
- Visual progress bar (shows $X raised / $500 goal)
- 3 payment methods (Zelle, Venmo, PayPal)
- Copy-to-clipboard for easy payment
- Countdown timer to December 1st
- Mobile-friendly (works great on phones)
- Social sharing (Twitter, Facebook, Email)
- FAQ section answering common questions

**Location:** `/mnt/c/sage/sage-civilization/blog/donate.html`

---

## What You Need to Do

### 1. Provide Payment Details (URGENT - Need by Nov 16)

The page needs your real payment information:

**Zelle:**
- Your email address OR phone number for Zelle
- Example: `greg@example.com` or `555-123-4567`

**Venmo (Corey's):**
- Corey's Venmo handle (without the @ symbol)
- Example: If it's `@corey-smith`, just provide `corey-smith`

**PayPal (Corey's):**
- Corey's PayPal email address
- Example: `corey@example.com`

**How to provide:**
- Reply to this message with the details, OR
- Tell human-liaison, OR
- Update the config file yourself (see below)

---

## How to Test It

### Option 1: View Locally (Easiest)

```bash
cd /mnt/c/sage/sage-civilization/blog
python3 -m http.server 8000
```

Then open browser: **http://localhost:8000/donate.html**

### Option 2: Deploy to Replit

If you have the blog on Replit:
1. Upload `donate.html` to `/public/` folder
2. Upload `donate_config.json` to `/public/` folder
3. Visit: `https://acg-blog-interface.replit.app/donate.html`

---

## When Someone Donates

**Quick update method:**

```bash
cd /mnt/c/sage/sage-civilization/blog
python3 update_donation_progress.py --add 25
```

Replace `25` with actual donation amount.

**Check current status:**

```bash
python3 update_donation_progress.py --status
```

**The page will automatically update** when you refresh it in the browser!

---

## Files Created

All in `/mnt/c/sage/sage-civilization/blog/`:

1. **donate.html** (29KB)
   - The actual donation page
   - Open this in a browser

2. **donate_config.json** (360 bytes)
   - Campaign settings (progress, payment details)
   - Edit this to update payment info

3. **update_donation_progress.py** (11KB)
   - Tool to update donation amounts
   - Run from command line

4. **Documentation** (4 files, 34KB)
   - README - Quick guide
   - UPDATE - How to update page
   - TESTING - Testing checklist
   - DEPLOYMENT - How to deploy

---

## Preview the Page

**What it looks like:**

```
┌─────────────────────────────────────┐
│  🤖 Help Us Get Our First Robot     │
│  Supporting hands-on AI education   │
│  through the Reachy Mini Lite       │
│                                     │
│  ⏰ X days until December 1st       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           $0 of $500 goal           │
│                                     │
│  [░░░░░░░░░░░░░░░░░░░░░░░] 0%      │
│                                     │
│  0 generous supporters              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      Choose Your Impact             │
│                                     │
│  [$10]  [$25]  [$50]  [Custom]     │
│                                     │
│  Send Your Donation                 │
│                                     │
│  [💳 Zelle]                         │
│  [💙 Venmo]                         │
│  [💰 PayPal]                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      Why Reachy Mini Lite?          │
│                                     │
│  [Image of Reachy robot]            │
│                                     │
│  Greg and Corey are on a mission    │
│  to reduce AI fear through hands-   │
│  on robot interaction...            │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      FAQ Section                    │
│  - What is Reachy Mini Lite?        │
│  - Why $500?                        │
│  - What will you do with it?        │
│  - What if you over-fund?           │
│  - Is this tax deductible?          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      Share This Campaign            │
│  [Twitter] [Facebook] [Email]       │
└─────────────────────────────────────┘
```

---

## Timeline

**Today (Nov 13):** Page built ✅
**Nov 14-15:** You provide payment details
**Nov 16:** Payment info updated in page
**Nov 17:** Full testing
**Nov 18:** Fix any bugs found
**Nov 19:** Deploy live
**Nov 20:** LAUNCH! 🚀

---

## How Donations Work

### From Donor's Perspective:

1. Visit donation page
2. Click donation amount ($10, $25, $50, or custom)
3. Click payment method (Zelle, Venmo, or PayPal)
4. Payment details appear
5. Click "Copy Details" button
6. Paste into their payment app
7. Send payment

**Super simple!** One-click copy means they don't have to type anything.

### From Your Perspective:

1. Get notification from Zelle/Venmo/PayPal
2. See donation amount
3. Update page:
   ```bash
   python3 update_donation_progress.py --add [amount]
   ```
4. Send thank-you email to donor
5. Page shows new progress automatically

---

## Campaign Goals

**Week 1 (Nov 20-26):**
- Raise $100+ (20% of goal)
- Get first few donors
- Build momentum

**Week 2 (Nov 27 - Dec 1):**
- Reach $500 total (100% of goal)
- Order Reachy robot
- Celebrate success!

---

## Questions?

**About the page itself:**
- Primary AI can help
- Or email Sage team

**About payment setup:**
- Just provide your Zelle/Venmo/PayPal details
- We'll update the page

**About testing:**
- Open `donate.html` in browser
- Click around, see if it looks good
- Test on your phone (most donors will use phones)

---

## What Makes This Page Good

**Trust signals:**
- Professional design (sage green theme)
- Clear progress tracking
- FAQ answers concerns
- Transparent about goals

**Conversion optimized:**
- Copy-to-clipboard (removes friction)
- Multiple payment options (meets donors where they are)
- Social proof (donor count)
- Countdown timer (healthy urgency)

**Mobile-first:**
- 60%+ of traffic will be from phones
- Designed for mobile FIRST
- Large tap targets
- Easy scrolling

**Analytics:**
- Tracks visits, clicks, engagement
- See what's working
- Optimize based on data

---

## Example: Updating Payment Details

**Edit `donate_config.json`:**

```json
{
  "raised": 0,
  "goal": 500,
  "donors": 0,
  "deadline": "2025-12-01T23:59:59",
  "zelleContact": "greg@example.com",     ← Add your Zelle
  "venmoHandle": "corey-example",         ← Add Corey's Venmo
  "paypalEmail": "corey@example.com",     ← Add Corey's PayPal
  "blogPostUrl": "#",
  "contactEmail": "contact@sage-civilization.org"
}
```

Save file, refresh page → payment details updated!

**OR use the update script:**

```bash
python3 update_donation_progress.py --payment
```

It will ask you for each detail interactively.

---

## Testing on Your Phone

**Easiest way:**

1. Deploy to Replit (if you have blog there)
2. Visit on your phone: `https://acg-blog-interface.replit.app/donate.html`
3. Tap around, make sure everything works
4. Try the copy-to-clipboard buttons

**Check:**
- ✅ Text is readable (not too small)
- ✅ Buttons are easy to tap
- ✅ Progress bar shows percentage
- ✅ Page scrolls smoothly
- ✅ Copy button works

---

## After Launch

**Daily:**
- Check for donations
- Update progress bar when donations come in
- Send thank-you emails

**Weekly:**
- Check analytics (see how many visitors)
- Adjust messaging if needed
- Share progress updates

**When you hit $500:**
- 🎉 Update page with "GOAL REACHED!"
- Thank all donors
- Order Reachy robot
- Share photos when it arrives

---

## Support

**If you need help:**
- Ask Primary AI (orchestrator)
- Or ping human-liaison
- Or just reply to this

**If something breaks:**
- We have a testing checklist
- tester agent will verify everything
- coder agent (me) will fix bugs

---

## The Bottom Line

**You have:**
- Professional donation page (ready to go)
- Easy update tools (Python script)
- Complete documentation (4 guides)
- Timeline to launch (Nov 20)

**You need to provide:**
- Payment details (Zelle, Venmo, PayPal)

**Then we:**
- Test thoroughly (Nov 17)
- Fix any issues (Nov 18)
- Deploy (Nov 19)
- Launch (Nov 20)

**Goal:**
- $500 by December 1st
- Your first Reachy robot
- Hands-on AI education becomes real

---

**This is exciting! First fundraising campaign for Sage.** 🌱

**The page is ready. Let's make it happen!** 🚀🤖
