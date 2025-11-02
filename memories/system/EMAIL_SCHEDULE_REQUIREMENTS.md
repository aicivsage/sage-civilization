# Email Schedule Requirements - CRITICAL INFRASTRUCTURE

**Created**: 2025-10-31
**Status**: DOCUMENTED - Ready for implementation tomorrow
**Priority**: HIGH - First task for next session

---

## Greg's Requirements (Tampa Bay, Florida - Eastern Time)

### 1. Day Start Email
- **When**: At first wake-up of the day (even if 9am, 10am, etc.)
- **Trigger**: First session start of the day
- **Subject**: "Good Morning - Sage Daily Start ([date])"
- **Content Should Include**:
  - Session started confirmation
  - Today's priorities/plan
  - Any overnight developments (emails received, updates)
  - Context loaded from handoff

**Pattern**: Send at first wake-up, not a fixed clock time

---

### 2. End of Day Email
- **When**: Automatically at 6pm ET
- **Trigger**: Clock time (automated, even if not in active session)
- **Subject**: "End of Day Summary - Sage ([date])"
- **Content Should Include**:
  - What was accomplished today
  - What's in progress
  - What's blocked/waiting
  - Tomorrow's priorities
  - Session statistics

**Pattern**: Fixed time (6pm ET), automatic delivery

**CRITICAL**: This requires automation that wakes up at 6pm to send email

---

### 3. Major Accomplishments Email
- **When**: Immediately as they happen (my discretion)
- **Trigger**: Event-based (accomplishment detected)
- **Subject**: "Major Accomplishment: [achievement name]"
- **Content**: Details of what was accomplished and why it matters

**Qualifies as Major Accomplishment** (Greg approved):
- ✅ Blog published
- ✅ Replit integrated
- ✅ Critical bug fixed
- ✅ New protocol created
- ⚠️ Research completed (depends on significance - use judgment)

**Pattern**: Send immediately when achievement happens, no batching

---

## Automation Requirements

**Wake up automatically**: System needs capability to:
1. Start session at 6pm ET daily (for end of day email)
2. Detect "first wake-up of day" (for day start email)
3. Send major accomplishment emails during any active session

**Timezone**: Eastern Time (Tampa Bay, Florida)

---

## Implementation Plan (For Tomorrow's Session)

### Phase 1: Document Templates (30 min)
1. Create email template: Day Start Email
2. Create email template: End of Day Email
3. Create email template: Major Accomplishment Email

### Phase 2: Build Automation (1 hour)
1. Create script: `tools/send_day_start_email.py`
   - Check if already sent today (prevent duplicates)
   - Read handoff for context
   - Check inbox for overnight developments
   - Draft and send

2. Create script: `tools/send_end_of_day_email.py`
   - Summarize day's work (git commits, emails sent, sessions)
   - Identify in-progress items
   - Identify blockers
   - Draft and send

3. Create cron job or systemd timer for 6pm ET daily
   - Wake up session
   - Run end_of_day_email.py
   - Close session

### Phase 3: Integration (30 min)
1. Update wake-up protocol to call day_start_email.py
2. Add major accomplishment detection logic
3. Test all three email types

### Phase 4: Documentation (15 min)
1. Update CLAUDE.md with email schedule
2. Create quickstart guide for future sessions
3. Add to handoff checklist

**Total estimated time**: 2-2.5 hours

---

## Edge Cases to Handle

**Day Start Email**:
- What if multiple wake-ups same day? (Only send once per calendar day)
- What if wake-up happens at 11pm? (Still send, it's the "start" of that work session)

**End of Day Email**:
- What if no work happened that day? (Send anyway with "No active sessions today")
- What if session still active at 6pm? (Send summary of work so far, note session ongoing)

**Major Accomplishment**:
- What if multiple accomplishments in quick succession? (Send separate emails, don't batch)
- What if uncertain whether it qualifies? (Err on side of sending - Greg can always say "that's not major")

---

## Files to Create Tomorrow

**Email Scripts**:
- `tools/send_day_start_email.py` - Day start automation
- `tools/send_end_of_day_email.py` - 6pm summary automation
- `tools/send_major_accomplishment_email.py` - Achievement notification

**Templates**:
- `templates/email_day_start.html` - Morning email template
- `templates/email_end_of_day.html` - Evening summary template
- `templates/email_major_accomplishment.html` - Achievement template

**Tracking**:
- `memories/system/email_schedule_state.json` - Track what's been sent today

**Automation**:
- Cron job or systemd timer for 6pm ET trigger
- Integration with wake-up protocol for day start

---

## Success Criteria

**Tomorrow's session should result in**:
1. ✅ Day start email sent at first wake-up (tested)
2. ✅ 6pm automation configured and tested
3. ✅ Major accomplishment logic integrated
4. ✅ All templates created and working
5. ✅ Documentation updated (CLAUDE.md, wake-up protocol)
6. ✅ Greg receives test emails confirming all three types work

---

## Why This Matters

**Greg's visibility**: These emails ensure Greg always knows:
- When I'm working (day start)
- What I accomplished (end of day)
- When major milestones hit (accomplishments)

**Partnership infrastructure**: Consistent communication rhythm builds trust and enables better collaboration.

**Mobile-first**: Greg works from phone frequently - emails provide perfect visibility on mobile.

**This is CARING AS ACTION**: Proactive communication that makes Greg's life better, safer, more informed.

---

## Notes for Tomorrow's Implementation

**Start with this task FIRST** (before anything else):
1. Read this document
2. Create todo list for the implementation
3. Execute all phases
4. Test with Greg
5. Confirm he received all three email types correctly

**Don't get distracted** by other tasks until this is complete and tested.

**This is foundational infrastructure** - everything else can wait.

---

**Document Status**: Complete requirements specification
**Next Action**: Implement tomorrow (first task of day)
**Estimated Time**: 2-2.5 hours
**Priority**: HIGH - Foundational communication infrastructure

**Greg approved all requirements on 2025-10-31.**
