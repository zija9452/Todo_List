from sqlmodel import SQLModel, Field
from typing import Optional
import datetime
from enum import Enum
from sqlalchemy import Column, DateTime


class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Task(SQLModel, table=True):
    """
    Task model representing a user's to-do item.

    Attributes:
        id: Unique identifier for the task
        user_id: Foreign key linking to the user who owns the task
        title: Task title (1-200 characters)
        description: Optional task description (up to 1000 characters)
        completed: Boolean indicating if the task is completed
        priority: Task priority level (high, medium, low, or null)
        due_date: Optional due date for the task
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Foreign key linking to user
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: Optional[PriorityEnum] = Field(sa_column=Column(name="priority", default="medium"))
    due_date: Optional[datetime.date] = Field(default=None)
    created_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime, default=datetime.datetime.utcnow)
    )
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    )


class TaskCreate(SQLModel):
    """
    Schema for creating a new task.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional task description (up to 1000 characters)
        priority: Task priority level (high, medium, low, or null)
        due_date: Optional due date for the task
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime.date] = None


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.

    Attributes:
        title: Task title (1-200 characters, optional)
        description: Optional task description (up to 1000 characters)
        completed: Boolean indicating if the task is completed
        priority: Task priority level (high, medium, low, or null)
        due_date: Optional due date for the task
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime.date] = None


class TaskResponse(SQLModel):
    """
    Schema for returning task information in API responses.

    Attributes:
        id: Unique identifier for the task
        user_id: Foreign key linking to the user who owns the task
        title: Task title
        description: Optional task description
        completed: Boolean indicating if the task is completed
        priority: Task priority level (high, medium, low, or null)
        due_date: Optional due date for the task
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
    """
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime.date] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime