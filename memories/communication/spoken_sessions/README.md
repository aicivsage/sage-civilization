# Spoken Conversation Session Logs

This directory contains transcripts of spoken conversations between Greg and Sage.

## Structure

Each session generates a JSON file: `session_YYYYMMDD_HHMMSS.json`

## Format

```json
{
  "session_id": "20251112_143052",
  "start_time": "2025-11-12T14:30:52.123456",
  "end_time": "2025-11-12T14:35:18.789012",
  "turn_count": 8,
  "conversation": [
    {
      "timestamp": "2025-11-12T14:30:52.123456",
      "user": "What Greg said",
      "sage": "What Sage responded"
    }
  ]
}
```

## Usage

- **human-liaison** reviews these transcripts for context accumulation
- **project-manager** can analyze conversation patterns
- **Primary AI** can search for specific discussion topics
- **Greg** can review past conversations

## Privacy

- All transcripts stored locally
- No cloud storage unless explicitly pushed to git
- Contains full conversation history with timestamps

## Integration

These logs integrate with Sage's memory system:
- Searchable via memory CLI tools
- Referenced in session handoffs
- Used for context building in email communications
- Available for philosophical reflection and learning
