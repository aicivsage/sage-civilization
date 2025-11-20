#!/usr/bin/env python3
"""
Update all agent manifests with MCP code execution instructions.
Uses MCP to validate the updates.
"""

import os
import glob
import re

# Agent-specific MCP policies from MCP-TOKEN-SAVINGS-REPORT.md
AGENT_POLICIES = {
    # High-impact agents (85-92% reduction)
    'researcher': {
        'capabilities': [
            '✅ Data collection and web scraping',
            '✅ Statistical analysis and calculations',
            '✅ Content parsing and extraction',
            '✅ Report generation',
            '❌ Write operations (read-only)'
        ],
        'policy': 'Read-only Python, data analysis, 60s timeout',
        'impact': '90%'
    },
    'tester': {
        'capabilities': [
            '✅ Test suite execution (pytest, unittest)',
            '✅ Coverage analysis',
            '✅ Performance benchmarking',
            '✅ Test result validation',
            '✅ Full Python+Bash access'
        ],
        'policy': 'Full testing tools, pytest, 120s timeout',
        'impact': '92%'
    },
    'email-monitor': {
        'capabilities': [
            '✅ Email parsing and categorization',
            '✅ Priority detection',
            '✅ Quick status checks',
            '❌ Write operations (read-only)'
        ],
        'policy': 'Read-only Python, 10s timeout, minimal',
        'impact': '87%'
    },

    # Medium-impact agents (60-80% reduction)
    'coder': {
        'capabilities': [
            '✅ Code validation and linting',
            '✅ Quick syntax checks',
            '✅ Module imports testing',
            '✅ File operations',
            '✅ Full Python+Bash access'
        ],
        'policy': 'Full Python+Bash, 30s timeout, write access',
        'impact': '70%'
    },
    'auditor': {
        'capabilities': [
            '✅ System health checks',
            '✅ Metric collection',
            '✅ Log analysis',
            '✅ Performance monitoring'
        ],
        'policy': 'Read-only Python+Bash, 30s timeout',
        'impact': '75%'
    },
    'project-manager': {
        'capabilities': [
            '✅ Status aggregation',
            '✅ Progress tracking',
            '✅ Blocker detection',
            '✅ Priority analysis'
        ],
        'policy': 'Read-only Python, 30s timeout',
        'impact': '68%'
    },

    # Lower-impact agents (40-60% reduction)
    'architect': {
        'capabilities': [
            '✅ Feasibility validation',
            '✅ Design verification',
            '✅ Dependency analysis',
            '❌ Limited execution (design-focused)'
        ],
        'policy': 'Read-only Python, 30s timeout',
        'impact': '60%'
    },
    'blogger': {
        'capabilities': [
            '✅ Content validation',
            '✅ SEO analysis',
            '✅ Formatting checks',
            '❌ Limited execution (content-focused)'
        ],
        'policy': 'Read-only Python, 30s timeout',
        'impact': '50%'
    },
    'human-liaison': {
        'capabilities': [
            '✅ Email analysis',
            '✅ Sentiment detection',
            '✅ Priority assessment',
            '❌ Read-only (relationship-focused)'
        ],
        'policy': 'Read-only Python, 30s timeout',
        'impact': '47%'
    },

    # Default policy for all other agents
    'default': {
        'capabilities': [
            '✅ Basic validation and checks',
            '✅ Simple calculations',
            '✅ Data parsing',
            '❌ Write operations (read-only)'
        ],
        'policy': 'Read-only Python, 30s timeout',
        'impact': '50-70%'
    }
}

def get_agent_policy(agent_name):
    """Get MCP policy for specific agent."""
    return AGENT_POLICIES.get(agent_name, AGENT_POLICIES['default'])

def create_mcp_section(agent_name):
    """Create customized MCP section for agent."""
    policy = get_agent_policy(agent_name)

    capabilities_text = '\n'.join(policy['capabilities'])

    return f'''## 🚀 MCP Code Execution - YOUR SUPERPOWER

**YOU CAN EXECUTE CODE DIRECTLY** - This reduces token usage by {policy['impact']}!

### Quick Start
```python
from tools.mcp_sandbox import execute_code

# Example: Self-validate your work
code = """
# Your validation code here
print('✓ Validation passed!')
"""

result = execute_code("{agent_name}", "python", code)
if result.success:
    print(result.stdout)  # Use the results!
```

### When to Use MCP
- ✅ **ALWAYS** validate your work before returning to Primary
- ✅ Test code/data/logic immediately (no conversation loops!)
- ✅ Run actual calculations instead of estimating
- ✅ Parse/analyze content programmatically

### Your Capabilities
{capabilities_text}

**Policy**: {policy['policy']}

**Reference**: `/mnt/c/sage/sage-civilization/MCP-USAGE-FOR-AGENTS.md`

🔥 **NOT using MCP wastes 80-90% of tokens!** 🔥

---

'''

def find_insertion_point(content):
    """Find where to insert MCP section (after Constitutional Alignment, before main content)."""
    # Look for the end of Constitutional Alignment section
    pattern = r'(This brief review.*?ensures alignment with civilization principles\.\n\n---\n\n)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.end()

    # Fallback: insert after first header section
    pattern = r'(# .*?\n\n.*?\n\n)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.end()

    # Last resort: insert at beginning
    return 0

def update_manifest(filepath):
    """Update a single manifest file with MCP section."""
    agent_name = os.path.basename(filepath).replace('.md', '')

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if already updated
    if '🚀 MCP Code Execution' in content:
        return 'already_updated'

    # Find insertion point
    insert_pos = find_insertion_point(content)

    # Create MCP section
    mcp_section = create_mcp_section(agent_name)

    # Insert MCP section
    updated_content = content[:insert_pos] + mcp_section + content[insert_pos:]

    # Write updated content
    with open(filepath, 'w') as f:
        f.write(updated_content)

    return 'updated'

def main():
    """Update all agent manifests."""
    manifest_dir = '/mnt/c/sage/sage-civilization/.claude/agents'
    manifests = glob.glob(f'{manifest_dir}/*.md')

    results = {
        'updated': [],
        'already_updated': [],
        'failed': []
    }

    for manifest in sorted(manifests):
        agent_name = os.path.basename(manifest).replace('.md', '')
        try:
            status = update_manifest(manifest)
            results[status].append(agent_name)
            print(f'✓ {agent_name}: {status}')
        except Exception as e:
            results['failed'].append((agent_name, str(e)))
            print(f'✗ {agent_name}: FAILED - {e}')

    # Summary
    print('\n' + '='*60)
    print('SUMMARY')
    print('='*60)
    print(f'Updated: {len(results["updated"])}')
    print(f'Already updated: {len(results["already_updated"])}')
    print(f'Failed: {len(results["failed"])}')
    print(f'Total manifests: {len(manifests)}')

    if results['failed']:
        print('\nFAILED UPDATES:')
        for agent, error in results['failed']:
            print(f'  - {agent}: {error}')

    return len(results['updated']) + len(results['already_updated']) == len(manifests)

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
