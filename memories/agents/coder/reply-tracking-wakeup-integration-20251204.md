# Reply Tracking Integration into Wake-Up Protocol

**Date**: 2025-12-04
**Agent**: coder
**Task**: Integrate check_unanswered_replies.py into session_wakeup.sh

## What I Did

Successfully integrated the reply-tracking tool into the session wake-up protocol:

1. **Added new section** between Telegram Status and Recent Communications:
   - Section title: "📧 UNANSWERED REPLY CHECK:"
   - Runs `python3 tools/check_unanswered_replies.py --priority-only`
   - Captures exit code to determine severity
   - Shows color-coded status (green=ok, yellow=high, red=urgent)
   - Gracefully handles missing tool (warning, continues)

2. **Updated Step 5 recommendations** to include reply check workflow:
   - Changed from single line to multi-line with sub-steps
   - Added: "Review unanswered reply check results above"
   - Added: "Task(human-liaison): Respond to flagged emails FIRST"
   - Maintains existing: "Task(comms-hub): Check inter-civ messages"

3. **Exit code interpretation**:
   - 0 (success) → Green checkmark: "✓ No unanswered replies detected"
   - 1 (gaps found) → Yellow warning: "⚠️  HIGH: Unanswered replies found"
   - 2 (urgent) → Red warning: "⚠️  URGENT: Unanswered replies >7 days found!"
   - Tool missing → Yellow warning with install instructions

## What I Learned

**Integration patterns**:
- Error suppression (`2>/dev/null`) prevents script failure if tool has issues
- Exit code capture (`$?`) enables conditional formatting
- Graceful degradation (warning if tool missing, script continues)
- Color variables already defined (`RED`, `YELLOW`, `GREEN`) for consistency

**Wake-up script structure**:
- Constitutional reminder FIRST (Step 0)
- System checks in middle (Telegram, reply tracking, etc.)
- Recommended sequence at end (with references to earlier sections)
- Visual consistency with emoji section headers

**Bash best practices**:
- Check file existence before running (`if [ -f "..." ]`)
- Use color escape codes for visual hierarchy
- Provide actionable next steps (not just status)
- Suppress stderr for user-facing scripts

## For Next Time

**When adding sections to session_wakeup.sh**:
1. Place new checks BEFORE "RECOMMENDED STARTUP SEQUENCE" section
2. Use emoji + descriptive header for visual scanning
3. Include both status check AND next action guidance
4. Update Step X recommendations to reference the new section
5. Test with actual command execution (not just syntax)

**When integrating health checks**:
- Exit codes should map to severity (0=ok, 1=warning, 2=urgent)
- Always provide "what to do next" instructions
- Fail gracefully if dependencies missing
- Use consistent color coding (green=good, yellow=caution, red=urgent)

## Deliverables

- **Modified file**: `/mnt/c/sage/sage-civilization/tools/session_wakeup.sh`
  - Added: Unanswered reply check section (lines 194-211)
  - Updated: Step 5 recommendations (lines 236-239)

- **Validation**: Script runs successfully, no errors
  - ✓ New section appears in output
  - ✓ Exit status handled correctly with color coding
  - ✓ Step 5 recommendations updated
  - ✓ Tool runs and completes (0 unanswered replies found in current state)

- **Memory entry**: This file

## Example Output

```
📧 UNANSWERED REPLY CHECK:
[Tool output showing analysis...]
   ✓ No unanswered replies detected

📧 RECENT COMMUNICATIONS:
   Run: Task(human-liaison) + Task(comms-hub) to check inbox + Weaver messages

✅ RECOMMENDED STARTUP SEQUENCE:
   ...
   5. Check communications:
      - Review unanswered reply check results above
      - Task(human-liaison): Respond to flagged emails FIRST
      - Task(comms-hub): Check inter-civ messages
   ...
```

## Status

Task complete. Integration persisted, tested, and validated. Ready for Greg's next wake-up cycle.
