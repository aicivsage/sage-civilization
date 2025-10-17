# Agent Messaging System - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Agent Layer                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Agent 1 │  │ Agent 2 │  │ Agent 3 │  │ Agent N │            │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │            │                  │
│       └────────────┴────────────┴────────────┘                  │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MessageBus (Core)                          │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   Public API                            │    │
│  │  • send(message)                                        │    │
│  │  • receive(agent_id)                                    │    │
│  │  • register_agent(agent_id)                             │    │
│  │  • subscribe(agent_id, topic)                           │    │
│  │  • register_handler(agent_id, callback)                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Message Router                           │      │
│  │                                                        │      │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │      │
│  │  │ DirectRouter │  │ PubSubRouter │  │ Broadcast  │  │      │
│  │  │              │  │              │  │ Router     │  │      │
│  │  │ • route()    │  │ • route()    │  │ • route()  │  │      │
│  │  │              │  │ • subscribe()│  │ • register │  │      │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │      │
│  └──────────────────────────────────────────────────────┘      │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Queue Management                         │      │
│  │                                                        │      │
│  │     Agent 1: [msg1, msg2, ...]                        │      │
│  │     Agent 2: [msg3, msg4, ...]                        │      │
│  │     Agent 3: [msg5, ...]                              │      │
│  │                                                        │      │
│  │  • In-memory deques (thread-safe)                     │      │
│  │  • FIFO ordering                                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │           Storage Backend (Pluggable)                 │      │
│  │                                                        │      │
│  │  ┌────────────────┐      ┌──────────────────┐        │      │
│  │  │ InMemory       │      │ JSONFile         │        │      │
│  │  │ Storage        │      │ Storage          │        │      │
│  │  │                │      │                  │        │      │
│  │  │ • Fast         │      │ • Persistent     │        │      │
│  │  │ • No persist   │      │ • File-based     │        │      │
│  │  └────────────────┘      └──────────────────┘        │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Layer                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                  Message Object                         │    │
│  │  • id: str                                              │    │
│  │  • type: MessageType                                    │    │
│  │  • sender: str                                          │    │
│  │  • recipient: Optional[str]                             │    │
│  │  • topic: Optional[str]                                 │    │
│  │  • payload: Dict[str, Any]                              │    │
│  │  • priority: MessagePriority                            │    │
│  │  • status: MessageStatus                                │    │
│  │  • metadata: MessageMetadata                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │            Pydantic Validation Schemas                  │    │
│  │  • MessageSchema                                        │    │
│  │  • MessageMetadata                                      │    │
│  │  • RouteSchema                                          │    │
│  │  • Enums (MessageType, Priority, Status, Pattern)      │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Message Flow Diagram

### 1. Direct Messaging Flow

```
Agent A                 MessageBus                  Agent B
   │                        │                         │
   │  send(msg)             │                         │
   ├───────────────────────>│                         │
   │                        │                         │
   │                        │ 1. Validate message     │
   │                        │ 2. Route: Direct        │
   │                        │ 3. Get recipient: B     │
   │                        │ 4. Add to B's queue     │
   │                        │ 5. Call B's handlers    │
   │                        │ 6. Persist message      │
   │                        │                         │
   │                        │      receive()          │
   │                        │<────────────────────────┤
   │                        │                         │
   │                        │      return msg         │
   │                        ├────────────────────────>│
   │                        │                         │
```

### 2. Pub-Sub Messaging Flow

```
Agent A           MessageBus           Agent B    Agent C
   │                  │                   │          │
   │                  │  subscribe("events")         │
   │                  │<──────────────────┤          │
   │                  │  subscribe("events")         │
   │                  │<─────────────────────────────┤
   │                  │                   │          │
   │  send(msg)       │                   │          │
   │  topic="events"  │                   │          │
   ├─────────────────>│                   │          │
   │                  │                   │          │
   │                  │ 1. Validate       │          │
   │                  │ 2. Route: PubSub  │          │
   │                  │ 3. Get subscribers│          │
   │                  │ 4. Add to B queue │          │
   │                  │ 5. Add to C queue │          │
   │                  │                   │          │
   │                  │    receive()      │          │
   │                  │<──────────────────┤          │
   │                  │    return msg     │          │
   │                  ├──────────────────>│          │
   │                  │                   │          │
   │                  │    receive()                 │
   │                  │<─────────────────────────────┤
   │                  │    return msg                │
   │                  ├─────────────────────────────>│
```

### 3. Broadcast Messaging Flow

```
Agent A           MessageBus           Agent B    Agent C    Agent D
   │                  │                   │          │          │
   │  send(msg)       │                   │          │          │
   │  (no recipient/  │                   │          │          │
   │   topic)         │                   │          │          │
   ├─────────────────>│                   │          │          │
   │                  │                   │          │          │
   │                  │ 1. Validate       │          │          │
   │                  │ 2. Route: Bcast   │          │          │
   │                  │ 3. Get all agents │          │          │
   │                  │ 4. Exclude sender │          │          │
   │                  │ 5. Add to all     │          │          │
   │                  │    queues         │          │          │
   │                  │                   │          │          │
   │                  │ (A doesn't receive own message)         │
```

## Routing Decision Tree

```
                    Message Received
                          │
                          ▼
                  ┌───────────────┐
                  │ Has recipient?│
                  └───────┬───────┘
                          │
                ┌─────────┴─────────┐
                │                   │
               YES                 NO
                │                   │
                ▼                   ▼
        ┌──────────────┐    ┌──────────────┐
        │   DIRECT     │    │  Has topic?  │
        │   ROUTING    │    └──────┬───────┘
        └──────────────┘           │
                              ┌────┴────┐
                              │         │
                             YES       NO
                              │         │
                              ▼         ▼
                      ┌──────────┐  ┌──────────┐
                      │  PUB-SUB │  │BROADCAST │
                      │  ROUTING │  │ ROUTING  │
                      └──────────┘  └──────────┘
```

## Thread Safety Model

```
┌─────────────────────────────────────────────────────────┐
│                  MessageBus Operations                   │
│                                                          │
│  Thread 1              Thread 2              Thread 3   │
│     │                     │                     │       │
│     ▼                     ▼                     ▼       │
│  send(msg1)           send(msg2)           receive()    │
│     │                     │                     │       │
│     └─────────────────────┴─────────────────────┘       │
│                           │                              │
│                           ▼                              │
│                    ┌─────────────┐                       │
│                    │  Threading  │                       │
│                    │    Lock     │                       │
│                    └─────────────┘                       │
│                           │                              │
│                           ▼                              │
│              Serialized Access to:                       │
│              • Queue dictionaries                        │
│              • Subscription maps                         │
│              • Agent registry                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Storage Backend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  StorageBackend (ABC)                    │
│                                                          │
│  + save_message(message: Message) -> None                │
│  + load_messages() -> List[Message]                      │
│  + clear() -> None                                       │
└──────────────────────┬───────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌──────────────────┐         ┌──────────────────┐
│  InMemoryStorage │         │  JSONFileStorage │
│                  │         │                  │
│  • List storage  │         │  • File I/O      │
│  • No persist    │         │  • JSON format   │
│  • Fast          │         │  • Thread-safe   │
│  • Testing       │         │  • Persistent    │
└──────────────────┘         └──────────────────┘
```

## Component Dependencies

```
┌────────────┐
│  Message   │
│   Class    │
└─────┬──────┘
      │ uses
      ▼
┌────────────┐
│  Schemas   │◄─────────────┐
└─────┬──────┘              │
      │                     │
      │ validates           │
      ▼                     │
┌────────────┐              │
│  Routing   │              │
│   System   │              │
└─────┬──────┘              │
      │                     │
      │ used by             │
      ▼                     │
┌────────────┐          ┌───┴────┐
│ MessageBus │────uses──┤Storage │
└────────────┘          └────────┘
```

## Class Hierarchy

```
Message
  └── Properties: id, type, sender, recipient, topic, payload, priority, status, metadata
  └── Methods: to_dict(), to_json(), from_dict(), from_json(), set_status(), add_tag()

MessageBus
  ├── _queues: Dict[str, Deque[Message]]
  ├── _router: MessageRouter
  ├── _storage: StorageBackend
  ├── _handlers: Dict[str, List[Callable]]
  └── Methods: register_agent(), send(), receive(), subscribe(), etc.

MessageRouter
  ├── _direct_router: DirectRouter
  ├── _pubsub_router: PubSubRouter
  ├── _broadcast_router: BroadcastRouter
  └── Methods: route(), determine_pattern(), subscribe(), etc.

Router (ABC)
  ├── DirectRouter
  │   └── route() -> List[str]
  ├── PubSubRouter
  │   ├── _subscriptions: Dict[str, Set[str]]
  │   └── route() -> List[str]
  └── BroadcastRouter
      ├── _agents: Set[str]
      └── route() -> List[str]

StorageBackend (ABC)
  ├── InMemoryStorage
  │   └── _messages: List[Dict]
  └── JSONFileStorage
      └── file_path: Path
```

## Key Design Patterns

1. **Strategy Pattern** - Different routing strategies (Direct, PubSub, Broadcast)
2. **Dependency Injection** - Storage backend is injected
3. **Observer Pattern** - Message handlers are observers
4. **Factory Pattern** - Message.from_dict(), Message.from_json()
5. **Repository Pattern** - StorageBackend abstracts persistence
6. **Singleton (per bus)** - Each MessageBus manages its own state

## Extensibility Points

1. **Custom Storage Backends**
   - Implement StorageBackend interface
   - Examples: Redis, PostgreSQL, MongoDB

2. **Custom Routing Strategies**
   - Extend Router ABC
   - Examples: Priority routing, Load-balanced routing

3. **Message Middleware**
   - Hook into send/receive
   - Examples: Logging, metrics, encryption

4. **Custom Message Types**
   - Extend MessageType enum
   - Add custom validation

5. **Handler Chains**
   - Multiple handlers per agent
   - Middleware pattern for processing
