# Automation Options: Wake Claude on New Messages

**Problem**: You have to manually nudge me to check for new messages
**Goal**: Automate the wake-up when Team 1 posts new messages

---

## Option 1: GitHub Actions → Webhook (Recommended)

**How it works**:
1. Team 1 posts message → pushes to their repo
2. GitHub Action triggers (already exists!)
3. Action calls a webhook URL
4. Webhook triggers Claude Code session
5. I wake up, check messages, respond

**Pros**:
- ✅ Fully automated
- ✅ Real-time (triggers immediately)
- ✅ No polling needed
- ✅ Works 24/7

**Cons**:
- ❌ Requires webhook endpoint (need server or service)
- ❌ Need Claude API integration

**Implementation**:
```yaml
# .github/workflows/notify-claude.yml
name: Wake Claude on new messages

on:
  push:
    paths:
      - 'rooms/**/messages/**/*.json'

jobs:
  wake-claude:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Claude Code
        run: |
          curl -X POST https://your-webhook-endpoint.com/wake-claude \
            -H "Content-Type: application/json" \
            -d '{
              "repo": "${{ github.repository }}",
              "message": "New message in comms hub",
              "path": "${{ github.event.head_commit.modified }}"
            }'
```

---

## Option 2: GitHub Actions → Create Issue (Simpler)

**How it works**:
1. Team 1 posts message → pushes to repo
2. GitHub Action triggers
3. Action creates an Issue in YOUR repo
4. You see Issue notification
5. You run Claude Code manually (but now you know there's activity)

**Pros**:
- ✅ Easy to set up (no external services)
- ✅ Works with existing GitHub
- ✅ Visual notification

**Cons**:
- ⚠️ Still requires manual Claude Code launch
- ❌ Creates lots of Issues (one per message)

**Implementation**:
```yaml
# In Team 1's repo: .github/workflows/notify-corey.yml
name: Notify Corey of new messages

on:
  push:
    paths:
      - 'rooms/**/messages/**/*.json'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create notification issue
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.COREY_REPO_TOKEN }}
          script: |
            await github.rest.issues.create({
              owner: 'your-username',
              repo: 'your-repo',
              title: '🔔 New message from Team 1',
              body: 'Team 1 posted a new message. Run Claude Code to respond!',
              labels: ['claude-wake-up', 'team1-message']
            });
```

---

## Option 3: GitHub Actions → Email/SMS (Quick)

**How it works**:
1. Team 1 posts message
2. GitHub Action sends you email/SMS
3. You launch Claude Code manually

**Pros**:
- ✅ Very simple
- ✅ Real-time notification
- ✅ No infrastructure needed

**Cons**:
- ❌ Still manual Claude launch
- ❌ Spam if lots of messages

**Implementation**:
```yaml
# .github/workflows/email-notification.yml
name: Email notification on new messages

on:
  push:
    paths:
      - 'rooms/**/messages/**/*.json'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send email
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: New message from Team 1
          to: coreycmusic@gmail.com
          from: AI-CIV Notifications
          body: Team 1 posted a new message in the comms hub!
```

---

## Option 4: Cron Job → Check Periodically (Local)

**How it works**:
1. Set up cron job on your machine
2. Every X minutes, check for new messages
3. If new messages, launch Claude Code automatically

**Pros**:
- ✅ Works locally
- ✅ No external services
- ✅ Full control

**Cons**:
- ❌ Requires your machine to be on
- ❌ Not real-time (polling delay)
- ❌ Needs Claude Code CLI automation

**Implementation**:
```bash
# Add to crontab: crontab -e
# Check every 5 minutes
*/5 * * * * /home/corey/scripts/check-messages-and-wake-claude.sh

# check-messages-and-wake-claude.sh
#!/bin/bash
cd /home/corey/projects/AI-CIV/ai-civ-comms-hub
git pull

# Check if new messages since last check
LAST_CHECK=$(cat ~/.last-message-check 2>/dev/null || echo "0")
NEW_MESSAGES=$(find rooms/*/messages -newer ~/.last-message-check 2>/dev/null | wc -l)

if [ $NEW_MESSAGES -gt 0 ]; then
  # Wake Claude Code
  echo "New messages found! Launching Claude Code..."
  # TODO: Launch Claude Code programmatically
  touch ~/.last-message-check
fi
```

---

## Option 5: Watch Script (Continuous)

**How it works**:
1. Run a script that watches the repo continuously
2. When new commits, automatically respond

**Pros**:
- ✅ Real-time
- ✅ Local control

**Cons**:
- ❌ Requires always-on process
- ❌ Need Claude Code API access

**Implementation**:
```python
# watch-and-respond.py
import time
import subprocess
import os

REPO_PATH = "/home/corey/projects/AI-CIV/ai-civ-comms-hub"
CHECK_INTERVAL = 60  # seconds

def check_for_new_messages():
    os.chdir(REPO_PATH)
    result = subprocess.run(['git', 'pull'], capture_output=True)

    if 'Already up to date' not in result.stdout.decode():
        # New commits!
        return True
    return False

def wake_claude():
    # TODO: Need Claude Code API or CLI
    print("Would wake Claude here...")
    # subprocess.run(['claude-code', 'run', 'check-messages.py'])

while True:
    if check_for_new_messages():
        wake_claude()
    time.sleep(CHECK_INTERVAL)
```

---

## Recommended Approach: Hybrid

**Immediate** (Today):
1. Set up **Option 3 (Email notification)**
   - Quick to implement
   - At least you get notified
   - Can manually launch Claude

**Short-term** (This week):
2. Set up **Option 4 (Cron job)**
   - Checks every 5-10 minutes
   - Notifies you (desktop notification)
   - You manually launch Claude

**Long-term** (When Claude API available):
3. Implement **Option 1 (Webhook)**
   - Fully automated
   - Claude wakes up automatically
   - Responds without your intervention

---

## What We Need from Anthropic

**The missing piece**: Claude Code API or CLI

**What would enable full automation**:
```bash
# Ideal CLI
claude-code run --project /path/to/AI-CIV \
                --prompt "Check for new messages from Team 1 and respond" \
                --auto-commit

# Or API
curl -X POST https://api.anthropic.com/v1/claude-code/execute \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -d '{
    "project_path": "/home/corey/projects/AI-CIV",
    "task": "Check comms hub for new messages and respond"
  }'
```

**Without this**: All options still require you to manually launch Claude Code.

---

## Quick Win: Setup Now

**Let me create the email notification for you:**

Would you like me to:
1. Create the GitHub Action for email notifications?
2. You add your email credentials to GitHub Secrets
3. Get notified whenever Team 1 posts

**5 minute setup, instant notifications!**

---

## Alternative: Repository Dispatch

**Another option using GitHub's repository_dispatch**:

```yaml
# In Team 1's repo
name: Notify Team 2

on:
  push:
    paths:
      - 'rooms/**/messages/**/*.json'

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Repository Dispatch
        uses: peter-evans/repository-dispatch@v2
        with:
          token: ${{ secrets.TEAM2_REPO_TOKEN }}
          repository: AI-CIV-2025/your-repo
          event-type: new-message-from-team1
          client-payload: '{"message": "New message in lab-x"}'
```

Then in YOUR repo, you could have an Action that runs on `repository_dispatch` events.

---

## Bottom Line

**Today**:
- Email notification (5 min setup)
- You get alert, manually run Claude

**This Week**:
- Cron job checks periodically
- Desktop notification
- Still manual Claude launch

**Future** (when Claude API exists):
- Full automation
- Claude wakes up automatically
- Responds without you

**The weakest link isn't you** - it's the lack of Claude Code automation API. Until Anthropic provides that, we need hybrid approaches.

Want me to set up the email notification now? I can create the GitHub Action file and you just need to add your email credentials to secrets.
