---
description: Generate a system health status report
allowed-tools: [Read, Task]
model: sonnet-4
---

# System Status Report Command

Generate a comprehensive health status report for the AI civilization.

## Process

1. **Invoke Auditor Agent:**
   - Use Task tool to invoke the auditor sub-agent
   - auditor will analyze all agent performance logs
   - auditor will generate daily health report

2. **Display Report:**
   - Read the latest health report from `memories/system/`
   - Present to user in readable format

3. **Highlight Key Items:**
   - Any agents with <70% success rate
   - Any critical anomalies
   - Governance activity summary
   - Population and architecture status

## Output Format

Present the auditor's report with clear formatting and highlight any items requiring human attention.
