# HabitElevate Server Setup Guide

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Navigate to server directory
cd server

# Install Python dependencies
pip install -e .

# Or install specific packages
pip install sqlalchemy psycopg2-binary agno fastapi google-genai supabase python-dotenv
```

### 2. Environment Variables

Create a `.env` file in the server directory:

```bash
# Required - Gemini Model
DEFAULT_MODEL=gemini-1.5-flash

# Optional - Database Storage (for conversation persistence)
POSTGRES_DB_URL=postgresql://user:pass@host:port/db

# Optional - Voice Integration
VAPI_API_KEY=your-vapi-key
VAPI_PHONE_NUMBER_ID=your-phone-id
VAPI_ASSISTANT_ID=your-assistant-id

# Optional - Supabase (for todo storage)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### 3. Run the Server

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Configuration Details

### Simple Gemini Setup

The agent now uses a simple Gemini model configuration without Vertex AI:

```python
# In agent.py
model = Gemini(id="gemini-1.5-flash")
```

**No Google Cloud Project setup required!** Just ensure you have:
- Google AI Studio API key (if using API key authentication)
- Or proper authentication through Google Cloud SDK

### Available Models

- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable for complex tasks
- `gemini-2.0-flash` - Latest with improved capabilities

### Database Options

1. **No Database** - Agent works without any database
2. **PostgreSQL** - For conversation persistence (optional)
3. **Supabase** - For todo storage (optional)

## 🧪 Testing

### Test Basic Functionality

```bash
# Run the test script
python test_agent.py
```

### Test API Endpoints

```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a todo for user123 with text \"Test todo\"", "user_id": "user123"}'

# Test habit coaching
curl -X POST "http://localhost:8000/chat/habit-coaching" \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me build a morning routine", "habit_focus": "fitness", "user_id": "user123"}'
```

## 📡 API Endpoints

### Chat Endpoints

- `POST /chat` - Basic chat with optional user context
- `POST /chat/habit-coaching` - Habit-focused coaching
- `POST /api/v1/chat/chat` - Alternative chat endpoint

### Todo Endpoints

- `POST /api/v1/todos/` - Create todo
- `GET /api/v1/todos/` - Get todos
- `GET /api/v1/todos/{todo_id}` - Get specific todo
- `PUT /api/v1/todos/{todo_id}` - Update todo
- `DELETE /api/v1/todos/{todo_id}` - Delete todo

### Test Endpoints

- `GET /create_todo` - Test todo creation
- `GET /test-call` - Test phone call
- `GET /delete_todo` - Test todo deletion

## 🔍 Troubleshooting

### Common Issues

1. **SQLAlchemy Error**
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```

2. **Gemini API Error**
   - Check your Google AI Studio API key
   - Ensure you have proper authentication

3. **Import Errors**
   - Make sure you're in the server directory
   - Check that all dependencies are installed

4. **Database Connection Issues**
   - Check POSTGRES_DB_URL format
   - Ensure database is running and accessible

### Debug Mode

Enable debug mode for detailed logging:

```python
from agent import get_debug_agent

agent = get_debug_agent()
response = await agent.arun("Test message")
```

## 🎯 Usage Examples

### Basic Agent Usage

```python
from agent import get_default_agent

agent = get_default_agent()
response = await agent.arun("Create a todo for user123")
print(response.content)
```

### User-Specific Agent

```python
from agent import get_user_agent

agent = get_user_agent("user123", {"habit_focus": "fitness"})
response = await agent.arun("Help me with morning exercise")
print(response.content)
```

### Habit Coaching Agent

```python
from agent import get_habit_coaching_agent

agent = get_habit_coaching_agent("nutrition", "user456")
response = await agent.arun("I want to eat healthier")
print(response.content)
```

## 📚 Next Steps

1. **Set up environment variables** in `.env` file
2. **Install dependencies** using pip
3. **Test the agent** with the test script
4. **Start the server** and test API endpoints
5. **Integrate with frontend** using the API endpoints

---

The server is now configured to use simple Gemini models without the complexity of Vertex AI setup!
