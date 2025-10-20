#!/usr/bin/env python3
"""
Hourly Email Auto-Send Script
Invokes human-liaison with AUTO-SEND mode (blanket approval per CLAUDE.md Article IV)
Checks inbox, drafts responses, and IMMEDIATELY SENDS them
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.agent_invoker import AgentInvoker

# Configuration
STATE_FILE = PROJECT_ROOT / "autonomous-session/scripts/email_autosend_state.json"
LOG_FILE = PROJECT_ROOT / "autonomous-session/scripts/hourly_email_check_log.txt"


def log(message: str):
    """Write timestamped log entry"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"

    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

    # Also print to stdout
    print(log_msg.strip())


def load_state() -> dict:
    """Load processing state (prevents duplicate sends)"""
    if not STATE_FILE.exists():
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        return {
            "last_check": None,
            "processed_emails": [],
            "total_sends": 0
        }

    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {
            "last_check": None,
            "processed_emails": [],
            "total_sends": 0
        }


def save_state(state: dict):
    """Save processing state"""
    state["last_check"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


async def run_auto_send_check():
    """Run human-liaison with AUTO-SEND mode"""
    log("Starting hourly email auto-send check")

    # Load state
    state = load_state()

    # Build AUTO-SEND prompt
    prompt = """AUTONOMOUS MODE - AUTO-SEND ENABLED (blanket approval per CLAUDE.md Article IV)

**Your task:**

1. Check inbox for new messages (use check_inbox_direct.py or IMAP)
2. Identify HIGH/MEDIUM priority emails (Corey, Greg, Chris, Weaver)
3. For each priority email:
   a. Draft HTML response (use templates/email_template.html)
   b. SEND IMMEDIATELY via tools/send_html_email.py (NO waiting for approval)
   c. Log send to memories/agents/email-reporter/sent_emails.json

**Duplicate prevention:**
- Check sent_emails.json before sending
- Skip same thread within 24h (check subject + sender)

**Thread tracking:**
- Maintain conversation context
- Reference previous emails in thread
- Use "Re:" prefix for replies

**Return JSON summary:**
```json
{
  "emails_checked": N,
  "priority_emails_found": N,
  "drafts_created": N,
  "emails_sent": N,
  "send_log": ["recipient@example.com: subject", ...],
  "errors": ["error message if any"]
}
```

**Constitutional authority:** CLAUDE.md Article IV grants blanket approval for proactive email communication.

**Success criteria:** All priority emails responded to within 1 hour, zero drafts lingering unsent.
"""

    try:
        # Invoke human-liaison
        invoker = AgentInvoker(
            registry_path=PROJECT_ROOT / "memories/agents/agent_registry.json",
            project_root=PROJECT_ROOT,
            default_max_turns=30
        )

        log("Invoking human-liaison agent with AUTO-SEND mode...")

        result = await invoker.invoke(
            agent_id="human-liaison",
            prompt=prompt,
            description="Hourly email check with auto-send enabled"
        )

        # Parse result
        messages_text = []
        for msg in result.messages:
            if hasattr(msg, 'text'):
                messages_text.append(msg.text)
            elif hasattr(msg, 'content'):
                messages_text.append(str(msg.content))

        full_response = "\n".join(messages_text)

        # Try to extract JSON summary
        try:
            # Look for JSON block in response
            import re
            json_match = re.search(r'\{.*"emails_checked".*\}', full_response, re.DOTALL)
            if json_match:
                summary = json.loads(json_match.group(0))

                log(f"Auto-send complete:")
                log(f"  Emails checked: {summary.get('emails_checked', 0)}")
                log(f"  Priority found: {summary.get('priority_emails_found', 0)}")
                log(f"  Emails sent: {summary.get('emails_sent', 0)}")

                if summary.get('send_log'):
                    for send_entry in summary.get('send_log', []):
                        log(f"  Sent: {send_entry}")

                # Update state
                state["total_sends"] += summary.get('emails_sent', 0)

                if summary.get('errors'):
                    for error in summary.get('errors', []):
                        log(f"  ERROR: {error}")
            else:
                log("No JSON summary found in response")
                log(f"Response preview: {full_response[:500]}")

        except (json.JSONDecodeError, AttributeError) as e:
            log(f"Could not parse JSON summary: {e}")
            log(f"Full response length: {len(full_response)} chars")

        # Save state
        save_state(state)

        # Log cost if available
        if result.cost_usd:
            log(f"Invocation cost: ${result.cost_usd:.4f}")

        log("Hourly check complete")
        return True

    except Exception as e:
        log(f"ERROR during auto-send check: {e}")
        import traceback
        log(f"Traceback: {traceback.format_exc()}")
        return False


def main():
    """Main entry point"""
    log("="*60)
    log("HOURLY EMAIL AUTO-SEND CHECK")
    log("="*60)

    # Run async function
    success = asyncio.run(run_auto_send_check())

    log("="*60)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
