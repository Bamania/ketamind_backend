from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
import logging
from fastapi.responses import StreamingResponse
from service.chat_service import generate_agui_streaming_response
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None





@router.post("/")
async def chat_endpoint(chat_message: ChatMessage):
    """Chat endpoint using AGUI agent with streaming response"""
    try:
        logger.info(f"Chat endpoint called with message: {chat_message.message} and user_id: {chat_message.user_id}")
        
        return StreamingResponse(
            generate_agui_streaming_response(chat_message.message, chat_message.user_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {"error": str(e)}

