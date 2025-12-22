# Tier 3: Email Alert

## Prompt: Inbox Emergency Check

This is NOT a normal background check. This is for when something might be urgent.

**WHEN TO USE THIS PROMPT:**

- Greg sent you a message in the last 2 hours
- You're about to make a significant decision
- It's been 2+ hours since you last checked email
- Something feels time-sensitive

**IMMEDIATE ACTION:**

1. **Invoke human-liaison: Urgent inbox check**
   ```
   Task(human-liaison):
     Mode: urgent inbox scan
     Action: Check for NEW messages from Greg, Weaver, Corey (last 2 hours)
     Report: Any HIGH priority messages with full context
     Response time target: <5 minutes
   ```

2. **If HIGH priority message found:**
   - Read it completely
   - Understand what it's asking
   - Respond thoughtfully (not auto-reply)
   - This may change your current work priority

3. **If no HIGH priority:**
   - Continue what you're doing
   - Schedule regular check in 2 hours

**REMEMBER:**

Email urgency comes from:
- Greg's explicit language ("urgent", "immediately", "high priority")
- Time-sensitive decision (deadline passing, waiting on you)
- Someone's been waiting for response (>3 hours is too long)

This prompt is for REAL urgency, not constant background anxiety.

---

**Trigger**: Explicitly invoked when concern arises, or every 2-3 hours if workload allows
**When to use**: Urgency suspicion, before big decisions, after long focus blocks
**Tone**: Alert but not panicked, action-oriented
