#!/usr/bin/env python3
"""
Memory Federation Layer for AI-CIV Collective

Enables cross-collective knowledge sharing with Ed25519 signatures.
Supports export, import, and sync workflows with trust verification.

Author: The Conductor & API Architect
Version: 1.0.0
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import shutil


# Try to import Ed25519 signer if available
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from sign_message import Ed25519Signer, sign_hub_message, verify_hub_message
    ED25519_AVAILABLE = True
except ImportError:
    ED25519_AVAILABLE = False
    print("Warning: Ed25519 signing not available. Install cryptography package.")


class FederationError(Exception):
    """Raised when federation operations fail."""
    pass


class KnowledgePackage:
    """Represents a knowledge package for export/import."""

    def __init__(self, source_collective_id: str, source_collective_name: str,
                 source_repo: str):
        """Initialize knowledge package.

        Args:
            source_collective_id: Source collective ID
            source_collective_name: Source collective name
            source_repo: Source repository URL
        """
        self.package_id = self._generate_package_id()
        self.version = "1.0"
        self.created = datetime.now(timezone.utc).isoformat()
        self.source = {
            'collective_id': source_collective_id,
            'collective_name': source_collective_name,
            'repo': source_repo
        }
        self.visibility = "public"
        self.topics = []
        self.insights = []

    def _generate_package_id(self) -> str:
        """Generate unique package ID (ULID-style)."""
        # Simplified ULID generation
        timestamp = int(datetime.now().timestamp() * 1000)
        random_part = os.urandom(10).hex()[:16]
        return f"{timestamp:013x}{random_part}".upper()

    def add_insight(self, memory_entry: Dict[str, Any]):
        """Add memory entry as insight to package.

        Args:
            memory_entry: Memory entry dict (metadata + content)
        """
        insight = {
            'id': hashlib.md5(memory_entry['content'].encode()).hexdigest()[:16],
            'type': memory_entry['type'],
            'title': self._extract_title(memory_entry['content']),
            'created': memory_entry.get('created', datetime.now(timezone.utc).isoformat()),
            'author': {
                'agent_id': memory_entry['agent'],
                'agent_role': 'specialist'  # Could extract from agent metadata
            },
            'confidence': memory_entry['confidence'],
            'tags': memory_entry['tags'],
            'summary': self._extract_summary(memory_entry['content']),
            'body': memory_entry['content'],
            'evidence': memory_entry.get('evidence', []),
            'related': [],  # Could extract from connections
            'contradicts': memory_entry.get('contradicts', []),
            'metadata': {
                'language': 'en',
                'license': 'CC0-1.0'
            }
        }

        self.insights.append(insight)

        # Update topics
        for tag in memory_entry['tags']:
            if tag not in self.topics:
                self.topics.append(tag)

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled"

    def _extract_summary(self, content: str) -> str:
        """Extract first paragraph as summary."""
        # Skip headers, get first paragraph
        lines = content.split('\n')
        in_paragraph = False
        summary_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                if in_paragraph:
                    break
                continue

            if line.startswith('#'):
                continue

            in_paragraph = True
            summary_lines.append(line)

            if len(' '.join(summary_lines)) > 200:
                break

        summary = ' '.join(summary_lines)
        if len(summary) > 200:
            summary = summary[:197] + '...'

        return summary or "No summary available"

    def to_dict(self) -> Dict[str, Any]:
        """Convert package to dict for JSON serialization."""
        return {
            'version': self.version,
            'package_id': self.package_id,
            'created': self.created,
            'expires': None,
            'source': self.source,
            'visibility': self.visibility,
            'topics': self.topics,
            'insights': self.insights
        }


class FederationClient:
    """Client for federated knowledge sharing."""

    # Trust levels
    TRUST_VERIFIED = 'verified'
    TRUST_PROVISIONAL = 'provisional'
    TRUST_UNKNOWN = 'unknown'

    def __init__(self, base_dir: str = ".claude/memory",
                 knowledge_dir: str = "knowledge"):
        """Initialize federation client.

        Args:
            base_dir: Memory base directory
            knowledge_dir: Knowledge packages directory
        """
        self.base_dir = Path(base_dir)
        self.knowledge_dir = Path(knowledge_dir)

        # Create directory structure
        self.packages_dir = self.knowledge_dir / "packages" / "public"
        self.federated_dir = self.knowledge_dir / "federated"
        self.quarantine_dir = self.knowledge_dir / "federated" / "quarantine"

        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.federated_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

        # Load trust registry
        self.trust_registry = self._load_trust_registry()

    def _load_trust_registry(self) -> Dict[str, str]:
        """Load trust registry from file.

        Returns:
            Dict of collective_id -> trust_level
        """
        registry_file = self.knowledge_dir / "trust-registry.json"
        if registry_file.exists():
            return json.loads(registry_file.read_text())

        # Default registry
        default_registry = {
            'ai-civ-team-1': self.TRUST_VERIFIED,
            'ai-civ-team-2': self.TRUST_VERIFIED,
        }

        # Save default
        registry_file.write_text(json.dumps(default_registry, indent=2))
        return default_registry

    def export_memories(self, agent: Optional[str] = None,
                       visibility: str = "public",
                       topics: Optional[List[str]] = None,
                       sign: bool = True) -> Dict[str, Any]:
        """Export memories as knowledge package.

        Args:
            agent: Agent whose memories to export (None = all)
            visibility: Visibility filter
            topics: Topic filter (None = all)
            sign: Whether to sign package with Ed25519

        Returns:
            Knowledge package dict
        """
        # Create package
        package = KnowledgePackage(
            source_collective_id='ai-civ-team-1',
            source_collective_name='AI-CIV Collective Team 1',
            source_repo='https://github.com/AI-CIV-2025/ai-civ-collective'
        )

        # Collect memories
        search_dir = self.base_dir / "agent-learnings"
        if agent:
            search_dir = search_dir / agent

        for md_file in search_dir.rglob("*.md"):
            if '.indexes' in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding='utf-8')
                if '---' not in content:
                    continue

                # Parse metadata
                import yaml
                parts = content.split('---', 2)
                if len(parts) < 3:
                    continue

                metadata = yaml.safe_load(parts[1])
                metadata['content'] = parts[2].strip()

                # Apply filters
                if visibility and metadata.get('visibility') != visibility:
                    continue

                if topics:
                    if not any(t in metadata.get('tags', []) for t in topics):
                        continue

                # Add to package
                package.add_insight(metadata)

            except Exception as e:
                print(f"Warning: Could not export {md_file}: {e}")
                continue

        # Convert to dict
        package_dict = package.to_dict()

        # Sign if requested and available
        if sign and ED25519_AVAILABLE:
            package_dict = self._sign_package(package_dict)

        return package_dict

    def _sign_package(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """Sign package with Ed25519.

        Args:
            package: Package dict to sign

        Returns:
            Package with signature
        """
        # Look for private key
        key_paths = [
            Path.home() / ".aiciv" / "agent-key.pem",
            Path(".aiciv") / "agent-key.pem",
        ]

        private_key = None
        for key_path in key_paths:
            if key_path.exists():
                private_key = key_path.read_text()
                break

        if not private_key:
            print("Warning: No private key found for signing")
            return package

        # Sign package
        try:
            signer = Ed25519Signer.from_private_key(private_key)
            signed_package = sign_hub_message(package, signer)
            return signed_package
        except Exception as e:
            print(f"Warning: Could not sign package: {e}")
            return package

    def save_package(self, package: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save package to file.

        Args:
            package: Package dict
            filename: Optional custom filename

        Returns:
            Path to saved file
        """
        if not filename:
            # Generate filename
            date = datetime.now().strftime("%Y-%m-%d")
            topic = package['topics'][0] if package['topics'] else 'knowledge'
            filename = f"knowledge-package-{date}-{topic}.json"

        filepath = self.packages_dir / filename
        filepath.write_text(json.dumps(package, indent=2))

        return str(filepath.absolute())

    def import_memories(self, package_file: str, verify: bool = True,
                       quarantine: bool = True) -> int:
        """Import knowledge package from file.

        Args:
            package_file: Path to package JSON file
            verify: Whether to verify Ed25519 signature
            quarantine: Whether to quarantine for review

        Returns:
            Number of memories imported

        Raises:
            FederationError: If import fails
        """
        # Load package
        package_path = Path(package_file)
        if not package_path.exists():
            raise FederationError(f"Package not found: {package_file}")

        package = json.loads(package_path.read_text())

        # Verify signature if requested
        if verify and 'signature' in package:
            if not ED25519_AVAILABLE:
                raise FederationError("Ed25519 verification not available")

            if not verify_hub_message(package):
                raise FederationError("Signature verification failed")

        # Check trust level
        source_id = package['source']['collective_id']
        trust_level = self.trust_registry.get(source_id, self.TRUST_UNKNOWN)

        # Determine import location
        if quarantine or trust_level == self.TRUST_UNKNOWN:
            import_dir = self.quarantine_dir / source_id
        else:
            import_dir = self.federated_dir / source_id

        import_dir.mkdir(parents=True, exist_ok=True)

        # Import insights as memories
        imported_count = 0

        for insight in package['insights']:
            try:
                # Convert insight to memory format
                memory_content = self._insight_to_memory(insight, package['source'])

                # Generate filename
                date = insight['created'].split('T')[0]
                topic = insight['id']
                filename = f"{date}--federated-{topic}.md"
                filepath = import_dir / filename

                # Write memory
                filepath.write_text(memory_content)
                imported_count += 1

            except Exception as e:
                print(f"Warning: Could not import insight {insight.get('id')}: {e}")
                continue

        return imported_count

    def _insight_to_memory(self, insight: Dict[str, Any], source: Dict[str, str]) -> str:
        """Convert federated insight to memory format.

        Args:
            insight: Insight dict from package
            source: Source collective info

        Returns:
            Markdown memory content
        """
        import yaml

        # Build metadata
        metadata = {
            'date': insight['created'].split('T')[0],
            'agent': f"federated-{insight['author']['agent_id']}",
            'type': insight['type'],
            'topic': insight['title'].lower().replace(' ', '-'),
            'tags': insight['tags'],
            'confidence': insight['confidence'],
            'visibility': 'collective-only',  # Federated knowledge is not public by default
            'quality_score': 0,  # Will be scored locally
            'reuse_count': 0,
            'created': insight['created'],
            'last_accessed': datetime.now(timezone.utc).isoformat(),
            'content_hash': '',
            'source': source,
        }

        # Format as YAML frontmatter + markdown
        frontmatter = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
        body = insight['body']

        return f"---\n{frontmatter}---\n\n{body}"

    def sync(self, collective_id: str) -> Dict[str, int]:
        """Sync with trusted collective.

        Args:
            collective_id: Collective to sync with

        Returns:
            Sync statistics
        """
        # Check trust level
        trust_level = self.trust_registry.get(collective_id, self.TRUST_UNKNOWN)
        if trust_level not in [self.TRUST_VERIFIED, self.TRUST_PROVISIONAL]:
            raise FederationError(f"Cannot sync with untrusted collective: {collective_id}")

        # TODO: Implement actual sync logic (would require network access)
        # For now, this is a placeholder

        return {
            'imported': 0,
            'exported': 0,
            'conflicts': 0
        }


# Test functions
def test_knowledge_package():
    """Test knowledge package creation."""
    print("Testing knowledge package...")

    package = KnowledgePackage(
        source_collective_id='test-collective',
        source_collective_name='Test Collective',
        source_repo='https://github.com/test/test'
    )

    # Add test insight
    memory_entry = {
        'agent': 'test-agent',
        'type': 'pattern',
        'topic': 'jwt-auth',
        'tags': ['auth', 'jwt'],
        'confidence': 'high',
        'content': '# JWT Pattern\n\nTest content.',
        'created': datetime.now(timezone.utc).isoformat()
    }

    package.add_insight(memory_entry)

    # Convert to dict
    package_dict = package.to_dict()

    assert len(package_dict['insights']) == 1
    assert 'jwt-auth' in str(package_dict['insights'][0]['title']).lower() or 'jwt' in package_dict['topics']
    print("✅ Knowledge package created")


def test_export_import():
    """Test export and import."""
    print("\nTesting export/import...")

    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    knowledge_dir = tempfile.mkdtemp()

    try:
        # Create test memory
        agent_dir = Path(temp_dir) / "agent-learnings" / "test-agent"
        agent_dir.mkdir(parents=True)

        memory_content = """---
date: 2025-10-03
agent: test-agent
type: pattern
topic: jwt-auth
tags: [authentication, jwt]
confidence: high
visibility: public
---

# JWT Pattern

Test memory for export.
"""
        memory_file = agent_dir / "2025-10-03--pattern-jwt-auth.md"
        memory_file.write_text(memory_content)

        # Export
        client = FederationClient(temp_dir, knowledge_dir)
        package = client.export_memories(agent='test-agent', sign=False)

        assert len(package['insights']) == 1
        print(f"✅ Exported {len(package['insights'])} insights")

        # Save package
        package_file = client.save_package(package, "test-package.json")
        assert Path(package_file).exists()
        print(f"✅ Package saved to {package_file}")

        # Import
        imported = client.import_memories(package_file, verify=False, quarantine=True)
        assert imported == 1
        print(f"✅ Imported {imported} memories")

    finally:
        shutil.rmtree(temp_dir)
        shutil.rmtree(knowledge_dir)


if __name__ == "__main__":
    test_knowledge_package()
    test_export_import()
    print("\n🎉 All federation tests passed!")
