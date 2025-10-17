"""
Pydantic models for type-safe data handling.
"""

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


class TaskCollection(BaseModel):
    """Container for all tasks with version tracking"""

    version: str = "1.0.0"
    last_id: int = 0
    tasks: List[Task] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
