# Pattern Extractor - Quick Reference

## One-Line Commands

### Extract patterns from files
```bash
python3 tools/pattern_extractor.py --files "file1.py,file2.py" --agent coder
```

### Find similar code
```bash
python3 tools/pattern_extractor.py --similarity "myfile.py" --codebase .
```

### Suggest patterns for task
```bash
python3 tools/pattern_extractor.py --task-description "your task" --suggest-from memories/agents/coder/patterns
```

### Scan recent commits
```bash
python3 tools/pattern_extractor.py --scan-recent-commits 3 --agent coder
```

### Run demo
```bash
python3 tools/demo_pattern_extractor.py
```

## Common Workflows

### Session Start
```bash
# Suggest patterns for today's task
python3 tools/pattern_extractor.py \
  --task-description "Build REST API with FastAPI" \
  --suggest-from memories/agents/coder/patterns \
  --interactive
```

### Session End
```bash
# Extract patterns from today's work
python3 tools/pattern_extractor.py \
  --scan-recent-commits 1 \
  --agent coder
```

### Code Review
```bash
# Find similar code before implementing
python3 tools/pattern_extractor.py \
  --similarity "path/to/new_file.py" \
  --codebase /path/to/codebase
```

## Output Locations

- Patterns: `memories/agents/coder/patterns/`
- By type: `patterns/{class,import,error,doc}/`
- Timestamps: All files have `_YYYYMMDD_HHMMSS.md` suffix

## Pattern Types

- `class` - Pydantic, dataclass, visitor patterns
- `import` - Standard library, third-party
- `error` - Exception handling
- `doc` - Docstring coverage
- `python` - Custom patterns

## Quick Tips

- Use `--interactive` for guided pattern selection
- Use `--auto-suggest` to show similar patterns
- Combine with git: `git diff --name-only HEAD~3 | grep '\.py$'`
- Filter by confidence: `grep "Confidence: 0.9" patterns/*/*.md`

## Help
```bash
python3 tools/pattern_extractor.py --help
```

## Documentation
See `tools/PATTERN_EXTRACTOR_GUIDE.md` for full documentation
