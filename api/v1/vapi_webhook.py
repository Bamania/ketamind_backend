"""
VAPI Webhook Handler for Add_todo Tool

Handles incoming webhook requests from VAPI when the Add_todo tool is called.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uuid
import hashlib
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
        call_info = payload.get("call", {})
        
        
        customer = call_info.get("customer", {})
        phone_number = customer.get("number") or call_info.get("id", "unknown_user")
        
        # Convert phone number to UUID for database compatibility
        user_id = phone_to_uuid(phone_number) if phone_number != "unknown_user" else str(uuid.uuid4())
        print(f"Phone: {phone_number} -> UUID: {user_id}")
        
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
                elif function_name== "Delete_todo":
                    
                    arguments_raw = function_info.get("arguments", "{}")
                    print("args vapi sent",arguments_raw)
                    print("type of args vapi sent",type(arguments_raw))
                    arguments = arguments_raw
                    todo_text = arguments.get("todo")
                    # check if the todo is in the argument
                    if not todo_text:
                        results.append({
                            "error": "Missing 'todo' parameter"
                        })
                        continue
                    todo_data = TodoCreate(   #using the same modal as create to delete the todo !
                        text=todo_text,
                        user_id=str(user_id)
                    )        
                    result = await TodoService.get_todos(user_id)
                    todo_tobeDeleted = todo_text in result
                    
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
