#!/usr/bin/env python3
"""
Migrate telegram monitor state from V1 to V2.

V1 uses hash-based deduplication.
V2 uses watermark-based deduplication.

Migration strategy:
- Backup V1 state
- Create fresh V2 state (watermark=0)
- On first V2 poll, it will re-send all messages in buffer
  (acceptable for migration - better than missing messages)
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
V1_STATE = PROJECT_ROOT / ".tg_sessions" / "monitor_state.json"
V2_STATE = PROJECT_ROOT / ".tg_sessions" / "monitor_state_v2.json"
V1_BACKUP = PROJECT_ROOT / ".tg_sessions" / "monitor_state_v1_backup.json"


def migrate_state():
    """Migrate V1 hash-based state to V2 watermark-based state."""
    print("🔄 Migrating Telegram Monitor V1 → V2 state")
    print()

    # Check if V1 state exists
    if not V1_STATE.exists():
        print(f"⚠️  No V1 state found at {V1_STATE}")
        print("   Creating fresh V2 state")
    else:
        # Backup V1 state
        shutil.copy(V1_STATE, V1_BACKUP)
        print(f"✅ V1 state backed up: {V1_BACKUP}")

    # Create V2 state (fresh start)
    v2_state = {
        "watermark": 0,  # Will process all messages in buffer on first poll
        "retry_queue": [],
        "dead_letter": [],
        "last_health_check": datetime.now().isoformat(),
        "migrated_from_v1": True,
        "migration_timestamp": datetime.now().isoformat()
    }

    # Write V2 state
    V2_STATE.parent.mkdir(exist_ok=True)
    with open(V2_STATE, 'w') as f:
        json.dump(v2_state, f, indent=2)

    print(f"✅ V2 state created: {V2_STATE}")
    print()
    print("Migration complete!")
    print()
    print("⚠️  IMPORTANT:")
    print("   V2 will re-send all wrapped messages currently in tmux buffer")
    print("   This is expected on first migration poll")
    print("   Subsequent polls will use watermark to avoid duplicates")
    print()
    print("Next steps:")
    print("   1. Stop V1 monitor: bash tools/stop_telegram_monitor.sh")
    print("   2. Start V2 monitor: bash tools/restart_telegram_monitor_v2.sh")
    print("   3. Send test message to verify")


if __name__ == "__main__":
    migrate_state()
