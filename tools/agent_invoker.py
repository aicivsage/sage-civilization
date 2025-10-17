"""
Utilities for launching registered A-C-Gee agents via the Claude Agent SDK.

The real system triggers subagents through the Claude Code Task tool with
``subagent_type`` set to the agent identifier defined in
``memories/agents/agent_registry.json``.  This module mirrors that flow in
Python so Primary (or tests) can programmatically load the same registry,
construct ``ClaudeAgentOptions`` with sensible defaults, and invoke an agent.

The default ``client_factory`` creates a real ``ClaudeSDKClient`` instance.
For sandbox testing (recommended when no API access is available) supply a
custom factory that returns a fake client implementing the same async context
manager interface.  See ``tests/test_agent_invoker.py`` for an example.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Protocol

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient


class ClaudeClientProtocol(Protocol):
    """Subset of the Claude SDK client interface used by this module."""

    async def __aenter__(self) -> "ClaudeClientProtocol":
        ...

    async def __aexit__(self, exc_type, exc, tb) -> None:
        ...

    async def query(self, prompt: str) -> None:
        ...

    async def receive_messages(self) -> Iterable[Any]:
        ...


ClientFactory = Callable[[Dict[str, Any], ClaudeAgentOptions], ClaudeClientProtocol]


@dataclass
class InvocationResult:
    """Result returned after running a single agent task."""

    agent_id: str
    prompt: str
    options: ClaudeAgentOptions
    messages: list[Any]
    cost_usd: Optional[float] = None


class AgentInvoker:
    """
    Helper for spawning registered agents using the Claude Agent SDK.

    Parameters
    ----------
    registry_path:
        Path to ``agent_registry.json``.
    project_root:
        Working directory supplied to the SDK (mirrors Claude Code cwd).
    client_factory:
        Callable that produces a Claude client.  Defaults to ``ClaudeSDKClient``.
    default_permission_mode:
        Permission mode applied when agent manifest does not override it.
    default_max_turns:
        SDK ``max_turns`` fallback.
    """

    def __init__(
        self,
        registry_path: Path | str = Path("memories/agents/agent_registry.json"),
        project_root: Path | str | None = None,
        client_factory: ClientFactory | None = None,
        default_permission_mode: str = "acceptEdits",
        default_max_turns: int = 40,
    ) -> None:
        self.registry_path = Path(registry_path)
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.default_permission_mode = default_permission_mode
        self.default_max_turns = default_max_turns
        self.client_factory = client_factory or self._default_client_factory
        self._registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Dict[str, Any]]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Agent registry not found: {self.registry_path}")

        data = json.loads(self.registry_path.read_text())
        agents = {}
        for agent in data.get("agents", []):
            agent_id = agent.get("id")
            if not agent_id:
                continue
            agents[agent_id] = agent
        if not agents:
            raise ValueError("Agent registry contains no agents")
        return agents

    def list_agents(self) -> list[str]:
        """Return all registered agent identifiers."""
        return sorted(self._registry.keys())

    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Return raw config for a specific agent."""
        try:
            return self._registry[agent_id]
        except KeyError as exc:
            raise KeyError(f"Unknown agent_id '{agent_id}'") from exc

    def build_options(
        self,
        agent_id: str,
        *,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> ClaudeAgentOptions:
        """Construct ClaudeAgentOptions for a registered agent."""
        config = self.get_agent_config(agent_id)
        overrides = overrides or {}

        allowed_tools = overrides.get(
            "allowed_tools", config.get("tools", [])
        )
        permission_mode = overrides.get(
            "permission_mode", config.get("permission_mode", self.default_permission_mode)
        )
        max_turns = overrides.get("max_turns", self.default_max_turns)
        model = overrides.get("model", config.get("model"))
        cwd = overrides.get("cwd", self.project_root)

        options = ClaudeAgentOptions(
            allowed_tools=list(allowed_tools),
            permission_mode=permission_mode,
            max_turns=max_turns,
            model=model,
            cwd=str(cwd),
        )

        disallowed_tools = overrides.get("disallowed_tools") or config.get("disallowed_tools")
        if disallowed_tools:
            options.disallowed_tools = list(disallowed_tools)

        return options

    async def invoke(
        self,
        agent_id: str,
        prompt: str,
        *,
        description: str | None = None,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> InvocationResult:
        """
        Run a task with the specified agent.

        ``description`` is included for parity with the Task tool signature and
        is not currently used, but kept for future logging.
        """
        options = self.build_options(agent_id, overrides=overrides)
        agent_config = self.get_agent_config(agent_id)
        client = self.client_factory(agent_config, options)

        messages: list[Any] = []
        cost: Optional[float] = None

        async with client:
            await client.query(prompt)

            async for message in client.receive_messages():
                if hasattr(message, "total_cost_usd"):
                    cost = getattr(message, "total_cost_usd")
                messages.append(message)

        return InvocationResult(
            agent_id=agent_id,
            prompt=prompt,
            options=options,
            messages=messages,
            cost_usd=cost,
        )

    @staticmethod
    def _default_client_factory(
        agent_config: Dict[str, Any],
        options: ClaudeAgentOptions,
    ) -> ClaudeClientProtocol:
        """Instantiate a real Claude SDK client."""
        _ = agent_config  # Reserved for future per-agent customisation
        return ClaudeSDKClient(options=options)


__all__ = ["AgentInvoker", "InvocationResult", "ClaudeClientProtocol"]
