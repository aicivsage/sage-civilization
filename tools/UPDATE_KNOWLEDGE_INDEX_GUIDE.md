# Knowledge Index Update Tool - Usage Guide

## Overview

`update_knowledge_index.py` is an automated tool that keeps `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/knowledge/INDEX.md` up-to-date with the latest knowledge base content.

**Key Features:**
- Automatic scanning of ADRs, patterns, tools, flows, and protocols
- Preserves researcher-curated content
- Fast incremental updates (0.5s)
- Dry-run preview mode
- HTML comment markers for section management

## Quick Start

```bash
# Update the index (runs in ~0.5 seconds)
python3 tools/update_knowledge_index.py

# Preview changes without writing
python3 tools/update_knowledge_index.py --dry-run

# Incremental update (faster for large repos)
python3 tools/update_knowledge_index.py --incremental

# Full rebuild from scratch
python3 tools/update_knowledge_index.py --full-rebuild
```

## What It Scans

### 1. Architecture Decision Records (ADRs)
- **Location:** `memories/knowledge/architecture/ADR-*.md`
- **Extracts:** ID, title, status, date, decision makers, file size
- **Output:** Sortable table with links

### 2. Agent Patterns
- **Location:** `memories/agents/*/patterns/*.json`
- **Extracts:** Agent name, pattern name, category, success rate, last used
- **Output:** Tables grouped by agent

### 3. Tools
- **Location:** `tools/*.py`
- **Extracts:** Name, purpose (from docstring), executable flag, last modified
- **Output:** Table with tool descriptions

### 4. Flows & Workflows
- **Location:** `memories/flows/*.yaml`
- **Extracts:** Flow ID, name, status, duration, category, description, participating agents
- **Output:** Tables grouped by status (Proven/Active/Needs Testing)
- **Note:** YAML files with syntax errors are silently skipped

### 5. Protocols & Guides
- **Location:** `memories/knowledge/*protocol*.md`, `memories/knowledge/*guide*.md`
- **Extracts:** Title, description, last modified
- **Output:** Table with protocol descriptions

## Index Structure

The generated INDEX.md has two types of sections:

### AUTO Sections (Managed by Tool)
These are automatically updated on every run:
```markdown
<!-- AUTO:ADRS:START -->
[auto-generated content]
<!-- AUTO:ADRS:END -->
```

**Available AUTO sections:**
- `AUTO:ADRS` - Architecture Decision Records table
- `AUTO:PATTERNS` - Agent patterns grouped by agent
- `AUTO:TOOLS` - Tools table
- `AUTO:FLOWS` - Flows grouped by status
- `AUTO:PROTOCOLS` - Protocols and guides table

### CURATED Sections (Researcher-Maintained)
These are preserved across updates:
```markdown
<!-- CURATED:TIPS:START -->
[researcher's custom content - never overwritten]
<!-- CURATED:TIPS:END -->
```

**Available CURATED sections:**
- `CURATED:NAVIGATION` - Quick navigation links
- `CURATED:TIPS` - Search tips and tricks
- `CURATED:RECOMMENDATIONS` - Curated recommendations

**IMPORTANT:** Only content BETWEEN the markers is preserved. The tool will never modify text inside `<!-- CURATED:*:START -->` and `<!-- CURATED:*:END -->` markers.

## Usage Examples

### Daily Automated Update (Cron)

Add to crontab to run daily at 2 AM:
```bash
crontab -e
```

```cron
# Update knowledge index daily at 2 AM
0 2 * * * cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch && python3 tools/update_knowledge_index.py --incremental >> logs/index_update.log 2>&1
```

### Manual Update After Adding Knowledge

```bash
# Added new ADR, update index
python3 tools/update_knowledge_index.py

# Check what changed
git diff memories/knowledge/INDEX.md
```

### Preview Before Updating

```bash
# See what would change without writing
python3 tools/update_knowledge_index.py --dry-run | less
```

### Customizing Curated Sections

Edit `memories/knowledge/INDEX.md` directly:

```markdown
<!-- CURATED:TIPS:START -->
*This section is curated by the researcher agent*

**Quick searches:**
- Find ADRs: `ls memories/knowledge/architecture/`
- Find flows: `ls memories/flows/`

**My custom tip:** Use fzf for interactive search!
<!-- CURATED:TIPS:END -->
```

Run the tool again - your custom tip will be preserved:
```bash
python3 tools/update_knowledge_index.py
grep "My custom tip" memories/knowledge/INDEX.md  # Still there!
```

## Performance

Measured on repository with:
- 4 ADRs (192 KB total)
- 15 tools
- 32 flow files (some with YAML errors)
- 0 patterns, 0 protocols

**Results:**
- Incremental update: ~0.5 seconds
- Full rebuild: ~0.5 seconds
- Memory usage: <50 MB

**Scalability estimates:**
- 100 ADRs: ~1-2 seconds
- 1000 ADRs: ~5-10 seconds
- 10,000 ADRs: ~30-60 seconds

For very large repos, use `--incremental` mode.

## Incremental vs Full Rebuild

### Incremental Mode (`--incremental`)
- **When to use:** Daily automated updates
- **Speed:** Fast (only scans changed files)
- **Trade-off:** Currently scans all files (optimization TODO)

### Full Rebuild Mode (`--full-rebuild`)
- **When to use:** After major refactoring or if index is corrupted
- **Speed:** Same as incremental currently (~0.5s)
- **Guarantee:** Rebuilds entire index from scratch

**Note:** The incremental mode is currently implemented but doesn't yet filter by modified time. This optimization is planned for future versions.

## Error Handling

### YAML Syntax Errors in Flows
The tool silently skips flow files with YAML syntax errors. This is intentional - many flows are still being developed and may have syntax issues.

To see which flows were skipped, check the count:
```bash
ls memories/flows/*.yaml | wc -l  # Total files
grep "flows/" memories/knowledge/INDEX.md | wc -l  # Successfully parsed
```

### Missing Directories
If a scanned directory doesn't exist, the tool continues gracefully and returns empty results for that category.

### Corrupted Index File
If INDEX.md is corrupted, run:
```bash
# Backup old file
mv memories/knowledge/INDEX.md memories/knowledge/INDEX.md.backup

# Regenerate
python3 tools/update_knowledge_index.py --full-rebuild
```

## Integration with Other Tools

### With pattern_extractor.py
After extracting patterns:
```bash
python3 tools/pattern_extractor.py coder
python3 tools/update_knowledge_index.py  # Index automatically includes new patterns
```

### With Memory System
The index can be used as a fast lookup table for memory searches:
```bash
# Find ADRs about email
grep -i email memories/knowledge/INDEX.md

# Find tools by purpose
grep "Memory" memories/knowledge/INDEX.md
```

### With Git Hooks
Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
# Auto-update index after commits to knowledge base
if git diff-tree --name-only -r HEAD | grep -q "^memories/knowledge/"; then
    python3 tools/update_knowledge_index.py --incremental
    git add memories/knowledge/INDEX.md
    git commit --amend --no-edit
fi
```

## Troubleshooting

### Index Not Updating
**Problem:** Run the tool but index doesn't change

**Solutions:**
1. Check if content actually changed: `git diff memories/knowledge/INDEX.md`
2. The tool may have determined no update needed
3. Check timestamps: `grep LAST_UPDATE memories/knowledge/INDEX.md`

### Curated Content Lost
**Problem:** Custom content in CURATED sections disappeared

**Root Cause:** Content was outside the CURATED markers

**Solution:**
1. Always put custom content INSIDE the markers:
   ```markdown
   <!-- CURATED:TIPS:START -->
   Your content here
   <!-- CURATED:TIPS:END -->
   ```

2. Not like this:
   ```markdown
   <!-- CURATED:TIPS:END -->
   Your content here  # Will be lost!
   ```

### Performance Degradation
**Problem:** Tool takes >10 seconds to run

**Solutions:**
1. Use `--incremental` mode (once implemented fully)
2. Check for very large files in scanned directories
3. Consider breaking up large ADRs into smaller documents

### Wrong File Paths in Links
**Problem:** Links in INDEX.md are broken

**Root Cause:** Tool assumes INDEX.md is at `memories/knowledge/INDEX.md`

**Solution:**
If you moved INDEX.md, update links manually or use `--base-path`:
```bash
python3 tools/update_knowledge_index.py --base-path /custom/path
```

## Advanced Usage

### Custom Base Path
Run from different repository:
```bash
python3 update_knowledge_index.py --base-path /path/to/other/repo
```

### Automated Testing
Test the tool in CI/CD:
```bash
# In .github/workflows/test.yml
- name: Test index update
  run: |
    python3 tools/update_knowledge_index.py --dry-run
    # Should complete in <5 seconds
```

### Monitoring Changes
Track index growth over time:
```bash
# Add to monitoring script
wc -l memories/knowledge/INDEX.md >> logs/index_size_history.log
git diff --stat memories/knowledge/INDEX.md >> logs/index_changes.log
```

## Success Criteria

The tool meets its success criteria if:

- ✅ INDEX.md updated within 24h of new knowledge (via daily cron)
- ✅ Zero data loss (curated content preserved) - **VERIFIED**
- ✅ Runs in <10 seconds incremental, <30 seconds full - **0.5s measured**
- ✅ Clear diff output showing what changed - **Built-in git diff**

## Future Enhancements

Planned improvements:
1. **True incremental mode** - Only scan files modified since last run (use mtime)
2. **Statistics section** - Show knowledge base growth over time
3. **Search index** - Generate searchable index for faster lookups
4. **Multi-repo support** - Scan and merge indexes from multiple repositories
5. **Validation mode** - Check for broken links and missing files
6. **Auto-fix flows** - Attempt to fix common YAML syntax errors

## Related Tools

- `pattern_extractor.py` - Extracts patterns that this tool indexes
- `memory_cli.py` - Search and manage memories (can use INDEX.md)
- `synthesize_memory.py` - Creates synthesis documents for indexing

## Questions?

Check the tool's help:
```bash
python3 tools/update_knowledge_index.py --help
```

Or read the source code - it's well-documented!
