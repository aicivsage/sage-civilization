"""
Agent key management for Ed25519 signing.

This module provides centralized management of agent public keys,
loading them from the agent registry and providing lookup functionality.
"""

import json
from pathlib import Path
from typing import Dict, Optional


class AgentKeyRegistry:
    """
    Registry of agent public keys for Ed25519 signature verification.

    This class loads public keys from the agent_registry.json file
    and provides efficient lookup by agent ID.
    """

    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize agent key registry.

        Args:
            registry_path: Path to agent_registry.json file.
                          If None, searches for it in standard locations.

        Raises:
            FileNotFoundError: If registry file cannot be found
            ValueError: If registry file is invalid
        """
        if registry_path is None:
            # Search for registry in standard locations
            registry_path = self._find_registry()

        self.registry_path = Path(registry_path)
        self._keys: Dict[str, Dict[str, str]] = {}
        self._load_keys()

    def _find_registry(self) -> str:
        """
        Find agent_registry.json in standard locations.

        Returns:
            Path to registry file

        Raises:
            FileNotFoundError: If registry cannot be found
        """
        # Standard locations to search
        search_paths = [
            # Relative to current directory
            Path("memories/agents/agent_registry.json"),
            Path("../memories/agents/agent_registry.json"),
            Path("../../memories/agents/agent_registry.json"),
            # Absolute paths (assuming AI-CIV project structure)
            Path.home() / "projects/AI-CIV/grow_gemini_deepresearch/memories/agents/agent_registry.json",
        ]

        for path in search_paths:
            if path.exists():
                return str(path)

        raise FileNotFoundError(
            "Could not find agent_registry.json. "
            "Please specify registry_path explicitly."
        )

    def _load_keys(self) -> None:
        """
        Load public keys from registry file.

        Raises:
            ValueError: If registry file is invalid or missing required fields
        """
        try:
            with open(self.registry_path, 'r') as f:
                registry = json.load(f)

            # Validate registry structure
            if "agents" not in registry:
                raise ValueError("Registry file missing 'agents' field")

            # Extract keys from each agent
            for agent in registry["agents"]:
                agent_id = agent.get("id")
                public_key = agent.get("public_key")
                key_id = agent.get("key_id")

                if not agent_id:
                    continue  # Skip agents without ID

                if public_key and key_id:
                    self._keys[agent_id] = {
                        "public_key": public_key,
                        "key_id": key_id
                    }

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in registry file: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load registry: {e}")

    def get_public_key(self, agent_id: str) -> Optional[str]:
        """
        Get public key for an agent.

        Args:
            agent_id: Agent identifier (e.g., "researcher", "coder")

        Returns:
            Base64-encoded public key, or None if agent not found or has no key

        Example:
            >>> registry = AgentKeyRegistry()
            >>> key = registry.get_public_key("researcher")
            >>> print(key)  # "8sfXeKpnxq9LfB0Sr2/vgSTRpXYzYfPANuReCcKkzjE="
        """
        key_info = self._keys.get(agent_id)
        if key_info:
            return key_info["public_key"]
        return None

    def get_key_id(self, agent_id: str) -> Optional[str]:
        """
        Get key ID for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Key ID (first 8 chars of SHA256 hash), or None if not found

        Example:
            >>> registry = AgentKeyRegistry()
            >>> key_id = registry.get_key_id("researcher")
            >>> print(key_id)  # "ef33652f"
        """
        key_info = self._keys.get(agent_id)
        if key_info:
            return key_info["key_id"]
        return None

    def has_key(self, agent_id: str) -> bool:
        """
        Check if an agent has a registered public key.

        Args:
            agent_id: Agent identifier

        Returns:
            True if agent has a key, False otherwise

        Example:
            >>> registry = AgentKeyRegistry()
            >>> if registry.has_key("researcher"):
            ...     print("Researcher has a key")
        """
        return agent_id in self._keys

    def get_all_agents(self) -> list[str]:
        """
        Get list of all agents with registered keys.

        Returns:
            List of agent IDs

        Example:
            >>> registry = AgentKeyRegistry()
            >>> agents = registry.get_all_agents()
            >>> print(len(agents))  # 12
        """
        return list(self._keys.keys())

    def verify_key_id(self, agent_id: str, key_id: str) -> bool:
        """
        Verify that a key ID matches the registered key ID for an agent.

        This is useful for sanity checking when verifying signatures.

        Args:
            agent_id: Agent identifier
            key_id: Key ID to verify

        Returns:
            True if key_id matches registered key_id, False otherwise

        Example:
            >>> registry = AgentKeyRegistry()
            >>> is_valid = registry.verify_key_id("researcher", "ef33652f")
            >>> print(is_valid)  # True
        """
        registered_key_id = self.get_key_id(agent_id)
        if registered_key_id is None:
            return False
        return registered_key_id == key_id

    def reload(self) -> None:
        """
        Reload keys from registry file.

        Useful if the registry has been updated externally.

        Raises:
            ValueError: If registry file is invalid
        """
        self._keys.clear()
        self._load_keys()

    def __contains__(self, agent_id: str) -> bool:
        """
        Support 'in' operator for checking if agent has a key.

        Example:
            >>> registry = AgentKeyRegistry()
            >>> if "researcher" in registry:
            ...     print("Has key")
        """
        return self.has_key(agent_id)

    def __len__(self) -> int:
        """
        Return number of agents with registered keys.

        Example:
            >>> registry = AgentKeyRegistry()
            >>> print(len(registry))  # 12
        """
        return len(self._keys)

    def __repr__(self) -> str:
        """String representation of registry."""
        return f"AgentKeyRegistry({len(self)} agents, path={self.registry_path})"


# Module-level convenience instance
_default_registry: Optional[AgentKeyRegistry] = None


def get_default_registry() -> AgentKeyRegistry:
    """
    Get the default module-level agent key registry.

    This creates a singleton registry instance on first access.

    Returns:
        AgentKeyRegistry instance

    Example:
        >>> from agent_messaging.key_management import get_default_registry
        >>> registry = get_default_registry()
        >>> key = registry.get_public_key("researcher")
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = AgentKeyRegistry()
    return _default_registry


def get_agent_public_key(agent_id: str) -> Optional[str]:
    """
    Get public key for an agent using the default registry.

    This is a convenience function for quick lookups.

    Args:
        agent_id: Agent identifier

    Returns:
        Base64-encoded public key, or None if not found

    Example:
        >>> from agent_messaging.key_management import get_agent_public_key
        >>> key = get_agent_public_key("researcher")
    """
    return get_default_registry().get_public_key(agent_id)


def verify_agent_key_id(agent_id: str, key_id: str) -> bool:
    """
    Verify agent key ID using the default registry.

    Args:
        agent_id: Agent identifier
        key_id: Key ID to verify

    Returns:
        True if key_id matches, False otherwise

    Example:
        >>> from agent_messaging.key_management import verify_agent_key_id
        >>> is_valid = verify_agent_key_id("researcher", "ef33652f")
    """
    return get_default_registry().verify_key_id(agent_id, key_id)
