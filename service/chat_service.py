#here we will list down the basic chat handle using AGUI agent!
from typing import Optional, AsyncGenerator
from agent import get_user_agent
import logging
import json
import asyncio
import time

logger = logging.getLogger(__name__)


async def generate_agui_streaming_response(message: str, user_id: str) -> AsyncGenerator[str, None]:
    """Generate streaming response using AGUI agent with inline UI components"""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"Generating AGUI streaming response for message: {message} and user_id: {user_id} (attempt {attempt + 1})")
            
            # Use the agent directly to generate response
            agent=get_user_agent(user_id)
            
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
            return  # Success, exit the retry loop
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"Error in AGUI streaming response (attempt {attempt + 1}): {error_str}")
            
            # Check if it's a rate limit error
            if "429" in error_str or "Too Many Requests" in error_str or "quota" in error_str.lower():
                if attempt < max_retries - 1:
                    # Wait before retrying
                    logger.info(f"Rate limit hit, waiting {retry_delay} seconds before retry...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Max retries reached
                    error_data = {
                        "type": "error",
                        "error": "The AI service is currently experiencing high traffic. Please try again in a moment."
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                    return
            else:
                # Other error, don't retry
                error_data = {
                    "type": "error",
                    "error": f"An error occurred: {error_str}"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                return
