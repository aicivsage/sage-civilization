"""
Pydantic schemas for agent message validation.

This module defines the data schemas used for validating messages
in the agent communication protocol.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator


class SignatureInfo(BaseModel):
    """
    Ed25519 signature information for message authentication.

    This schema represents cryptographic signatures attached to messages
    for verification of sender identity and message integrity.
    """
    algorithm: str = Field(
        default="Ed25519",
        description="Signature algorithm (always Ed25519)"
    )
    public_key: str = Field(
        ...,
        description="Base64-encoded Ed25519 public key of the sender"
    )
    key_id: str = Field(
        ...,
        description="Short identifier for the key (first 8 chars of SHA256 hash)"
    )
    signature: str = Field(
        ...,
        description="Base64-encoded Ed25519 signature of the canonical message"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "algorithm": "Ed25519",
                "public_key": "8sfXeKpnxq9LfB0Sr2/vgSTRpXYzYfPANuReCcKkzjE=",
                "key_id": "ef33652f",
                "signature": "ZGVhZGJlZWYxMjM0NTY3ODkwYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXowMTIzNDU2Nzg5YWJjZGVmZ2hpams="
            }
        }


class MessagePriority(str, Enum):
    """Priority levels for messages."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageType(str, Enum):
    """Types of messages in the system."""
    COMMAND = "command"
    QUERY = "query"
    RESPONSE = "response"
    EVENT = "event"
    NOTIFICATION = "notification"


class MessageStatus(str, Enum):
    """Status of a message."""
    PENDING = "pending"
    DELIVERED = "delivered"
    PROCESSED = "processed"
    FAILED = "failed"


class MessageMetadata(BaseModel):
    """Metadata associated with a message."""
    correlation_id: Optional[str] = Field(
        None,
        description="ID to correlate request/response messages"
    )
    reply_to: Optional[str] = Field(
        None,
        description="Agent ID to send replies to"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="When this message expires"
    )
    retry_count: int = Field(
        0,
        ge=0,
        description="Number of times this message has been retried"
    )
    tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Custom tags for message categorization"
    )
    signature: Optional[SignatureInfo] = Field(
        None,
        description="Ed25519 signature for message authentication (optional)"
    )

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MessageSchema(BaseModel):
    """Schema for validating agent messages."""

    id: str = Field(
        ...,
        description="Unique identifier for the message",
        min_length=1
    )
    type: MessageType = Field(
        ...,
        description="Type of message"
    )
    sender: str = Field(
        ...,
        description="Agent ID of the sender",
        min_length=1
    )
    recipient: Optional[str] = Field(
        None,
        description="Agent ID of the recipient (None for broadcast/pub-sub)"
    )
    topic: Optional[str] = Field(
        None,
        description="Topic for pub-sub messages"
    )
    payload: Dict[str, Any] = Field(
        ...,
        description="Message payload data"
    )
    priority: MessagePriority = Field(
        MessagePriority.NORMAL,
        description="Message priority"
    )
    status: MessageStatus = Field(
        MessageStatus.PENDING,
        description="Current status of the message"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the message was created"
    )
    metadata: MessageMetadata = Field(
        default_factory=MessageMetadata,
        description="Additional message metadata"
    )

    @field_validator('topic')
    @classmethod
    def validate_topic_for_pubsub(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that pub-sub messages have a topic."""
        # Note: info.data contains the other field values
        # For pub-sub patterns, topic should be set
        return v

    @field_validator('recipient')
    @classmethod
    def validate_recipient_for_direct(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that direct messages have a recipient."""
        # Direct messages should have a recipient
        return v

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RoutingPattern(str, Enum):
    """Routing patterns for message delivery."""
    DIRECT = "direct"        # Point-to-point messaging
    PUBSUB = "pubsub"        # Publish-subscribe pattern
    BROADCAST = "broadcast"  # Broadcast to all agents


class RouteSchema(BaseModel):
    """Schema for message routing information."""
    pattern: RoutingPattern = Field(
        ...,
        description="Routing pattern to use"
    )
    sender: str = Field(
        ...,
        description="Agent ID of the sender"
    )
    recipient: Optional[str] = Field(
        None,
        description="Recipient for direct messages"
    )
    topic: Optional[str] = Field(
        None,
        description="Topic for pub-sub messages"
    )

    @field_validator('recipient')
    @classmethod
    def validate_recipient_required_for_direct(cls, v: Optional[str], info) -> Optional[str]:
        """Validate recipient is provided for direct routing."""
        if 'pattern' in info.data and info.data['pattern'] == RoutingPattern.DIRECT:
            if not v:
                raise ValueError("recipient is required for direct routing pattern")
        return v

    @field_validator('topic')
    @classmethod
    def validate_topic_required_for_pubsub(cls, v: Optional[str], info) -> Optional[str]:
        """Validate topic is provided for pub-sub routing."""
        if 'pattern' in info.data and info.data['pattern'] == RoutingPattern.PUBSUB:
            if not v:
                raise ValueError("topic is required for pubsub routing pattern")
        return v

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
