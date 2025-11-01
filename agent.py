"""
HabitElevate AI Agent Configuration

This module provides a centralized agent configuration for the HabitElevate application.
It exports a configurable agent instance that can be used throughout the application.
"""
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.storage.postgres import PostgresStorage
from agno.memory.v2.memory import Memory
# from agno.memory.v2.memory import UserMemory
import os
from agno.app.agui.app import AGUIApp
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
# from agno.storage.postgres import PostgresStorage
# from agno.storage.postgres import PostgresMemoryDb
# from agno.memory.memory import Memory
# Import tools
from tools.calling_tool import CallingTool
from tools.crudTodos_tool import crud_todos_tool
from tools.getcalltranscript_tool import GetCallTranscriptTool

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
POSTGRES_DB_URL = os.getenv("POSTGRES_AGNO_DB_URL")

def load_system_instructions() -> str:
    """
    Load system instructions from the system_prompt.txt file.
    
    Returns:
        System instructions string
    """
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("system_prompt.txt file not found!")
        return "You are HabitElevate, a helpful AI agent specialized in habit tracking and todo management."
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        return "You are HabitElevate, a helpful AI agent specialized in habit tracking and todo management."

# Load system instructions from file
SYSTEM_INSTRUCTIONS = load_system_instructions()



def get_storage():
    """Initialize global storage and memory instances"""
    try:
        storage = PostgresStorage(
            db_url=POSTGRES_DB_URL,
            table_name="agent_sessions",
            schema="public",
        )
        
      
        memory_db = PostgresMemoryDb(
            db_url=POSTGRES_DB_URL,
            table_name="agno_memories",
            schema="public",
        )
        
        '''try:
            memory_db.create()
        except Exception as create_error:
            logger.warning(f"Memory table already exists or creation failed: {create_error}")'''

        memory = Memory(db=memory_db)

        return storage, memory
    except Exception as e:
        logger.warning(f"Could not connect to database: {e}")
        logger.info("Continuing without persistent storage...")
        return None, None

def get_additional_context(
    user_id: Optional[str] = None,
    user_preferences: Optional[Dict[str, Any]] = None,
    session_context: Optional[str] = None,
    habit_focus: Optional[str] = None
) -> str:
    """
    Generate additional context for the agent based on user preferences and session context.
    
    Args:
        user_id: Current user ID
        user_preferences: User-specific preferences and settings
        session_context: Current session context
        habit_focus: Specific habit area to focus on
        
    Returns:
        Additional context string
    """
    context_parts = []
    
    if user_id:
        context_parts.append(f"\n👤 CURRENT USER: {user_id}")
        context_parts.append(f"\n⚠️ IMPORTANT: When using CRUD todo tools (create_todo, get_todos, clear_completed_todos), ALWAYS pass user_id='{user_id}' as a parameter.")
        context_parts.append(f"\n📝 Example: create_todo(text='Complete task', user_id='{user_id}')")
    
    if user_preferences:
        context_parts.append(f"\n⚙️ USER PREFERENCES: {user_preferences}")
    
    
    if session_context:
        context_parts.append(f"\n📋 SESSION CONTEXT: {session_context}")
    
    if habit_focus:
        context_parts.append(f"\n🎯 HABIT FOCUS: {habit_focus}")
        context_parts.append(f"\n💡 COACHING FOCUS: Provide specific guidance for {habit_focus} habits")
    
    return "".join(context_parts)

# this function is about to build the agent instace with your rules and tools
def get_agent(
    model_name: Optional[str] = None,
    user_id: str = None,
    user_preferences: Optional[Dict[str, Any]] = None,
    session_context: Optional[str] = None,
    habit_focus: Optional[str] = None,
    tool_choice: Optional[str] = None,
    enable_storage: bool = True,
    debug_mode: bool = False,
    show_tool_calls: bool = True
) -> Agent:
    """
    Get a configured agent instance with specified parameters.
    
    Args:
        model_name: Name of the model to use (defaults to DEFAULT_MODEL)
        user_id: Current user ID for context
        user_preferences: User-specific preferences
        session_context: Current session context
        habit_focus: Specific habit area to focus on
        tool_choice: Specific tool to force usage of
        enable_storage: Whether to enable conversation persistence
        debug_mode: Whether to enable debug mode
        show_tool_calls: Whether to show tool calls in responses
        
    Returns:
        Configured Agent instance
    """
    # Determine model to use
    if model_name:
        if "/" in model_name:
            # Extract model name from "provider/model" format
            model_id = model_name.split("/")[-1]
        else:
            model_id = model_name
    else:
        model_id = DEFAULT_MODEL
    
    logger.info(f"Using model: {model_id}")
    
    # Initialize model with simple Gemini configuration
    # Use simple Gemini model (no Vertex AI)
    logger.info(f"Using simple Gemini model: {model_id}")
    
    model = Gemini(id=model_id)
    
    # Get storage if enabled
    storage = None
    if enable_storage:
        storage, memory = get_storage()
    
    # Get additional context
    additional_context = get_additional_context(
        user_id=user_id,
        user_preferences=user_preferences,
        session_context=session_context,
        habit_focus=habit_focus
    )
    
    # Combine instructions with additional context
    full_instructions = SYSTEM_INSTRUCTIONS + additional_context
    
    # Initialize tools
    tools = [
        CallingTool(),
        crud_todos_tool(),
        GetCallTranscriptTool(),
    ]
    
    # Create agent
    agent = Agent(
        model=model,
        agent_id="habit-elevate-agent",
        name="HabitElevate AI Assistant",
        session_id=user_id,
        memory=memory,
        instructions=full_instructions,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": tool_choice}} if tool_choice else None,
        markdown=True,
        show_tool_calls=show_tool_calls,
        debug_mode=debug_mode,
        monitoring=True,
        stream_intermediate_steps=False,
        add_history_to_messages=True,
        num_history_runs=10,
        add_datetime_to_instructions=True,
        storage=storage,
    )
    
    logger.info("Agent initialized successfully")
    return agent


def get_default_agent() -> Agent:
    """
    Get a default agent instance with standard configuration.
    
    Returns:
        Default configured Agent instance
    """
    return get_agent()


def get_user_agent(user_id: str, preferences: Optional[Dict[str, Any]] = None) -> Agent:
    """
    Get an agent instance configured for a specific user.
    
    Args:
        user_id: User ID to configure the agent for
        preferences: User-specific preferences
        
    Returns:
        User-configured Agent instance
    """
    return get_agent(
        user_id=user_id,
        user_preferences=preferences,
        enable_storage=True
    )



agui_app = AGUIApp(
    agent=get_default_agent(),
    name="AG-UI Agno Agent",
    app_id="agno_agent",
)
app = agui_app.get_app()

default_agent = get_default_agent()

# Example usage:
# agent = get_agent(user_id="user123", habit_focus="exercise")
# response = await agent.arun("Help me create a morning exercise routine")
