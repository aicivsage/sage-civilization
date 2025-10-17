"""
Message routing patterns for agent communication.

This module implements different routing strategies for delivering
messages between agents: direct, pub-sub, and broadcast.
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Set

from .message import Message
from .schemas import RoutingPattern


class Router(ABC):
    """Abstract base class for message routing strategies."""

    @abstractmethod
    def route(self, message: Message) -> List[str]:
        """
        Determine the recipients for a message.

        Args:
            message: Message to route

        Returns:
            List of agent IDs that should receive the message
        """
        pass


class DirectRouter(Router):
    """
    Direct (point-to-point) message routing.

    Routes messages directly from sender to a specific recipient.
    """

    def route(self, message: Message) -> List[str]:
        """
        Route message to its direct recipient.

        Args:
            message: Message to route

        Returns:
            List containing the recipient agent ID

        Raises:
            ValueError: If message has no recipient
        """
        if not message.recipient:
            raise ValueError("Direct routing requires a recipient")
        return [message.recipient]


class PubSubRouter(Router):
    """
    Publish-Subscribe message routing.

    Routes messages based on topics. Agents subscribe to topics
    and receive all messages published to those topics.
    """

    def __init__(self):
        """Initialize the pub-sub router."""
        self._subscriptions: Dict[str, Set[str]] = defaultdict(set)

    def subscribe(self, agent_id: str, topic: str) -> None:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: ID of the agent subscribing
            topic: Topic to subscribe to
        """
        self._subscriptions[topic].add(agent_id)

    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """
        Unsubscribe an agent from a topic.

        Args:
            agent_id: ID of the agent unsubscribing
            topic: Topic to unsubscribe from
        """
        if topic in self._subscriptions:
            self._subscriptions[topic].discard(agent_id)
            # Clean up empty topic
            if not self._subscriptions[topic]:
                del self._subscriptions[topic]

    def get_subscribers(self, topic: str) -> Set[str]:
        """
        Get all subscribers for a topic.

        Args:
            topic: Topic to query

        Returns:
            Set of agent IDs subscribed to the topic
        """
        return self._subscriptions.get(topic, set()).copy()

    def get_topics_for_agent(self, agent_id: str) -> List[str]:
        """
        Get all topics an agent is subscribed to.

        Args:
            agent_id: Agent ID to query

        Returns:
            List of topics the agent is subscribed to
        """
        return [
            topic
            for topic, subscribers in self._subscriptions.items()
            if agent_id in subscribers
        ]

    def route(self, message: Message) -> List[str]:
        """
        Route message to all subscribers of its topic.

        Args:
            message: Message to route

        Returns:
            List of agent IDs subscribed to the message's topic

        Raises:
            ValueError: If message has no topic
        """
        if not message.topic:
            raise ValueError("Pub-sub routing requires a topic")

        subscribers = self._subscriptions.get(message.topic, set())
        # Don't send message back to the sender
        return [agent_id for agent_id in subscribers if agent_id != message.sender]


class BroadcastRouter(Router):
    """
    Broadcast message routing.

    Routes messages to all registered agents in the system.
    """

    def __init__(self):
        """Initialize the broadcast router."""
        self._agents: Set[str] = set()

    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent for broadcast messages.

        Args:
            agent_id: ID of the agent to register
        """
        self._agents.add(agent_id)

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from broadcast messages.

        Args:
            agent_id: ID of the agent to unregister
        """
        self._agents.discard(agent_id)

    def get_agents(self) -> Set[str]:
        """
        Get all registered agents.

        Returns:
            Set of all registered agent IDs
        """
        return self._agents.copy()

    def route(self, message: Message) -> List[str]:
        """
        Route message to all registered agents.

        Args:
            message: Message to route

        Returns:
            List of all registered agent IDs (excluding sender)
        """
        # Don't send message back to the sender
        return [agent_id for agent_id in self._agents if agent_id != message.sender]


class MessageRouter:
    """
    Main message router that delegates to specific routing strategies.

    This class coordinates between direct, pub-sub, and broadcast routing
    patterns based on message configuration.
    """

    def __init__(self):
        """Initialize the message router with all routing strategies."""
        self._direct_router = DirectRouter()
        self._pubsub_router = PubSubRouter()
        self._broadcast_router = BroadcastRouter()

    @property
    def pubsub(self) -> PubSubRouter:
        """Get the pub-sub router."""
        return self._pubsub_router

    @property
    def broadcast(self) -> BroadcastRouter:
        """Get the broadcast router."""
        return self._broadcast_router

    def determine_pattern(self, message: Message) -> RoutingPattern:
        """
        Determine the routing pattern for a message.

        Args:
            message: Message to analyze

        Returns:
            The appropriate routing pattern
        """
        if message.recipient:
            return RoutingPattern.DIRECT
        elif message.topic:
            return RoutingPattern.PUBSUB
        else:
            return RoutingPattern.BROADCAST

    def route(self, message: Message) -> List[str]:
        """
        Route a message to its recipients.

        Args:
            message: Message to route

        Returns:
            List of agent IDs that should receive the message

        Raises:
            ValueError: If routing requirements are not met
        """
        pattern = self.determine_pattern(message)

        if pattern == RoutingPattern.DIRECT:
            return self._direct_router.route(message)
        elif pattern == RoutingPattern.PUBSUB:
            return self._pubsub_router.route(message)
        else:  # BROADCAST
            return self._broadcast_router.route(message)

    def subscribe(self, agent_id: str, topic: str) -> None:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: ID of the agent subscribing
            topic: Topic to subscribe to
        """
        self._pubsub_router.subscribe(agent_id, topic)

    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """
        Unsubscribe an agent from a topic.

        Args:
            agent_id: ID of the agent unsubscribing
            topic: Topic to unsubscribe from
        """
        self._pubsub_router.unsubscribe(agent_id, topic)

    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent for broadcast messages.

        Args:
            agent_id: ID of the agent to register
        """
        self._broadcast_router.register_agent(agent_id)

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from broadcast messages.

        Args:
            agent_id: ID of the agent to unregister
        """
        self._broadcast_router.unregister_agent(agent_id)
        # Also remove from all topic subscriptions
        for topic in self._pubsub_router.get_topics_for_agent(agent_id):
            self._pubsub_router.unsubscribe(agent_id, topic)
