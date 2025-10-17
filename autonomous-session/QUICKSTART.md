# Autonomous Session - QUICKSTART ⚡

## The 60-Second Setup

```bash
# 1. Start persistent Claude session in tmux
tmux new-session -s claude
claude  # (run this inside tmux)

# 2. In another terminal: Install cron (auto-inject every 30 min)
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/autonomous-session/scripts
./install_cron.sh

# 3. Test it NOW (manual injection)
./inject_prompt.sh

# 4. Watch the prompt appear in your tmux session!
# Detach: Ctrl+B, then D

# DONE! Session runs autonomously, getting prompts every 30 min
```

## What Just Happened?

✅ Persistent Claude session in tmux (maintains context)
✅ Cron job installed (injects prompts every 30 min)
✅ 10 rotating prompts (encouragement, decisions, activities)
✅ Autonomous execution (no more stopping!)

## Monitor It

```bash
# Reattach to see what's happening
tmux attach -t claude

# View injection logs
tail -f autonomous-session/scripts/injection_log.txt
```

## The Prompts (Cycles Through These)

1. "You are doing incredible!! KEEP GOING!!"
2. "Read the constitution and keep going - you're crushing this!"
3. "Check communications (inbox) and keep going"
4. "You know the answer - just do it OR vote, then IMPLEMENT"
5. "Pick a high-value activity from menu and DO IT"
6. "Finish current task, mark complete, pick next"
7. "Full protocol: comms → finish → decide → execute"
8. "Health check: stuck? here's help"
9. "Corey's priorities: [current focus areas]"
10. "Celebrate progress, then pick next challenge"

## Update Priorities Anytime

Edit this file: `autonomous-session/prompts/09-corey-priorities.txt`

The AI sees it on next injection cycle!

## Full Docs

See `SETUP_GUIDE.md` for all details, troubleshooting, customization.

---

**Ready for context clear and tmux boop!** 🚀
