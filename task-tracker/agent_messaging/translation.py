"""
Translation layer between ADR-004 message format and Ed25519 signing library.

This module provides bidirectional translation between the agent_messaging
Message format (ADR-004) and the comms hub message format used by Ed25519
signing library.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

from .message import Message
from .schemas import MessageMetadata, MessagePriority, MessageType, SignatureInfo


class MessageTranslator:
    """
    Translates between ADR-004 Message objects and comms hub message dictionaries.

    The comms hub message format follows the schema used by Weaver's Ed25519
    signing library, with fields like 'version', 'room', 'author', etc.
    """

    COMMS_HUB_VERSION = "1.0"

    @staticmethod
    def adr004_to_hub(message: Message, room: str = "default") -> Dict[str, Any]:
        """
        Convert ADR-004 Message to comms hub message dictionary.

        Args:
            message: ADR-004 Message object
            room: Hub room/channel name (default: "default")

        Returns:
            Dictionary in comms hub message format, ready for Ed25519 signing

        Example:
            >>> msg = Message(
            ...     type=MessageType.COMMAND,
            ...     sender="agent-1",
            ...     payload={"action": "test"}
            ... )
            >>> hub_msg = MessageTranslator.adr004_to_hub(msg)
            >>> # hub_msg can now be passed to sign_hub_message()
        """
        # Extract signature if present (will be re-added after signing)
        signature_info = None
        if message.metadata and message.metadata.signature:
            signature_info = message.metadata.signature

        # Build comms hub message structure
        hub_message = {
            "version": MessageTranslator.COMMS_HUB_VERSION,
            "id": message.id,
            "room": room,
            "author": {
                "id": message.sender,
                "display": message.sender  # Use agent ID as display name
            },
            "ts": message.created_at.isoformat() + "Z",
            "type": "structured",  # Our messages are structured data
            "summary": MessageTranslator._generate_summary(message),
            "body": {
                "message_type": message.type.value,
                "recipient": message.recipient,
                "topic": message.topic,
                "payload": message.payload,
                "priority": message.priority.value,
                "status": message.status.value
            }
        }

        # Add metadata as extensions if present
        if message.metadata:
            extensions = {}

            if message.metadata.correlation_id:
                extensions["correlation_id"] = message.metadata.correlation_id

            if message.metadata.reply_to:
                extensions["reply_to"] = message.metadata.reply_to

            if message.metadata.expires_at:
                extensions["expires_at"] = message.metadata.expires_at.isoformat() + "Z"

            if message.metadata.retry_count > 0:
                extensions["retry_count"] = message.metadata.retry_count

            if message.metadata.tags:
                extensions["tags"] = message.metadata.tags

            # Add signature if it was present
            if signature_info:
                extensions["signature"] = {
                    "algorithm": signature_info.algorithm,
                    "public_key": signature_info.public_key,
                    "key_id": signature_info.key_id,
                    "signature": signature_info.signature
                }

            if extensions:
                hub_message["extensions"] = extensions

        return hub_message

    @staticmethod
    def hub_to_adr004(hub_message: Dict[str, Any]) -> Message:
        """
        Convert comms hub message dictionary to ADR-004 Message object.

        Args:
            hub_message: Dictionary in comms hub message format

        Returns:
            ADR-004 Message object

        Raises:
            ValueError: If hub message is missing required fields
            KeyError: If required fields are not present

        Example:
            >>> hub_msg = {...}  # From comms hub
            >>> msg = MessageTranslator.hub_to_adr004(hub_msg)
            >>> # msg is now an ADR-004 Message object
        """
        # Extract required fields
        try:
            message_id = hub_message["id"]
            sender = hub_message["author"]["id"]
            created_at_str = hub_message["ts"]
            body = hub_message["body"]

            # Parse message type
            message_type = MessageType(body["message_type"])
            priority = MessagePriority(body.get("priority", "normal"))

            # Extract routing info
            recipient = body.get("recipient")
            topic = body.get("topic")
            payload = body.get("payload", {})

        except KeyError as e:
            raise ValueError(f"Missing required field in hub message: {e}")

        # Parse timestamp
        created_at = datetime.fromisoformat(created_at_str.rstrip("Z"))

        # Build metadata from extensions
        metadata = MessageMetadata()

        if "extensions" in hub_message:
            ext = hub_message["extensions"]

            if "correlation_id" in ext:
                metadata.correlation_id = ext["correlation_id"]

            if "reply_to" in ext:
                metadata.reply_to = ext["reply_to"]

            if "expires_at" in ext:
                metadata.expires_at = datetime.fromisoformat(ext["expires_at"].rstrip("Z"))

            if "retry_count" in ext:
                metadata.retry_count = ext["retry_count"]

            if "tags" in ext:
                metadata.tags = ext["tags"]

            # Extract signature if present
            if "signature" in ext:
                sig = ext["signature"]
                metadata.signature = SignatureInfo(
                    algorithm=sig["algorithm"],
                    public_key=sig["public_key"],
                    key_id=sig["key_id"],
                    signature=sig["signature"]
                )

        # Create Message object
        message = Message(
            type=message_type,
            sender=sender,
            payload=payload,
            recipient=recipient,
            topic=topic,
            priority=priority,
            message_id=message_id,
            metadata=metadata
        )

        # Override created_at to match hub timestamp
        message._created_at = created_at

        # Set status from body if present
        if "status" in body:
            from .schemas import MessageStatus
            message._status = MessageStatus(body["status"])

        return message

    @staticmethod
    def _generate_summary(message: Message) -> str:
        """
        Generate a human-readable summary for a message.

        Args:
            message: ADR-004 Message object

        Returns:
            Short summary string (max 100 chars)
        """
        msg_type = message.type.value.upper()
        sender = message.sender

        # Generate context-aware summary
        if message.recipient:
            target = f"to {message.recipient}"
        elif message.topic:
            target = f"on {message.topic}"
        else:
            target = "broadcast"

        # Try to extract meaningful info from payload
        payload_summary = ""
        if message.payload:
            if "action" in message.payload:
                payload_summary = f": {message.payload['action']}"
            elif "query" in message.payload:
                payload_summary = f": {message.payload['query']}"
            elif "event" in message.payload:
                payload_summary = f": {message.payload['event']}"

        summary = f"{msg_type} from {sender} {target}{payload_summary}"

        # Truncate to 100 chars
        if len(summary) > 100:
            summary = summary[:97] + "..."

        return summary


# Convenience functions for common operations

def message_to_signable(message: Message, room: str = "default") -> Dict[str, Any]:
    """
    Convert ADR-004 Message to a dictionary ready for Ed25519 signing.

    This is a convenience wrapper around MessageTranslator.adr004_to_hub().

    Args:
        message: ADR-004 Message object
        room: Hub room/channel name

    Returns:
        Dictionary ready for signing with sign_hub_message()
    """
    return MessageTranslator.adr004_to_hub(message, room)


def signable_to_message(hub_message: Dict[str, Any]) -> Message:
    """
    Convert signed hub message dictionary back to ADR-004 Message.

    This is a convenience wrapper around MessageTranslator.hub_to_adr004().

    Args:
        hub_message: Dictionary in comms hub format (possibly signed)

    Returns:
        ADR-004 Message object with signature in metadata
    """
    return MessageTranslator.hub_to_adr004(hub_message)


def extract_signature(message: Message) -> Optional[SignatureInfo]:
    """
    Extract signature information from a message.

    Args:
        message: ADR-004 Message object

    Returns:
        SignatureInfo if message is signed, None otherwise
    """
    if message.metadata and message.metadata.signature:
        return message.metadata.signature
    return None


def is_signed(message: Message) -> bool:
    """
    Check if a message has a cryptographic signature.

    Args:
        message: ADR-004 Message object

    Returns:
        True if message has a signature, False otherwise
    """
    return extract_signature(message) is not None
