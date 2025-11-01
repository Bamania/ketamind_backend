#here we will list down the basic chat handle using AGUI agent!
from typing import Optional, AsyncGenerator
from agent import get_user_agent
import logging
import json
import asyncio

logger = logging.getLogger(__name__)


async def generate_agui_streaming_response(message: str, user_id: Optional[str] = None) -> AsyncGenerator[str, None]:
    """Generate streaming response using AGUI agent with inline UI components"""
    try:
        logger.info(f"Generating AGUI streaming response for message: {message} and user_id: {user_id}")
        
        # Use the agent directly to generate response
        if user_id:
            agent = get_user_agent(user_id)
        # else:
        #     agent = get_default_agent()
        
        response = await agent.arun(message)
        
        # Stream the response content
        if hasattr(response, 'content'):
            content = response.content
        else:
            content = str(response)
        
        # Send the full response as a single chunk to preserve UI components
        data = {
            "content": content,
            "type": "agui_content"
        }
        yield f"data: {json.dumps(data)}\n\n"
        
        # Send completion signal
        completion_data = {
            "type": "done",
            "message": "AGUI stream completed"
        }
        yield f"data: {json.dumps(completion_data)}\n\n"
        
    except Exception as e:
        logger.error(f"Error in AGUI streaming response: {str(e)}")
        error_data = {
            "type": "error",
            "error": str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"
