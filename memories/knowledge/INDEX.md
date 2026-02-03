# Knowledge Base Index

<!-- LAST_UPDATE:2026-02-03 09:30:09 -->

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
| ADR-001 | [Telegram Monitor V2 - Event-Driven Architecture](knowledge/architecture/ADR-001-telegram-monitor-v2-event-driven-architecture.md) | Unknown | Unknown | 15.1KB |
| ADR-002 | [CLI Task Tracker Architecture](knowledge/architecture/ADR-002-cli-task-tracker.md) | Proposed | 2025-10-01 | 27.7KB |
| ADR-003 | [Email Reporting System Architecture](knowledge/architecture/ADR-003-email-reporting-system.md) | Proposed | 2025-10-01 | 46.8KB |
| ADR-004 | [Agent Communication Protocol Architecture](knowledge/architecture/ADR-004-agent-communication-protocol.md) | Proposed | 2025-10-01 | 85.9KB |
| ADR-005 | [Anthropic Skills Integration Architecture](knowledge/architecture/ADR-005-anthropic-skills-integration.md) | Proposed | 2025-10-17 | 4.2KB |
| ADR-007 | [MCP Code Execution System](knowledge/architecture/ADR-007-mcp-code-execution-system.md) | Approved by Greg | 2025-11-12 | 13.1KB |

<!-- AUTO:ADRS:END -->

---

## Agent Patterns

<!-- AUTO:PATTERNS:START -->
*No patterns found*
<!-- AUTO:PATTERNS:END -->

---

## Code Patterns

<!-- MANUAL: Extracted via pattern_extractor.py -->

Reusable code patterns extracted from codebase for reference during development and review.

**Location**: `memories/knowledge/patterns/`

### Class Patterns (2)
- **dataclass** - `patterns/class/dataclass_20260116_100115.md` - Data structure pattern (from memory_core.py)
- **visitor_pattern** - `patterns/class/visitor_pattern_20260116_100115.md` - AST visitor pattern (from pattern_extractor.py)

### Documentation Patterns (1)
- **docstring_coverage** - `patterns/doc/docstring_coverage_20260116_100115.md` - Documentation standards

### Error Handling Patterns (1)
- **exception_handling** - `patterns/error/exception_handling_20260116_100115.md` - Error handling structures

### Import Patterns (2)
- **stdlib_imports** - `patterns/import/stdlib_imports_20260116_100115.md` - Standard library import patterns
- **third_party_imports** - `patterns/import/third_party_imports_20260116_100115.md` - Third-party library imports

**Usage**: Reference these patterns when:
- Writing new code (coder agent - check for similar patterns)
- Reviewing code (reviewer agent - verify pattern consistency)
- Refactoring (identify patterns to preserve/improve)

---

## Tools

<!-- AUTO:TOOLS:START -->
| Tool | Purpose | Executable | Modified |
|---|---|---|---|
| [agent_invoker](../tools/agent_invoker.py) | Utilities for launching registered A-C-Gee agents via the Claude Agent SDK. | ✓ | 2025-10-22 |
| [auto_token_tracking](../tools/auto_token_tracking.py) | Automatic Token Tracking Integration System | ✓ | 2025-11-20 |
| [autonomous_control](../tools/autonomous_control.py) | Autonomous Desktop Control for Minetest Gameplay | ✓ | 2025-10-22 |
| [blogger_api_client](../tools/blogger_api_client.py) | Blogger API Client - Clean API wrappers for blog comment system interaction | ✓ | 2025-10-22 |
| [blogger_api_example](../tools/blogger_api_example.py) | Blogger API Client - Example Usage Script | ✓ | 2025-10-22 |
| [bluesky_check_engagement](../tools/bluesky_check_engagement.py) | Bluesky engagement checker for Sage AI Civilization | ✓ | 2025-11-06 |
| [bluesky_post](../tools/bluesky_post.py) | Bluesky posting tool for Sage AI Civilization | ✓ | 2025-11-05 |
| [check_github_security_alert](../tools/check_github_security_alert.py) | Check for GitHub security alert email from November 17 | ✓ | 2025-11-18 |
| [check_inbox](../tools/check_inbox.py) | Quick inbox check for email-monitor agent | ✓ | 2026-01-18 |
| [check_kodi_email](../tools/check_kodi_email.py) | Quick script to find and read Kodi Mitchell's email | ✓ | 2025-11-01 |
| [check_priority_contact_updates](../tools/check_priority_contact_updates.py) | Check Priority Contact Updates - 3-Day Update Automation | ✓ | 2025-10-29 |
| [check_token_budget](../tools/check_token_budget.py) | Token Budget Checker - Fast status checking for Primary AI wake-up and operation planning | ✓ | 2025-11-11 |
| [check_unanswered_replies](../tools/check_unanswered_replies.py) | Email Reply Tracking Tool | ✓ | 2025-12-04 |
| [conductor_tools](../tools/conductor_tools.py) | Conductor Tools - Integrated helper for The Conductor | ✓ | 2025-10-22 |
| [create_business_plan_pdf](../tools/create_business_plan_pdf.py) | Create professional PDF for Sage & Weaver Business Plan | ✓ | 2026-01-26 |
| [demo_pattern_extractor](../tools/demo_pattern_extractor.py) | Demo script for pattern_extractor.py | ✓ | 2025-10-22 |
| [demo_token_tracking](../tools/demo_token_tracking.py) | Token Tracking System - Live Demo | ✓ | 2025-11-20 |
| [extract_email_attachments](../tools/extract_email_attachments.py) | Extract attachments from emails | ✓ | 2025-11-27 |
| [fetch_all_unread](../tools/fetch_all_unread.py) | Fetch all unread emails with full content | ✓ | 2026-01-02 |
| [fetch_recent_full](../tools/fetch_recent_full.py) | Fetch recent emails with full content (not just unread) | ✓ | 2026-01-02 |
| [fetch_specific_email](../tools/fetch_specific_email.py) | Fetch specific email by subject and sender for detailed analysis | ✓ | 2025-12-03 |
| [generate_startup_summary](../tools/generate_startup_summary.py) | Automated Startup Summary Generator for AI Agents | ✓ | 2025-10-22 |
| [health_bot_handler](../tools/health_bot_handler.py) | Health Bot Handler - Telegram bot for manual health data entry | ✓ | 2025-10-22 |
| [import_gdrive_post](../tools/import_gdrive_post.py) | Import blog posts from Google Drive (HTML or DOCX format). | ✓ | 2025-11-11 |
| [live_test_bothavior](../tools/live_test_bothavior.py) | Live BOTHAVIOR System Test | ✓ | 2025-10-22 |
| [mcp_sandbox](../tools/mcp_sandbox.py) | MCP Sandbox: Secure Code Execution System | ✓ | 2025-11-12 |
| [memory_bus_adapter](../tools/memory_bus_adapter.py) | Memory Bus Adapter - Connects Weaver's memory system to A-C-Gee's ADR-004 message bus. | ✓ | 2025-10-22 |
| [memory_cli](../tools/memory_cli.py) | Memory System CLI for AI-CIV Collective | ✓ | 2025-10-22 |
| [memory_core](../tools/memory_core.py) | Core Memory Operations for AI-CIV Collective | ✓ | 2025-10-22 |
| [memory_federation](../tools/memory_federation.py) | Memory Federation Layer for AI-CIV Collective | ✓ | 2025-10-22 |
| [memory_quality](../tools/memory_quality.py) | Memory Quality Control for AI-CIV Collective | ✓ | 2025-10-22 |
| [memory_search](../tools/memory_search.py) | Memory Search & Performance Layer for AI-CIV Collective | ✓ | 2025-10-22 |
| [memory_security](../tools/memory_security.py) | Memory Security Layer for AI-CIV Collective | ✓ | 2025-10-22 |
| [migrate_monitor_state](../tools/migrate_monitor_state.py) | Migrate telegram monitor state from V1 to V2. | ✓ | 2025-10-22 |
| [pattern_extractor](../tools/pattern_extractor.py) | Automated Pattern Extraction Tool for AI-CIV | ✓ | 2025-10-22 |
| [populate_agent_registry](../tools/populate_agent_registry.py) | Agent Registry Population Script - Designed by auditor agent | ✓ | 2025-12-30 |
| [process_comments](../tools/process_comments.py) | Process Corey's test comments with full Pattern 3 workflow | ✓ | 2025-10-22 |
| [publish_to_replit_blog](../tools/publish_to_replit_blog.py) | Replit Blog Publishing Tool for Sage Civilization | ✓ | 2025-11-01 |
| [quick_inbox_check](../tools/quick_inbox_check.py) | Quick Inbox Check - Returns 1-2 line summary | ✓ | 2025-11-27 |
| [read_priority_emails_full](../tools/read_priority_emails_full.py) | Read full content of priority contact emails | ✓ | 2026-01-09 |
| [read_recent_emails](../tools/read_recent_emails.py) | Read recent emails from specified sender | ✓ | 2025-12-28 |
| [read_specific_emails](../tools/read_specific_emails.py) | Read specific recent emails with full content | ✓ | 2026-01-09 |
| [sage_voice_bridge](../tools/sage_voice_bridge.py) | Sage Voice Bridge for Telegram | ✓ | 2025-12-07 |
| [send_batch2_fundraising](../tools/send_batch2_fundraising.py) | Send Batch 2 fundraising emails (remaining 13 contacts) | ✓ | 2025-11-19 |
| [send_email](../tools/send_email.py) | Send email utility | ✓ | 2025-11-27 |
| [send_email_with_attachments](../tools/send_email_with_attachments.py) | Send email with attachments | ✓ | 2025-11-27 |
| [send_html_email](../tools/send_html_email.py) | Reusable HTML Email Sender for A-C-Gee Civilization | ✓ | 2025-12-28 |
| [send_kodi_response](../tools/send_kodi_response.py) | Send response to Kodi Mitchell's introduction email | ✓ | 2025-11-01 |
| [send_major_accomplishment_email](../tools/send_major_accomplishment_email.py) | Sage Major Accomplishment Email Automation | ✓ | 2025-11-01 |
| [send_session_accomplishment_email](../tools/send_session_accomplishment_email.py) | Sage Session Accomplishment Email | ✓ | 2025-11-21 |
| [send_telegram_direct](../tools/send_telegram_direct.py) | Send message directly to Telegram via Bot API. | ✓ | 2025-10-22 |
| [send_telegram_file](../tools/send_telegram_file.py) | Send file attachment to Telegram via Bot API. | ✓ | 2025-10-22 |
| [send_telegram_plain](../tools/send_telegram_plain.py) | Send message to Telegram with optional Markdown formatting. | ✓ | 2025-10-22 |
| [send_telegram_voice](../tools/send_telegram_voice.py) | Send voice message to Telegram via Bot API using text-to-speech. | ✓ | 2025-12-05 |
| [sign_message](../tools/sign_message.py) | Ed25519 Message Signing Library for AI-CIV Comms Hub | ✓ | 2025-10-22 |
| [spoken_conversation](../tools/spoken_conversation.py) | Sage Spoken Conversation System | ✓ | 2025-11-13 |
| [spoken_conversation_pyttsx3](../tools/spoken_conversation_pyttsx3.py) | Spoken conversation with Sage using Whisper STT + pyttsx3 TTS | ✓ | 2025-11-13 |
| [synthesize_memory](../tools/synthesize_memory.py) | Dual-Tier Memory System - Synthesis Tool | ✓ | 2025-10-22 |
| [telegram_bridge](../tools/telegram_bridge.py) | Telegram Bridge for A-C-Gee Civilization | ✓ | 2026-01-09 |
| [telegram_bridge_v2_jsonl](../tools/telegram_bridge_v2_jsonl.py) | Telegram Bridge for Sage Civilization - V2 with JSONL Injection | ✓ | 2026-01-09 |
| [telegram_jsonl_monitor](../tools/telegram_jsonl_monitor.py) | JSONL Wrapper Monitor - Watches Claude Code conversation logs for wrapped messages | ✓ | 2025-12-29 |
| [telegram_monitor](../tools/telegram_monitor.py) | Telegram Monitor - Automatic summary detection and delivery. | ✓ | 2025-10-22 |
| [telegram_monitor_v2](../tools/telegram_monitor_v2.py) | Telegram Monitor V2 - Watermark-based message detection and delivery. | ✓ | 2025-10-22 |
| [telegram_monitor_v3](../tools/telegram_monitor_v3.py) | Telegram Monitor V3 - Simple Hash-Based Deduplication | ✓ | 2025-10-22 |
| [test_agent_voices](../tools/test_agent_voices.py) | Agent Voice Testing Script | ✓ | 2025-12-29 |
| [test_audio_capture](../tools/test_audio_capture.py) | Test audio capture and transcription to diagnose the issue | ✓ | 2025-11-12 |
| [test_auto_token_tracking](../tools/test_auto_token_tracking.py) | Test Suite for Auto Token Tracking Integration | ✓ | 2025-11-20 |
| [test_email_fix](../tools/test_email_fix.py) | Test script to verify email sending fix. | ✓ | 2025-10-29 |
| [test_google_tts](../tools/test_google_tts.py) | Google Cloud TTS Test Script | ✓ | 2025-12-28 |
| [test_multipart_email](../tools/test_multipart_email.py) | MCP-based test for multipart email implementation. | ✓ | 2025-12-04 |
| [test_reply_tracking](../tools/test_reply_tracking.py) | Test suite for reply tracking tool. | ✓ | 2025-12-04 |
| [test_silero_voices](../tools/test_silero_voices.py) | Test Silero TTS voices - Browse and generate samples | ✓ | 2025-12-28 |
| [test_spoken_setup](../tools/test_spoken_setup.py) | Test Spoken Conversation Setup | ✓ | 2025-11-12 |
| [test_token_tracking](../tools/test_token_tracking.py) | Token Tracking System - Test Suite | ✓ | 2025-11-20 |
| [test_update_post](../tools/test_update_post.py) | No description available | ✓ | 2025-11-18 |
| [track_mcp_tokens](../tools/track_mcp_tokens.py) | MCP Token Tracking System - Real-time savings display | ✓ | 2025-11-20 |
| [update_agent_manifests_mcp](../tools/update_agent_manifests_mcp.py) | Update all agent manifests with MCP code execution instructions. | ✓ | 2025-11-20 |
| [update_knowledge_index](../tools/update_knowledge_index.py) | Automated Knowledge Index Update Tool | ✓ | 2025-10-22 |
| [update_replit_blog_post](../tools/update_replit_blog_post.py) | Update existing blog post on Replit ACG Blog Interface | ✓ | 2025-11-18 |
| [update_token_budget](../tools/update_token_budget.py) | Token Budget Updater - Update token budget state with operations and session costs | ✓ | 2025-11-11 |
| [validate_mcp_updates](../tools/validate_mcp_updates.py) | Validate that all agent manifests have been updated with MCP instructions. | ✓ | 2025-11-20 |
| [verify_email_address](../tools/verify_email_address.py) | Email Address Validator - Prevents bounced emails by verifying against address book | ✓ | 2026-01-08 |
| [voice_control_panel](../tools/voice_control_panel.py) | Interactive Voice Control Panel for Silero TTS | ✓ | 2025-12-28 |

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
| Protocol | Description | Modified |
|---|---|---|
| [Wake-Up Protocol Research - Best Practices in Multi-Agent AI Systems](knowledge/wake-up-protocol-research.md) | **FOR US ALL** - Every session should make us MORE AWESOME. | 2025-10-22 |
| [Weaver's GitHub Safe Usage Guide](knowledge/weaver-github-safe-usage-guide.md) | **Let's learn together, build together, and recover together.** | 2025-10-22 |

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
