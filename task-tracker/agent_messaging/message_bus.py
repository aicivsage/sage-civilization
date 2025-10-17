"""
Message bus implementation for agent communication.

This module provides the core MessageBus class that manages message
queuing, routing, and persistence for agent communication.
"""

import json
import threading
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Deque, Dict, List, Optional

from .message import Message
from .routing import MessageRouter
from .schemas import MessageStatus


class StorageBackend:
    """Abstract storage backend for message persistence."""

    def save_message(self, message: Message) -> None:
        """Save a message to storage."""
        raise NotImplementedError

    def load_messages(self) -> List[Message]:
        """Load all messages from storage."""
        raise NotImplementedError

    def clear(self) -> None:
        """Clear all messages from storage."""
        raise NotImplementedError


class JSONFileStorage(StorageBackend):
    """JSON file-based storage backend for messages."""

    def __init__(self, file_path: str = "messages.json"):
        """
        Initialize JSON file storage.

        Args:
            file_path: Path to the JSON file for message storage
        """
        self.file_path = Path(file_path)
        self._lock = threading.Lock()

    def save_message(self, message: Message) -> None:
        """
        Save a message to the JSON file.

        Args:
            message: Message to save
        """
        with self._lock:
            messages = []
            if self.file_path.exists() and self.file_path.stat().st_size > 0:
                with open(self.file_path, "r") as f:
                    messages = json.load(f)

            messages.append(message.to_dict())

            with open(self.file_path, "w") as f:
                json.dump(messages, f, indent=2)

    def load_messages(self) -> List[Message]:
        """
        Load all messages from the JSON file.

        Returns:
            List of Message objects
        """
        with self._lock:
            if not self.file_path.exists():
                return []

            with open(self.file_path, "r") as f:
                data = json.load(f)

            return [Message.from_dict(msg_data) for msg_data in data]

    def clear(self) -> None:
        """Clear all messages from the JSON file."""
        with self._lock:
            if self.file_path.exists():
                self.file_path.unlink()


class InMemoryStorage(StorageBackend):
    """In-memory storage backend for messages (no persistence)."""

    def __init__(self):
        """Initialize in-memory storage."""
        self._messages: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def save_message(self, message: Message) -> None:
        """
        Save a message to memory.

        Args:
            message: Message to save
        """
        with self._lock:
            self._messages.append(message.to_dict())

    def load_messages(self) -> List[Message]:
        """
        Load all messages from memory.

        Returns:
            List of Message objects
        """
        with self._lock:
            return [Message.from_dict(msg_data) for msg_data in self._messages]

    def clear(self) -> None:
        """Clear all messages from memory."""
        with self._lock:
            self._messages.clear()


class MessageBus:
    """
    Main message bus for agent communication.

    The message bus manages message queues, routing, and delivery
    between agents using in-memory queues.
    """

    def __init__(self, storage: Optional[StorageBackend] = None):
        """
        Initialize the message bus.

        Args:
            storage: Storage backend for message persistence (defaults to in-memory)
        """
        self._queues: Dict[str, Deque[Message]] = defaultdict(deque)
        self._router = MessageRouter()
        self._storage = storage or InMemoryStorage()
        self._handlers: Dict[str, List[Callable[[Message], None]]] = defaultdict(list)
        self._lock = threading.Lock()

    @property
    def router(self) -> MessageRouter:
        """Get the message router."""
        return self._router

    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent with the message bus.

        Args:
            agent_id: ID of the agent to register
        """
        with self._lock:
            if agent_id not in self._queues:
                self._queues[agent_id] = deque()
            self._router.register_agent(agent_id)

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from the message bus.

        Args:
            agent_id: ID of the agent to unregister
        """
        with self._lock:
            if agent_id in self._queues:
                del self._queues[agent_id]
            self._router.unregister_agent(agent_id)
            if agent_id in self._handlers:
                del self._handlers[agent_id]

    def subscribe(self, agent_id: str, topic: str) -> None:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: ID of the agent subscribing
            topic: Topic to subscribe to
        """
        self._router.subscribe(agent_id, topic)

    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """
        Unsubscribe an agent from a topic.

        Args:
            agent_id: ID of the agent unsubscribing
            topic: Topic to unsubscribe from
        """
        self._router.unsubscribe(agent_id, topic)

    def register_handler(
        self, agent_id: str, handler: Callable[[Message], None]
    ) -> None:
        """
        Register a message handler for an agent.

        Handlers are called automatically when a message is delivered
        to the agent's queue.

        Args:
            agent_id: ID of the agent
            handler: Callback function to handle messages
        """
        with self._lock:
            self._handlers[agent_id].append(handler)

    def send(self, message: Message) -> None:
        """
        Send a message through the bus.

        The message is routed to appropriate recipients based on
        its routing pattern (direct, pub-sub, or broadcast).

        Args:
            message: Message to send
        """
        # Route the message to get recipients
        recipients = self._router.route(message)

        # Deliver to each recipient
        with self._lock:
            for recipient_id in recipients:
                if recipient_id in self._queues:
                    # Add to queue
                    self._queues[recipient_id].append(message)

                    # Call handlers if any
                    if recipient_id in self._handlers:
                        for handler in self._handlers[recipient_id]:
                            try:
                                handler(message)
                            except Exception as e:
                                # Log error but don't stop delivery
                                print(f"Handler error for {recipient_id}: {e}")

            # Update message status
            message.set_status(MessageStatus.DELIVERED)

            # Persist the message
            self._storage.save_message(message)

    def receive(self, agent_id: str, block: bool = False) -> Optional[Message]:
        """
        Receive a message from an agent's queue.

        Args:
            agent_id: ID of the agent receiving the message
            block: If True, block until a message is available

        Returns:
            The next message in the queue, or None if queue is empty
        """
        with self._lock:
            if agent_id not in self._queues:
                return None

            queue = self._queues[agent_id]

            if queue:
                message = queue.popleft()
                message.set_status(MessageStatus.PROCESSED)
                return message

            return None

    def peek(self, agent_id: str) -> Optional[Message]:
        """
        Peek at the next message without removing it from the queue.

        Args:
            agent_id: ID of the agent

        Returns:
            The next message in the queue, or None if queue is empty
        """
        with self._lock:
            if agent_id not in self._queues:
                return None

            queue = self._queues[agent_id]
            return queue[0] if queue else None

    def get_queue_size(self, agent_id: str) -> int:
        """
        Get the number of messages in an agent's queue.

        Args:
            agent_id: ID of the agent

        Returns:
            Number of messages in the queue
        """
        with self._lock:
            if agent_id not in self._queues:
                return 0
            return len(self._queues[agent_id])

    def clear_queue(self, agent_id: str) -> None:
        """
        Clear all messages from an agent's queue.

        Args:
            agent_id: ID of the agent
        """
        with self._lock:
            if agent_id in self._queues:
                self._queues[agent_id].clear()

    def get_all_messages(self) -> List[Message]:
        """
        Get all messages from persistent storage.

        Returns:
            List of all stored messages
        """
        return self._storage.load_messages()

    def clear_storage(self) -> None:
        """Clear all messages from persistent storage."""
        self._storage.clear()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get message bus statistics.

        Returns:
            Dictionary containing bus statistics
        """
        with self._lock:
            total_queued = sum(len(queue) for queue in self._queues.values())
            return {
                "registered_agents": list(self._queues.keys()),
                "total_agents": len(self._queues),
                "total_queued_messages": total_queued,
                "queue_sizes": {
                    agent_id: len(queue) for agent_id, queue in self._queues.items()
                },
                "total_persisted_messages": len(self._storage.load_messages()),
            }
