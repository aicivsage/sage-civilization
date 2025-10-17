#!/usr/bin/env python3
"""
Test script for the agent messaging system.

This script demonstrates all the core functionality of the message bus:
- Direct messaging (agent-to-agent)
- Pub-sub messaging (topic-based)
- Broadcast messaging
- Message persistence
- Message handlers
"""

from agent_messaging import (
    Message,
    MessageBus,
    MessageType,
    MessagePriority,
    JSONFileStorage,
    InMemoryStorage,
)


def test_direct_messaging():
    """Test direct agent-to-agent messaging."""
    print("\n=== Testing Direct Messaging ===")

    bus = MessageBus()

    # Register agents
    bus.register_agent("agent_1")
    bus.register_agent("agent_2")

    # Send a direct message
    msg = Message(
        type=MessageType.COMMAND,
        sender="agent_1",
        recipient="agent_2",
        payload={"action": "process", "data": "test_data"},
        priority=MessagePriority.HIGH,
    )

    bus.send(msg)
    print(f"Sent message: {msg}")

    # Receive the message
    received = bus.receive("agent_2")
    print(f"Received message: {received}")
    assert received is not None
    assert received.id == msg.id
    assert received.payload == msg.payload

    print("✓ Direct messaging works!")


def test_pubsub_messaging():
    """Test pub-sub topic-based messaging."""
    print("\n=== Testing Pub-Sub Messaging ===")

    bus = MessageBus()

    # Register agents
    bus.register_agent("agent_1")
    bus.register_agent("agent_2")
    bus.register_agent("agent_3")

    # Subscribe agents to topics
    bus.subscribe("agent_2", "notifications")
    bus.subscribe("agent_3", "notifications")

    # Publish a message to the topic
    msg = Message(
        type=MessageType.EVENT,
        sender="agent_1",
        topic="notifications",
        payload={"event": "task_completed", "task_id": "123"},
    )

    bus.send(msg)
    print(f"Published message to 'notifications': {msg}")

    # Both subscribers should receive it
    received_2 = bus.receive("agent_2")
    received_3 = bus.receive("agent_3")

    print(f"Agent 2 received: {received_2}")
    print(f"Agent 3 received: {received_3}")

    assert received_2 is not None
    assert received_3 is not None
    assert received_2.id == msg.id
    assert received_3.id == msg.id

    # Agent 1 should not receive it (sender doesn't get own message)
    received_1 = bus.receive("agent_1")
    assert received_1 is None

    print("✓ Pub-sub messaging works!")


def test_broadcast_messaging():
    """Test broadcast messaging to all agents."""
    print("\n=== Testing Broadcast Messaging ===")

    bus = MessageBus()

    # Register agents
    agents = ["agent_1", "agent_2", "agent_3"]
    for agent_id in agents:
        bus.register_agent(agent_id)

    # Send a broadcast message (no recipient or topic)
    msg = Message(
        type=MessageType.NOTIFICATION,
        sender="agent_1",
        payload={"announcement": "System maintenance in 1 hour"},
    )

    bus.send(msg)
    print(f"Broadcast message: {msg}")

    # All agents except sender should receive it
    received_2 = bus.receive("agent_2")
    received_3 = bus.receive("agent_3")

    print(f"Agent 2 received: {received_2}")
    print(f"Agent 3 received: {received_3}")

    assert received_2 is not None
    assert received_3 is not None
    assert received_2.id == msg.id

    # Sender should not receive it
    received_1 = bus.receive("agent_1")
    assert received_1 is None

    print("✓ Broadcast messaging works!")


def test_message_handlers():
    """Test automatic message handlers."""
    print("\n=== Testing Message Handlers ===")

    bus = MessageBus()
    received_messages = []

    def handler(message: Message):
        """Handler that collects messages."""
        received_messages.append(message)
        print(f"Handler received: {message.id}")

    # Register agent and handler
    bus.register_agent("agent_1")
    bus.register_agent("agent_2")
    bus.register_handler("agent_2", handler)

    # Send a message
    msg = Message(
        type=MessageType.QUERY,
        sender="agent_1",
        recipient="agent_2",
        payload={"query": "status"},
    )

    bus.send(msg)

    # Handler should have been called automatically
    assert len(received_messages) == 1
    assert received_messages[0].id == msg.id

    print("✓ Message handlers work!")


def test_json_persistence():
    """Test JSON file persistence."""
    print("\n=== Testing JSON Persistence ===")

    import tempfile
    import os

    # Create a temporary file for testing
    fd, temp_file = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    try:
        # Create bus with JSON storage
        storage = JSONFileStorage(temp_file)
        bus = MessageBus(storage=storage)

        bus.register_agent("agent_1")
        bus.register_agent("agent_2")

        # Send some messages
        for i in range(3):
            msg = Message(
                type=MessageType.COMMAND,
                sender="agent_1",
                recipient="agent_2",
                payload={"command": f"task_{i}"},
            )
            bus.send(msg)

        # Load messages from storage
        persisted = bus.get_all_messages()
        print(f"Persisted {len(persisted)} messages")

        assert len(persisted) == 3
        for i, msg in enumerate(persisted):
            assert msg.payload["command"] == f"task_{i}"

        print("✓ JSON persistence works!")

    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_queue_management():
    """Test queue management operations."""
    print("\n=== Testing Queue Management ===")

    bus = MessageBus()

    bus.register_agent("agent_1")
    bus.register_agent("agent_2")

    # Send multiple messages
    for i in range(5):
        msg = Message(
            type=MessageType.COMMAND,
            sender="agent_1",
            recipient="agent_2",
            payload={"task": i},
        )
        bus.send(msg)

    # Check queue size
    queue_size = bus.get_queue_size("agent_2")
    print(f"Queue size for agent_2: {queue_size}")
    assert queue_size == 5

    # Peek at next message without removing it
    peeked = bus.peek("agent_2")
    print(f"Peeked message: {peeked}")
    assert peeked is not None
    assert peeked.payload["task"] == 0

    # Queue size should still be 5
    assert bus.get_queue_size("agent_2") == 5

    # Receive one message
    received = bus.receive("agent_2")
    assert received.id == peeked.id

    # Queue size should now be 4
    assert bus.get_queue_size("agent_2") == 4

    # Clear the queue
    bus.clear_queue("agent_2")
    assert bus.get_queue_size("agent_2") == 0

    print("✓ Queue management works!")


def test_statistics():
    """Test message bus statistics."""
    print("\n=== Testing Statistics ===")

    bus = MessageBus()

    # Register agents
    for i in range(3):
        bus.register_agent(f"agent_{i}")

    # Send some messages
    msg = Message(
        type=MessageType.COMMAND,
        sender="agent_0",
        recipient="agent_1",
        payload={"test": "data"},
    )
    bus.send(msg)

    # Get statistics
    stats = bus.get_statistics()
    print(f"Bus statistics: {stats}")

    assert stats["total_agents"] == 3
    assert stats["total_queued_messages"] == 1
    assert "agent_0" in stats["registered_agents"]

    print("✓ Statistics work!")


def main():
    """Run all tests."""
    print("Testing Agent Messaging System")
    print("=" * 50)

    try:
        test_direct_messaging()
        test_pubsub_messaging()
        test_broadcast_messaging()
        test_message_handlers()
        test_json_persistence()
        test_queue_management()
        test_statistics()

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
