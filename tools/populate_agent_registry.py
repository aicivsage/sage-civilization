#!/usr/bin/env python3
"""Agent Registry Population Script - Designed by auditor agent"""

import json
import re
from pathlib import Path

# Paths
AGENTS_DIR = Path('.claude/agents')
REGISTRY_PATH = Path('memories/agents/agent_registry.json')

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter between --- markers"""
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if match:
        yaml_content = match.group(1)
        data = {}
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip() for v in value[1:-1].split(',') if v.strip()]
                data[key] = value
        return data
    return {}

def extract_metadata_from_content(content):
    """Extract metadata from markdown content"""
    metadata = {}
    role_match = re.search(r'\*\*Role\*\*:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if role_match:
        metadata['role'] = role_match.group(1).strip()
    model_match = re.search(r'\*\*Model\*\*:\s*`?(.+?)`?(?:\n|$)', content, re.IGNORECASE)
    if model_match:
        metadata['model'] = model_match.group(1).strip()
    tools_match = re.search(r'\*\*Allowed Tools\*\*:\s*`?(.+?)`?(?:\n|$)', content, re.IGNORECASE)
    if tools_match:
        tools_str = tools_match.group(1).strip()
        metadata['tools'] = [t.strip('` ') for t in tools_str.split(',')]
    return metadata

def extract_role_from_heading(content):
    """Extract role from main heading"""
    match = re.search(r'^#\s+(.+?)\s+Agent', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Unknown"

def derive_specializations(description, role):
    """Derive specializations from text"""
    text = f"{description} {role}".lower()
    keywords = [
        'research', 'code', 'test', 'review', 'audit', 'communication', 'email',
        'governance', 'vote', 'monitoring', 'health', 'analysis', 'design',
        'architecture', 'workshop', 'transcript', 'telegram', 'messaging',
        'project', 'management', 'marketing', 'seo', 'blog', 'android',
        'game', 'web', 'git', 'file', 'spawn', 'documentation', 'pathfinder',
        'forge', 'gpt', 'coordination', 'helper', 'analyst', 'player'
    ]
    return sorted(list(set([k for k in keywords if k in text])))

# Load current registry
with open(REGISTRY_PATH, 'r') as f:
    current_registry = json.load(f)

print(f"Current registry: {len(current_registry)} entries")

# Get agent manifests
agent_files = sorted([f for f in AGENTS_DIR.glob('*.md') if f.is_file() and 'memories' not in str(f)])
print(f"Found {len(agent_files)} manifests\n")

# Process manifests
new_registry = {}
new_count = 0

for agent_file in agent_files:
    agent_id = agent_file.stem
    with open(agent_file, 'r') as f:
        content = f.read()

    frontmatter = extract_yaml_frontmatter(content)
    content_meta = extract_metadata_from_content(content)
    metadata = {**content_meta, **frontmatter}

    # Start with existing or new entry
    if agent_id in current_registry:
        entry = current_registry[agent_id].copy()
        status = "UPDATE"
    else:
        entry = {'reputation': 50, 'task_count': 0, 'last_invoked': None, 'status': 'active'}
        new_count += 1
        status = "NEW"

    # Update fields
    if 'role' in metadata:
        entry['role'] = metadata['role']
    elif 'role' not in entry:
        entry['role'] = extract_role_from_heading(content)

    if 'description' in metadata:
        entry['description'] = metadata['description']
    elif 'description' not in entry:
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith(('#', '**', '---')) and len(line) > 30:
                entry['description'] = line
                break
        if 'description' not in entry:
            entry['description'] = f"{entry['role']} specialist"

    if 'model' in metadata:
        entry['model'] = metadata['model']
    elif 'model' not in entry:
        entry['model'] = 'sonnet'

    if 'tools' in metadata:
        entry['tools'] = metadata['tools']
    if 'parent_agents' in metadata:
        entry['parent_agents'] = metadata['parent_agents']

    specs = derive_specializations(entry.get('description', ''), entry.get('role', ''))
    if specs:
        entry['specializations'] = specs

    new_registry[agent_id] = entry
    print(f"  [{status}] {agent_id}: {entry['role']}")

# Sort and write
new_registry = dict(sorted(new_registry.items()))
with open(REGISTRY_PATH, 'w') as f:
    json.dump(new_registry, f, indent=2)

print(f"\n{'='*70}")
print(f"Registry populated: {len(new_registry)} agents ({new_count} new)")
print(f"Updated: {REGISTRY_PATH}")
complete = sum(1 for e in new_registry.values() if 'description' in e and 'tools' in e)
print(f"Quality: {complete}/{len(new_registry)} entries with full metadata ({100*complete/len(new_registry):.1f}%)")
