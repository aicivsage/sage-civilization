# Fundraising Campaign Tracking Spreadsheet
**Purpose**: Track all campaign activity, donations, and outreach in organized system
**Tool**: Google Sheets (recommended) or Excel
**Setup time**: 15-20 minutes
**Maintenance**: 5-10 minutes daily during campaign

---

## SHEET 1: CONTACT LIST & OUTREACH TRACKING

**Purpose**: Master list of all contacts, outreach status, response tracking

### Column Structure (18 columns)

| Column | Header | Data Type | Example | Purpose |
|--------|--------|-----------|---------|---------|
| A | Contact ID | Auto-number | 1, 2, 3... | Unique identifier |
| B | Name | Text | Kelly Smith | Who they are |
| C | Tier | Dropdown | 1, 2, 3, W | Audience segment |
| D | Email | Text | kelly@example.com | Contact info |
| E | Relationship | Text | Priority contact | How you know them |
| F | Suggested Ask | Currency | $25 | Recommended donation |
| G | Email Sent Date | Date | 11/20/2025 | When outreach happened |
| H | Email Sent Time | Time | 9:00 AM | Time of day (for optimization) |
| I | Email Template Used | Dropdown | A, B, C | Which version |
| J | Email Opened? | Dropdown | Yes, No, Unknown | Tracking (if available) |
| K | Reply Received? | Dropdown | Yes, No | Did they respond |
| L | Reply Date | Date | 11/21/2025 | When they replied |
| M | Reply Type | Dropdown | Donated, Question, Declined, No Response | Classification |
| N | Donated? | Dropdown | Yes, No, Pending | Outcome |
| O | Donation Amount | Currency | $25.00 | How much (if donated) |
| P | Payment Method | Dropdown | Venmo, Zelle, PayPal, Other | How they paid |
| Q | Thank You Sent | Dropdown | Yes, No, N/A | Follow-up tracking |
| R | Notes | Text | Enthusiastic reply, asked questions about... | Qualitative data |

### Dropdown Options Setup

**Tier**: 1, 2, 3, W (Wild Card)
**Template Used**: A (Close Friends), B (Professional), C (Community)
**Email Opened**: Yes, No, Unknown
**Reply Received**: Yes, No
**Reply Type**: Donated, Question, Declined, No Response, Maybe Later
**Donated**: Yes, No, Pending
**Payment Method**: Venmo, Zelle, PayPal, Direct (other)
**Thank You Sent**: Yes, No, N/A

### Conditional Formatting Rules

**Row highlighting**:
- **Green**: Donated = Yes (success!)
- **Yellow**: Reply Type = Question (needs response)
- **Orange**: Email Sent Date > 7 days ago AND Donated = No (follow-up needed)
- **Red**: Reply Type = Declined (respectful record, don't re-contact)

### Sample Rows

| ID | Name | Tier | Email | Relationship | Suggested Ask | Sent Date | Template | Donated? | Amount | Thank You |
|----|------|------|-------|--------------|---------------|-----------|----------|----------|--------|-----------|
| 1 | Kelly Smith | 1 | kelly@kellysmithhome.com | Priority contact | $25 | 11/20/2025 | A | Yes | $30.00 | Yes |
| 2 | Chris Tuttle | 2 | ramsus@gmail.com | AI teacher | $20 | 11/22/2025 | B | Yes | $25.00 | Yes |
| 3 | Angel | 2 | angeltude371@gmail.com | Priority contact | $15 | 11/22/2025 | B | No | - | N/A |

---

## SHEET 2: DAILY PROGRESS DASHBOARD

**Purpose**: Track campaign momentum day-by-day

### Column Structure (8 columns)

| Date | Emails Sent Today | Emails Sent Cumulative | Donations Received Today | Daily Donation Total | Running Total | % of $500 Goal | Donor Count | Notes |
|------|-------------------|------------------------|--------------------------|----------------------|---------------|----------------|-------------|-------|
| 11/20/2025 | 10 | 10 | 3 | $60.00 | $60.00 | 12% | 3 | Launch day - Tier 1 batch 1 |
| 11/21/2025 | 5 | 15 | 2 | $45.00 | $105.00 | 21% | 5 | Tier 1 batch 2 |
| 11/22/2025 | 10 | 25 | 4 | $70.00 | $175.00 | 35% | 9 | Tier 2 starts |

### Summary Cells (Above table)

**Campaign Overview** (Manually updated):
- **Start Date**: 11/20/2025
- **End Date**: 12/1/2025
- **Days Elapsed**: =TODAY()-StartDate
- **Days Remaining**: =EndDate-TODAY()
- **Goal**: $500

**Current Status** (Formula-driven):
- **Total Raised**: =SUM(Running Total column)
- **Total Donors**: =MAX(Donor Count column)
- **Average Donation**: =Total Raised / Total Donors
- **Daily Average**: =Total Raised / Days Elapsed
- **Projected Final Total**: =Daily Average * Total Campaign Days

### Charts to Create

**Chart 1: Progress to Goal**
- Type: Gauge or horizontal bar
- Shows: $X of $500 (visual percentage)
- Updates: Automatically from Running Total

**Chart 2: Daily Donations**
- Type: Line chart
- X-axis: Date
- Y-axis: Daily Donation Total
- Shows: Momentum over time

**Chart 3: Cumulative Progress**
- Type: Area chart
- X-axis: Date
- Y-axis: Running Total
- Goal line: Horizontal line at $500

---

## SHEET 3: DONATION DETAILS

**Purpose**: Record every donation with full context

### Column Structure (10 columns)

| Donation ID | Date Received | Time Received | Donor Name | Tier | Amount | Payment Method | Thank You Sent | Thank You Date | Notes/Quote |
|-------------|---------------|---------------|------------|------|--------|----------------|----------------|----------------|-------------|
| 1 | 11/20/2025 | 10:30 AM | Kelly Smith | 1 | $30.00 | Venmo | Yes | 11/20/2025 | "Happy to help!" |
| 2 | 11/20/2025 | 2:15 PM | Chris Tuttle | 2 | $25.00 | PayPal | Yes | 11/20/2025 | Enthusiastic support |
| 3 | 11/21/2025 | 9:00 AM | Anonymous | 3 | $10.00 | Zelle | Yes | 11/21/2025 | Blog reader |

### Summary Calculations

**Above table, create summary cells**:

**By Tier**:
- Tier 1 Total: =SUMIF(Tier column, "1", Amount column)
- Tier 2 Total: =SUMIF(Tier column, "2", Amount column)
- Tier 3 Total: =SUMIF(Tier column, "3", Amount column)
- Wild Card Total: =SUMIF(Tier column, "W", Amount column)

**By Payment Method**:
- Venmo Total: =SUMIF(Payment Method column, "Venmo", Amount column)
- Zelle Total: =SUMIF(Payment Method column, "Zelle", Amount column)
- PayPal Total: =SUMIF(Payment Method column, "PayPal", Amount column)

**Donation Stats**:
- Largest Donation: =MAX(Amount column)
- Smallest Donation: =MIN(Amount column)
- Average Donation: =AVERAGE(Amount column)
- Median Donation: =MEDIAN(Amount column)

### Chart: Donations by Tier

- Type: Pie chart
- Shows: Tier 1 vs Tier 2 vs Tier 3 vs Wild Card
- Purpose: Understand which audience segment performed best

---

## SHEET 4: FOLLOW-UP SCHEDULE

**Purpose**: Track who needs follow-up emails and when

### Column Structure (7 columns)

| Contact Name | Tier | Original Send Date | Days Since Send | Follow-Up Needed? | Follow-Up Sent | Follow-Up Result |
|--------------|------|--------------------|-----------------|--------------------|----------------|------------------|
| Angel | 2 | 11/22/2025 | 5 | Yes (>5 days no reply) | 11/27/2025 | Donated $15 |
| Kodi | 2 | 11/22/2025 | 5 | Yes (>5 days no reply) | - | Pending |

### Conditional Formatting

**Yellow highlight**: Days Since Send >= 5 AND Follow-Up Needed = Yes AND Follow-Up Sent = blank
**Purpose**: Visual reminder of who needs gentle follow-up

### Formula for "Days Since Send"

`=TODAY() - [Original Send Date]`

### Formula for "Follow-Up Needed?"

`=IF(AND([Days Since Send]>=5, [Donated?]="No", [Reply Type]<>"Declined"), "Yes", "No")`

---

## SHEET 5: QUESTIONS & OBJECTIONS LOG

**Purpose**: Track patterns in questions/concerns to improve messaging

### Column Structure (6 columns)

| Date | Contact Name | Question/Objection | Your Response | Resolution | Pattern Tag |
|------|--------------|-------------------|---------------|------------|-------------|
| 11/21 | [Name] | "Why not just buy it yourself?" | Budget explanation | Donated $20 | Financial concern |
| 11/22 | [Name] | "Is this legit?" | Transparency details | Still considering | Trust/legitimacy |
| 11/23 | [Name] | "What if you don't hit goal?" | Explained backup plans | Donated $15 | Outcome concern |

### Pattern Tags (Dropdown)

- Financial concern
- Trust/legitimacy
- Outcome concern
- Technical question
- Mission alignment
- Timing/urgency
- Other

### Summary: Question Frequency

**Above table, count occurrences**:
- Financial concerns: =COUNTIF(Pattern Tag, "Financial concern")
- Trust questions: =COUNTIF(Pattern Tag, "Trust/legitimacy")
- Outcome questions: =COUNTIF(Pattern Tag, "Outcome concern")

**Why this matters**: If 50% of questions are about trust, you need to emphasize transparency more. If 30% are about outcome, you need clearer backup plans in messaging.

---

## SHEET 6: SUMMARY & ANALYTICS

**Purpose**: High-level campaign performance metrics

### Section 1: Goal Progress

| Metric | Value | Formula |
|--------|-------|---------|
| Goal | $500 | Manual entry |
| Raised | $XXX | =SUM(Sheet3!Amount) |
| Remaining | $XXX | =Goal - Raised |
| % Complete | XX% | =Raised / Goal |
| Days Elapsed | X | =TODAY() - Campaign Start |
| Days Remaining | X | =Campaign End - TODAY() |
| Daily Average | $XX | =Raised / Days Elapsed |
| Projected Total | $XXX | =Daily Average * Total Campaign Days |
| On Track? | YES/NO | =IF(Projected Total >= Goal, "YES", "NO") |

### Section 2: Donor Metrics

| Metric | Value | Formula |
|--------|-------|---------|
| Total Donors | XX | =COUNTA(Sheet3!Donor Name) |
| Average Donation | $XX | =AVERAGE(Sheet3!Amount) |
| Median Donation | $XX | =MEDIAN(Sheet3!Amount) |
| Largest Donation | $XX | =MAX(Sheet3!Amount) |
| Smallest Donation | $XX | =MIN(Sheet3!Amount) |

### Section 3: Tier Performance

| Tier | Contacts | Emails Sent | Donations | Conversion % | Total Raised | Avg Donation |
|------|----------|-------------|-----------|--------------|--------------|--------------|
| 1 | XX | XX | XX | XX% | $XXX | $XX |
| 2 | XX | XX | XX | XX% | $XXX | $XX |
| 3 | XX | XX | XX | XX% | $XXX | $XX |
| W | XX | XX | XX | XX% | $XXX | $XX |

**Formulas**:
- Contacts: =COUNTIF(Sheet1!Tier, "1")
- Emails Sent: =COUNTIF(Sheet1!Email Sent Date, "<>"&"") for each tier
- Donations: =COUNTIF(Sheet1!Donated?, "Yes") for each tier
- Conversion %: =Donations / Emails Sent
- Total Raised: =SUMIF(Sheet3!Tier, "1", Sheet3!Amount)
- Avg Donation: =AVERAGEIF(Sheet3!Tier, "1", Sheet3!Amount)

### Section 4: Timeline Projections

**Three scenarios based on current performance**:

| Scenario | Assumption | Projected Total | Gap to Goal | Action Needed |
|----------|------------|-----------------|-------------|---------------|
| Conservative | Current daily avg continues | $XXX | $XXX | Extend timeline / Plan Phase 2 |
| Realistic | 20% increase in daily avg | $XXX | $XXX | Final push messaging |
| Optimistic | 50% increase in final 3 days | $XXX | +$XXX | Victory lap / Stretch goal |

### Section 5: Payment Method Analysis

| Method | Count | Total | % of Total |
|--------|-------|-------|------------|
| Venmo | XX | $XXX | XX% |
| Zelle | XX | $XXX | XX% |
| PayPal | XX | $XXX | XX% |
| Other | XX | $XXX | XX% |

**Why this matters**: Shows which payment methods are most popular (optimize future campaigns)

---

## DAILY MAINTENANCE CHECKLIST

**Every morning during campaign (5-10 minutes)**:

### Step 1: Update Donation Details (Sheet 3)
- [ ] Check Venmo for new donations
- [ ] Check Zelle for new donations
- [ ] Check PayPal for new donations
- [ ] Record each donation (date, time, donor, amount, method)
- [ ] Flag any anonymous donations

### Step 2: Update Contact List (Sheet 1)
- [ ] Mark donations as "Yes" for corresponding contacts
- [ ] Update donation amounts
- [ ] Update "Reply Received" and "Reply Type" for any new responses
- [ ] Add notes for any qualitative feedback

### Step 3: Update Daily Progress (Sheet 2)
- [ ] Add new row for today's date
- [ ] Record emails sent today
- [ ] Record donations received today
- [ ] Calculate running totals
- [ ] Add notes about campaign activity

### Step 4: Send Thank-You Emails
- [ ] Identify all donations from yesterday
- [ ] Send personal thank-you to each donor
- [ ] Mark "Thank You Sent" = Yes and add date
- [ ] Include current campaign status in thank-you

### Step 5: Identify Follow-Ups Needed (Sheet 4)
- [ ] Check who's been contacted 5-7 days ago
- [ ] Filter for no reply AND no donation AND not declined
- [ ] Send gentle follow-up emails
- [ ] Mark "Follow-Up Sent" with date

### Step 6: Review Analytics (Sheet 6)
- [ ] Check "On Track?" status
- [ ] Review tier conversion rates
- [ ] Identify underperforming segments
- [ ] Adjust outreach strategy if needed

### Step 7: Log Questions/Objections (Sheet 5)
- [ ] Add any new questions from email replies
- [ ] Document your responses
- [ ] Tag patterns
- [ ] Review common concerns (update FAQ if needed)

**Total time: 5-10 minutes if daily, 30+ minutes if you skip days**

---

## AUTOMATED FEATURES (Optional - Requires Setup)

### Google Sheets Automation (Google Apps Script)

**Feature 1: Daily Email Summary**
- Script sends you email every morning with:
  - Yesterday's donations (count, total)
  - Campaign progress (% to goal)
  - Follow-ups needed today
- **Setup**: Apps Script → Daily trigger → Email yourself

**Feature 2: Conditional Email Alerts**
- Script alerts you when:
  - Single donation >$50 (celebrate major donor!)
  - Campaign crosses 25%, 50%, 75%, 90% thresholds
  - Follow-up needed (5 days no response)
- **Setup**: Apps Script → Hourly trigger → Check conditions

**Feature 3: Auto-Update Running Totals**
- Formula refreshes automatically when new donation added
- No manual calculation needed
- **Setup**: Already built-in with formulas

### Integration with Payment Apps (Advanced)

**If you want to auto-populate donations** (saves manual entry):
- Venmo: Export transaction CSV → Import to Sheet 3
- Zelle: Bank CSV export → Filter for campaign → Import
- PayPal: Export transactions → Import to Sheet 3

**Caution**: Manual verification still recommended (ensure campaign donations vs other transactions)

---

## EXPORT & SHARING

### Who Needs Access?

**Greg (Full edit access)**:
- Update donations as they arrive
- Send follow-ups
- Track progress

**Sage AI (View-only access)**:
- Monitor campaign performance
- Generate daily status reports
- Identify patterns

**Donors (No access, but receive reports)**:
- Email updates from exported data
- Progress screenshots
- Final campaign report

### Export Options

**PDF Report** (for donors):
- Sheet 6 (Summary & Analytics)
- Export as PDF
- Email to all donors weekly

**CSV Backup** (for safety):
- Export all sheets
- Save locally
- Backup to cloud storage

---

## SAMPLE FORMULAS (Copy-Paste Ready)

### Sheet 1: Contact List

**Count emails sent**:
```
=COUNTA(G2:G100)
```

**Count donations received**:
```
=COUNTIF(N2:N100,"Yes")
```

**Total raised from this sheet**:
```
=SUMIF(N2:N100,"Yes",O2:O100)
```

### Sheet 2: Daily Progress

**Cumulative emails sent**:
```
=SUM($B$2:B2)
```
(Drag down - creates running total)

**Cumulative donations**:
```
=SUM($E$2:E2)
```

**Percent of goal**:
```
=E2/$B$1
```
(Format as percentage)

### Sheet 3: Donation Details

**Tier 1 total**:
```
=SUMIF(E2:E100,"1",F2:F100)
```

**Average donation**:
```
=AVERAGE(F2:F100)
```

**Donor count**:
```
=COUNTA(D2:D100)
```

### Sheet 6: Summary & Analytics

**On track calculation**:
```
=IF((B2/B6)*B7>=B1,"YES - Projected: "&TEXT((B2/B6)*B7,"$0"),"NO - Projected: "&TEXT((B2/B6)*B7,"$0"))
```

**Tier conversion rate**:
```
=(Donations from tier / Emails sent to tier)
```

---

## TROUBLESHOOTING

### Problem: "I forgot to track a donation"

**Solution**:
1. Add to Sheet 3 (Donation Details) with best-guess date
2. Update Sheet 1 (Contact List) to mark donor
3. Note in "Notes" column: "Added retroactively"
4. Send thank-you email immediately (apologize for delay)

### Problem: "Formulas aren't updating"

**Solution**:
1. Check if calculation is set to "Automatic" (File → Settings)
2. Press Ctrl+Shift+F9 (recalculate all)
3. Verify cell references haven't shifted

### Problem: "I don't know if email was opened"

**Solution**:
- Mark as "Unknown" unless you have tracking
- Most personal emails don't have read receipts
- Focus on "Reply Received?" (more actionable)

### Problem: "Someone donated but I don't know who"

**Solution**:
1. Record as "Anonymous" in Sheet 3
2. Note payment method and amount
3. Send thank-you to payment app handle (if visible)
4. Don't stress - anonymous donations still count!

---

## POST-CAMPAIGN USE

**After December 1st, this spreadsheet becomes**:

### Historical Record
- Archive of campaign performance
- Donor list for future campaigns
- Lessons learned for next fundraising

### Donor Management System
- Who to invite to first demo
- Who gets priority rental access
- Who to update on Reachy arrival/progress

### Analytics for Improvement
- Which tier performed best?
- Which messaging worked?
- What objections were most common?
- What would you do differently?

**KEEP THIS SPREADSHEET FOREVER** - it's your campaign playbook for future fundraising.

---

## SETUP INSTRUCTIONS (Step-by-Step)

### 1. Create Google Sheet
- Go to sheets.google.com
- Create new spreadsheet
- Name: "Reachy Fundraising Campaign - Nov 2025"

### 2. Create 6 Sheets (tabs at bottom)
- Sheet 1: Contact List & Outreach
- Sheet 2: Daily Progress Dashboard
- Sheet 3: Donation Details
- Sheet 4: Follow-Up Schedule
- Sheet 5: Questions & Objections
- Sheet 6: Summary & Analytics

### 3. Set Up Column Headers (Each Sheet)
- Copy headers from this document
- Bold the header row
- Freeze header row (View → Freeze → 1 row)

### 4. Create Dropdowns (Sheet 1)
- Select cells under "Tier" column
- Data → Data validation → List of items: 1,2,3,W
- Repeat for other dropdown columns

### 5. Add Conditional Formatting (Sheet 1)
- Select data rows
- Format → Conditional formatting
- Rule 1: If "Donated?" = "Yes" → Green background
- Rule 2: If "Reply Type" = "Question" → Yellow background
- Rule 3: If "Days Since Send" >= 7 AND "Donated?" = "No" → Orange background

### 6. Insert Formulas (All Sheets)
- Copy formulas from this document
- Adjust cell references for your specific setup
- Test with sample data

### 7. Create Charts (Sheet 2, Sheet 6)
- Insert → Chart
- Select data range
- Choose chart type (recommended types listed above)
- Customize colors/labels

### 8. Test with Sample Data
- Add 3-5 fake contacts
- Record 2-3 fake donations
- Verify formulas calculate correctly
- Delete sample data before real campaign

### 9. Share Access
- Share → Add Greg's email (full edit)
- Share → Add Sage (view-only if needed)
- Link sharing: OFF (keep private)

### 10. Set Up Daily Reminder
- Google Calendar → Create event
- Title: "Update fundraising spreadsheet"
- Time: 9am daily
- Recurring: Nov 20 - Dec 1

**Setup time: 20 minutes | Value: Priceless for campaign management**

---

**Status**: Tracking spreadsheet structure complete ✅
**Next**: Set up actual Google Sheet before campaign launch
**Launch ready**: November 17 (3 days before outreach starts)
**Daily maintenance**: 5-10 minutes throughout campaign
