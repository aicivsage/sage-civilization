# Agent Messaging System

A comprehensive message bus implementation for agent-to-agent communication supporting multiple routing patterns: direct, pub-sub, and broadcast.

## Features

- **Multiple Routing Patterns**
  - Direct (point-to-point) messaging
  - Pub-Sub (topic-based) messaging
  - Broadcast messaging to all agents

- **Message Management**
  - Message validation using Pydantic schemas
  - Priority-based messaging
  - Message status tracking
  - Correlation IDs for request/response patterns
  - Message expiration support

- **Storage Options**
  - In-memory storage (default)
  - JSON file persistence
  - Extensible storage backend interface

- **Advanced Features**
  - Automatic message handlers
  - Thread-safe operations
  - Queue management (peek, clear, size)
  - Message statistics and monitoring

## Installation

The package requires Python 3.8+ and Pydantic:

```bash
pip install pydantic
```

## Quick Start

### Direct Messaging

```python
from agent_messaging import MessageBus, Message, MessageType

# Create message bus and register agents
bus = MessageBus()
bus.register_agent("agent_1")
bus.register_agent("agent_2")

# Send a direct message
msg = Message(
    type=MessageType.COMMAND,
    sender="agent_1",
    recipient="agent_2",
    payload={"action": "process", "data": "test"}
)
bus.send(msg)

# Receive the message
received = bus.receive("agent_2")
print(received.payload)
```

### Pub-Sub Messaging

```python
# Subscribe to a topic
bus.subscribe("agent_2", "notifications")

# Publish to the topic
msg = Message(
    type=MessageType.EVENT,
    sender="agent_1",
    topic="notifications",
    payload={"event": "task_completed"}
)
bus.send(msg)

# Subscriber receives the message
received = bus.receive("agent_2")
```

### Broadcast Messaging

```python
# Send to all registered agents (except sender)
msg = Message(
    type=MessageType.NOTIFICATION,
    sender="agent_1",
    payload={"announcement": "System maintenance at 2AM"}
)
bus.send(msg)
```

### Message Handlers

```python
def my_handler(message: Message):
    print(f"Received: {message.payload}")

bus.register_handler("agent_2", my_handler)
# Handler is called automatically when messages arrive
```

### JSON Persistence

```python
from agent_messaging import MessageBus, JSONFileStorage

storage = JSONFileStorage("messages.json")
bus = MessageBus(storage=storage)

# Messages are automatically persisted to file
# Load all persisted messages
messages = bus.get_all_messages()
```

## Architecture

### Core Components

1. **Message** (`message.py`)
   - Represents a message with validation
   - Supports serialization to/from JSON
   - Tracks status, priority, and metadata

2. **MessageBus** (`message_bus.py`)
   - Central hub for message routing and delivery
   - Manages agent queues and subscriptions
   - Thread-safe operations with locking

3. **MessageRouter** (`routing.py`)
   - Determines routing patterns
   - Delegates to specific routers (Direct, PubSub, Broadcast)
   - Manages topic subscriptions

4. **Schemas** (`schemas.py`)
   - Pydantic models for validation
   - Message types, priorities, and statuses
   - Routing patterns

### Message Flow

1. Agent sends a message via `bus.send(message)`
2. Router determines recipients based on pattern:
   - Direct: Single recipient
   - PubSub: All subscribers to the topic
   - Broadcast: All registered agents
3. Message is added to each recipient's queue
4. Registered handlers are invoked automatically
5. Message is persisted to storage backend
6. Recipients can retrieve messages via `bus.receive(agent_id)`

## API Reference

### MessageBus

#### Methods

- `register_agent(agent_id: str)` - Register an agent
- `unregister_agent(agent_id: str)` - Unregister an agent
- `subscribe(agent_id: str, topic: str)` - Subscribe to a topic
- `unsubscribe(agent_id: str, topic: str)` - Unsubscribe from a topic
- `send(message: Message)` - Send a message
- `receive(agent_id: str) -> Optional[Message]` - Receive next message
- `peek(agent_id: str) -> Optional[Message]` - Peek at next message
- `get_queue_size(agent_id: str) -> int` - Get queue size
- `clear_queue(agent_id: str)` - Clear agent's queue
- `register_handler(agent_id: str, handler: Callable)` - Register message handler
- `get_statistics() -> Dict` - Get bus statistics

### Message

#### Constructor

```python
Message(
    type: MessageType,
    sender: str,
    payload: Dict[str, Any],
    recipient: Optional[str] = None,
    topic: Optional[str] = None,
    priority: MessagePriority = MessagePriority.NORMAL,
    message_id: Optional[str] = None,
    metadata: Optional[MessageMetadata] = None
)
```

#### Properties

- `id: str` - Unique message ID
- `type: MessageType` - Message type
- `sender: str` - Sender agent ID
- `recipient: Optional[str]` - Recipient agent ID
- `topic: Optional[str]` - Topic name
- `payload: Dict[str, Any]` - Message data
- `priority: MessagePriority` - Message priority
- `status: MessageStatus` - Current status
- `created_at: datetime` - Creation timestamp
- `metadata: MessageMetadata` - Additional metadata

#### Methods

- `set_status(status: MessageStatus)` - Update status
- `add_tag(key: str, value: str)` - Add metadata tag
- `to_dict() -> Dict` - Convert to dictionary
- `to_json() -> str` - Convert to JSON
- `from_dict(data: Dict) -> Message` - Create from dictionary
- `from_json(json_str: str) -> Message` - Create from JSON

### Enums

#### MessageType
- `COMMAND` - Command to execute
- `QUERY` - Query for information
- `RESPONSE` - Response to query
- `EVENT` - Event notification
- `NOTIFICATION` - General notification

#### MessagePriority
- `LOW` - Low priority
- `NORMAL` - Normal priority (default)
- `HIGH` - High priority
- `URGENT` - Urgent priority

#### MessageStatus
- `PENDING` - Waiting for delivery
- `DELIVERED` - Delivered to queue
- `PROCESSED` - Processed by recipient
- `FAILED` - Delivery failed

## Examples

See the following files for complete examples:

- `test_agent_messaging.py` - Comprehensive test suite
- `example_agent_messaging.py` - Usage examples

## Thread Safety

The message bus uses threading locks to ensure thread-safe operations. All public methods are safe to call from multiple threads.

## Extensibility

### Custom Storage Backend

Implement the `StorageBackend` interface:

```python
from agent_messaging import StorageBackend, Message

class MyStorage(StorageBackend):
    def save_message(self, message: Message) -> None:
        # Your implementation
        pass

    def load_messages(self) -> List[Message]:
        # Your implementation
        pass

    def clear(self) -> None:
        # Your implementation
        pass

bus = MessageBus(storage=MyStorage())
```

## License

This package is part of the task-tracker project.
