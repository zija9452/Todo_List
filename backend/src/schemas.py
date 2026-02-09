from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class TaskBase(BaseModel):
    """
    Base schema for task data.
    Contains common fields shared between TaskCreate and TaskUpdate.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description (up to 1000 characters)")
    priority: Optional[PriorityEnum] = Field(None, description="Task priority level (high, medium, low, or null)")
    due_date: Optional[date] = Field(None, description="Optional due date for the task")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    Inherits from TaskBase and adds any creation-specific fields.
    """
    pass  # All fields come from TaskBase


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title (1-200 characters, optional)")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description (up to 1000 characters)")
    completed: Optional[bool] = Field(None, description="Boolean indicating if the task is completed")
    priority: Optional[PriorityEnum] = Field(None, description="Task priority level (high, medium, low, or null)")
    due_date: Optional[date] = Field(None, description="Optional due date for the task")


class TaskResponse(TaskBase):
    """
    Schema for returning task information in API responses.
    Includes all base fields plus additional response-specific fields.
    """
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """
    Schema for returning a list of tasks.
    """
    tasks: List[TaskResponse]


class TaskQueryParams(BaseModel):
    """
    Schema for query parameters for filtering and sorting tasks.
    """
    status: Optional[str] = Field(None, description="Filter by status: all|pending|completed")
    sort: Optional[str] = Field(None, description="Sort by: created|title|due_date")
    order: Optional[str] = Field(None, description="Order: asc|desc")


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for JWT token data.
    """
    user_id: Optional[str] = None
    username: Optional[str] = None


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user information.
    """
    id: int
    username: str
    email: str
    created_at: datetime


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str


class HealthCheck(BaseModel):
    """
    Schema for health check response.
    """
    status: str
    timestamp: datetime