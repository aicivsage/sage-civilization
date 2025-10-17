"""
Signed message bus wrapper with Ed25519 signature support.

This module provides a SignedMessageBus class that wraps the standard
MessageBus and adds automatic message signing and verification using Ed25519.
"""

import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Import Ed25519 signing library from shared deliverables
ED25519_LIB_PATH = Path.home() / "projects/AI-CIV/SHARED-DELIVERABLES/weaver-team1/ed25519-signing"
if ED25519_LIB_PATH.exists():
    sys.path.insert(0, str(ED25519_LIB_PATH))

try:
    from sign_message import Ed25519Signer, sign_hub_message, verify_hub_message, VerificationError
except ImportError:
    # Ed25519 library not available - provide graceful fallback
    Ed25519Signer = None
    sign_hub_message = None
    verify_hub_message = None
    VerificationError = Exception

from .message import Message
from .message_bus import MessageBus
from .translation import MessageTranslator, is_signed
from .key_management import AgentKeyRegistry


class SigningError(Exception):
    """Raised when message signing fails."""
    pass


class SignedMessageBus:
    """
    Message bus with Ed25519 signature support.

    This class wraps the standard MessageBus and adds automatic signing
    and verification of messages using Ed25519 cryptographic signatures.

    Features:
    - Automatic signing of outgoing messages (optional)
    - Automatic verification of incoming messages (optional)
    - Backward compatible with unsigned messages
    - Transparent translation between ADR-004 and hub formats
    """

    def __init__(
        self,
        message_bus: Optional[MessageBus] = None,
        agent_id: Optional[str] = None,
        private_key_path: Optional[str] = None,
        auto_sign: bool = True,
        auto_verify: bool = True,
        key_registry: Optional[AgentKeyRegistry] = None,
        room: str = "default"
    ):
        """
        Initialize signed message bus.

        Args:
            message_bus: Underlying MessageBus instance. If None, creates new one.
            agent_id: ID of the agent using this bus (for signing)
            private_key_path: Path to Ed25519 private key file.
                             If None, uses ~/.aiciv/keys/{agent_id}.key
            auto_sign: Automatically sign all published messages
            auto_verify: Automatically verify all received messages
            key_registry: AgentKeyRegistry for public key lookups.
                         If None, creates default registry.
            room: Hub room name for message translation (default: "default")

        Raises:
            SigningError: If Ed25519 library is not available
            FileNotFoundError: If private key file not found (when auto_sign=True)
        """
        # Check Ed25519 availability
        if Ed25519Signer is None:
            raise SigningError(
                "Ed25519 library not available. "
                "Please ensure sign_message.py is in SHARED-DELIVERABLES."
            )

        self._bus = message_bus or MessageBus()
        self._agent_id = agent_id
        self._auto_sign = auto_sign
        self._auto_verify = auto_verify
        self._room = room

        # Initialize key registry
        self._key_registry = key_registry or AgentKeyRegistry()

        # Initialize signer if auto-signing is enabled
        self._signer: Optional[Ed25519Signer] = None
        if auto_sign:
            if not agent_id:
                raise SigningError("agent_id required when auto_sign=True")

            # Determine private key path
            if private_key_path is None:
                private_key_path = str(Path.home() / ".aiciv" / "keys" / f"{agent_id}.key")

            # Load private key
            try:
                from sign_message import load_private_key
                private_key = load_private_key(private_key_path)
                self._signer = Ed25519Signer.from_private_key(private_key)
            except FileNotFoundError:
                raise SigningError(f"Private key not found: {private_key_path}")
            except Exception as e:
                raise SigningError(f"Failed to load private key: {e}")

    def send(
        self,
        message: Message,
        sign: Optional[bool] = None
    ) -> None:
        """
        Send a message to the bus, optionally signing it.

        Args:
            message: Message to send
            sign: Override auto_sign setting for this message.
                 If None, uses auto_sign from constructor.

        Raises:
            SigningError: If signing fails

        Example:
            >>> bus = SignedMessageBus(agent_id="researcher", auto_sign=True)
            >>> msg = Message(
            ...     type=MessageType.COMMAND,
            ...     sender="researcher",
            ...     payload={"action": "test"}
            ... )
            >>> bus.send(msg)  # Automatically signed
        """
        should_sign = sign if sign is not None else self._auto_sign

        if should_sign and not is_signed(message):
            # Sign the message
            message = self._sign_message(message)

        # Send to underlying bus
        self._bus.send(message)

    def register_handler(
        self,
        agent_id: str,
        handler: Callable[[Message], None],
        verify: Optional[bool] = None
    ) -> None:
        """
        Register a message handler, optionally verifying signatures.

        Args:
            agent_id: Agent ID to register handler for
            handler: Callback function to handle messages
            verify: Override auto_verify setting for this handler.
                   If None, uses auto_verify from constructor.

        Example:
            >>> def handle_message(msg: Message):
            ...     print(f"Received: {msg.id}")
            >>> bus = SignedMessageBus(auto_verify=True)
            >>> bus.register_handler("researcher", handle_message)
        """
        should_verify = verify if verify is not None else self._auto_verify

        if should_verify:
            # Wrap handler with verification
            wrapped_handler = self._create_verifying_handler(handler)
            self._bus.register_handler(agent_id, wrapped_handler)
        else:
            # Register directly without verification
            self._bus.register_handler(agent_id, handler)

    def subscribe(
        self,
        agent_id: str,
        topic: str
    ) -> None:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: Agent ID to subscribe
            topic: Topic name to subscribe to

        Example:
            >>> bus = SignedMessageBus()
            >>> bus.subscribe("researcher", "updates")
        """
        self._bus.subscribe(agent_id, topic)

    def register_agent(self, agent_id: str) -> None:
        """Register an agent with the bus."""
        self._bus.register_agent(agent_id)

    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent from the bus."""
        self._bus.unregister_agent(agent_id)

    def receive(
        self,
        agent_id: str,
        block: bool = False,
        verify: Optional[bool] = None
    ) -> Optional[Message]:
        """
        Receive a message for an agent, optionally verifying signature.

        Args:
            agent_id: Agent ID to receive message for
            block: Whether to block until a message is available
            verify: Override auto_verify setting

        Returns:
            Message if available (and verified if verify=True), None otherwise

        Example:
            >>> bus = SignedMessageBus(auto_verify=True)
            >>> msg = bus.receive("researcher")
            >>> # Message has been signature-verified
        """
        message = self._bus.receive(agent_id, block)

        if message is None:
            return None

        should_verify = verify if verify is not None else self._auto_verify

        if should_verify and is_signed(message):
            try:
                if not self._verify_message(message):
                    # Skip message with invalid signature
                    return None
            except Exception:
                # Skip message that can't be verified
                return None

        return message

    def _sign_message(self, message: Message) -> Message:
        """
        Sign a message using Ed25519.

        Args:
            message: Message to sign

        Returns:
            New message with signature in metadata

        Raises:
            SigningError: If signing fails
        """
        if self._signer is None:
            raise SigningError("No signer available (auto_sign=False or no key loaded)")

        try:
            # Convert to hub format
            hub_message = MessageTranslator.adr004_to_hub(message, self._room)

            # Sign the message
            signed_hub_message = sign_hub_message(hub_message, self._signer)

            # Convert back to ADR-004 format
            signed_message = MessageTranslator.hub_to_adr004(signed_hub_message)

            return signed_message

        except Exception as e:
            raise SigningError(f"Failed to sign message: {e}")

    def _verify_message(self, message: Message) -> bool:
        """
        Verify a message signature.

        Args:
            message: Signed message to verify

        Returns:
            True if signature is valid, False otherwise

        Raises:
            VerificationError: If verification process fails
        """
        if not is_signed(message):
            return False  # Can't verify unsigned message

        try:
            # Get sender's public key from registry
            sender_public_key = self._key_registry.get_public_key(message.sender)

            if sender_public_key is None:
                # Sender not in registry - try using key from message
                sender_public_key = None

            # Convert to hub format
            hub_message = MessageTranslator.adr004_to_hub(message, self._room)

            # Verify signature
            is_valid = verify_hub_message(hub_message, sender_public_key)

            return is_valid

        except VerificationError:
            return False
        except Exception:
            return False

    def _create_verifying_handler(
        self,
        original_handler: Callable[[Message], None]
    ) -> Callable[[Message], None]:
        """
        Create a handler wrapper that verifies signatures before calling original handler.

        Args:
            original_handler: Original message handler

        Returns:
            Wrapped handler that verifies signatures
        """
        def verifying_handler(message: Message) -> None:
            """Handler that verifies message signature before processing."""
            # If message is signed, verify it
            if is_signed(message):
                try:
                    if not self._verify_message(message):
                        # Skip messages with invalid signatures
                        return
                except Exception:
                    # Skip messages that can't be verified
                    return

            # Call original handler
            original_handler(message)

        return verifying_handler

    # Delegate other methods to underlying bus

    @property
    def bus(self) -> MessageBus:
        """Get the underlying MessageBus instance."""
        return self._bus

    def clear(self) -> None:
        """Clear all messages from the bus."""
        self._bus.clear()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SignedMessageBus("
            f"agent_id={self._agent_id}, "
            f"auto_sign={self._auto_sign}, "
            f"auto_verify={self._auto_verify}, "
            f"room={self._room})"
        )


# Convenience function for creating signed bus instances

def create_signed_bus(
    agent_id: str,
    auto_sign: bool = True,
    auto_verify: bool = True,
    room: str = "default"
) -> SignedMessageBus:
    """
    Create a signed message bus for an agent.

    This is a convenience function that handles all the initialization.

    Args:
        agent_id: Agent identifier (used for signing and key lookup)
        auto_sign: Automatically sign all published messages
        auto_verify: Automatically verify all received messages
        room: Hub room name for message translation

    Returns:
        Configured SignedMessageBus instance

    Raises:
        SigningError: If Ed25519 library is not available or keys not found

    Example:
        >>> from agent_messaging.signed_bus import create_signed_bus
        >>> bus = create_signed_bus("researcher")
        >>> # Ready to send and receive signed messages
    """
    return SignedMessageBus(
        agent_id=agent_id,
        auto_sign=auto_sign,
        auto_verify=auto_verify,
        room=room
    )
