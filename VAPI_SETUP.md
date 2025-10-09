# 🚀 VAPI Add_todo Integration Setup Guide

## What You Have

You've created a VAPI tool called **"Add_todo"** with one parameter:
- `todo` (string) - The todo text to add

## What We've Built

A webhook endpoint that:
1. Receives requests from VAPI when users say "add a todo"
2. Extracts the todo text from the request
3. Saves it to your Supabase database
4. Returns a confirmation message

## Quick Setup (5 minutes)

### Step 1: Test the Webhook Locally

```bash
# Make sure your server is running
cd server
uvicorn main:app --reload
```

In a new terminal:
```bash
# Run the test script
python test_vapi_webhook.py
```

You should see:
```
✅ Testing webhook health...
✅ Testing simple add todo endpoint...
✅ Testing VAPI webhook with real payload format...
✅ All tests completed!
```

### Step 2: Expose with ngrok

```bash
# In a new terminal
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123-456-789.ngrok-free.app`)

### Step 3: Update VAPI Tool Configuration

In your VAPI dashboard (the screenshot you showed):

1. **Server Settings** section at the bottom
2. Set **Server URL** to: `https://YOUR-NGROK-URL.ngrok-free.app/api/v1/vapi/webhook`
   - Example: `https://fz79a7aa8752.ngrok-free.app/api/v1/vapi/webhook`

3. Click **Save**

### Step 4: Test with a Real Call

1. Call your VAPI phone number
2. Say: **"Add a todo to buy milk"**
3. VAPI should respond: **"Successfully added todo: 'buy milk' to your list!"**

### Step 5: Verify It Worked

Check your Supabase database - you should see the new todo!

## How It Works

```
User says: "Add a todo to buy groceries"
           ↓
VAPI processes speech and extracts: {todo: "buy groceries"}
           ↓
VAPI calls your webhook: POST /api/v1/vapi/webhook
           ↓
Your webhook saves to database
           ↓
Returns: "Successfully added todo: 'buy groceries' to your list!"
           ↓
VAPI speaks this to the user
```

## Testing the Webhook Manually

### Using curl:

```bash
curl -X POST http://localhost:8000/api/v1/vapi/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "tool-calls",
      "toolCalls": [{
        "type": "function",
        "function": {
          "name": "Add_todo",
          "arguments": "{\"todo\": \"Test todo from curl\"}"
        }
      }]
    },
    "call": {
      "id": "test_call",
      "customer": {
        "number": "+1234567890"
      }
    }
  }'
```

Expected response:
```json
{
  "results": [{
    "result": "Successfully added todo: 'Test todo from curl' to your list!"
  }]
}
```

### Using the test endpoint:

```bash
curl -X POST "http://localhost:8000/api/v1/vapi/webhook/test-add-todo?todo_text=Buy%20milk&user_id=test123"
```

## Troubleshooting

### Webhook not receiving requests?
- ✅ Check ngrok is running: `ngrok http 8000`
- ✅ Verify Server URL in VAPI matches ngrok URL
- ✅ Check server logs for incoming requests

### Todos not being saved?
- ✅ Check Supabase connection in `.env`
- ✅ Verify `todos` table exists in Supabase
- ✅ Check server logs for errors

### VAPI not calling the tool?
- ✅ Check tool description mentions when to use it
- ✅ Try explicit phrase: "Add a todo to..."
- ✅ Check VAPI call logs in dashboard

## What Users Can Say

The tool will trigger when users say things like:
- "Add a todo to buy milk"
- "Add a task to call John"
- "Create a todo to finish the report"
- "Add to my list: buy groceries"

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/vapi/webhook` | POST | Main webhook for VAPI |
| `/api/v1/vapi/webhook/test` | GET | Health check |
| `/api/v1/vapi/webhook/test-add-todo` | POST | Simple test endpoint |

## Environment Variables

Make sure you have in `server/.env`:
```env
# Database
DATABASE_URL=your_supabase_url
POSTGRES_DB_URL=your_postgres_url

# Optional VAPI settings
VAPI_API_KEY=your_vapi_key
```

## Files Created

- `server/api/v1/vapi_webhook.py` - Main webhook handler
- `server/test_vapi_webhook.py` - Test script
- `server/VAPI_SETUP.md` - This guide

## Next Steps

Once basic todos work, you can enhance the tool:

1. **Add due dates**: Add a `due_date` parameter
2. **Add priority**: Add a `priority` parameter  
3. **Add categories**: Add a `category` parameter
4. **Get todos**: Create a second tool to retrieve todos
5. **Complete todos**: Create a tool to mark todos done

## Success Checklist

- [ ] Server running on localhost:8000
- [ ] Test script passes all tests
- [ ] ngrok tunnel active
- [ ] VAPI Server URL updated
- [ ] Test call made
- [ ] Todo appears in Supabase
- [ ] User hears confirmation

---

**You're all set!** 🎉 Update the Server URL in VAPI and start testing!
