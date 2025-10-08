"""
Examples of how to use the centralized models throughout the application.
This file serves as a reference for developers on how to properly use the models.
"""

from models import (
    TodoCreate, 
    TodoUpdate, 
    TodoResponse,
    APIResponse,
    SuccessResponse,
    ErrorResponse,
    UserCreate,
    HabitCreate,
    PaginatedResponse,
    TodoFilter,
    BulkTodoUpdate
)
from typing import List

# =============================================================================
# TODO MODEL USAGE EXAMPLES
# =============================================================================

def example_todo_creation():
    """Example of creating a todo"""
    # Create a new todo
    new_todo = TodoCreate(
        text="Complete the project documentation",
        user_id="user123"
    )
    
    # Update a todo
    todo_update = TodoUpdate(
        text="Updated project documentation",
        completed=True
    )
    
    # Example response
    todo_response = TodoResponse(
        id="todo123",
        text="Complete the project documentation",
        completed=False,
        created_at="2024-01-15T10:30:00Z",
        user_id="user123"
    )
    
    return new_todo, todo_update, todo_response

# =============================================================================
# API RESPONSE USAGE EXAMPLES
# =============================================================================

def example_api_responses():
    """Example of using standardized API responses"""
    
    # Success response with data
    success_response = SuccessResponse(
        message="Todo created successfully",
        data={
            "id": "todo123",
            "text": "Complete documentation",
            "completed": False
        }
    )
    
    # Error response
    error_response = ErrorResponse(
        message="Failed to create todo",
        errors=["Text cannot be empty", "User ID is required"],
        code="VALIDATION_ERROR"
    )
    
    # Generic API response
    api_response: APIResponse[TodoResponse] = APIResponse(
        success=True,
        message="Todo retrieved successfully",
        data=TodoResponse(
            id="todo123",
            text="Complete documentation",
            completed=False,
            created_at="2024-01-15T10:30:00Z"
        )
    )
    
    return success_response, error_response, api_response

# =============================================================================
# FILTERING AND PAGINATION EXAMPLES
# =============================================================================

def example_filtering_and_pagination():
    """Example of using filtering and pagination models"""
    
    # Todo filtering
    todo_filter = TodoFilter(
        completed=False,
        user_id="user123",
        search="documentation"
    )
    
    # Paginated response
    paginated_todos = PaginatedResponse[TodoResponse](
        items=[
            TodoResponse(
                id="todo1",
                text="Task 1",
                completed=False,
                created_at="2024-01-15T10:30:00Z"
            ),
            TodoResponse(
                id="todo2", 
                text="Task 2",
                completed=True,
                created_at="2024-01-15T11:00:00Z"
            )
        ],
        total=25,
        page=1,
        limit=10,
        pages=3,
        has_next=True,
        has_prev=False
    )
    
    return todo_filter, paginated_todos

# =============================================================================
# BULK OPERATIONS EXAMPLES
# =============================================================================

def example_bulk_operations():
    """Example of bulk operations"""
    
    # Bulk update request
    bulk_update = BulkTodoUpdate(
        todo_ids=["todo1", "todo2", "todo3"],
        completed=True
    )
    
    return bulk_update

# =============================================================================
# FUTURE MODELS EXAMPLES
# =============================================================================

def example_future_models():
    """Examples of user and habit models for future expansion"""
    
    # User creation
    new_user = UserCreate(
        email="user@example.com",
        username="johndoe",
        full_name="John Doe",
        password="securepassword123"
    )
    
    # Habit creation
    new_habit = HabitCreate(
        name="Morning Exercise",
        description="30 minutes of morning exercise",
        frequency="daily",
        target_count=1,
        user_id="user123"
    )
    
    return new_user, new_habit

# =============================================================================
# USAGE IN SERVICES
# =============================================================================

def example_service_usage():
    """
    Example of how to use these models in service classes
    """
    
    # In your service methods, you can now import and use:
    # from models import TodoCreate, TodoUpdate, TodoResponse, SuccessResponse
    
    # async def create_todo(todo_data: TodoCreate) -> SuccessResponse:
    #     # Your business logic here
    #     return SuccessResponse(
    #         message="Todo created successfully",
    #         data={"id": "new_todo_id", "text": todo_data.text}
    #     )
    
    pass

# =============================================================================
# USAGE IN API ROUTES  
# =============================================================================

def example_api_usage():
    """
    Example of how to use these models in FastAPI routes
    """
    
    # In your API routes, you can now import and use:
    # from models import TodoCreate, TodoUpdate, TodoResponse, SuccessResponse
    
    # @router.post("/todos/", response_model=SuccessResponse)
    # async def create_todo(todo: TodoCreate):
    #     result = await TodoService.create_todo(todo)
    #     return SuccessResponse(
    #         message="Todo created successfully",
    #         data=result
    #     )
    
    pass

if __name__ == "__main__":
    print("🎯 Todo Models Examples")
    print("=" * 50)
    
    # Run examples
    todo_examples = example_todo_creation()
    response_examples = example_api_responses()
    filter_examples = example_filtering_and_pagination()
    bulk_examples = example_bulk_operations()
    future_examples = example_future_models()
    
    print("✅ All model examples created successfully!")
    print("\n📚 Available models:")
    print("- TodoCreate, TodoUpdate, TodoResponse")
    print("- APIResponse, SuccessResponse, ErrorResponse")
    print("- UserCreate, UserResponse (for future use)")
    print("- HabitCreate, HabitResponse (for future use)")
    print("- PaginatedResponse, TodoFilter, BulkTodoUpdate")
    print("\n🚀 Import these models using: from models import ModelName")
