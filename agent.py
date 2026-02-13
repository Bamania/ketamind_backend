"""
HabitElevate AI Agent Configuration - Updated for Agno v2
"""
from agno.db.postgres import PostgresDb  # Changed from agno.storage.postgres
import os
from agno.os import AgentOS  # Changed from AGUIApp
from agno.os.interfaces.agui import AGUI
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

# Import tools
from tools.calling_tool import CallingTool
from tools.crudTodos_tool import crud_todos_tool
from tools.getcalltranscript_tool import GetCallTranscriptTool

load_dotenv()
logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
POSTGRES_DB_URL = os.getenv("POSTGRES_AGNO_DB_URL")

def load_system_instructions() -> str:
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("system_prompt.txt file not found!")
        return "You are HabitElevate, a helpful AI agent specialized in habit tracking and todo management."
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        return "You are HabitElevate, a helpful AI agent specialized in habit tracking and todo management."

SYSTEM_INSTRUCTIONS = load_system_instructions()

def get_db():
    """Initialize database instance"""
    try:
        db = PostgresDb(
            db_url=POSTGRES_DB_URL,
            session_table="agent_sessions",  # Renamed from table_name
            memory_table="agno_memories",    # Memory table now part of same db
            db_schema="public",
        )
        return db
    except Exception as e:
        logger.warning(f"Could not connect to database: {e}")
        return None

def get_additional_context(
    user_id: Optional[str] = None,
    user_preferences: Optional[Dict[str, Any]] = None,
    session_context: Optional[str] = None,
    habit_focus: Optional[str] = None
) -> str:
    context_parts = []
    if user_id:
        context_parts.append(f" CURRENT USER: {user_id}")
        context_parts.append(f" IMPORTANT: When using CRUD todo tools, ALWAYS pass user_id='{user_id}'")
    if user_preferences:
        context_parts.append(f" USER PREFERENCES: {user_preferences}")
    if session_context:
        context_parts.append(f" SESSION CONTEXT: {session_context}")
    if habit_focus:
        context_parts.append(f" HABIT FOCUS: {habit_focus}")
    return "".join(context_parts)

def get_agent(
    model_name: Optional[str] = None,
    user_id: Optional[str] = None,
    user_preferences: Optional[Dict[str, Any]] = None,
    session_context: Optional[str] = None,
    habit_focus: Optional[str] = None,
    tool_choice: Optional[str] = None,
    enable_storage: bool = True,
    debug_mode: bool = False,
    show_tool_calls: bool = True
) -> Agent:
    model_id = model_name.split("/")[-1] if model_name and "/" in model_name else (model_name or DEFAULT_MODEL)
    model = Gemini(id=model_id)
    
    db = get_db() if enable_storage else None
    
    additional_context = get_additional_context(
        user_id=user_id,
        user_preferences=user_preferences,
        session_context=session_context,
        habit_focus=habit_focus
    )
    full_instructions = SYSTEM_INSTRUCTIONS + additional_context
    
    tools = [CallingTool(), crud_todos_tool(), GetCallTranscriptTool()]
    
    agent = Agent(
        model=model,
        id="habit-elevate-agent",
        name="HabitElevate AI Assistant",
        user_id=user_id,
        db=db,  # Changed from storage=storage
        enable_user_memories=True,  # Replaces memory=memory
        # enable_agentic_memory=True,
        instructions=full_instructions,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": tool_choice}} if tool_choice else None,
        markdown=True,
        # show_tool_calls=show_tool_calls,
        debug_mode=debug_mode,
        # monitoring=True,
        add_history_to_context=True,  # Renamed from add_history_to_messages
        num_history_runs=10,
        # add_datetime_to_instructions=True,
    )
    
    logger.info("Agent initialized successfully")
    return agent

def get_default_agent() -> Agent:
    return get_agent()

def get_user_agent(user_id: str, preferences: Optional[Dict[str, Any]] = None) -> Agent:
    return get_agent(user_id=user_id, user_preferences=preferences, enable_storage=True)

# Updated to use AgentOS instead of AGUIApp
agent_os = AgentOS(
    agents=[get_default_agent()],
    interfaces=[AGUI(agent=get_default_agent())],
)
app = agent_os.get_app()

default_agent = get_default_agent()