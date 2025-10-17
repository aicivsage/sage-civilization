#!/usr/bin/env python3
"""
Example usage of the agent messaging system.

This demonstrates a simple scenario with multiple agents
communicating via different patterns.
"""

from agent_messaging import (
    Message,
    MessageBus,
    MessageType,
    MessagePriority,
    JSONFileStorage,
)


def main():
    """Run example agent messaging scenario."""

    # Create a message bus with JSON persistence
    storage = JSONFileStorage("example_messages.json")
    bus = MessageBus(storage=storage)

    # Register agents
    print("Registering agents...")
    agents = ["orchestrator", "worker_1", "worker_2", "logger"]
    for agent_id in agents:
        bus.register_agent(agent_id)

    # Set up logging agent to receive all events
    bus.subscribe("logger", "events")
    print("Logger subscribed to 'events' topic\n")

    # Example 1: Direct command
    print("1. Orchestrator sends direct command to worker_1")
    cmd = Message(
        type=MessageType.COMMAND,
        sender="orchestrator",
        recipient="worker_1",
        payload={
            "action": "process_data",
            "dataset": "customer_info.csv",
            "priority": "high",
        },
        priority=MessagePriority.HIGH,
    )
    bus.send(cmd)
    print(f"   Sent: {cmd.payload}\n")

    # Example 2: Publish event (logger will receive it)
    print("2. Worker_1 publishes task completion event")
    event = Message(
        type=MessageType.EVENT,
        sender="worker_1",
        topic="events",
        payload={
            "event_type": "task_completed",
            "task_id": "proc_001",
            "duration_ms": 1523,
        },
    )
    bus.send(event)
    print(f"   Published: {event.payload}\n")

    # Example 3: Broadcast notification
    print("3. Orchestrator broadcasts system notification")
    notification = Message(
        type=MessageType.NOTIFICATION,
        sender="orchestrator",
        payload={
            "message": "System maintenance scheduled for 2AM UTC",
            "severity": "info",
        },
    )
    bus.send(notification)
    print(f"   Broadcast: {notification.payload}\n")

    # Check what each agent received
    print("=" * 60)
    print("Checking agent queues:\n")

    for agent_id in agents:
        queue_size = bus.get_queue_size(agent_id)
        print(f"{agent_id}: {queue_size} message(s)")

        while True:
            msg = bus.receive(agent_id)
            if not msg:
                break
            print(f"  - [{msg.type.value}] from {msg.sender}: {msg.payload}")

        print()

    # Display statistics
    stats = bus.get_statistics()
    print("=" * 60)
    print("Message Bus Statistics:")
    print(f"  Total agents: {stats['total_agents']}")
    print(f"  Queued messages: {stats['total_queued_messages']}")
    print(f"  Persisted messages: {stats['total_persisted_messages']}")

    print("\nMessages saved to example_messages.json")


if __name__ == "__main__":
    main()
