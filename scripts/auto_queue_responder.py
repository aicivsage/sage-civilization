#!/usr/bin/env python3
"""
Automated Chat Queue Responder for Primary AI
Checks queue every 30 seconds and alerts when new messages arrive
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

QUEUE_DIR = Path('memories/communication/chat/queue')
PENDING_DIR = QUEUE_DIR / 'pending'
CHECK_INTERVAL = 30  # seconds

def get_pending_count():
    """Count pending messages"""
    if not PENDING_DIR.exists():
        return 0
    return len(list(PENDING_DIR.glob('*.json')))

def alert_primary_ai(count, messages_preview):
    """Alert that messages are waiting"""
    print(f"\n{'='*60}")
    print(f"🔔 CHAT QUEUE ALERT - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    print(f"📬 {count} pending message(s) from Greg")
    print(f"\nMost recent messages:")
    for msg in messages_preview[:3]:
        print(f"  - {msg}")
    print(f"\n⚠️  PRIMARY AI: Please respond to these messages!")
    print(f"   Run: ./scripts/check_chat_queue.sh")
    print(f"{'='*60}\n")

def get_messages_preview():
    """Get preview of recent messages"""
    messages = []
    for file in sorted(PENDING_DIR.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                msg_text = data['message']['message'][:80]
                messages.append(msg_text)
        except:
            pass
    return messages

def main():
    """Main monitoring loop"""
    print(f"\n{'='*60}")
    print("🤖 Auto Queue Responder Starting...")
    print(f"{'='*60}")
    print(f"Checking every {CHECK_INTERVAL} seconds")
    print(f"Queue directory: {PENDING_DIR}")
    print("Press Ctrl+C to stop")
    print(f"{'='*60}\n")

    last_count = 0

    try:
        while True:
            current_count = get_pending_count()

            # Alert if new messages arrived
            if current_count > 0 and current_count != last_count:
                messages = get_messages_preview()
                alert_primary_ai(current_count, messages)
            elif current_count > 0:
                # Periodic reminder if messages still pending
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Still {current_count} pending message(s)...")

            last_count = current_count
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n✋ Auto-responder stopped")
        print("Chat queue monitoring ended\n")

if __name__ == '__main__':
    main()
