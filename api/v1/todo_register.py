from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from service.todo_crud import TodoService
from models import TodoCreate, TodoUpdate

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])

@router.post("/")
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    # Validate that user_id is provided
    if not todo.user_id:
        raise HTTPException(status_code=400, detail="user_id is required to create a todo")
    
    result = await TodoService.create_todo(todo)
    
    if result["success"]:
        return {
            "status": "success",
            "data": result["data"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.get("/")
async def get_todos(user_id: Optional[str] = Query(None, description="Filter todos by user ID")):
    """Get all todos, optionally filtered by user_id"""
    # Make user_id required
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required to fetch todos")
    
    result = await TodoService.get_todos(user_id)
    
    if result["success"]:
        return {
            "status": "success",
            "data": result["data"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@router.get("/{todo_id}")
async def get_todo(todo_id: str):
    """Get a specific todo by ID"""
    result = await TodoService.get_todo_by_id(todo_id)
    
    if result["success"]:
        return {
            "status": "success",
            "data": result["data"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=404, detail=result["message"])

@router.put("/{todo_id}")
async def update_todo(todo_id: str, todo: TodoUpdate):
    """Update a todo"""
    result = await TodoService.update_todo(todo_id, todo)
    
    if result["success"]:
        return {
            "status": "success",
            "data": result["data"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.patch("/{todo_id}/toggle")
async def toggle_todo(todo_id: str):
    """Toggle todo completion status"""
    result = await TodoService.toggle_todo(todo_id)
    
    if result["success"]:
        return {
            "status": "success",
            "data": result["data"],
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    result = await TodoService.delete_todo(todo_id)
    
    if result["success"]:
        return {
            "status": "success",
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@router.delete("/completed/clear")
async def clear_completed_todos(user_id: Optional[str] = Query(None, description="Clear completed todos for specific user")):
    """Delete all completed todos"""
    # Make user_id required
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required to clear completed todos")
    
    result = await TodoService.clear_completed_todos(user_id)
    
    if result["success"]:
        return {
            "status": "success",
            "message": result["message"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["message"])
