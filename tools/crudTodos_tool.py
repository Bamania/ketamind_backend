"""
CRUD Operations Tool for Todo Management

This module provides a toolkit for performing CRUD (Create, Read, Update, Delete) 
operations on todo items using the centralized models and TodoService.
"""

from typing import List

from agno.agent import Agent
from agno.tools import Toolkit
from agno.utils.log import logger
from models import TodoCreate, TodoUpdate
from service.todo_crud import TodoService

class crud_todos_tool(Toolkit):
    """
    A toolkit that provides CRUD operations for todo management.
    
    This class wraps the TodoService methods to provide a tool interface
    for AI agents to interact with todo data.
    
    Available Operations:
    - create_todo: Create a new todo item
    - delete_todo: Delete an existing todo by ID
    - update_todo: Update an existing todo's information
    - get_todos: Retrieve all todos for a user
    """
    def __init__(self, **kwargs):
        """
        Initialize the CRUD todos toolkit.
        
        Args:
            **kwargs: Additional keyword arguments passed to the parent Toolkit class.
        """
        super().__init__(
            name="crud_todos_tool", 
            tools=[
                self.create_todo, 
                self.delete_todo, 
                self.update_todo, 
                self.get_todos,
                self.toggle_todo,
                self.clear_completed_todos
            ], 
            **kwargs
        )

    async def create_todo(self, text: str, user_id: str) -> str:
        """
        Create a new todo item for a user.

        Args:
            text (str): The text content of the todo item.
            user_id (str): The ID of the user who owns this todo.
        
        Returns:
            str: JSON string containing the result with success status, data, and message.
            
        Example:
            result = await create_todo("Complete project documentation", "user123")
        """
        try:
            # Create TodoCreate model from simple parameters
            todo_data = TodoCreate(text=text, user_id=user_id)
            result = await TodoService.create_todo(todo_data)
            return str(result)
        except Exception as e:
            logger.error(f"Error in create_todo tool: {str(e)}")
            return str({
                "success": False,
                "data": None,
                "message": f"Error creating todo: {str(e)}"
            })

    async def delete_todo(self, todo_id: str) -> str:
        """
        Delete a specific todo by its ID.

        Args:
            todo_id (str): The unique identifier of the todo to delete.
        
        Returns:
            str: JSON string containing the result with success status and message.
            
        Example:
            result = await delete_todo("todo123")
        """
        try:
            result = await TodoService.delete_todo(todo_id)
            return str(result)
        except Exception as e:
            logger.error(f"Error in delete_todo tool: {str(e)}")
            return str({
                "success": False,
                "data": None,
                "message": f"Error deleting todo: {str(e)}"
            })

    async def update_todo(self, todo_id: str, text: str , completed: bool ) -> str:
        """
        Update an existing todo with new information.

        Args:
            todo_id (str): The unique identifier of the todo to update.
            text (str, optional): The updated text content of the todo.
            completed (bool, optional): The updated completion status of the todo.
        
        Returns:
            str: JSON string containing the result with success status, updated data, and message.
            
        Example:
            result = await update_todo("todo123", text="Updated task description", completed=True)
        """
        try:
            # Create TodoUpdate model from simple parameters
            update_data = {}
            if text is not None:
                update_data["text"] = text
            if completed is not None:
                update_data["completed"] = completed
                
            if not update_data:
                return str({
                    "success": False,
                    "data": None,
                    "message": "No fields provided for update"
                })
                
            todo_update = TodoUpdate(**update_data)
            result = await TodoService.update_todo(todo_id, todo_update)
            return str(result)
        except Exception as e:
            logger.error(f"Error in update_todo tool: {str(e)}")
            return str({
                "success": False,
                "data": None,
                "message": f"Error updating todo: {str(e)}"
            })

    async def get_todos(self, user_id: str) -> str:
        """
        Retrieve all todos for a specific user.

        Args:
            user_id (str): The ID of the user whose todos to retrieve.
        
        Returns:
            str: JSON string containing the result with success status, list of todos, and message.
            
        Example:
            result = await get_todos("user123")
        """
        try:
            result = await TodoService.get_todos(user_id)
            return str(result)
        except Exception as e:
            logger.error(f"Error in get_todos tool: {str(e)}")
            return str({
                "success": False,
                "data": [],
                "message": f"Error retrieving todos: {str(e)}"
            })

    async def toggle_todo(self, todo_id: str) -> str:
        """
        Toggle the completion status of a todo (completed <-> not completed).

        Args:
            todo_id (str): The unique identifier of the todo to toggle.
        
        Returns:
            str: JSON string containing the result with success status, updated data, and message.
            
        Example:
            result = await toggle_todo("todo123")
        """
        try:
            result = await TodoService.toggle_todo(todo_id)
            return str(result)
        except Exception as e:
            logger.error(f"Error in toggle_todo tool: {str(e)}")
            return str({
                "success": False,
                "data": None,
                "message": f"Error toggling todo: {str(e)}"
            })

    async def clear_completed_todos(self, user_id: str) -> str:
        """
        Delete all completed todos for a specific user.

        Args:
            user_id (str): The ID of the user whose completed todos should be cleared.
        
        Returns:
            str: JSON string containing the result with success status and message.
            
        Example:
            result = await clear_completed_todos("user123")
        """
        try:
            result = await TodoService.clear_completed_todos(user_id)
            return str(result)
        except Exception as e:
            logger.error(f"Error in clear_completed_todos tool: {str(e)}")
            return str({
                "success": False,
                "data": None,
                "message": f"Error clearing completed todos: {str(e)}"
            })

