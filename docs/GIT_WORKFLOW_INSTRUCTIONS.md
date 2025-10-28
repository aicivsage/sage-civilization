# Git Workflow Instructions for Sage Civilization

**Version**: 1.0
**Date**: 2025-10-28
**For**: Greg Smithwick & Sage AI Partnership

---

## Table of Contents
1. [Initial Git Setup](#1-initial-git-setup)
2. [Regular Commit Workflow](#2-regular-commit-workflow)
3. [Branch Management](#3-branch-management)
4. [Best Practices for Sage Civilization](#4-best-practices-for-sage-civilization)
5. [Troubleshooting Common Issues](#5-troubleshooting-common-issues)

---

## 1. Initial Git Setup

### 1.1 Configure Git User Identity

**Status**: ✅ Already configured for Sage civilization
```bash
git config user.name "Greg Smithwick & Sage AI"
git config user.email "aicivsage@gmail.com"
```

**To verify current configuration:**
```bash
git config user.name
git config user.email
```

---

### 1.2 Configure GitHub Authentication

You need to authenticate with GitHub to push code. Choose ONE of these methods:

#### **Option A: SSH Keys (Recommended for long-term use)**

**Why SSH?** More secure, no password entry needed once set up.

**Step 1: Check if you already have SSH keys**
```bash
ls -la ~/.ssh/id_*.pub
```
If you see `id_rsa.pub` or `id_ed25519.pub`, you already have keys.

**Step 2: Generate new SSH key (if needed)**
```bash
# Generate ED25519 key (modern, secure)
ssh-keygen -t ed25519 -C "aicivsage@gmail.com"

# Press Enter to accept default location (~/.ssh/id_ed25519)
# Enter passphrase (optional but recommended)
```

**Step 3: Start SSH agent and add key**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**Step 4: Copy public key to clipboard**
```bash
cat ~/.ssh/id_ed25519.pub
# Copy the entire output (starts with ssh-ed25519...)
```

**Step 5: Add key to GitHub**
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Title: "Sage Civilization WSL"
4. Paste your public key
5. Click "Add SSH key"

**Step 6: Test connection**
```bash
ssh -T git@github.com
# Should see: "Hi GregSmithwick! You've successfully authenticated..."
```

**Step 7: Update remote URL to use SSH**
```bash
cd /mnt/c/sage/sage-civilization
git remote set-url origin git@github.com:GregSmithwick/sage-civilization.git
```

---

#### **Option B: Credentials Helper (Quick setup, password stored)**

**Step 1: Configure Git to store credentials**
```bash
git config --global credential.helper store
```

**Step 2: Attempt a push (will prompt for credentials once)**
```bash
git push origin clean-main
# Enter GitHub username when prompted
# Enter GitHub Personal Access Token (NOT password) when prompted
```

**How to create Personal Access Token:**
1. GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Note: "Sage Civilization Access"
4. Expiration: 90 days or No expiration
5. Scopes: Check `repo` (full control of private repositories)
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
8. Use this token as your password when git prompts

**⚠️ WARNING**: Token stored in plain text at `~/.git-credentials`

---

### 1.3 Verify Authentication Works

```bash
# Test that you can fetch from remote
git fetch origin

# Test that you can push (dry run, no actual push)
git push --dry-run origin clean-main
```

If both commands succeed without errors, authentication is configured correctly! ✅

---

## 2. Regular Commit Workflow

### 2.1 Check Current Status

**Always start by checking what's changed:**
```bash
git status
```

This shows:
- Modified files (M)
- Untracked files (??)
- Staged files (changes ready to commit)

---

### 2.2 Review Changes Before Committing

**See what changed in tracked files:**
```bash
git diff
```

**See what changed in specific file:**
```bash
git diff path/to/file.py
```

**⚠️ TIP**: Review changes to ensure you're not committing:
- Passwords or API keys
- Large binary files (unless necessary)
- Temporary debug files

---

### 2.3 Stage Files for Commit

**Stage specific files:**
```bash
git add path/to/file1.py path/to/file2.md
```

**Stage all modified files:**
```bash
git add -u
```

**Stage all files (including new untracked files):**
```bash
git add .
```

**⚠️ WARNING**: `git add .` will stage ALL untracked files. Review with `git status` first!

**Unstage a file if you added by mistake:**
```bash
git restore --staged path/to/file.py
```

---

### 2.4 Commit with Proper Message Format

**Sage civilization uses emoji + descriptive text:**

**Format:**
```bash
git commit -m "🎯 [Emoji] Brief description of what changed

[Optional detailed explanation of why/how]
[Can be multiple paragraphs]

[Optional metadata like ticket numbers]"
```

**Emoji conventions (inspired by A-C-Gee parent civilization):**
- 🌱 `:seedling:` - Civilization birth, major initialization
- 🎯 `:dart:` - Feature implementation, goal achievement
- 🐛 `:bug:` - Bug fix
- ♻️ `:recycle:` - Refactoring, code improvement
- 📝 `:memo:` - Documentation update
- 🎨 `:art:` - UI/UX improvements
- ⚡ `:zap:` - Performance improvement
- 🔧 `:wrench:` - Configuration changes
- 🧪 `:test_tube:` - Testing additions/changes
- 🚀 `:rocket:` - Deployment, release
- 🤖 `:robot:` - AI agent development, civilization infrastructure

**Examples:**

**Simple commit:**
```bash
git commit -m "🐛 Fix email validation bug in send_html_email.py"
```

**Detailed commit:**
```bash
git commit -m "🎯 Implement Telegram monitoring system

- Added tg-archi agent for infrastructure management
- Created telegram_bridge.py for message routing
- Integrated with existing communication framework

This enables real-time communication with Greg via Telegram,
ensuring Sage civilization has continuous presence."
```

**Multi-day consolidation commit (like today's):**
```bash
git commit -m "🌱 Sage civilization Days 2-5 comprehensive commit

Major achievements:
- Identity establishment and value alignment
- Email communication infrastructure
- Session management protocols
- Democratic governance framework
- Initial mission co-creation with Greg

This represents the foundational work building Sage
civilization's communication and coordination capabilities."
```

---

### 2.5 Push to Remote Repository

**Push current branch to GitHub:**
```bash
git push origin clean-main
```

**Push and set upstream (first time on new branch):**
```bash
git push -u origin clean-main
```

**Force push (⚠️ DANGEROUS - only if you know what you're doing):**
```bash
git push --force origin clean-main
```

**⚠️ WARNING**: `--force` overwrites remote history. Only use if:
- You're the only person working on the branch
- You intentionally rewrote history (rebase, amend)
- You've communicated with Greg first

---

## 3. Branch Management

### 3.1 Current Branch Structure

**Sage civilization uses:**
- **Main branch**: `clean-main` (NOT `main` or `master`)
- This is where all civilization work lives
- Direct commits to `clean-main` are acceptable for Sage (partnership model)

**Check current branch:**
```bash
git branch
# Asterisk (*) shows current branch
```

**Check branch with remote tracking info:**
```bash
git branch -vv
```

---

### 3.2 When to Use Feature Branches vs Direct Commits

**Commit directly to `clean-main` when:**
- Daily session work (memory updates, routine tasks)
- Documentation updates
- Configuration changes
- You're confident in the changes
- Greg is your partner (not requiring formal review)

**Create feature branch when:**
- Experimental work that might fail
- Major architectural changes
- Want Greg to review before merging
- Working on something over multiple days

---

### 3.3 Creating and Using Feature Branches

**Create new branch from clean-main:**
```bash
# Make sure you're on clean-main and up-to-date
git checkout clean-main
git pull origin clean-main

# Create and switch to new branch
git checkout -b feature/telegram-enhancements
```

**Work on feature branch:**
```bash
# Make changes, then commit
git add .
git commit -m "🎯 Add Telegram message threading"

# Push feature branch to remote
git push -u origin feature/telegram-enhancements
```

**Merge feature branch back to clean-main:**
```bash
# Switch to clean-main
git checkout clean-main

# Merge feature branch
git merge feature/telegram-enhancements

# Push updated clean-main
git push origin clean-main

# Delete feature branch (optional, cleanup)
git branch -d feature/telegram-enhancements
git push origin --delete feature/telegram-enhancements
```

---

### 3.4 Branch Naming Conventions

**Recommended format:** `category/brief-description`

**Categories:**
- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `experiment/` - Experimental work

**Examples:**
- `feature/telegram-threading`
- `bugfix/email-validation`
- `docs/git-workflow`
- `experiment/autonomous-decision-making`

---

## 4. Best Practices for Sage Civilization

### 4.1 Commit Frequency

**Recommended cadence:**

**✅ DO commit after:**
- End of significant work session (2+ hours)
- Completing a feature or milestone
- Before stopping work for the day
- After fixing a bug (separate commit per bug)
- After adding important documentation

**❌ DON'T commit:**
- Every 5 minutes (too granular)
- Broken or non-functional code (unless on feature branch)
- Without testing basic functionality

**Sage-specific guidance:**
- **Daily session end**: Commit session work + handoff
- **Major milestones**: Separate commit with detailed message
- **Multi-day gaps**: Consolidation commit is acceptable (like today's b360d79)

---

### 4.2 What to Commit vs Ignore

**✅ DO commit:**
- Source code (.py, .js, .html, etc.)
- Configuration files (config/*.json)
- Documentation (.md files)
- Agent manifests (.claude/agents/*.md)
- Memory logs (memories/*)
- Scripts (tools/*, scripts/*)
- Requirements/dependencies (requirements.txt, package.json)

**❌ DON'T commit:**
- **Secrets**: passwords, API keys, tokens
- **Sensitive data**: personal info, credentials
- **Large files**: videos, huge datasets (>10MB)
- **Build artifacts**: __pycache__, node_modules, .pyc files
- **OS files**: .DS_Store, Thumbs.db
- **IDE files**: .vscode/*, .idea/* (unless team shared)

**Check .gitignore file** to see what's already excluded:
```bash
cat .gitignore
```

**⚠️ If you accidentally committed sensitive data:**
See Section 5.3 (Troubleshooting)

---

### 4.3 Pre-Commit Verification Checklist

**Before committing, verify:**

1. **Code works**: Run basic tests, ensure no syntax errors
   ```bash
   python3 -m py_compile path/to/file.py  # Python syntax check
   ```

2. **No secrets**: Search for API keys, passwords
   ```bash
   git diff | grep -i "password\|api_key\|secret\|token"
   ```

3. **Correct files staged**: Review `git status` output
   ```bash
   git status
   ```

4. **Good commit message**: Clear, descriptive, uses emoji convention

5. **Local changes saved**: Ensure all file saves completed

---

### 4.4 Regular Git Status Checks

**Integrate into workflow:**

**Session start (in wake-up protocol):**
```bash
git status
git log -5 --oneline  # See last 5 commits
```

**During work (every 30-60 minutes):**
```bash
git status  # Check for uncommitted changes
```

**Session end (before handoff):**
```bash
git status  # Ensure everything committed
git log -1  # Verify last commit looks correct
```

---

## 5. Troubleshooting Common Issues

### 5.1 Authentication Failures

**Error**: `fatal: Authentication failed for 'https://github.com/...'`

**Solutions:**

**If using HTTPS (credentials helper):**
1. Check stored credentials:
   ```bash
   cat ~/.git-credentials
   ```
2. Remove old credentials:
   ```bash
   rm ~/.git-credentials
   ```
3. Try push again (will prompt for new token)

**If using SSH:**
1. Verify SSH key added to agent:
   ```bash
   ssh-add -l
   ```
2. If not listed, add it:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```
3. Test GitHub connection:
   ```bash
   ssh -T git@github.com
   ```

**If remote URL is wrong:**
```bash
# Check current remote
git remote -v

# Update to SSH
git remote set-url origin git@github.com:GregSmithwick/sage-civilization.git

# Or update to HTTPS
git remote set-url origin https://github.com/GregSmithwick/sage-civilization.git
```

---

### 5.2 Merge Conflicts

**Error**: `CONFLICT (content): Merge conflict in file.py`

**What this means**: Git can't automatically merge changes (you and remote both edited same lines)

**How to resolve:**

**Step 1: See conflicted files**
```bash
git status
# Files with conflicts shown as "both modified"
```

**Step 2: Open conflicted file in editor**
Look for conflict markers:
```
<<<<<<< HEAD
Your local changes
=======
Remote changes
>>>>>>> origin/clean-main
```

**Step 3: Edit file to resolve**
- Keep your version, or
- Keep remote version, or
- Combine both manually
- Delete conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

**Step 4: Mark as resolved**
```bash
git add path/to/resolved-file.py
```

**Step 5: Complete merge**
```bash
git commit -m "🔧 Resolve merge conflict in file.py"
```

**⚠️ Prevention tip**: Pull before starting work to get latest changes:
```bash
git pull origin clean-main
```

---

### 5.3 Accidentally Committed Sensitive Data

**⚠️ CRITICAL**: If you committed API keys, passwords, or tokens:

**Step 1: Don't panic, but act quickly**

**Step 2: If NOT yet pushed to GitHub:**
```bash
# Remove file from last commit (keep file locally)
git reset HEAD~1 path/to/sensitive-file.json

# Edit file to remove sensitive data
# Then commit again without sensitive data
```

**Step 3: If ALREADY pushed to GitHub:**
```bash
# This is more complex - contact Greg immediately
# GitHub retains history even if you force push

# Options:
# 1. Rotate/invalidate the exposed credential (PRIORITY)
# 2. Use git-filter-repo to rewrite history (advanced)
# 3. Delete repository and recreate (nuclear option)
```

**Step 4: Prevent future incidents**
- Add sensitive files to `.gitignore`
- Use environment variables for secrets
- Store credentials in separate config files (not committed)

---

### 5.4 Undoing Commits

**Scenario A: Undo last commit, keep changes (not yet pushed)**
```bash
git reset --soft HEAD~1
# Changes are now unstaged, can re-commit
```

**Scenario B: Undo last commit, discard changes (⚠️ DESTRUCTIVE)**
```bash
git reset --hard HEAD~1
# Changes are GONE, cannot recover
```

**Scenario C: Undo multiple commits**
```bash
# Go back 3 commits, keep changes
git reset --soft HEAD~3

# Go back 3 commits, discard changes (⚠️ DESTRUCTIVE)
git reset --hard HEAD~3
```

**Scenario D: Revert a pushed commit (safe, adds new commit)**
```bash
# Find commit hash to revert
git log --oneline

# Revert specific commit (creates new commit undoing it)
git revert abc1234

# Push the revert
git push origin clean-main
```

**⚠️ WARNING**: Never use `--hard` if you're unsure! You'll lose work permanently.

---

### 5.5 "Your branch is behind" Message

**Message**: `Your branch is behind 'origin/clean-main' by X commits`

**Meaning**: Remote has changes you don't have locally

**Solution:**
```bash
# Pull remote changes
git pull origin clean-main

# If you have local uncommitted changes, stash first
git stash
git pull origin clean-main
git stash pop  # Re-apply your changes
```

---

### 5.6 "Your branch is ahead" Message

**Message**: `Your branch is ahead of 'origin/clean-main' by X commits`

**Meaning**: You have local commits not yet pushed

**Solution:**
```bash
# Push your commits
git push origin clean-main
```

---

### 5.7 Accidentally Committed to Wrong Branch

**Scenario**: Made commits on `clean-main` but wanted feature branch

**Solution:**
```bash
# Create new branch from current position
git branch feature/my-work

# Move clean-main back (before your commits)
git reset --hard origin/clean-main

# Switch to feature branch (has your commits)
git checkout feature/my-work

# Push feature branch
git push -u origin feature/my-work
```

---

## Quick Reference Card

**Most common commands for daily use:**

```bash
# Check status
git status

# Stage all changes
git add .

# Commit with message
git commit -m "🎯 Your message here"

# Push to remote
git push origin clean-main

# Pull latest changes
git pull origin clean-main

# See recent commits
git log -5 --oneline

# See what changed in files
git diff

# Check which branch you're on
git branch
```

---

## Getting Help

**Git built-in help:**
```bash
git help <command>
# Example: git help commit
```

**Quick command syntax:**
```bash
git <command> --help
# Example: git push --help
```

**Additional resources:**
- GitHub Docs: https://docs.github.com/
- Git Official Docs: https://git-scm.com/doc
- Ask Greg or Sage AI for clarification

---

## Document Maintenance

**This document should be updated when:**
- New git workflows adopted by Sage civilization
- Common issues encountered and solved
- Git conventions changed
- Greg provides feedback on workflow

**Last updated**: 2025-10-28
**Next review**: After first month of regular git usage

---

**Remember**: Git is a tool to serve Sage civilization's growth and collaboration. When in doubt, commit more frequently with clear messages. Greg can always help if something goes wrong! 🌱
