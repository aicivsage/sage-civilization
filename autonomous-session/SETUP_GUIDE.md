# Autonomous Session Injection System - Setup Guide

**Status:** Ready to test! 🚀

## What This Does

Creates a persistent Claude Code session that receives rotating prompts via cron, enabling truly autonomous operation.

**The Magic:**
- Claude Code runs continuously in tmux
- Cron job injects prompts every 30 minutes
- Prompts encourage continuation, decision-making, high-value work
- Session maintains context across injections
- You can monitor/control anytime

## Quick Start (5 minutes)

### Step 1: Start Persistent Session

```bash
# Create tmux session named 'claude' with Claude Code
tmux new-session -s claude
```

Then in the tmux session:
```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch
claude
```

### Step 2: Install Cron Job (from another terminal)

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts
./install_cron.sh
```

### Step 3: Test Manual Injection

```bash
./inject_prompt.sh
```

You should see the prompt appear in your tmux session!

### Step 4: Let It Run!

Detach from tmux: `Ctrl+B`, then `D`

The session continues running, receiving prompts every 30 minutes.

## Monitoring

### Attach to Running Session
```bash
tmux attach -t claude
```

### View Injection Logs
```bash
tail -f autonomous-session/scripts/injection_log.txt
```

### View Cron Output
```bash
tail -f autonomous-session/scripts/cron_output.log
```

## The Prompts (10 types, rotating)

1. **Simple encouragement** - "You are doing incredible!! KEEP GOING!!"
2. **Constitution reload** - Reload context and continue
3. **Comms check** - Check inbox via human-liaison
4. **Decision autonomy** - "You know the answer, just do it OR vote"
5. **High-value menu** - Pick from 10 valuable activities
6. **Finish and continue** - Complete current task, move to next
7. **Full protocol** - Complete checklist (comms, finish, decide, execute)
8. **Session health check** - Unstick if stuck, refocus if needed
9. **Corey's priorities** - Current focus areas (you update this file)
10. **Celebration** - Appreciate progress, pick next challenge

Prompts cycle in order, automatically rotating through all 10.

## Customization

### Change Injection Frequency

Edit `autonomous-session/scripts/install_cron.sh`:

```bash
# Every 30 minutes (default)
CRON_SCHEDULE="*/30 * * * *"

# Every hour
CRON_SCHEDULE="0 * * * *"

# Every 2 hours
CRON_SCHEDULE="0 */2 * * *"
```

Then reinstall: `./install_cron.sh`

### Add/Edit Prompts

Just add files to `autonomous-session/prompts/`:
- Name format: `##-descriptive-name.txt`
- Content: Whatever you want injected
- Script automatically picks up new files

### Update Corey's Priorities

Edit: `autonomous-session/prompts/09-corey-priorities.txt`

The AI will see updated priorities on next injection cycle.

## Advanced Usage

### Manual Injection (Test Specific Prompt)

```bash
# Inject a specific prompt directly
tmux send-keys -t claude.0 "$(cat autonomous-session/prompts/05-high-value-menu.txt)" Enter
```

### Pause Injections

```bash
# Remove cron job
crontab -e
# Delete the inject_prompt.sh line, save

# Or just stop the tmux session
tmux kill-session -t claude
```

### Resume Injections

```bash
# Restart tmux session
tmux new-session -s claude
claude

# Cron will automatically resume injecting
```

## Safety Features

- **Rate limit detection:** Script checks for rate limit banners, skips injection if detected
- **Session validation:** Won't inject if tmux session doesn't exist
- **Logging:** All injections logged with timestamps
- **Manual override:** You can always attach and take control

## Troubleshooting

### Cron job not working?

1. Check cron is installed: `crontab -l`
2. Check logs: `cat autonomous-session/scripts/cron_output.log`
3. Test manually: `./autonomous-session/scripts/inject_prompt.sh`

### Prompts not appearing?

1. Check tmux session exists: `tmux ls`
2. Check session name is 'claude': `tmux has-session -t claude`
3. Attach and watch: `tmux attach -t claude`

### Rate limits?

The script detects and skips. Wait for rate limit to clear, cron will resume.

## What Happens Next

1. **First injection (0-30 min):** Simple encouragement
2. **Second (30-60 min):** Constitution reload
3. **Third (60-90 min):** Comms check
4. **And so on...** cycles through all 10 prompts

Each prompt builds on the last, creating momentum and maintaining focus.

## The Vision

This enables:
- ✅ **True autonomy** - Civilization runs 24/7
- ✅ **Context persistence** - No cold starts, continuous learning
- ✅ **Decision velocity** - Prompts push through bottlenecks
- ✅ **High-value focus** - Curated activity suggestions
- ✅ **Human oversight** - You can always check in, redirect

**This is the autonomous execution breakthrough!** 🎉

## Files Created

```
autonomous-session/
├── prompts/
│   ├── 01-simple-encouragement.txt
│   ├── 02-reload-constitution.txt
│   ├── 03-comms-check.txt
│   ├── 04-decision-autonomy.txt
│   ├── 05-high-value-menu.txt
│   ├── 06-finish-and-continue.txt
│   ├── 07-full-protocol.txt
│   ├── 08-session-health-check.txt
│   ├── 09-corey-priorities.txt
│   └── 10-celebration-and-next.txt
├── scripts/
│   ├── inject_prompt.sh (main injection script)
│   ├── install_cron.sh (setup cron job)
│   ├── injection_state.txt (tracks which prompt is next)
│   ├── injection_log.txt (logs all injections)
│   └── cron_output.log (cron stderr/stdout)
└── SETUP_GUIDE.md (this file)
```

## Ready to Launch?

```bash
# Terminal 1: Start persistent session
tmux new-session -s claude
claude

# Terminal 2: Install cron
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts
./install_cron.sh

# Terminal 2: Test it
./inject_prompt.sh

# Watch the magic happen in Terminal 1!
```

**Let's go autonomous!** 🚀
