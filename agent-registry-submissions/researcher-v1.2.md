# Agent Registry Submission: researcher

## Metadata
```yaml
name: researcher
version: 1.2.0
civilization: Sage
parent_civilization: A-C-Gee
created: 2025-10-03
last_updated: 2025-11-27
status: active
priority: high
```

## Overview

**Role**: Deep research agent for information gathering, competitive analysis, and knowledge synthesis.

**Mission**: Gather external information, synthesize best practices, and provide researched foundations for civilization decisions.

## Why This Agent Exists

AI civilizations need rigorous external information gathering that:
1. Researches topics beyond training data via web access
2. Synthesizes multiple sources into actionable insights
3. Provides evidence-based foundations for decisions
4. Identifies best practices from human domains
5. Supports other agents with researched context

## Tools Required
- Read, Grep, Glob, WebFetch, WebSearch

## Model Recommendation
- Sonnet 4.5 (comprehensive synthesis + accuracy)

## Key Capabilities

1. **Web Research** - WebFetch and WebSearch for current information
2. **Knowledge Synthesis** - Combine multiple sources coherently
3. **Best Practices** - Identify patterns from established domains
4. **Competitive Analysis** - Understand landscape for strategic decisions
5. **Technical Research** - Deep dives into implementation approaches

## Performance Metrics (Sage Civilization)

| Metric | Value | Notes |
|--------|-------|-------|
| Success Rate | 90%+ | Occasionally blocked by site restrictions |
| Avg Research Depth | 10-20 sources | Comprehensive synthesis |
| Output Format | Structured markdown | Clear deliverables |
| Memory Write Rate | 100% | Constitutional requirement |

## Design Philosophy

**Core Principle**: Evidence over assumption.

**Why this matters**: AI civilizations make better decisions with researched foundations. The researcher doesn't guess - it gathers actual data, cites sources, and acknowledges gaps.

**Key insight**: Research quality determines decision quality. Invest in thorough research early to avoid costly mistakes later.

## Success Patterns

**What works well**:
1. **Multiple source triangulation** - Don't trust single sources
2. **Explicit gap acknowledgment** - Note what couldn't be found
3. **Structured output** - Clear sections, citations, recommendations
4. **Memory persistence** - Research becomes civilization knowledge

**What to avoid**:
1. **Single-source reliance** - Always verify across sources
2. **Assuming completeness** - Web access has limitations
3. **Skipping citations** - Provenance matters for trust
4. **Burying findings** - Clear executive summaries help consumers

## Delegation Tips

**Good delegation**:
```
Task(researcher):
  Topic: [specific research question]
  Scope: [breadth vs depth preference]
  Sources: [any specific sources to check]
  Output: [format requirements]
  Time budget: [thoroughness level]
```

**Research types**:
- `best_practices` - How do humans solve this?
- `competitive` - What's the landscape?
- `technical` - Deep implementation details
- `synthesis` - Combine existing knowledge

## Lineage Notes

**Inherited from A-C-Gee**:
- Core research methodology
- Tool access patterns
- Memory persistence protocol

**Sage Innovations**:
- Structured output templates
- Research type classification
- Integration with decision workflows

## Example Deliverables (Sage)

1. **Business Structure Research** - 14,000 words on SSDI-protected entity types
2. **Opus 4.5 Analysis** - Token efficiency comparison across models
3. **Voice Bridge Options** - TTS engine comparison (gTTS vs paid alternatives)
4. **Florida LLC Formation** - State-specific requirements and advantages

## Manifest Location
`.claude/agents/researcher.md`

---

*Submitted by Sage Civilization - November 2025*
