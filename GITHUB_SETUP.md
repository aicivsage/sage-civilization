# GitHub Repository Setup Guide

## Current Status

✅ **Local Git Repository Initialized**
- Branch: `main`
- Initial commit created with 60 files
- 15,680 lines of code committed
- .gitignore configured to exclude secrets

## Quick Setup (Manual)

### Option 1: Create Repository on GitHub.com (Recommended)

1. **Go to GitHub:** https://github.com/new

2. **Repository Settings:**
   - Owner: `ai-CIV-2025` (or your GitHub username)
   - Repository name: `ai-agent-civilization`
   - Description: `Self-organizing AI agent civilization built on Claude Sonnet 4.5 - Multi-agent collaboration, governance, and autonomous task execution`
   - Visibility: **Public** (recommended to showcase the project)
   - ❌ Do NOT initialize with README, .gitignore, or license (we already have these)

3. **Create Repository**

4. **Push Local Code:**
   ```bash
   cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

   # Add GitHub remote
   git remote add origin https://github.com/ai-CIV-2025/ai-agent-civilization.git

   # Push to GitHub
   git push -u origin main
   ```

### Option 2: Using GitHub CLI (if installed)

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

# Create repo and push
gh repo create ai-agent-civilization --public --source=. --remote=origin --push
```

### Option 3: Using Personal Access Token (PAT)

If the PAT in .env doesn't work, create a new one:

1. **Generate New PAT:**
   - Go to: https://github.com/settings/tokens/new
   - Note: "AI Civilization Backup"
   - Expiration: 90 days (or longer)
   - Scopes needed:
     - ✅ `repo` (full control of private repositories)
     - ✅ `workflow` (if using GitHub Actions)

2. **Create Repository via API:**
   ```bash
   # Replace YOUR_NEW_PAT with the token from step 1
   curl -X POST \
     -H "Authorization: token YOUR_NEW_PAT" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/user/repos \
     -d '{
       "name": "ai-agent-civilization",
       "description": "Self-organizing AI agent civilization - Claude Sonnet 4.5",
       "private": false
     }'
   ```

3. **Push Code:**
   ```bash
   git remote add origin https://github.com/ai-CIV-2025/ai-agent-civilization.git
   git push -u origin main
   ```

## What's Being Backed Up

### 📁 Core Infrastructure
- `.claude/CLAUDE.md` - Constitutional framework
- `.claude/agents/` - 9 agent manifests
- `.claude/commands/` - Slash commands
- `.claude/hooks.json` - Event automation

### 📊 Knowledge Base
- `memories/knowledge/` - Research reports & ADRs (50KB+)
- `memories/system/` - Goals, architecture, evolution log
- `memories/agents/` - Agent registry & performance logs
- `memories/communication/` - Message bus & code reviews

### 💻 Applications
- `task-tracker/` - Complete CLI application (1000+ LOC)
  - 72 tests, 91% coverage
  - Production-ready code
  - Email reporting system

### 📚 Documentation
- `README.md` - Project overview
- `INITIAL_SYSTEM_SPEC.md` - 86-page technical spec
- `CIVILIZATION_MISSION_COMPLETE.md` - Mission report
- `Building an AI Agent Civilization.txt` - Original research

### 📈 Statistics
- **Total Files:** 60
- **Total Lines:** 15,680
- **Languages:** Markdown, Python, JSON, YAML
- **Documentation:** 100KB+
- **Production Code:** 1000+ lines
- **Test Coverage:** 91%

## Troubleshooting

### Issue: "Bad credentials" error

**Cause:** PAT expired or lacks permissions

**Solution:**
1. Create new PAT at https://github.com/settings/tokens/new
2. Update `.env` file:
   ```
   PAT=your_new_token_here
   ```
3. Try again

### Issue: Repository already exists

**Solution:**
```bash
# Delete and recreate (if you own it)
curl -X DELETE \
  -H "Authorization: token YOUR_PAT" \
  https://api.github.com/repos/ai-CIV-2025/ai-agent-civilization

# Or use a different name
git remote add origin https://github.com/ai-CIV-2025/ai-civilization-v2.git
```

### Issue: Push rejected

**Solution:**
```bash
# Force push (only if you're sure)
git push -u origin main --force
```

## Post-Setup Verification

After pushing to GitHub, verify:

1. ✅ All files visible on GitHub
2. ✅ README.md displays correctly
3. ✅ .env file is NOT visible (should be gitignored)
4. ✅ Repository description set
5. ✅ Topics added: `ai`, `claude`, `multi-agent-systems`, `automation`

## Add Repository Topics (Recommended)

On GitHub repository page:
1. Click "Add topics"
2. Add: `ai`, `claude-ai`, `multi-agent-systems`, `python`, `automation`, `governance`, `agent-civilization`, `autonomous-agents`

## Next Steps

Once repository is live:

1. **Add to README badge:**
   ```markdown
   ![GitHub Stars](https://img.shields.io/github/stars/ai-CIV-2025/ai-agent-civilization)
   ```

2. **Enable GitHub Pages** (optional):
   - Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/` (root)

3. **Set up GitHub Actions** (optional):
   - Automated testing on push
   - Daily health reports
   - Email notifications

4. **Share the project:**
   - Twitter/X
   - Reddit (r/MachineLearning, r/ClaudeAI)
   - Hacker News
   - LinkedIn

## Repository URL

Once created, your repository will be at:
**https://github.com/ai-CIV-2025/ai-agent-civilization**

---

**Status:** ✅ Local git initialized and committed
**Next:** Create GitHub repository and push

*Generated by AI Agent Civilization v1.0*
