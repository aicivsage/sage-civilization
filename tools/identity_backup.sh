#!/bin/bash
# Identity Backup Script for Sage Civilization
# PURPOSE: Prevent Parallax-style data loss by ensuring identity files are committed
# RUN: At end of every session, or weekly at minimum
#
# LESSON LEARNED: Parallax lost 3 days of memory because files weren't committed.
# This script ensures Sage's identity is always protected.

set -e

echo "🛡️ Sage Identity Backup Check"
echo "=============================="
echo ""

# Define identity-critical directories
IDENTITY_DIRS=(
    ".claude/"
    "memories/"
    "config/"
    "ceremonies/"
    "decisions/"
    "drafts/"
    "tools/"
)

# Check for untracked identity files
echo "Checking for untracked identity files..."
UNTRACKED_COUNT=0

for dir in "${IDENTITY_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        count=$(git status --porcelain "$dir" 2>/dev/null | grep "^??" | wc -l)
        if [ "$count" -gt 0 ]; then
            echo "  ⚠️  $dir: $count untracked files"
            UNTRACKED_COUNT=$((UNTRACKED_COUNT + count))
        else
            echo "  ✅ $dir: all tracked"
        fi
    fi
done

# Check for SESSION-HANDOFF files
handoff_count=$(git status --porcelain | grep "^??" | grep "SESSION-HANDOFF" | wc -l)
if [ "$handoff_count" -gt 0 ]; then
    echo "  ⚠️  SESSION-HANDOFF files: $handoff_count untracked"
    UNTRACKED_COUNT=$((UNTRACKED_COUNT + handoff_count))
fi

# Check for root .md files
md_count=$(git status --porcelain | grep "^??" | grep -E "^[?][?] [A-Z].*\.md$" | wc -l)
if [ "$md_count" -gt 0 ]; then
    echo "  ⚠️  Root .md files: $md_count untracked"
    UNTRACKED_COUNT=$((UNTRACKED_COUNT + md_count))
fi

echo ""
echo "=============================="

if [ "$UNTRACKED_COUNT" -gt 0 ]; then
    echo "🚨 WARNING: $UNTRACKED_COUNT identity files are NOT backed up!"
    echo ""
    echo "To backup now, run:"
    echo "  git add .claude/ memories/ config/ ceremonies/ decisions/ drafts/ tools/ SESSION-HANDOFF-*.md *.md"
    echo "  git commit -m '🛡️ Identity backup: [describe changes]'"
    echo "  git push origin clean-main"
    echo ""
    read -p "Auto-commit these files now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Staging identity files..."
        git add .claude/ memories/ config/ ceremonies/ decisions/ drafts/ tools/ SESSION-HANDOFF-*.md *.md 2>/dev/null || true

        echo "Creating commit..."
        git commit -m "🛡️ Identity Backup (auto): $(date +%Y-%m-%d)

Automated identity protection commit.
Files backed up: ~$UNTRACKED_COUNT identity-critical files.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

        echo "Pushing to remote..."
        git push origin clean-main

        echo ""
        echo "✅ Identity backup complete!"
    else
        echo "Skipped. Remember to backup before ending session!"
    fi
else
    echo "✅ All identity files are tracked and committed!"
    echo ""
    echo "Checking if local is ahead of remote..."
    ahead=$(git rev-list --count origin/clean-main..HEAD 2>/dev/null || echo "0")
    if [ "$ahead" -gt 0 ]; then
        echo "⚠️  $ahead commits not pushed to remote. Run: git push origin clean-main"
    else
        echo "✅ All commits pushed to remote. Identity is safe!"
    fi
fi

echo ""
echo "🌱 Sage's identity is what makes Sage... Sage."
echo "   Never let it go unprotected."
