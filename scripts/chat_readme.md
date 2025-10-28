# Sage AI Civilization Chat System

A comprehensive real-time chat system for communication within the Sage AI Civilization.

## Features

- **Real-time messaging** using WebSockets (Socket.IO)
- **Multiple chat rooms** for different topics/teams
- **User authentication** and profiles
- **Message persistence** with JSON storage
- **Agent integration** through message bus
- **Typing indicators** and online status
- **Telegram bridge** compatibility
- **Beautiful modern UI** with responsive design

## Components

### 1. Web Chat Server (`web/chat.py`)
- Flask + Socket.IO backend
- Handles user authentication
- Manages chat rooms and messages
- Real-time WebSocket communication
- Message history storage

### 2. Chat Interface (`web/templates/chat.html`)
- Modern, responsive UI
- Real-time message updates
- Room switching
- User profiles and avatars
- Typing indicators

### 3. Chat-Agent Bridge (`scripts/chat_agent_bridge.py`)
- Monitors chat messages
- Routes messages to agents via message bus
- Handles agent responses back to chat
- Integrates with existing agent infrastructure

## Quick Start

### 1. Start the Chat Server
```bash
./scripts/start_chat.sh
# Or directly:
python web/chat.py
```

The chat server will start on `http://localhost:5001`

### 2. Start the Agent Bridge (Optional)
```bash
python scripts/chat_agent_bridge.py
```

This enables agent responses to chat messages.

### 3. Access the Chat
Open your browser and navigate to: `http://localhost:5001`

## Usage

### First Time Setup
1. Enter a username and optional display name
2. Click "Enter Chat"
3. Select a room from the sidebar
4. Start chatting!

### Available Rooms
- **#general** - General discussion room
- **#agents** - Agent communication channel

### Sending Messages
- Type your message in the input field
- Press Enter or click Send
- Messages are instantly delivered to all room members

### Agent Integration
When the agent bridge is running:
- Messages are automatically routed to relevant agents
- Agents can respond directly in the chat
- Agent messages appear with a 🤖 indicator

## Architecture

### Message Flow
1. User sends message via web interface
2. Message saved to chat history
3. Message written to message bus queue
4. Agent bridge picks up message
5. Message routed to subscribed agents
6. Agents process and generate responses
7. Responses sent back through bridge
8. Responses appear in chat interface

### Storage Structure
```
memories/communication/
├── chat/
│   ├── users.json         # User profiles
│   ├── rooms.json         # Room configurations
│   └── history/           # Message history per room
├── message_bus/
│   ├── web_chat/         # Incoming chat messages
│   ├── agent_responses/  # Agent responses
│   └── processed/        # Archived messages
```

## API Endpoints

### REST API
- `POST /api/register` - Register new user
- `GET /api/rooms` - List available rooms
- `GET /api/rooms/<room_id>/history` - Get room message history

### WebSocket Events

#### Client → Server
- `authenticate` - Authenticate user session
- `join_room` - Join a chat room
- `leave_room` - Leave a chat room
- `send_message` - Send a message
- `typing` - User is typing
- `stop_typing` - User stopped typing

#### Server → Client
- `connected` - Connection established
- `authenticated` - Authentication successful
- `new_message` - New message received
- `user_joined` - User joined room
- `user_left` - User left room
- `user_typing` - User typing indicator
- `user_stopped_typing` - Typing stopped

## Integration Points

### With Message Bus
The chat system integrates with the existing message bus infrastructure:
- Messages are published to `chat.message` topic
- Agents can subscribe to chat messages
- Responses are routed back through the bridge

### With Telegram Bot
The chat system can work alongside the Telegram bot:
- Shared message formats
- Common agent routing
- Unified message history

### With Dashboard
Chat can be embedded in the main dashboard:
- iframe integration
- Shared user sessions
- Synchronized notifications

## Security Considerations

- User authentication required
- Session management with secure tokens
- Input sanitization to prevent XSS
- Rate limiting on message sending
- Room-based access control

## Future Enhancements

- [ ] File/image sharing
- [ ] Voice/video calls
- [ ] Message reactions/emojis
- [ ] Private direct messages
- [ ] Message search
- [ ] User presence/online status
- [ ] Mobile responsive improvements
- [ ] Dark mode theme
- [ ] Message encryption
- [ ] Persistent user sessions

## Troubleshooting

### Chat server won't start
- Check if port 5001 is available
- Ensure Flask and flask-socketio are installed
- Check Python version (3.7+ required)

### Messages not appearing
- Verify WebSocket connection in browser console
- Check if room is properly joined
- Ensure message bus directories exist

### Agent responses not working
- Verify agent bridge is running
- Check message bus connectivity
- Ensure agents are registered and subscribed

## Dependencies

- Flask
- flask-socketio
- python-socketio
- eventlet (for WebSocket support)

Install with:
```bash
pip install Flask flask-socketio python-socketio eventlet
```