# Fundraising Campaign Tracking Spreadsheet
**Campaign**: Reachy Mini Lite Robot
**Goal**: $500 by December 1, 2025
**Duration**: November 20 - December 1 (12 days active)

---

## SPREADSHEET STRUCTURE

### Sheet 1: Contact List & Outreach Tracking

| Column | Header | Data Type | Purpose |
|--------|--------|-----------|---------|
| A | Contact Name | Text | Full name of contact |
| B | Email Address | Email | Verified email address |
| C | Tier | Dropdown | 1 (Close), 2 (Professional), 3 (Community), W (Wild Card) |
| D | Relationship Type | Dropdown | Family, Friend, Colleague, Team Member, LinkedIn, Community, Other |
| E | Relationship Notes | Text | Brief context (how you know them, why likely to donate) |
| F | Outreach Date | Date | When email was sent |
| G | Template Used | Dropdown | A (Close Friends), B (Professional), C (Community), Custom |
| H | Customization Notes | Text | What you personalized in email |
| I | Email Opened? | Checkbox/Yes/No | If tracking available |
| J | Response Date | Date | When they replied (if applicable) |
| K | Response Type | Dropdown | Donated, Question, Decline, No Response |
| L | Donated? | Checkbox | YES/NO |
| M | Donation Amount | Currency | $0 if not donated |
| N | Payment Method | Dropdown | Venmo, PayPal, Zelle, Other |
| O | Thank-You Sent? | Checkbox | YES/NO |
| P | Thank-You Date | Date | When thank-you email sent |
| Q | Follow-Up Needed? | Checkbox | If requires additional action |
| R | Notes | Text | Questions asked, concerns, follow-up plans |

**Total rows needed**: 60-70 (50 contacts + buffer)

---

### Sheet 2: Daily Campaign Progress

| Date | Emails Sent (Day) | Emails Sent (Cumulative) | Responses Received | Donations Received | Amount Raised (Day) | Amount Raised (Cumulative) | % of Goal | Days Remaining | Notes |
|------|-------------------|-------------------------|-------------------|-------------------|---------------------|---------------------------|-----------|----------------|-------|
| Nov 20 | 10 | 10 | 2 | 1 | $25 | $25 | 5% | 11 | Launch day - Tier 1 batch 1 |
| Nov 21 | 5 | 15 | 4 | 3 | $65 | $90 | 18% | 10 | Tier 1 batch 2 |
| Nov 22 | 10 | 25 | 6 | 4 | $80 | $170 | 34% | 9 | Tier 2 batch 1 |
| Nov 23 | 10 | 35 | 3 | 2 | $35 | $205 | 41% | 8 | Tier 2 batch 2 |
| Nov 24 | 15 | 50 | 5 | 3 | $45 | $250 | 50% | 7 | Tier 3 + blog launch |
| Nov 25 | 5 | 55 | 2 | 1 | $20 | $270 | 54% | 6 | Follow-ups begin |
| Nov 26 | 0 | 55 | 4 | 2 | $40 | $310 | 62% | 5 | Delayed responses coming in |
| Nov 27 | 5 | 60 | 3 | 2 | $35 | $345 | 69% | 4 | Final push messaging |
| Nov 28 | 0 | 60 | 2 | 2 | $50 | $395 | 79% | 3 | Close to goal! |
| Nov 29 | 3 | 63 | 1 | 1 | $30 | $425 | 85% | 2 | Extended asks |
| Nov 30 | 0 | 63 | 2 | 2 | $60 | $485 | 97% | 1 | Final day push |
| Dec 1 | 0 | 63 | 1 | 1 | $25 | $510 | 102% | 0 | GOAL MET! |

**Note**: This is a PROJECTED timeline - actual will vary

---

### Sheet 3: Donation Details

| Donor Name | Tier | Donation Amount | Date Received | Payment Method | Running Total | % of Goal | Thank-You Sent? | Public Acknowledgment OK? | Quote/Message |
|------------|------|-----------------|---------------|----------------|---------------|-----------|-----------------|--------------------------|---------------|
| [Example] | 1 | $25 | Nov 20 | Venmo | $25 | 5% | ✓ | Yes | "Love what you're building!" |
| [Example] | 1 | $50 | Nov 20 | PayPal | $75 | 15% | ✓ | No | [No public mention requested] |
| [Example] | 2 | $15 | Nov 21 | Zelle | $90 | 18% | ✓ | Yes | [No message provided] |
| [Continue...] | | | | | | | | | |

**Columns explained**:
- **Public Acknowledgment OK?**: Permission to mention name on blog/social
- **Quote/Message**: Any message they included with donation (for sharing with permission)
- **Running Total**: Cumulative total after each donation

---

### Sheet 4: Summary Statistics

**Campaign Overview**:
- Start Date: November 20, 2025
- End Date: December 1, 2025
- Duration: 12 days
- Goal: $500
- Stretch Goal: $600

**Contact Statistics**:
- Total Contacts: [Auto-count from Sheet 1]
- Tier 1 (Close): [Auto-count]
- Tier 2 (Professional): [Auto-count]
- Tier 3 (Community): [Auto-count]
- Wild Card: [Auto-count]

**Outreach Statistics**:
- Emails Sent: [Auto-count where Outreach Date not empty]
- Emails Opened: [Auto-count where Email Opened = Yes]
- Open Rate: [Opened / Sent * 100]%
- Responses Received: [Auto-count where Response Type not empty]
- Response Rate: [Responses / Sent * 100]%

**Donation Statistics**:
- Total Donors: [Auto-count where Donated = Yes]
- Total Raised: [Auto-sum of Donation Amount]
- % of Goal: [Total Raised / Goal * 100]%
- Average Donation: [Total Raised / Total Donors]
- Median Donation: [Calculated median]
- Conversion Rate: [Donors / Emails Sent * 100]%

**By Tier Performance**:

| Tier | Contacts | Emails Sent | Responses | Donors | Amount Raised | Avg Donation | Conversion Rate |
|------|----------|-------------|-----------|--------|---------------|--------------|-----------------|
| 1 | [count] | [count] | [count] | [count] | $[sum] | $[avg] | [%] |
| 2 | [count] | [count] | [count] | [count] | $[sum] | $[avg] | [%] |
| 3 | [count] | [count] | [count] | [count] | $[sum] | $[avg] | [%] |
| W | [count] | [count] | [count] | [count] | $[sum] | $[avg] | [%] |
| **TOTAL** | [sum] | [sum] | [sum] | [sum] | $[sum] | $[avg] | [%] |

**Payment Method Breakdown**:
- Venmo: [count] donations, $[sum]
- PayPal: [count] donations, $[sum]
- Zelle: [count] donations, $[sum]
- Other: [count] donations, $[sum]

**Response Type Breakdown**:
- Donated: [count] ([%])
- Asked Question: [count] ([%])
- Declined: [count] ([%])
- No Response: [count] ([%])

**Timeline Analysis**:
- Fastest donation: [time from email send to donation]
- Average time to donate: [calculated average]
- Peak donation day: [date with most donations]

---

### Sheet 5: Questions & Objections Log

| Date | Source | Question/Objection | How We Responded | Result | Category |
|------|--------|-------------------|------------------|--------|----------|
| Nov 20 | [Name] | "Why not buy it yourself?" | [Response given] | Donated $15 | Financial |
| Nov 21 | [Name] | "Is this legitimate?" | [Response given] | No donation yet | Trust |
| Nov 22 | [Name] | "What's the business model?" | [Response given] | Donated $25 | Business |
| [Continue...] | | | | | |

**Categories**: Financial, Trust, Business, Technical, Mission, Timeline, Other

**Purpose**: Track patterns in questions/objections to:
1. Improve messaging for future outreach
2. Add FAQ section to blog post
3. Prepare better responses
4. Identify common concerns

---

### Sheet 6: Follow-Up Schedule

| Contact Name | Tier | Original Email Date | Follow-Up Due Date | Follow-Up Sent? | Follow-Up Date | Second Follow-Up Needed? | Notes |
|--------------|------|-------------------|-------------------|-----------------|----------------|------------------------|-------|
| [Example] | 1 | Nov 20 | Nov 25 | Yes | Nov 25 | No | Responded after follow-up |
| [Example] | 2 | Nov 21 | Nov 28 | No | | Yes | Haven't heard back |
| [Continue...] | | | | | | | |

**Follow-up rules**:
- Tier 1: Follow up after 5 days if no response
- Tier 2: Follow up after 7 days if no response
- Tier 3: No individual follow-ups (blog updates only)
- Second follow-up: Only for Tier 1, only if close to goal and need final push

---

## GOOGLE SHEETS FORMULAS (If Using Spreadsheet Software)

### Useful Formulas

**Total Raised** (Sheet 4):
```
=SUM(Sheet1!M:M)
```

**Conversion Rate** (Sheet 4):
```
=COUNTIF(Sheet1!L:L,"Yes")/COUNTA(Sheet1!F:F)*100
```

**Average Donation** (Sheet 4):
```
=AVERAGE(Sheet1!M:M) [where M > 0]
```

**Tier 1 Statistics** (Sheet 4):
```
=COUNTIFS(Sheet1!C:C,"1",Sheet1!L:L,"Yes")  [for Tier 1 donors]
=SUMIFS(Sheet1!M:M,Sheet1!C:C,"1")  [for Tier 1 total raised]
```

**Progress Bar** (Visual):
```
=REPT("█",INT(Total_Raised/Goal*20))  [20-character progress bar]
```

**Days Remaining** (Sheet 2):
```
=MAX(0,DATE(2025,12,1)-TODAY())
```

---

## DAILY MAINTENANCE CHECKLIST

### Every Morning (8am)

- [ ] Check all payment accounts (Venmo, PayPal, Zelle) for overnight donations
- [ ] Update Sheet 3 (Donation Details) with any new donations
- [ ] Update Sheet 2 (Daily Progress) with yesterday's totals
- [ ] Check emails for responses
- [ ] Update Sheet 1 (Contact List) with response statuses
- [ ] Send thank-you emails to any new donors (within 24 hours)
- [ ] Review follow-up schedule - any follow-ups due today?

### Every Evening (6pm)

- [ ] Final check of payment accounts for today's donations
- [ ] Update all sheets with end-of-day data
- [ ] Calculate today's statistics (donations, responses, conversion rate)
- [ ] Review tomorrow's outreach plan (who gets emails?)
- [ ] Draft any needed follow-up emails for tomorrow
- [ ] Update blog progress tracker (if applicable)
- [ ] Post social media update if significant progress made

### Weekly Review (Sundays)

- [ ] Analyze week's performance (what worked, what didn't)
- [ ] Adjust strategy if needed (messaging, timing, follow-ups)
- [ ] Review questions/objections log for patterns
- [ ] Plan next week's outreach and follow-ups
- [ ] Update Greg on status (if he's not checking spreadsheet directly)

---

## RED FLAGS TO WATCH FOR

**Underperformance Indicators**:
- Open rate <40% for Tier 1 → Emails going to spam?
- Conversion rate <30% for Tier 1 → Messaging not resonating?
- No donations in 48 hours → Need to increase outreach urgency?
- High "decline" responses → Ask is too high? Mission unclear?

**Overperformance Indicators**:
- Goal hit before November 27 → Consider stretch goal?
- Average donation >$30 → Can ask for slightly more?
- High share rate on social → Amplify public content?

---

## BACKUP TRACKING (If Spreadsheet Fails)

### Manual Log Format

```
DATE: November 20, 2025

OUTREACH:
- Sent to: [Name 1], [Name 2], [Name 3]... (10 total)
- Templates: 8x Template A, 2x Custom

RESPONSES:
- [Name 1]: Donated $25 via Venmo ✓
- [Name 2]: Asked question about timeline - responded
- [Name 3]: No response yet

DONATIONS TODAY: 1 donor, $25 raised
CUMULATIVE: 1 donor, $25 raised (5% of goal)

NOTES:
- [Any patterns, concerns, observations]

TOMORROW'S PLAN:
- Send Tier 1 batch 2 (5 people)
- Follow up with [Name 2] after answering question
```

---

## EXPORT & SHARING

**Who needs access**:
- Greg (full access, can edit)
- Corey (view access for business context)
- Human-liaison agent (tracking for updates)

**Privacy considerations**:
- DO NOT share donor names/emails publicly without permission
- DO share aggregate statistics (total raised, donor count)
- DO share anonymous quotes/messages if relevant

**Backup frequency**:
- Daily export to CSV (prevent data loss)
- Weekly snapshot for records
- Final export after campaign ends for analysis

---

## POST-CAMPAIGN ANALYSIS (After December 1)

### Questions to Answer

1. **What was our final conversion rate by tier?**
   - Did Tier 1 perform as expected (70-80%)?
   - Did any tier dramatically over/underperform?

2. **What messaging resonated most?**
   - Review questions/objections log
   - Which template got best response?
   - What language did donors respond to?

3. **What timing worked best?**
   - Day of week with most donations?
   - Time from email send to donation?
   - Follow-up effectiveness?

4. **What would we do differently next time?**
   - Start sooner?
   - Different ask amounts?
   - More/less personalization?
   - Different payment methods?

5. **Who were our champions?**
   - Who donated most?
   - Who shared most?
   - Who connected us with others?
   - How do we thank them extraordinarily?

6. **What surprised us?**
   - Unexpected donors?
   - Unexpected objections?
   - Unexpected outcomes?

---

## DELIVERABLE STATUS

✅ **Sheet 1**: Contact tracking structure defined
✅ **Sheet 2**: Daily progress tracking template
✅ **Sheet 3**: Donation details logging
✅ **Sheet 4**: Summary statistics formulas
✅ **Sheet 5**: Questions/objections tracking
✅ **Sheet 6**: Follow-up scheduling system
✅ **Maintenance**: Daily/weekly checklist provided
✅ **Analysis**: Post-campaign review framework

**Next Steps**:
1. Create actual Google Sheet or Excel file with these structures
2. Populate Sheet 1 with Greg's contact list (from donor expansion document)
3. Set up formulas for automatic calculations
4. Share with Greg for input and tracking access

**Status**: Tracking spreadsheet structure complete ✅
