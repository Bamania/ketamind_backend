# Models package - Central location for all Pydantic models
from .base_models import (
    # Todo models
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    
    # Common response models
    APIResponse,
    SuccessResponse,
    ErrorResponse,
    
    # User models (for future expansion)
    UserBase,
    UserCreate,
    UserResponse,
    
    # Habit models (for future expansion)
    HabitBase,
    HabitCreate,
    HabitResponse,
)

__all__ = [
    # Todo models
    "TodoCreate",
    "TodoUpdate", 
    "TodoResponse",
    
    # Common response models
    "APIResponse",
    "SuccessResponse",
    "ErrorResponse",
    
    # User models
    "UserBase",
    "UserCreate",
    "UserResponse",
    
    # Habit models
    "HabitBase",
    "HabitCreate",
    "HabitResponse",
]
