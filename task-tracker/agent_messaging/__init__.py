"""
Agent Messaging System

A comprehensive message bus implementation for agent-to-agent communication
supporting multiple routing patterns: direct, pub-sub, and broadcast.

Usage:
    from agent_messaging import MessageBus, Message, MessageType

    # Create a message bus
    bus = MessageBus()

    # Register agents
    bus.register_agent("agent_1")
    bus.register_agent("agent_2")

    # Direct messaging
    msg = Message(
        type=MessageType.COMMAND,
        sender="agent_1",
        recipient="agent_2",
        payload={"action": "process", "data": "test"}
    )
    bus.send(msg)

    # Pub-sub messaging
    bus.subscribe("agent_2", "notifications")
    msg = Message(
        type=MessageType.EVENT,
        sender="agent_1",
        topic="notifications",
        payload={"event": "task_completed"}
    )
    bus.send(msg)

    # Receive messages
    received = bus.receive("agent_2")
"""

from .message import Message
from .message_bus import (
    InMemoryStorage,
    JSONFileStorage,
    MessageBus,
    StorageBackend,
)
from .routing import (
    BroadcastRouter,
    DirectRouter,
    MessageRouter,
    PubSubRouter,
    Router,
)
from .schemas import (
    MessageMetadata,
    MessagePriority,
    MessageSchema,
    MessageStatus,
    MessageType,
    RouteSchema,
    RoutingPattern,
    SignatureInfo,
)

# Ed25519 signing support (optional imports)
try:
    from .translation import (
        MessageTranslator,
        message_to_signable,
        signable_to_message,
        extract_signature,
        is_signed,
    )
    from .key_management import (
        AgentKeyRegistry,
        get_default_registry,
        get_agent_public_key,
        verify_agent_key_id,
    )
    from .signed_bus import (
        SignedMessageBus,
        create_signed_bus,
        SigningError,
    )
    _SIGNING_AVAILABLE = True
except ImportError:
    _SIGNING_AVAILABLE = False
    MessageTranslator = None
    SignedMessageBus = None
    AgentKeyRegistry = None

__version__ = "0.1.0"

__all__ = [
    # Core classes
    "Message",
    "MessageBus",
    # Storage backends
    "StorageBackend",
    "InMemoryStorage",
    "JSONFileStorage",
    # Routing
    "Router",
    "DirectRouter",
    "PubSubRouter",
    "BroadcastRouter",
    "MessageRouter",
    # Schemas and enums
    "MessageType",
    "MessagePriority",
    "MessageStatus",
    "MessageMetadata",
    "MessageSchema",
    "RoutingPattern",
    "RouteSchema",
    "SignatureInfo",
]

# Add signing-related exports if available
if _SIGNING_AVAILABLE:
    __all__.extend([
        # Translation
        "MessageTranslator",
        "message_to_signable",
        "signable_to_message",
        "extract_signature",
        "is_signed",
        # Key management
        "AgentKeyRegistry",
        "get_default_registry",
        "get_agent_public_key",
        "verify_agent_key_id",
        # Signed bus
        "SignedMessageBus",
        "create_signed_bus",
        "SigningError",
    ])
