# Central Models Directory

This directory contains all the Pydantic models used throughout the HabitElevate application. By centralizing all models in one location, we ensure consistency, reusability, and easier maintenance.

## 📁 Directory Structure

```
models/
├── __init__.py          # Package initialization and exports
├── base_models.py       # All Pydantic model definitions
├── examples.py          # Usage examples and patterns
└── README.md           # This documentation file
```

## 🎯 Available Models

### Todo Models
- `TodoBase` - Base todo model with common fields
- `TodoCreate` - Model for creating new todos
- `TodoUpdate` - Model for updating existing todos  
- `TodoResponse` - Model for todo API responses

### Common Response Models
- `APIResponse[T]` - Generic API response wrapper
- `SuccessResponse` - Standardized success response
- `ErrorResponse` - Standardized error response

### User Models (Future Expansion)
- `UserBase` - Base user model
- `UserCreate` - Model for user registration
- `UserResponse` - Model for user API responses

### Habit Models (Future Expansion)
- `HabitBase` - Base habit model
- `HabitCreate` - Model for creating habits
- `HabitResponse` - Model for habit API responses
- `HabitFrequency` - Enum for habit frequency options

### Utility Models
- `PaginationParams` - Parameters for pagination
- `PaginatedResponse[T]` - Generic paginated response
- `TodoFilter` - Filtering options for todos
- `BulkTodoUpdate` - Model for bulk todo operations
- `BulkOperationResponse` - Response for bulk operations

## 🚀 Usage

### Basic Import
```python
from models import TodoCreate, TodoUpdate, TodoResponse
```

### Service Layer Usage
```python
from models import TodoCreate, SuccessResponse

class TodoService:
    async def create_todo(self, todo_data: TodoCreate) -> SuccessResponse:
        # Your business logic here
        return SuccessResponse(
            message="Todo created successfully",
            data={"id": "new_id", "text": todo_data.text}
        )
```

### API Route Usage
```python
from models import TodoCreate, TodoResponse, SuccessResponse
from fastapi import APIRouter

router = APIRouter()

@router.post("/todos/", response_model=SuccessResponse)
async def create_todo(todo: TodoCreate):
    result = await TodoService.create_todo(todo)
    return SuccessResponse(
        message="Todo created successfully", 
        data=result
    )
```

## ✨ Benefits

1. **Centralized Management** - All models in one location
2. **Consistency** - Standardized field names and types
3. **Reusability** - Models can be imported anywhere in the project
4. **Type Safety** - Full Pydantic validation and type checking
5. **Documentation** - Built-in schema generation for API docs
6. **Future-Proof** - Ready for expansion with user and habit models

## 🔧 Adding New Models

When adding new models:

1. Add the model class to `base_models.py`
2. Export it in `__init__.py` 
3. Add usage examples to `examples.py`
4. Update this README with the new model info

## 📖 Examples

See `examples.py` for comprehensive usage examples including:
- Model creation and validation
- API response patterns
- Filtering and pagination
- Bulk operations
- Service and API integration patterns

## 🔍 Model Features

All models include:
- **Validation** - Automatic data validation with Pydantic
- **Documentation** - Built-in field descriptions
- **Examples** - JSON schema examples for API documentation
- **Type Hints** - Full type safety with Python type hints
- **Serialization** - Automatic JSON serialization/deserialization

## 🎨 Best Practices

1. **Import from models package**: `from models import ModelName`
2. **Use type hints**: Always specify model types in function signatures
3. **Leverage validation**: Let Pydantic handle data validation
4. **Use response models**: Standardize API responses with response models
5. **Keep models focused**: Each model should have a single responsibility

---

**Note**: This centralized model system replaces the previous approach of defining models directly in service files. All existing imports have been updated to use this centralized location.
