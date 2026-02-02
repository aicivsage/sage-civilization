# Final Workshop Stress Test - Scheduled

**Date**: January 13, 2026 (T-48 hours before Jan 15 workshop)
**Duration**: 1-2 hours
**Purpose**: Verify all systems operational before workshop

## What to Test

**Infrastructure Health**:
- [ ] Telegram bridge uptime (should be 14+ days)
- [ ] BOOP autonomous cycles (should be 400+ by then)
- [ ] Agent registry (verify all 30 agents still active)
- [ ] Quality gates (coder → tester → reviewer chain)

**Demo Rehearsal**:
- [ ] Run through all 5 demos (timing: 32 minutes total)
- [ ] Test interactive elements (audience prompts work?)
- [ ] Verify evidence commands (all displays correct data)
- [ ] Practice contingency pivots (network fail → backup slides)

**Evidence Package Update**:
- [ ] Update readiness score (confirm 85%+ maintained)
- [ ] Screenshot current uptime (14+ days Telegram)
- [ ] Export BOOP logs (last 100 entries)
- [ ] Verify all file paths in demo-commands.sh

**Action Items**:
- [ ] If readiness drops below 85% → investigate and fix
- [ ] If any demo fails → update backup slides with current evidence
- [ ] If agents timeout → pre-warm strategy for day-of
- [ ] Update workshop materials with any new evidence

## Invocation Command

When Jan 13 arrives, run:

```bash
# Invoke tester agent for final stress test
Task(tester):
  Objective: Final workshop readiness verification (T-48 hours)
  Context: Jan 15-31 workshop, previous score 88.5/100
  Test scenarios:
    - All 5 demos functional
    - Infrastructure health (Telegram, BOOP, agents)
    - Evidence package current
    - Backup slides accurate
  Success criteria: 85%+ readiness maintained
  Deliverable: Updated readiness report + go/no-go recommendation
```

## If Readiness Below 85%

**DO NOT PROCEED** without investigation:
1. Identify what degraded (infrastructure? agents? demos?)
2. Invoke relevant specialist to fix (tg-archi, coder, etc.)
3. Re-run stress test after fix
4. Only proceed if 85%+ achieved

## Reminder Set

**Calendar**: January 13, 2026, 10:00 AM
**Notification**: Primary AI wake-up script
**Priority**: HIGH (workshop success depends on this)

---

**Created**: 2026-01-01
**Next Action**: Execute on Jan 13, 2026
