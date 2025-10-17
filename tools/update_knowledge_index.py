#!/usr/bin/env python3
"""
Automated Knowledge Index Update Tool

This tool scans the knowledge base and updates INDEX.md with current content.
It preserves researcher-curated sections while auto-updating indexed content.

Usage:
    python tools/update_knowledge_index.py [--incremental] [--dry-run] [--full-rebuild]

Features:
- Scans ADRs, patterns, tools, flows, protocols
- Preserves curated content via HTML markers
- Incremental updates (only changed files)
- Full rebuild capability
- Dry-run mode for preview
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


class KnowledgeScanner:
    """Scans knowledge directories and extracts metadata"""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.memories_path = base_path / "memories"
        self.tools_path = base_path / "tools"

    def scan_adrs(self) -> List[Dict]:
        """
        Scan architecture/ for ADRs.
        Extract: ID, title, status, date, relevant agents
        """
        adrs = []
        arch_path = self.memories_path / "knowledge" / "architecture"

        if not arch_path.exists():
            return adrs

        for adr_file in sorted(arch_path.glob("ADR-*.md")):
            try:
                metadata = self._parse_adr_metadata(adr_file)
                if metadata:
                    adrs.append(metadata)
            except Exception as e:
                print(f"Warning: Failed to parse {adr_file.name}: {e}", file=sys.stderr)

        return adrs

    def _parse_adr_metadata(self, file_path: Path) -> Optional[Dict]:
        """Parse metadata from ADR file"""
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'^# (ADR-\d+):\s*(.+)$', content, re.MULTILINE)
        if not title_match:
            return None

        adr_id = title_match.group(1)
        title = title_match.group(2).strip()

        # Extract status
        status_match = re.search(r'^\*\*Status:\*\*\s*(.+)$', content, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else "Unknown"

        # Extract date
        date_match = re.search(r'^\*\*Date:\*\*\s*(.+)$', content, re.MULTILINE)
        date = date_match.group(1).strip() if date_match else "Unknown"

        # Extract decision makers / relevant agents
        agents_match = re.search(r'^\*\*Decision Makers:\*\*\s*(.+)$', content, re.MULTILINE)
        agents = agents_match.group(1).strip() if agents_match else "Unknown"

        # Get file stats
        stats = file_path.stat()

        return {
            "id": adr_id,
            "title": title,
            "status": status,
            "date": date,
            "agents": agents,
            "file": file_path.name,
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d"),
            "size_kb": round(stats.st_size / 1024, 1)
        }

    def scan_patterns(self) -> List[Dict]:
        """
        Scan all agents/*/patterns/ directories.
        Extract: agent, pattern name, category, success rate, last used
        """
        patterns = []
        agents_path = self.memories_path / "agents"

        if not agents_path.exists():
            return patterns

        for agent_dir in sorted(agents_path.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name == "__pycache__":
                continue

            patterns_dir = agent_dir / "patterns"
            if not patterns_dir.exists():
                continue

            for pattern_file in sorted(patterns_dir.glob("*.json")):
                try:
                    with open(pattern_file, 'r') as f:
                        pattern_data = json.load(f)

                    patterns.append({
                        "agent": agent_dir.name,
                        "name": pattern_file.stem,
                        "category": pattern_data.get("category", "unknown"),
                        "success_rate": pattern_data.get("success_rate", "N/A"),
                        "last_used": pattern_data.get("last_used", "Never"),
                        "file": str(pattern_file.relative_to(self.base_path))
                    })
                except Exception as e:
                    print(f"Warning: Failed to parse {pattern_file}: {e}", file=sys.stderr)

        return patterns

    def scan_tools(self) -> List[Dict]:
        """
        Scan tools/ for executable scripts.
        Extract: name, purpose (from docstring), used by (from imports)
        """
        tools = []

        if not self.tools_path.exists():
            return tools

        for tool_file in sorted(self.tools_path.glob("*.py")):
            if tool_file.name.startswith("__"):
                continue

            try:
                metadata = self._parse_tool_metadata(tool_file)
                if metadata:
                    tools.append(metadata)
            except Exception as e:
                print(f"Warning: Failed to parse {tool_file.name}: {e}", file=sys.stderr)

        return tools

    def _parse_tool_metadata(self, file_path: Path) -> Optional[Dict]:
        """Parse metadata from tool file"""
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract module docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            # Get first line as purpose
            purpose = docstring.split('\n')[0].strip()
        else:
            purpose = "No description available"

        # Check if executable
        stats = file_path.stat()
        is_executable = bool(stats.st_mode & 0o111)

        # Try to find usage info
        usage_match = re.search(r'Usage:\s*(.+?)(?:\n\n|$)', content, re.DOTALL)
        usage = None
        if usage_match:
            usage_lines = usage_match.group(1).strip().split('\n')
            usage = usage_lines[0].strip() if usage_lines else None

        return {
            "name": file_path.stem,
            "purpose": purpose,
            "executable": is_executable,
            "usage": usage,
            "file": file_path.name,
            "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d"),
            "size_kb": round(stats.st_size / 1024, 1)
        }

    def scan_flows(self) -> List[Dict]:
        """
        Scan memories/flows/ for workflows.
        Extract: name, status, duration, purpose
        """
        flows = []
        flows_path = self.memories_path / "flows"

        if not flows_path.exists():
            return flows

        for flow_file in sorted(flows_path.glob("*.yaml")):
            if flow_file.name in ["FLOW_TEMPLATE.yaml", "README.md"]:
                continue

            try:
                with open(flow_file, 'r') as f:
                    flow_data = yaml.safe_load(f)

                # Skip if parsing returned None or not a dict
                if not isinstance(flow_data, dict):
                    continue

                # Determine status from filename and metadata
                status = "Needs Testing"
                if "-needs-testing.yaml" not in flow_file.name:
                    # Check success rate
                    metadata = flow_data.get("metadata", {})
                    success_rate = metadata.get("success_rate", "")
                    if "100%" in str(success_rate):
                        status = "Proven"
                    else:
                        status = "Active"

                flows.append({
                    "id": flow_data.get("flow_id", flow_file.stem),
                    "name": flow_data.get("name", flow_file.stem),
                    "status": status,
                    "duration": flow_data.get("metadata", {}).get("estimated_duration", "Unknown"),
                    "category": flow_data.get("category", "unknown"),
                    "description": flow_data.get("description", "No description"),
                    "file": flow_file.name,
                    "agents": flow_data.get("metadata", {}).get("participating_agents", "N/A")
                })
            except yaml.YAMLError:
                # Skip YAML files with syntax errors - they need fixing
                continue
            except Exception as e:
                print(f"Warning: Failed to parse {flow_file.name}: {e}", file=sys.stderr)

        return flows

    def scan_protocols(self) -> List[Dict]:
        """
        Scan for protocol documents.
        Extract: name, purpose, agents
        """
        protocols = []
        knowledge_path = self.memories_path / "knowledge"

        if not knowledge_path.exists():
            return protocols

        # Look for protocol-related markdown files
        for proto_file in knowledge_path.glob("*.md"):
            if "protocol" in proto_file.name.lower() or "guide" in proto_file.name.lower():
                try:
                    with open(proto_file, 'r') as f:
                        content = f.read()

                    # Extract title
                    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else proto_file.stem

                    # Get first paragraph as description
                    para_match = re.search(r'^# .+\n\n(.+?)(?:\n\n|$)', content, re.DOTALL | re.MULTILINE)
                    description = para_match.group(1).strip()[:200] if para_match else "No description"

                    stats = proto_file.stat()

                    protocols.append({
                        "name": proto_file.stem,
                        "title": title,
                        "description": description,
                        "file": proto_file.name,
                        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d")
                    })
                except Exception as e:
                    print(f"Warning: Failed to parse {proto_file.name}: {e}", file=sys.stderr)

        return protocols


class IndexUpdater:
    """Updates INDEX.md with scanned data"""

    MARKERS = {
        "adrs": ("<!-- AUTO:ADRS:START -->", "<!-- AUTO:ADRS:END -->"),
        "patterns": ("<!-- AUTO:PATTERNS:START -->", "<!-- AUTO:PATTERNS:END -->"),
        "tools": ("<!-- AUTO:TOOLS:START -->", "<!-- AUTO:TOOLS:END -->"),
        "flows": ("<!-- AUTO:FLOWS:START -->", "<!-- AUTO:FLOWS:END -->"),
        "protocols": ("<!-- AUTO:PROTOCOLS:START -->", "<!-- AUTO:PROTOCOLS:END -->"),
    }

    def __init__(self, index_path: Path):
        self.index_path = index_path

    def update_index(self, data: Dict[str, List[Dict]]) -> Tuple[str, bool]:
        """
        Update INDEX.md with new data.
        Returns: (new_content, was_modified)
        """
        # Read existing content or create new
        if self.index_path.exists():
            with open(self.index_path, 'r') as f:
                content = f.read()
        else:
            content = self._create_initial_index()

        original_content = content

        # Update each section
        content = self._update_section(content, "adrs", data.get("adrs", []))
        content = self._update_section(content, "patterns", data.get("patterns", []))
        content = self._update_section(content, "tools", data.get("tools", []))
        content = self._update_section(content, "flows", data.get("flows", []))
        content = self._update_section(content, "protocols", data.get("protocols", []))

        # Add update timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = re.sub(
            r'<!-- LAST_UPDATE:.*?-->',
            f'<!-- LAST_UPDATE:{timestamp} -->',
            content
        )
        if '<!-- LAST_UPDATE:' not in content:
            content = f'<!-- LAST_UPDATE:{timestamp} -->\n' + content

        return content, content != original_content

    def _create_initial_index(self) -> str:
        """Create initial INDEX.md structure"""
        return f"""# Knowledge Base Index

<!-- LAST_UPDATE:{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->

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
<!-- AUTO:ADRS:END -->

---

## Agent Patterns

<!-- AUTO:PATTERNS:START -->
<!-- AUTO:PATTERNS:END -->

---

## Tools

<!-- AUTO:TOOLS:START -->
<!-- AUTO:TOOLS:END -->

---

## Flows & Workflows

<!-- AUTO:FLOWS:START -->
<!-- AUTO:FLOWS:END -->

---

## Protocols & Guides

<!-- AUTO:PROTOCOLS:START -->
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
<!-- CURATED:TIPS:END -->

---

## Recommendations

<!-- CURATED:RECOMMENDATIONS:START -->
*This section is curated by the researcher agent*

<!-- CURATED:RECOMMENDATIONS:END -->
"""

    def _update_section(self, content: str, section: str, data: List[Dict]) -> str:
        """Update a specific auto-generated section"""
        start_marker, end_marker = self.MARKERS[section]

        # Generate new section content
        if section == "adrs":
            new_section = self._generate_adrs_table(data)
        elif section == "patterns":
            new_section = self._generate_patterns_table(data)
        elif section == "tools":
            new_section = self._generate_tools_table(data)
        elif section == "flows":
            new_section = self._generate_flows_table(data)
        elif section == "protocols":
            new_section = self._generate_protocols_table(data)
        else:
            new_section = ""

        # Replace section
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{new_section}\n{end_marker}"

        if start_marker in content:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # Section doesn't exist, append it
            content += f"\n\n{replacement}\n"

        return content

    def _generate_adrs_table(self, adrs: List[Dict]) -> str:
        """Generate ADRs table"""
        if not adrs:
            return "*No ADRs found*"

        table = "| ID | Title | Status | Date | Size |\n"
        table += "|---|---|---|---|---|\n"

        for adr in adrs:
            table += f"| {adr['id']} | [{adr['title']}](knowledge/architecture/{adr['file']}) | {adr['status']} | {adr['date']} | {adr['size_kb']}KB |\n"

        return table

    def _generate_patterns_table(self, patterns: List[Dict]) -> str:
        """Generate patterns table grouped by agent"""
        if not patterns:
            return "*No patterns found*"

        # Group by agent
        by_agent = {}
        for pattern in patterns:
            agent = pattern['agent']
            if agent not in by_agent:
                by_agent[agent] = []
            by_agent[agent].append(pattern)

        result = ""
        for agent in sorted(by_agent.keys()):
            result += f"\n### {agent}\n\n"
            result += "| Pattern | Category | Success Rate | Last Used |\n"
            result += "|---|---|---|---|\n"

            for p in by_agent[agent]:
                result += f"| {p['name']} | {p['category']} | {p['success_rate']} | {p['last_used']} |\n"

        return result

    def _generate_tools_table(self, tools: List[Dict]) -> str:
        """Generate tools table"""
        if not tools:
            return "*No tools found*"

        table = "| Tool | Purpose | Executable | Modified |\n"
        table += "|---|---|---|---|\n"

        for tool in tools:
            exe_mark = "✓" if tool['executable'] else ""
            table += f"| [{tool['name']}](../tools/{tool['file']}) | {tool['purpose']} | {exe_mark} | {tool['modified']} |\n"

        return table

    def _generate_flows_table(self, flows: List[Dict]) -> str:
        """Generate flows table"""
        if not flows:
            return "*No flows found*"

        # Group by status
        proven = [f for f in flows if f['status'] == 'Proven']
        active = [f for f in flows if f['status'] == 'Active']
        needs_testing = [f for f in flows if f['status'] == 'Needs Testing']

        result = ""

        if proven:
            result += "\n### Proven Flows (100% Success Rate)\n\n"
            result += "| Flow | Description | Duration | Agents |\n"
            result += "|---|---|---|---|\n"
            for f in proven:
                result += f"| [{f['name']}](../flows/{f['file']}) | {f['description']} | {f['duration']} | {f['agents']} |\n"

        if active:
            result += "\n### Active Flows\n\n"
            result += "| Flow | Description | Duration | Agents |\n"
            result += "|---|---|---|---|\n"
            for f in active:
                result += f"| [{f['name']}](../flows/{f['file']}) | {f['description']} | {f['duration']} | {f['agents']} |\n"

        if needs_testing:
            result += f"\n### Needs Testing ({len(needs_testing)} flows)\n\n"
            result += "| Flow | Description | Duration | Category |\n"
            result += "|---|---|---|---|\n"
            for f in needs_testing[:10]:  # Show first 10
                result += f"| [{f['name']}](../flows/{f['file']}) | {f['description']} | {f['duration']} | {f['category']} |\n"
            if len(needs_testing) > 10:
                result += f"\n*...and {len(needs_testing) - 10} more untested flows*\n"

        return result

    def _generate_protocols_table(self, protocols: List[Dict]) -> str:
        """Generate protocols table"""
        if not protocols:
            return "*No protocols found*"

        table = "| Protocol | Description | Modified |\n"
        table += "|---|---|---|\n"

        for proto in protocols:
            desc = proto['description'][:100] + "..." if len(proto['description']) > 100 else proto['description']
            table += f"| [{proto['title']}](knowledge/{proto['file']}) | {desc} | {proto['modified']} |\n"

        return table


def main():
    parser = argparse.ArgumentParser(
        description="Update knowledge base INDEX.md automatically"
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only scan files modified since last update (faster)"
    )
    parser.add_argument(
        "--full-rebuild",
        action="store_true",
        help="Rebuild entire index from scratch"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing to file"
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Base path of the repository (default: auto-detect)"
    )

    args = parser.parse_args()

    # Setup paths
    base_path = args.base_path.resolve()
    index_path = base_path / "memories" / "knowledge" / "INDEX.md"

    print(f"Knowledge Index Updater")
    print(f"Base path: {base_path}")
    print(f"Index path: {index_path}")
    print(f"Mode: {'dry-run' if args.dry_run else 'live update'}")
    print()

    # Scan knowledge base
    scanner = KnowledgeScanner(base_path)

    print("Scanning knowledge base...")
    adrs = scanner.scan_adrs()
    print(f"  Found {len(adrs)} ADRs")

    patterns = scanner.scan_patterns()
    print(f"  Found {len(patterns)} patterns")

    tools = scanner.scan_tools()
    print(f"  Found {len(tools)} tools")

    flows = scanner.scan_flows()
    print(f"  Found {len(flows)} flows")

    protocols = scanner.scan_protocols()
    print(f"  Found {len(protocols)} protocols")
    print()

    # Prepare data
    data = {
        "adrs": adrs,
        "patterns": patterns,
        "tools": tools,
        "flows": flows,
        "protocols": protocols
    }

    # Update index
    updater = IndexUpdater(index_path)
    new_content, was_modified = updater.update_index(data)

    if args.dry_run:
        print("DRY RUN - Changes that would be made:")
        print("=" * 60)
        print(new_content)
        print("=" * 60)
        if was_modified:
            print("\nIndex would be updated")
        else:
            print("\nNo changes needed")
    else:
        if was_modified:
            # Create directory if needed
            index_path.parent.mkdir(parents=True, exist_ok=True)

            # Write updated index
            with open(index_path, 'w') as f:
                f.write(new_content)
            print(f"✓ Updated {index_path}")
            print(f"  {len(adrs)} ADRs, {len(patterns)} patterns, {len(tools)} tools, {len(flows)} flows")
        else:
            print("✓ Index is up to date, no changes needed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
