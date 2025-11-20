#!/usr/bin/env python3
"""
Validate that all agent manifests have been updated with MCP instructions.
Demonstrates MCP code execution capability.
"""

import os
import glob
import re

def validate_mcp_section(filepath):
    """Validate MCP section exists and is properly formatted."""
    with open(filepath, 'r') as f:
        content = f.read()

    agent_name = os.path.basename(filepath).replace('.md', '')

    checks = {
        'has_mcp_header': '🚀 MCP Code Execution' in content,
        'has_quick_start': 'Quick Start' in content,
        'has_capabilities': 'Your Capabilities' in content,
        'has_reference': 'MCP-USAGE-FOR-AGENTS.md' in content,
        'has_warning': 'NOT using MCP wastes' in content,
        'has_agent_name': f'execute_code("{agent_name}"' in content
    }

    return checks

def main():
    """Validate all manifests."""
    manifest_dir = '/mnt/c/sage/sage-civilization/.claude/agents'
    manifests = glob.glob(f'{manifest_dir}/*.md')

    all_valid = True
    failed_agents = []

    print('Validating MCP sections in agent manifests...\n')

    for manifest in sorted(manifests):
        agent_name = os.path.basename(manifest).replace('.md', '')
        checks = validate_mcp_section(manifest)

        # Check if all validations passed
        if all(checks.values()):
            print(f'✓ {agent_name}: All checks passed')
        else:
            print(f'✗ {agent_name}: FAILED')
            for check, passed in checks.items():
                if not passed:
                    print(f'  - Missing: {check}')
            failed_agents.append(agent_name)
            all_valid = False

    print('\n' + '='*60)
    print('VALIDATION SUMMARY')
    print('='*60)
    print(f'Total manifests: {len(manifests)}')
    print(f'Valid: {len(manifests) - len(failed_agents)}')
    print(f'Failed: {len(failed_agents)}')

    if failed_agents:
        print(f'\nFailed agents: {", ".join(failed_agents)}')
    else:
        print('\n✓ ALL MANIFESTS VALID!')

    return all_valid

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
