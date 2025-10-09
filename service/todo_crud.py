from typing import List, Optional, Dict, Any
from datetime import datetime
from database.supabaseClient import supabase
from models import TodoCreate, TodoUpdate, TodoResponse

class TodoService:
    @staticmethod
    async def create_todo(todo_data: TodoCreate) -> Dict[str, Any]:
        """Create a new todo"""
        try:
            todo_dict = {
                "text": todo_data.text,
                "completed": False,
                "created_at": datetime.utcnow().isoformat(),
                "user_id": todo_data.user_id
            }
            result = supabase.table("todos").insert(todo_dict).execute()
            
            if result.data:
                return {
                    "success": True,
                    "data": result.data[0],
                    "message": "Todo created successfully"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": "Failed to create todo"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error creating todo: {str(e)}"
            }

    @staticmethod
    async def get_todos(user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get all todos, optionally filtered by user_id"""
        try:
            query = supabase.table("todos").select("*").order("created_at", desc=True)
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.execute()
            
            return {
                "success": True,
                "data": result.data,
                "message": "Todos retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Error retrieving todos: {str(e)}"
            }

    @staticmethod
    async def get_todo_by_id(todo_id: str) -> Dict[str, Any]:
        """Get a specific todo by ID"""
        try:
            result = supabase.table("todos").select("*").eq("id", todo_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "data": result.data[0],
                    "message": "Todo retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": "Todo not found"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error retrieving todo: {str(e)}"
            }

    @staticmethod
    async def update_todo(todo_id: str, todo_data: TodoUpdate) -> Dict[str, Any]:
        """Update a todo"""
        try:
            update_dict = {}
            if todo_data.text is not None:
                update_dict["text"] = todo_data.text
            if todo_data.completed is not None:
                update_dict["completed"] = todo_data.completed
            
            if not update_dict:
                return {
                    "success": False,
                    "data": None,
                    "message": "No fields to update"
                }
            
            result = supabase.table("todos").update(update_dict).eq("id", todo_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "data": result.data[0],
                    "message": "Todo updated successfully"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": "Todo not found or failed to update"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error updating todo: {str(e)}"
            }

    @staticmethod
    async def delete_todo(todo_id: str) -> Dict[str, Any]:
        """Delete a todo"""
        try:
            result = supabase.table("todos").delete().eq("text", todo_id).execute()
            
            return {
                "success": True,
                "data": None,
                "message": "Todo deleted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error deleting todo: {str(e)}"
            }

    @staticmethod
    async def toggle_todo(todo_id: str) -> Dict[str, Any]:
        """Toggle todo completion status"""
        try:
            # First get the current todo
            current_todo = await TodoService.get_todo_by_id(todo_id)
            if not current_todo["success"]:
                return current_todo
            
            # Toggle the completed status
            new_completed = not current_todo["data"]["completed"]
            
            result = supabase.table("todos").update({
                "completed": new_completed
            }).eq("id", todo_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "data": result.data[0],
                    "message": f"Todo {'completed' if new_completed else 'uncompleted'} successfully"
                }
            else:
                return {
                    "success": False,
                    "data": None,
                    "message": "Failed to toggle todo"
                }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error toggling todo: {str(e)}"
            }

    @staticmethod
    async def clear_completed_todos(user_id: Optional[str] = None) -> Dict[str, Any]:
        """Delete all completed todos"""
        try:
            query = supabase.table("todos").delete().eq("completed", True)
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.execute()
            
            return {
                "success": True,
                "data": None,
                "message": "Completed todos cleared successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error clearing completed todos: {str(e)}"
            }
