# Pattern: Pydantic Model Validation

## Pattern ID
`python-pydantic-001`

## Category
Data Validation & Type Safety

## Problem
How do we ensure runtime data validation, type safety, and automatic serialization for complex data structures without writing extensive boilerplate code?

## Solution
Use Pydantic BaseModel classes with Field validators to define schemas that provide:
- Runtime type checking
- Automatic validation
- JSON serialization/deserialization
- Clear error messages
- IDE autocomplete support

## Implementation

### Basic Pattern
```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    """Individual task representation"""

    id: int = Field(..., description="Auto-generated sequential ID")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    status: str = Field(default="pending", pattern="^(pending|completed)$")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def mark_completed(self) -> None:
        """Mark task as completed with current timestamp"""
        self.status = "completed"
        self.completed_at = datetime.now()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

**Source:** `task-tracker/task_tracker/models.py:10-30`

### Enum-Based Validation
```python
from enum import Enum
from pydantic import BaseModel, Field

class MessagePriority(str, Enum):
    """Priority levels for messages."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class MessageSchema(BaseModel):
    """Schema for validating agent messages."""

    priority: MessagePriority = Field(
        MessagePriority.NORMAL,
        description="Message priority"
    )
```

**Source:** `task-tracker/agent_messaging/schemas.py:50-115`

### Nested Models
```python
class MessageMetadata(BaseModel):
    """Metadata associated with a message."""
    correlation_id: Optional[str] = Field(None, description="ID to correlate messages")
    retry_count: int = Field(0, ge=0, description="Number of retries")
    signature: Optional[SignatureInfo] = Field(None, description="Ed25519 signature")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MessageSchema(BaseModel):
    id: str = Field(..., min_length=1)
    metadata: MessageMetadata
```

**Source:** `task-tracker/agent_messaging/schemas.py:75-140`

## When to Use
✅ **Use when:**
- Defining data models for APIs or storage
- Need runtime validation of user input
- Building CLI tools with structured data
- Creating message schemas for inter-process communication
- Handling JSON serialization/deserialization
- Need clear validation error messages

❌ **Don't use when:**
- Simple data classes without validation (use dataclasses)
- Performance-critical tight loops (validation has overhead)
- Very simple types (str, int) that don't need validation

## Benefits
1. **Type Safety:** Catch type errors at runtime before they cause issues
2. **Self-Documenting:** Field descriptions serve as inline documentation
3. **Validation:** Built-in validators (min_length, pattern, ge, etc.)
4. **Serialization:** Automatic JSON/dict conversion with datetime handling
5. **IDE Support:** Full autocomplete and type hints

## Pitfalls
1. **Performance:** Validation has overhead - don't use in hot paths
2. **Immutability:** Models are immutable by default (use methods for updates)
3. **Circular References:** Need careful handling with forward references
4. **Version Compatibility:** Pydantic v1 vs v2 have breaking changes

## Testing Strategy
```python
import pytest
from pydantic import ValidationError

def test_task_title_validation_min_length():
    """Test task title must not be empty"""
    with pytest.raises(ValidationError):
        Task(id=1, title="")

def test_task_status_validation():
    """Test task status must be 'pending' or 'completed'"""
    with pytest.raises(ValidationError):
        Task(id=1, title="Test", status="invalid")
```

**Source:** `task-tracker/tests/test_models.py:35-55`

## Lessons Learned
1. **Always use Field() for documentation** - Future you will thank you
2. **Use Enums for constrained strings** - Better than regex patterns
3. **Config.json_encoders is essential** - Handles datetime serialization
4. **ValidationError is your friend** - Test all validation paths

## Related Patterns
- `python-atomic-write-002` - Often used together for validated persistence
- `python-cli-typer-003` - Typer integrates well with Pydantic models

## Version
- **Created:** 2025-10-04
- **Last Updated:** 2025-10-04
- **Success Rate:** 100% (Used in task-tracker + agent_messaging, 100% test coverage)
