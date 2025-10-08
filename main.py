from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.todo_register import router as todo_router
from api.v1.chat_interaction import router as chat_router
from agent import  get_user_agent, get_habit_coaching_agent

load_dotenv()
app = FastAPI(
    title="HabitElevate AI Agent Server",
    description="AI-powered habit tracking with voice integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the default agent


# Include routers
app.include_router(todo_router)
app.include_router(chat_router)



@app.post("/testChat")
async def chat_endpoint(message: str, user_id: str = None):
    """Chat endpoint for interacting with the AI agent"""
    try:
        # Use user-specific agent if user_id provided
        if user_id:
            agent = get_user_agent(user_id)
  
            
        response = await agent.arun(message)
        return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}


@app.post("/chat/habit-coaching")
async def habit_coaching_endpoint(message: str, habit_focus: str, user_id: str = None):
    """Habit coaching endpoint with specific habit focus"""
    try:
        agent = get_habit_coaching_agent(habit_focus, user_id)
        response = await agent.arun(message)
        return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-call")
async def test_call():
    """Test endpoint for making a call"""
    response = await get_user_agent.arun("can you call +91 8957517207")
    print(response.content)
    return response.content

@app.get("/create_todo")
async def create_todo():
    """
    Test endpoint to trigger the AI agent to create a todo item for a specific user.

    This endpoint sends a prompt to the reasoning agent to create a todo for user 123
    with the text 'Complete the project documentation'. The response from the agent
    is printed to the console and returned as the API response.

    Returns:
        str: The content returned by the reasoning agent after processing the request.
    """
    response = await get_user_agent.arun("create a todo for user 786 ,with the text 'Ansh ko chod diya jaye bhuut jor se'")
    print(response.content)
    return response.content



@app.get("/delete_todo")
async def delete_todo():
    
    """
    Test endpoint to trigger the AI agent to delete a todo item for a specific user.

    This endpoint sends a prompt to the reasoning agent to delete a todo for the given user_id and todo_id.
    The response from the agent is printed to the console and returned as the API response.

    Args:
        todo_id (str): The ID of the todo to delete.
        user_id (str): The ID of the user who owns the todo.

    Returns:
        str: The content returned by the reasoning agent after processing the request.
    """
    prompt = "Delete the todo with id '6 ' for user 786."
    response = await get_user_agent.arun(prompt)
    print(response.content)
    return response.content


if __name__ == "__main__":
    import uvicorn
    
    print("🎯 HabitElevate - AI Agent Server with Twilio Voice Integration")
    print("=" * 60)
    print("🌐 Starting FastAPI server...")
    print("📍 Server will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Chat: POST http://localhost:8000/chat")
    print("   - Twilio Voice: POST http://localhost:8000/api/v1/twilio/voice")
    print("   - Twilio Status: GET http://localhost:8000/api/v1/twilio/status")
    print("   - Make Call: POST http://localhost:8000/api/v1/twilio/call")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
