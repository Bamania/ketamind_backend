"""
VAPI Webhook Handler for Add_todo Tool

Handles incoming webhook requests from VAPI when the Add_todo tool is called.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uuid
from service.todo_crud import TodoService
from models import TodoCreate

router = APIRouter(prefix="/api/v1/vapi", tags=["vapi"])
logger = logging.getLogger(__name__)


def phone_to_uuid(phone_number: str) -> str:
    """
    Convert a phone number to a deterministic UUID.
    Same phone number will always generate the same UUID.
    """
    # Create a namespace UUID for phone numbers
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # DNS namespace
    # Generate UUID v5 from phone number
    return str(uuid.uuid5(namespace, phone_number))


class VapiToolRequest(BaseModel):
    """Model for VAPI tool call request"""
    message: Optional[Dict[str, Any]] = None
    call: Optional[Dict[str, Any]] = None


@router.post("/webhook")
async def vapi_add_todo_webhook(request: Request):
    """
    Webhook endpoint to handle VAPI Add_todo tool calls.
    
    When a user says something like "add a todo to buy milk" during a VAPI call,
    this endpoint receives the request and saves the todo to the database.
    
    Expected payload from VAPI:
    {
        "message": {
            "type": "tool-calls",
            "toolCalls": [{
                "function": {
                    "name": "Add_todo",
                    "arguments": "{\"todo\": \"buy milk\"}"
                }
            }]
        },
        "call": {
            "id": "call_123",
            "customer": {
                "number": "+1234567890"
            }
        }
    }
    """
    try:
    
        payload = await request.json()
        print(f"Received VAPI webhook request: {payload}")
        
        
        # Extract the message and call information
        message = payload.get("message", {})
        
        # phone_number = (
        #     payload.get("call", {})
        #         .get("customer", {})
        #         .get("number")
        # ) or (
        #     payload.get("customer", {})
        #         .get("number")
        # ) or call_info.get("id", "unknown_user")

        # print("PHONE NUMBER ---->>>>",phone_number)
        phone_number = (
            payload.get("message", {})
                .get("call", {})
                .get("customer", {})
                .get("number")
        ) or (
            payload.get("call", {})
                .get("customer", {})
                .get("number")
        ) or "unknown_user"
        
        print("PHONE NUMBER ---->>>>", phone_number)
        
        # Query users_profile table to get the actual user_id using phone number
        if phone_number and phone_number != "unknown_user":
            from database.supabaseClient import supabase
            
            try:
                # Query users_profile table for user with matching phone number
                result = supabase.table("users_profile").select("id").eq("phone", phone_number).execute()
                
                if result.data and len(result.data) > 0:
                    user_id = result.data[0]["id"]
                    print(f"Found user in database - Phone: {phone_number} -> User ID: {user_id}")
                else:
                    logger.warning(f"No user found with phone number: {phone_number}")
                    return {
                        "results": [{
                            "error": f"No user account found for phone number {phone_number}. Please sign up first."
                        }]
                    }
            except Exception as db_error:
                logger.error(f"Database error while fetching user: {str(db_error)}")
                return {
                    "results": [{
                        "error": "Failed to authenticate user. Please try again."
                    }]
                }
        else:
            logger.error("No phone number found in webhook payload")
            return {
                "results": [{
                    "error": "Could not identify caller. Please try again."
                }]
            }
        
        # Check if this is a tool call
        message_type = message.get("type")
        
        if message_type == "tool-calls":
            # Extract tool calls
            tool_calls = message.get("toolCalls", [])
            
            if not tool_calls:
                return {
                    "results": [{
                        "error": "No tool calls found in request"
                    }]
                }
            
            # Process each tool call
            results = []
            print("all the tools calls vapi did",tool_calls)
            for tool_call in tool_calls:
                function_info = tool_call.get("function", {})
                function_name = function_info.get("name")
                
                # Handle Add_todo function
                if function_name == "Add_todo":
                    # Parse arguments (VAPI can send as JSON string or dict)
                    import json
                    arguments_raw = function_info.get("arguments", "{}")
                    print("args vapi sent",arguments_raw)
                    print("type of args vapi sent",type(arguments_raw))
                    
                    # Check if arguments is already a dict or needs parsing
                    if isinstance(arguments_raw, str):
                        arguments = json.loads(arguments_raw)
                    else:
                        arguments = arguments_raw
                    
                    todo_text = arguments.get("todo")
                    
                    if not todo_text:
                        results.append({
                            "error": "Missing 'todo' parameter"
                        })
                        continue
                    
                    # Create the todo in database
                    
                    todo_data = TodoCreate(
                        text=todo_text,
                        user_id=str(user_id)
                    )
                    # need to add userId somehow in the todo_data !
                    result = await TodoService.create_todo(todo_data)
                    
                    if result["success"]:
                        print(f"Successfully created todo: {todo_text} for user: {user_id}")
                        results.append({
                            "result": f"Successfully added todo: '{todo_text}' to your list!"
                        })
                    else:
                        logger.error(f"Failed to create todo: {result['message']}")
                        results.append({
                            "error": f"Failed to add todo: {result['message']}"
                        })
                elif function_name == "Delete_todo":
                    # Parse arguments
                    import json
                    arguments_raw = function_info.get("arguments", "{}")
                    print("Delete_todo args:", arguments_raw)
                    print("Type of args:", type(arguments_raw))
                    
                    # Check if arguments is already a dict or needs parsing
                    if isinstance(arguments_raw, str):
                        arguments = json.loads(arguments_raw)
                    else:
                        arguments = arguments_raw
                    
                    todo_text = arguments.get("todo")
                    
                    if not todo_text:
                        results.append({
                            "error": "Missing 'todo' parameter"
                        })
                        continue
                    
                    # Get all user's todos to find the matching one
                    todos_result = await TodoService.get_todos(user_id)
                    
                    if not todos_result["success"]:
                        results.append({
                            "error": f"Failed to retrieve todos: {todos_result['message']}"
                        })
                        continue
                    
                    # Find the todo that matches the text (case-insensitive partial match)
                    matching_todo = None
                    todo_text_lower = todo_text.lower()
                    
                    for todo in todos_result["data"]:
                        if todo_text_lower in todo["text"].lower():
                            matching_todo = todo
                            break
                    
                    if not matching_todo:
                        results.append({
                            "error": f"Could not find a todo matching '{todo_text}'"
                        })
                        continue
                    
                    # Delete the todo using the ID
                    delete_result = await TodoService.delete_todo(matching_todo["id"])
                    
                    if delete_result["success"]:
                        print(f"Successfully deleted todo: {matching_todo['text']} for user: {user_id}")
                        results.append({
                            "result": f"Successfully deleted todo: '{matching_todo['text']}'"
                        })
                    else:
                        logger.error(f"Failed to delete todo: {delete_result['message']}")
                        results.append({
                            "error": f"Failed to delete todo: {delete_result['message']}"
                        })
                
                elif function_name == "Read_todo":
                    # Get all todos for the user
                    todos_result = await TodoService.get_todos(user_id)
                    
                    if not todos_result["success"]:
                        results.append({
                            "error": f"Failed to retrieve todos: {todos_result['message']}"
                        })
                        continue
                    
                    todos = todos_result["data"]
                    
                    if not todos or len(todos) == 0:
                        results.append({
                            "result": "You don't have any todos yet. Your list is empty!"
                        })
                        continue
                    
                    # Format todos into a readable string
                    # Separate completed and pending todos
                    pending_todos = [t for t in todos if not t.get("completed", False)]
                    completed_todos = [t for t in todos if t.get("completed", False)]
                    
                    response_parts = []
                    
                    if pending_todos:
                        response_parts.append(f"You have {len(pending_todos)} pending todo{'s' if len(pending_todos) != 1 else ''}:")
                        for idx, todo in enumerate(pending_todos, 1):
                            response_parts.append(f"{idx}. {todo['text']}")
                    
                    if completed_todos:
                        if pending_todos:
                            response_parts.append("")  # Add spacing
                        response_parts.append(f"You have {len(completed_todos)} completed todo{'s' if len(completed_todos) != 1 else ''}:")
                        for idx, todo in enumerate(completed_todos, 1):
                            response_parts.append(f"{idx}. {todo['text']} ✓")
                    
                    result_text = "\n".join(response_parts)
                    print(f"Successfully retrieved {len(todos)} todos for user: {user_id}")
                    results.append({
                        "result": result_text
                    })
                
                else:
                    results.append({
                        "error": f"Unknown function: {function_name}"
                    })
            
            return {"results": results}
        
        else:
            # Handle other message types if needed
            print(f"Received non-tool-call message type: {message_type}")
            return {
                "status": "received",
                "message": f"Received message type: {message_type}"
            }
            
    except Exception as e:
        logger.error(f"Error processing VAPI webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/webhook/test")
# async def test_webhook():
#     """Test endpoint to verify webhook is accessible"""
#     return {
#         "status": "ok",
#         "message": "VAPI webhook endpoint is working!",
#         "endpoint": "/api/v1/vapi/webhook"
#     }


# @router.post("/webhook/test-add-todo")
# async def test_add_todo(todo_text: str, user_id: str = "1234"):
#     """
#     Test endpoint to simulate VAPI calling the Add_todo tool.
    
#     Example usage:
#     POST /api/v1/vapi/webhook/test-add-todo?todo_text=buy%20milk&user_id=123
#     """
#     try:
#         todo_data = TodoCreate(
#             text=todo_text,
#             user_id=user_id
#         )
        
#         result = await TodoService.create_todo(todo_data)
#         return result
        
#     except Exception as e:
#         logger.error(f"Error in test endpoint: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e)
#         }
