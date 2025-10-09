"""
Test script for VAPI Add_todo webhook integration

Run this to test your webhook locally before configuring VAPI.
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_webhook_health():
    """Test if webhook endpoint is accessible"""
    print("🔍 Testing webhook health...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/api/v1/vapi/webhook/test")
            print(f"✅ Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            return False


async def test_add_todo_simple():
    """Test the simple test endpoint"""
    print("📝 Testing simple add todo endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/vapi/webhook/test-add-todo",
                params={
                    "todo_text": "Test todo from webhook",
                    "user_id": "test_user_123"
                }
            )
            print(f"✅ Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            return False


async def test_vapi_webhook_format():
    """Test webhook with actual VAPI payload format"""
    print("📞 Testing VAPI webhook with real payload format...")
    
    # This simulates what VAPI actually sends
    payload = {
        "message": {
            "type": "tool-calls",
            "toolCalls": [
                {
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "Add_todo",
                        "arguments": json.dumps({"todo": "Buy groceries from VAPI call"})
                    }
                }
            ]
        },
        "call": {
            "id": "call_123456",
            "customer": {
                "number": "+1234567890"
            }
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/vapi/webhook",
                json=payload
            )
            print(f"✅ Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            return False


async def test_multiple_todos():
    """Test adding multiple todos via webhook"""
    print("📝 Testing multiple todos...")
    
    todos = ["Buy milk", "Call mom", "Finish report"]
    
    for todo in todos:
        payload = {
            "message": {
                "type": "tool-calls",
                "toolCalls": [
                    {
                        "type": "function",
                        "function": {
                            "name": "Add_todo",
                            "arguments": json.dumps({"todo": todo})
                        }
                    }
                ]
            },
            "call": {
                "id": "test_call",
                "customer": {
                    "number": "+9876543210"
                }
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{BASE_URL}/api/v1/vapi/webhook",
                    json=payload
                )
                result = response.json()
                print(f"  ✅ Added: {todo}")
                print(f"     Response: {result['results'][0]}")
            except Exception as e:
                print(f"  ❌ Failed to add '{todo}': {str(e)}")
    
    print()


async def main():
    """Run all tests"""
    print("🚀 Starting VAPI Add_todo Webhook Tests")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not await test_webhook_health():
        print("❌ Webhook endpoint not accessible. Is the server running?")
        print("   Start server with: uvicorn main:app --reload")
        return
    
    # Test 2: Simple endpoint
    await test_add_todo_simple()
    
    # Test 3: Real VAPI format
    await test_vapi_webhook_format()
    
    # Test 4: Multiple todos
    await test_multiple_todos()
    
    print("=" * 60)
    print("✅ All tests completed!")
    print()
    print("💡 Next steps:")
    print("1. Make sure your FastAPI server is running")
    print("2. Start ngrok: ngrok http 8000")
    print("3. Copy ngrok URL (e.g., https://abc123.ngrok.io)")
    print("4. Update VAPI tool Server URL to: https://abc123.ngrok.io/api/v1/vapi/webhook")
    print("5. Make a test call and say: 'Add a todo to buy milk'")
    print()


if __name__ == "__main__":
    print("📋 VAPI Add_todo Webhook Test Suite")
    print("Make sure your server is running: uvicorn main:app --reload")
    print()
    
    asyncio.run(main())
