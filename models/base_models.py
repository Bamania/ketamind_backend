"""
Central location for all Pydantic models used across the application.
This file contains all base models that can be imported and used throughout the project.
"""

from typing import Optional, Any, List, Dict, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

# =============================================================================
# COMMON RESPONSE MODELS
# =============================================================================

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """Generic API response model"""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data")
    errors: Optional[List[str]] = Field(None, description="List of error messages")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class SuccessResponse(BaseModel):
    """Standard success response"""
    status: str = Field(default="success", description="Response status")
    message: str = Field(..., description="Success message")
    data: Optional[Any] = Field(None, description="Response data")

class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = Field(default="error", description="Response status")
    message: str = Field(..., description="Error message")
    errors: Optional[List[str]] = Field(None, description="Detailed error list")
    code: Optional[str] = Field(None, description="Error code")

# =============================================================================
# TODO MODELS
# =============================================================================

class TodoBase(BaseModel):
    """Base todo model with common fields"""
    text: str = Field(..., min_length=1, max_length=500, description="Todo text content")
    
class TodoCreate(TodoBase):
    """Model for creating a new todo"""
    user_id: Optional[str] = Field(None, description="User ID who owns this todo")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Complete the project documentation",
                "user_id": "user123"
            }
        }
    )

class TodoUpdate(BaseModel):
    """Model for updating an existing todo"""
    text: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated todo text")
    completed: Optional[bool] = Field(None, description="Todo completion status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Updated todo text",
                "completed": True
            }
        }
    )

class TodoResponse(TodoBase):
    """Model for todo responses"""
    id: str = Field(..., description="Unique todo identifier")
    completed: bool = Field(default=False, description="Todo completion status")
    created_at: str = Field(..., description="Todo creation timestamp")
    updated_at: Optional[str] = Field(None, description="Todo last update timestamp")
    user_id: Optional[str] = Field(None, description="User ID who owns this todo")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "todo123",
                "text": "Complete the project documentation",
                "completed": False,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T11:00:00Z",
                "user_id": "user123"
            }
        }
    )

# =============================================================================
# USER MODELS (for future expansion)
# =============================================================================

class UserBase(BaseModel):
    """Base user model"""
    email: str = Field(..., description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")

class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str = Field(..., min_length=8, description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "securepassword123"
            }
        }
    )

class UserResponse(UserBase):
    """Model for user responses"""
    id: str = Field(..., description="Unique user identifier")
    is_active: bool = Field(default=True, description="User active status")
    created_at: str = Field(..., description="User creation timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "user123",
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    )

# =============================================================================
# HABIT MODELS (for future expansion)
# =============================================================================

class HabitFrequency(str, Enum):
    """Habit frequency options"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class HabitBase(BaseModel):
    """Base habit model"""
    name: str = Field(..., min_length=1, max_length=200, description="Habit name")
    description: Optional[str] = Field(None, max_length=1000, description="Habit description")
    frequency: HabitFrequency = Field(default=HabitFrequency.DAILY, description="Habit frequency")
    target_count: int = Field(default=1, ge=1, description="Target count per frequency period")

class HabitCreate(HabitBase):
    """Model for creating a new habit"""
    user_id: Optional[str] = Field(None, description="User ID who owns this habit")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Morning Exercise",
                "description": "30 minutes of morning exercise",
                "frequency": "daily",
                "target_count": 1,
                "user_id": "user123"
            }
        }
    )

class HabitResponse(HabitBase):
    """Model for habit responses"""
    id: str = Field(..., description="Unique habit identifier")
    is_active: bool = Field(default=True, description="Habit active status")
    current_streak: int = Field(default=0, description="Current streak count")
    longest_streak: int = Field(default=0, description="Longest streak achieved")
    created_at: str = Field(..., description="Habit creation timestamp")
    updated_at: Optional[str] = Field(None, description="Habit last update timestamp")
    user_id: Optional[str] = Field(None, description="User ID who owns this habit")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "habit123",
                "name": "Morning Exercise",
                "description": "30 minutes of morning exercise",
                "frequency": "daily",
                "target_count": 1,
                "is_active": True,
                "current_streak": 5,
                "longest_streak": 10,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T11:00:00Z",
                "user_id": "user123"
            }
        }
    )

# =============================================================================
# PAGINATION MODELS
# =============================================================================

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")
    
class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")

# =============================================================================
# FILTER MODELS
# =============================================================================

class TodoFilter(BaseModel):
    """Todo filtering options"""
    completed: Optional[bool] = Field(None, description="Filter by completion status")
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    created_after: Optional[datetime] = Field(None, description="Filter todos created after this date")
    created_before: Optional[datetime] = Field(None, description="Filter todos created before this date")
    search: Optional[str] = Field(None, description="Search in todo text")

# =============================================================================
# BULK OPERATION MODELS
# =============================================================================

class BulkTodoUpdate(BaseModel):
    """Model for bulk todo updates"""
    todo_ids: List[str] = Field(..., description="List of todo IDs to update")
    completed: Optional[bool] = Field(None, description="Set completion status for all todos")

class BulkOperationResponse(BaseModel):
    """Response for bulk operations"""
    success_count: int = Field(..., description="Number of successfully processed items")
    failed_count: int = Field(..., description="Number of failed items")
    failed_ids: List[str] = Field(default_factory=list, description="IDs of failed items")
    message: str = Field(..., description="Operation summary message")
