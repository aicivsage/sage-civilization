"""
Message class for agent communication.

This module provides the core Message class that represents
messages exchanged between agents in the system.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import ValidationError

from .schemas import (
    MessageMetadata,
    MessagePriority,
    MessageSchema,
    MessageStatus,
    MessageType,
)


class Message:
    """
    Represents a message in the agent communication system.

    Messages are the fundamental unit of communication between agents.
    Each message has a unique ID, type, sender, payload, and optional routing info.
    """

    def __init__(
        self,
        type: MessageType,
        sender: str,
        payload: Dict[str, Any],
        recipient: Optional[str] = None,
        topic: Optional[str] = None,
        priority: MessagePriority = MessagePriority.NORMAL,
        message_id: Optional[str] = None,
        metadata: Optional[MessageMetadata] = None,
    ):
        """
        Initialize a new message.

        Args:
            type: Type of message (command, query, response, event, notification)
            sender: Agent ID of the sender
            payload: Message payload data
            recipient: Agent ID of the recipient (for direct messages)
            topic: Topic name (for pub-sub messages)
            priority: Message priority level
            message_id: Unique message ID (auto-generated if not provided)
            metadata: Additional message metadata

        Raises:
            ValidationError: If message validation fails
        """
        self._id = message_id or str(uuid.uuid4())
        self._type = type
        self._sender = sender
        self._recipient = recipient
        self._topic = topic
        self._payload = payload
        self._priority = priority
        self._status = MessageStatus.PENDING
        self._created_at = datetime.utcnow()
        self._metadata = metadata or MessageMetadata()

        # Validate the message
        self._validate()

    def _validate(self) -> None:
        """
        Validate the message using Pydantic schema.

        Raises:
            ValidationError: If validation fails
        """
        MessageSchema(
            id=self._id,
            type=self._type,
            sender=self._sender,
            recipient=self._recipient,
            topic=self._topic,
            payload=self._payload,
            priority=self._priority,
            status=self._status,
            created_at=self._created_at,
            metadata=self._metadata,
        )

    @property
    def id(self) -> str:
        """Get the message ID."""
        return self._id

    @property
    def type(self) -> MessageType:
        """Get the message type."""
        return self._type

    @property
    def sender(self) -> str:
        """Get the sender agent ID."""
        return self._sender

    @property
    def recipient(self) -> Optional[str]:
        """Get the recipient agent ID."""
        return self._recipient

    @property
    def topic(self) -> Optional[str]:
        """Get the message topic."""
        return self._topic

    @property
    def payload(self) -> Dict[str, Any]:
        """Get the message payload."""
        return self._payload

    @property
    def priority(self) -> MessagePriority:
        """Get the message priority."""
        return self._priority

    @property
    def status(self) -> MessageStatus:
        """Get the message status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Get the message creation timestamp."""
        return self._created_at

    @property
    def metadata(self) -> MessageMetadata:
        """Get the message metadata."""
        return self._metadata

    def set_status(self, status: MessageStatus) -> None:
        """
        Update the message status.

        Args:
            status: New status to set
        """
        self._status = status

    def add_tag(self, key: str, value: str) -> None:
        """
        Add a tag to the message metadata.

        Args:
            key: Tag key
            value: Tag value
        """
        self._metadata.tags[key] = value

    def increment_retry_count(self) -> None:
        """Increment the retry count in metadata."""
        self._metadata.retry_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary.

        Returns:
            Dictionary representation of the message
        """
        return {
            "id": self._id,
            "type": self._type.value if isinstance(self._type, MessageType) else self._type,
            "sender": self._sender,
            "recipient": self._recipient,
            "topic": self._topic,
            "payload": self._payload,
            "priority": self._priority.value if isinstance(self._priority, MessagePriority) else self._priority,
            "status": self._status.value if isinstance(self._status, MessageStatus) else self._status,
            "created_at": self._created_at.isoformat(),
            "metadata": {
                "correlation_id": self._metadata.correlation_id,
                "reply_to": self._metadata.reply_to,
                "expires_at": self._metadata.expires_at.isoformat() if self._metadata.expires_at else None,
                "retry_count": self._metadata.retry_count,
                "tags": self._metadata.tags,
            },
        }

    def to_json(self) -> str:
        """
        Convert the message to JSON string.

        Returns:
            JSON string representation of the message
        """
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """
        Create a Message from a dictionary.

        Args:
            data: Dictionary containing message data

        Returns:
            Message instance

        Raises:
            ValidationError: If data validation fails
        """
        # Parse datetime fields
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        # Parse metadata
        metadata_data = data.get("metadata", {})
        expires_at = metadata_data.get("expires_at")
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)

        metadata = MessageMetadata(
            correlation_id=metadata_data.get("correlation_id"),
            reply_to=metadata_data.get("reply_to"),
            expires_at=expires_at,
            retry_count=metadata_data.get("retry_count", 0),
            tags=metadata_data.get("tags", {}),
        )

        # Create message
        msg = cls(
            type=MessageType(data["type"]),
            sender=data["sender"],
            payload=data["payload"],
            recipient=data.get("recipient"),
            topic=data.get("topic"),
            priority=MessagePriority(data.get("priority", "normal")),
            message_id=data.get("id"),
            metadata=metadata,
        )

        # Set status and created_at if provided
        if "status" in data:
            msg._status = MessageStatus(data["status"])
        if created_at:
            msg._created_at = created_at

        return msg

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        """
        Create a Message from a JSON string.

        Args:
            json_str: JSON string containing message data

        Returns:
            Message instance

        Raises:
            ValidationError: If data validation fails
            json.JSONDecodeError: If JSON parsing fails
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        """String representation of the message."""
        return (
            f"Message(id={self._id}, type={self._type.value}, "
            f"sender={self._sender}, recipient={self._recipient}, "
            f"topic={self._topic}, priority={self._priority.value})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on message ID."""
        if not isinstance(other, Message):
            return NotImplemented
        return self._id == other._id
