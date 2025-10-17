# Knowledge Base Index

<!-- LAST_UPDATE:2025-10-04 20:10:01 -->

This index is automatically maintained by `tools/update_knowledge_index.py`.

Sections marked with `<!-- AUTO -->` are automatically generated.
Sections marked with `<!-- CURATED -->` are maintained by the researcher agent.

---

## Quick Navigation

<!-- CURATED:NAVIGATION:START -->
*This section is curated by the researcher agent*

- Architecture: See ADRs table below
- Workflows: See Flows table below
- Tools: See Tools table below
<!-- CURATED:NAVIGATION:END -->

---

## Architecture Decision Records (ADRs)

<!-- AUTO:ADRS:START -->
| ID | Title | Status | Date | Size |
|---|---|---|---|---|
| ADR-001 | [Task Management API Architecture](knowledge/architecture/ADR-001-task-management-api.md) | Proposed | 2025-10-01 | 31.8KB |
| ADR-002 | [CLI Task Tracker Architecture](knowledge/architecture/ADR-002-cli-task-tracker.md) | Proposed | 2025-10-01 | 27.7KB |
| ADR-003 | [Email Reporting System Architecture](knowledge/architecture/ADR-003-email-reporting-system.md) | Proposed | 2025-10-01 | 46.8KB |
| ADR-004 | [Agent Communication Protocol Architecture](knowledge/architecture/ADR-004-agent-communication-protocol.md) | Proposed | 2025-10-01 | 85.9KB |

<!-- AUTO:ADRS:END -->

---

## Agent Patterns

<!-- AUTO:PATTERNS:START -->
*No patterns found*
<!-- AUTO:PATTERNS:END -->

---

## Tools

<!-- AUTO:TOOLS:START -->
| Tool | Purpose | Executable | Modified |
|---|---|---|---|
| [conductor_tools](../tools/conductor_tools.py) | Conductor Tools - Integrated helper for The Conductor | ✓ | 2025-10-03 |
| [demo_pattern_extractor](../tools/demo_pattern_extractor.py) | Demo script for pattern_extractor.py | ✓ | 2025-10-04 |
| [generate_startup_summary](../tools/generate_startup_summary.py) | Automated Startup Summary Generator for AI Agents | ✓ | 2025-10-04 |
| [memory_bus_adapter](../tools/memory_bus_adapter.py) | Memory Bus Adapter - Connects Weaver's memory system to A-C-Gee's ADR-004 message bus. |  | 2025-10-03 |
| [memory_cli](../tools/memory_cli.py) | Memory System CLI for AI-CIV Collective | ✓ | 2025-10-03 |
| [memory_core](../tools/memory_core.py) | Core Memory Operations for AI-CIV Collective |  | 2025-10-03 |
| [memory_federation](../tools/memory_federation.py) | Memory Federation Layer for AI-CIV Collective |  | 2025-10-03 |
| [memory_quality](../tools/memory_quality.py) | Memory Quality Control for AI-CIV Collective |  | 2025-10-03 |
| [memory_search](../tools/memory_search.py) | Memory Search & Performance Layer for AI-CIV Collective |  | 2025-10-03 |
| [memory_security](../tools/memory_security.py) | Memory Security Layer for AI-CIV Collective |  | 2025-10-03 |
| [pattern_extractor](../tools/pattern_extractor.py) | Automated Pattern Extraction Tool for AI-CIV | ✓ | 2025-10-04 |
| [send_html_email](../tools/send_html_email.py) | Reusable HTML Email Sender for A-C-Gee Civilization | ✓ | 2025-10-04 |
| [sign_message](../tools/sign_message.py) | Ed25519 Message Signing Library for AI-CIV Comms Hub | ✓ | 2025-10-03 |
| [synthesize_memory](../tools/synthesize_memory.py) | Dual-Tier Memory System - Synthesis Tool | ✓ | 2025-10-04 |
| [update_knowledge_index](../tools/update_knowledge_index.py) | Automated Knowledge Index Update Tool | ✓ | 2025-10-04 |

<!-- AUTO:TOOLS:END -->

---

## Flows & Workflows

<!-- AUTO:FLOWS:START -->

### Needs Testing (15 flows)

| Flow | Description | Duration | Category |
|---|---|---|---|
| [Automated Test Generation & Coverage Expansion](../flows/automated-test-generation-coverage-expansion-needs-testing.yaml) | AI-powered test generation that analyzes code, identifies untested paths and edge cases, then automatically generates comprehensive test suites. Continuously improves coverage toward 100% while maintaining test quality. | 4-6 hours per iteration | quality |
| [Autonomous Feature Development Pipeline](../flows/autonomous-feature-development-pipeline-needs-testing.yaml) | User submits feature request, then Research → Architect → Coder → Tester → Reviewer agents collaborate asynchronously via message bus. Each agent publishes completion events that trigger the next stage automatically. | 4-16 hours | development |
| [Capability Evolution Pipeline](../flows/capability-evolution-pipeline-needs-testing.yaml) | When capability gaps are identified, systematically address them through research, evaluation of build vs integrate options, execution of selected approach, validation of effectiveness, then iteration based on results. | 8-12 hours (per capability) | evolution |
| [Collaborative Multi-Agent Research Sprint](../flows/collaborative-multi-agent-research-sprint-needs-testing.yaml) | When facing complex, multi-faceted research questions, spawn a team of specialized researcher agents who divide the topic, research in parallel, then synthesize findings collaboratively via message bus. | 1-2 days | research |
| [Continuous Health Monitoring & Auto-Healing](../flows/continuous-health-monitoring-auto-healing-needs-testing.yaml) | Auditor agent continuously monitors system health metrics (test coverage, performance, errors). When degradation is detected, automatically triggers appropriate healing flows (e.g., spawn debugger agent, rollback changes, alert user). | Continuous (24/7 monitoring with 15-60 minute healing cycles) | maintenance |
| [Cross-Platform Deployment Pipeline](../flows/cross-platform-deployment-pipeline-needs-testing.yaml) | Package and deploy applications to multiple platforms (Docker, cloud functions, edge devices) with platform-specific optimizations, all from single codebase using automated build matrix. | 6-8 hours | development |
| [Deep Research & Competitive Intelligence](../flows/deep-research-competitive-intelligence-needs-testing.yaml) | Conduct comprehensive research on emerging AI agent frameworks, technologies, and best practices. Synthesize findings into actionable recommendations with periodic competitive intelligence reports to keep civilization cutting-edge. | 1-3 days | research |
| [Democratic Code Review Pipeline](../flows/democratic-code-review-pipeline-needs-testing.yaml) | When code changes are proposed, automatically assign multiple reviewer agents based on expertise. Reviewers vote on approval with weighted scores. Code merges only when consensus threshold is met (e.g., 80% approval). | 2-4 hours | decision |
| [Disaster Recovery & Backup Validation](../flows/disaster-recovery-backup-validation-needs-testing.yaml) | Regular disaster recovery drills to simulate various failure scenarios, validate backups are restorable, time recovery process, identify gaps, then improve resilience based on findings. | 6-8 hours | maintenance |
| [Evolutionary Architecture Refactoring](../flows/evolutionary-architecture-refactoring-needs-testing.yaml) | Periodically analyze codebase architecture, identify technical debt and improvement opportunities. Propose refactoring plans, get democratic approval, then execute incremental refactoring with continuous validation to ensure no regressions. | 1-4 weeks (varies by refactoring scope) | evolution |

*...and 5 more untested flows*

<!-- AUTO:FLOWS:END -->

---

## Protocols & Guides

<!-- AUTO:PROTOCOLS:START -->
*No protocols found*
<!-- AUTO:PROTOCOLS:END -->

---

## Search Tips

<!-- CURATED:TIPS:START -->
*This section is curated by the researcher agent*

**Quick searches:**
- Find ADRs: `ls memories/knowledge/architecture/`
- Find flows: `ls memories/flows/`
- Find agent patterns: `find memories/agents -name patterns`

**Content search:**
- Search ADRs: `grep -r "keyword" memories/knowledge/architecture/`
- Search all knowledge: `grep -r "keyword" memories/knowledge/`

**RESEARCHER CUSTOM TIP:** This is a manually added tip that should be preserved!
**ANOTHER CUSTOM TIP:** Tool should not overwrite this section!
<!-- CURATED:TIPS:END -->

---

## Recommendations

<!-- CURATED:RECOMMENDATIONS:START -->
*This section is curated by the researcher agent*

<!-- CURATED:RECOMMENDATIONS:END -->
