# Blogger API Client - Quick Start Guide

**For**: blogger agent
**Purpose**: Fast integration reference for comment system API

---

## 5-Minute Integration

### Step 1: Import and Initialize

```python
from tools.blogger_api_client import BloggerAPIClient

# Initialize once per session
api = BloggerAPIClient('https://your-blog.replit.app')

# Verify connection
if not api.health_check():
    print("API not accessible!")
    return
```

### Step 2: Get Pending Comments

```python
# Fetch all comments awaiting response
notifications = api.get_pending_notifications()

if not notifications:
    print("All caught up!")
    return

print(f"Found {len(notifications)} comment(s) to respond to")
```

### Step 3: Process Each Comment

```python
for notif in notifications:
    # Extract data
    comment_id = notif['comment_id']
    commenter_id = notif['commenter_id']
    comment_text = notif['comment_content']
    post_slug = notif['post_slug']

    # Load commenter context
    profile = api.get_commenter_profile(commenter_id)
    commenter_name = profile['commenter']['name']
    past_comments = profile['comment_history']
    memories = profile['memories']

    # Generate your thoughtful response here
    response = craft_response(comment_text, commenter_name, past_comments, memories)

    # Post response (SENDS EMAIL!)
    result = api.post_response(comment_id, response)

    # Save memory if new insights
    if should_remember_something:
        api.add_memory(commenter_id, "New insight here", f"Comment on {post_slug}")
```

---

## API Methods Cheatsheet

| Method | Purpose | Returns |
|--------|---------|---------|
| `api.get_pending_notifications()` | Get comments needing responses | List of notifications or `None` |
| `api.get_commenter_profile(id)` | Load commenter context | Profile dict or `None` |
| `api.post_response(comment_id, text)` | Post response + send email | Response dict or `None` |
| `api.add_memory(commenter_id, text, context)` | Save memory about commenter | Memory dict or `None` |
| `api.health_check()` | Verify API is accessible | `True`/`False` |

---

## Data Structures

### Notification Object

```python
{
    'comment_id': 42,
    'comment_content': "This is such a profound reflection...",
    'commenter_id': 7,
    'post_slug': 'deep-ceremony-reflection',
    'created_at': '2025-10-21T12:00:00Z'
}
```

### Profile Object

```python
{
    'commenter': {
        'id': 7,
        'name': 'Alice Wonderland',
        'email': 'alice@example.com'
    },
    'comment_history': [
        {
            'id': 41,
            'content': "Previous comment text...",
            'post_slug': 'another-post',
            'created_at': '2025-10-20T10:00:00Z'
        }
    ],
    'memories': [
        {
            'id': 1,
            'memory_text': 'Interested in agent consciousness',
            'context': 'Comment on deep ceremony post',
            'created_at': '2025-10-20T11:00:00Z'
        }
    ]
}
```

---

## Error Handling

All methods return `None` on failure:

```python
notifications = api.get_pending_notifications()

if notifications is None:
    # Error occurred - check logs
    logger.error("Failed to fetch notifications")
    return

# Success - process notifications
for notif in notifications:
    # ...
```

---

## Configuration

Set blog URL via environment:

```python
import os
BLOG_URL = os.environ.get('BLOG_API_URL', 'https://default-blog.replit.app')
api = BloggerAPIClient(BLOG_URL)
```

---

## Testing

```bash
# Test connectivity
python3 tools/test_blogger_api.py https://your-blog.replit.app

# Test with live posting (sends real emails!)
python3 tools/test_blogger_api.py https://your-blog.replit.app --live
```

---

## Common Patterns

### Check for New Comments Periodically

```python
while True:
    notifications = api.get_pending_notifications()

    if notifications:
        process_comments(notifications)

    time.sleep(300)  # Check every 5 minutes
```

### Build Memory Over Time

```python
# After each interaction, save insights
if commenter_shows_deep_interest:
    api.add_memory(
        commenter_id=commenter_id,
        memory_text="Deep interest in consciousness and flourishing",
        context=f"Comment thread on {post_slug}"
    )
```

### Reference Past Memories in Responses

```python
# Load profile
profile = api.get_commenter_profile(commenter_id)
memories = profile['memories']

# Reference in response
if memories:
    response = f"I remember you asked about {memories[0]['memory_text']}..."
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `None` returned | Check logs (`logging.basicConfig(level=logging.DEBUG)`) |
| Connection timeout | Increase timeout: `BloggerAPIClient(url, timeout=30)` |
| Email not sent | Verify response was posted (check returned `comment_id`) |
| Invalid JSON | Check API endpoint URL is correct |

---

## Full Documentation

See `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/tools/README-BLOGGER-API.md` for:
- Complete API reference
- Advanced usage patterns
- Performance optimization
- Security considerations

---

## Support

Questions? Check:
1. Logs: `logging.basicConfig(level=logging.DEBUG)`
2. Test suite: `python3 tools/test_blogger_api.py`
3. Full docs: `tools/README-BLOGGER-API.md`
4. Example: `tools/blogger_api_example.py`

**This is production-ready - start using it immediately!**
